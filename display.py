import time
import board
import digitalio
import adafruit_ssd1306
import requests
from PIL import Image, ImageDraw, ImageFont

# SPI 连接设置
spi = board.SPI()  # 初始化 SPI
oled_cs = digitalio.DigitalInOut(board.D8)  # CS 引脚（GPIO 8）
oled_dc = digitalio.DigitalInOut(board.D24)  # DC 引脚（GPIO 24）
oled_reset = digitalio.DigitalInOut(board.D25)  # Reset 引脚（GPIO 25）

# 初始化 SSD1306 OLED 显示器（128x64 分辨率）
oled = adafruit_ssd1306.SSD1306_SPI(128, 64, spi, oled_dc, oled_reset, oled_cs)

# 清空显示器
oled.fill(0)
oled.show()

# 设置字体
font = ImageFont.load_default()

# functions
def get_cpu_info():
    """
    get cpu info from dash api /load/cpu 

    """
    # get CPU info
    url = "http://pinas:3001/load/cpu"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()  # resolve JSON data
    else:
        print("request failed, status code:", response.status_code)
        data = []
    
    # get cpu load and temperatue
    cpu_loads = [core["load"] for core in data]  # extract all cores load
    cpu_temps = [core["temp"] for core in data]  

    cpu_average_load = sum(cpu_loads) / len(cpu_loads) if cpu_loads else 0
    cpu_average_temp = cpu_temps[0] if cpu_temps else None

    return {"cpu_load": cpu_average_load, "cpu_temp": cpu_average_temp}

def get_ram_info(): 
    """
    get ram usage info from dash api /load/ram

    """
    # get RAM info
    url = "http://pinas:3001/load/ram"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()  # resolve JSON data
    else:
        print("request failed, status code:", response.status_code)
        data = []
    
    ram_used = round((data.get("load", 0)/1000000000),2)
    ram_total = 8.0

    ram_load =  ram_used / ram_total *100
    
    return {"ram_used": ram_used, "ram_load": ram_load}

def get_network_info(): 
    """
    get network usage info from dash api /load/network

    """
    # get Network info
    url = "http://pinas:3001/load/network"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()  # resolve JSON data
    else:
        print("request failed, status code:", response.status_code)
        data = []
    
    up = data.get("up", 0) / 1024
    down = data.get("down", 0) /1024

    # MB and KB convert function
    def convert_to_readable(size):
        if size >= 1024: 
            size_in_mb = size / 1024
            return f"{size_in_mb:.2f} MB"
        else:
            size_in_kb = size
            return f"{size_in_kb:.2f} Kb"
    
    network_up = convert_to_readable(up)
    network_down = convert_to_readable(down)
    
    return {"network_up": network_up, "network_down": network_down}


# 获取系统信息并显示在 OLED 上
def display_info():
    while True:
        # 创建图像对象，用于在屏幕上绘制
        image = Image.new("1", (oled.width, oled.height))
        draw = ImageDraw.Draw(image)

        # 获取时间和日期
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime("%Y-%m-%d")

        # 获取 CPU 使用率和温度
        cpu_result = get_cpu_info()
        cpu_load = cpu_result["cpu_load"]
        cpu_temp = cpu_result["cpu_temp"]

        # 获取内存数据和使用率
        memory_result = get_ram_info()
        memory_used = memory_result["ram_used"]
        memory_laod = memory_result["ram_load"]

        # 获取网速
        network_result = get_network_info()
        network_up = network_result["network_up"]
        network_down = network_result["network_down"]

        # 清空屏幕
        draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

        # 绘制文本
        draw.text((0, 0), f"{current_date}            {current_time}", font=font, fill=255)      # 第一行：时间和时间
        draw.text((0, 14), f"CPU: {cpu_load:.2f}%", font=font, fill=255)        # 第二行：CPU使用率和温度
        draw.text((70, 14), f"T: {cpu_temp:.2f}°C", font=font, fill=255) 
        draw.text((0, 27), f"Mem:{memory_used}/8.0Gb {memory_laod:.2f}%", font=font, fill=255)      # 第三行：内存和磁盘使用率
        draw.text((0, 40), f"Network up: {network_up}", font=font, fill=255)                   # 第四五行：网速
        draw.text((0, 53), f"Network down: {network_down}", font=font, fill=255)

        # 将图像加载到 OLED
        oled.image(image)
        oled.show()

        # 每秒更新一次
        time.sleep(1)

# 运行显示系统信息的函数
display_info()
