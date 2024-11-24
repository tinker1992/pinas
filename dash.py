import requests

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
    netwrok_down = convert_to_readable(down)
    
    return {"network_up": network_up, "network_down": netwrok_down}

cpu_result = get_cpu_info()
cpu_load = cpu_result["cpu_load"]
cpu_temp = cpu_result["cpu_temp"]
print(cpu_load, cpu_temp)

network_result = get_network_info()
network_up = network_result["network_up"]
network_down = network_result["network_down"]