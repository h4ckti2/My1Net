import requests

url = "https://iplogger.org/logger/D8TS3yw28D4B"

proxy_address = "184.170.245.148"
proxy_port = 4145

proxy = {
    "http": f"http://{proxy_address}:{proxy_port}",
    "https": f"https://{proxy_address}:{proxy_port}",
}

# Send a request to a website using the proxy
response = requests.get(url, proxies=proxy)

# Read the response
html = response.text

input("\nPress any key to continue . . . ")
