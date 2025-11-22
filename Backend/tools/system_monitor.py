import psutil 
from langchain.tools import tool 

@tool
def system_status():
    """Returns CPU, RAM and battery status."""
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent 
    
    return f"CPU: {cpu}%, RAM: {ram}%, Disk: {disk}%" 

# if __name__=="__main__": 
#     print(system_status())