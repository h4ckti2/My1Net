from bs4 import BeautifulSoup
import requests
import random
import time

# reading user-agents from a file
with open('user_agents.txt', 'r') as file:
    user_agents_list = file.read().splitlines()

# reading proxies from a file
with open('proxies.txt', 'r') as file:
    proxies_list = file.read().splitlines()

for i in range(len(user_agents_list)):
    headers = {'User-Agent': user_agents_list[i]}
    proxy = {proxies_list[i].split(':')[0]: proxies_list[i]}

    try:
        response = requests.get('https://httpbin.org/ip', headers=headers, proxies=proxy, timeout=3)
        # parse the response
        soup = BeautifulSoup(response.text, 'html.parser')
        # print the html of the website
        print(soup)
    except:
        # in case of connection error or timeout
        print("Error with the proxy: ", proxy)

    time.sleep(random.randint(5, 10))
