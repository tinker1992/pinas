import time
import psutil
import os
import board
import digitalio
import adafruit_ssd1306
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

# 获取 CPU 温度
def get_cpu_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    return temp.replace("temp=", "").replace("'C\n", "")

# 获取系统信息并显示在 OLED 上
def display_info():
    initial_bytes_sent = psutil.net_io_counters().bytes_sent
    initial_bytes_recv = psutil.net_io_counters().bytes_recv
    while True:
        # 创建图像对象，用于在屏幕上绘制
        image = Image.new("1", (oled.width, oled.height))
        draw = ImageDraw.Draw(image)

        # 获取时间和日期
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime("%Y-%m-%d")

        # 获取 CPU 使用率
        cpu_usage = psutil.cpu_percent(interval=1)

        # 获取 CPU 温度
        cpu_temp = get_cpu_temp()

        # 获取磁盘使用率
        disk_usage = psutil.disk_usage('/').percent

        # 获取内存使用率
        memory_usage = psutil.virtual_memory().percent

        # 获取网速
        # 获取当前的网络发送和接收字节数
        net_io = psutil.net_io_counters()
        bytes_sent = net_io.bytes_sent - initial_bytes_sent
        bytes_recv = net_io.bytes_recv - initial_bytes_recv
        # 更新初始值，准备下一秒的网速计算
        initial_bytes_sent = net_io.bytes_sent
        initial_bytes_recv = net_io.bytes_recv
        # 计算上传和下载速度
        net_speed_up = f"{bytes_sent / 1024:.2f} KB/s ↑"
        net_speed_down = f"{bytes_recv / 1024:.2f} KB/s ↓"

        # 清空屏幕
        draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

        # 绘制文本
        draw.text((0, 0), f"{current_date}         {current_time}", font=font, fill=255)      # 第一行：时间和时间
        draw.text((0, 14), f"CPU: {cpu_usage}% Temp: {cpu_temp}C", font=font, fill=255)        # 第二行：CPU使用率和温度
        draw.text((0, 27), f"Mem: {memory_usage}% Disk: {disk_usage}%", font=font, fill=255)      # 第三行：内存和磁盘使用率
        draw.text((0, 40), f"{net_speed_up}", font=font, fill=255)                   # 第四五行：网速
        draw.text((0, 53), f"{net_speed_down}", font=font, fill=255)

        # 将图像加载到 OLED
        oled.image(image)
        oled.show()

        # 每秒更新一次
        time.sleep(1)

# 运行显示系统信息的函数
display_info()
