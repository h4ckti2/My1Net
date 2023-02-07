import platform
import GPUtil
import psutil
import time
import sys
import os


def plot_performance():
    while True:
        cpu_info = platform.processor()
        gpu = GPUtil.getGPUs()[0]

        print(f"CPU : {cpu_info}")
        print(f"GPU : {gpu.name}\n")

        cpu_percent = psutil.cpu_percent()
        gpu_percent = gpu.load * 100

        print(f"CPU Usage: {cpu_percent:.2f}%\t"
              f"GPU Usage: {gpu_percent:.2f}%")

        time.sleep(5)

        if sys.platform == "linux":
            os.system("clear")
        else:
            os.system("cls")


plot_performance()
