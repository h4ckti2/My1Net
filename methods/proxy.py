import requests

url = input("URL: ")

proxy_url = input("Proxy url: ")

response = requests.get(proxy_url)
proxies = response.text.split()

for proxy in proxies:
    try:
        response = requests.get(url, proxies={"http": f"http://{proxy}"})

        if response.status_code == 200:
            print(f"\033[32m[+]\033[0m {proxy} ->", url)

    except requests.exceptions.ProxyError:
        print(f'\033[31m[-]\033[0m Proxy {proxy} failed')
