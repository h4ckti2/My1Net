import requests

# Open the file with a list of proxy sites
with open("proxy_sites.txt", "r") as proxy_sites:
    proxy_sites.seek(0)
    sites = proxy_sites.readlines()
    # Open a file to save the proxies
    with open("proxies.txt", "a") as proxies_file:
        # Iterate through each site
        for site in sites:
            site = site.strip()
            try:
                # Send a request to each site
                r = requests.get(site)
                # If the request was successful
                if r.status_code == 200:
                    # Get the proxy list from the site
                    proxies = r.text.split("\n")
                    # Iterate through the proxies
                    for proxy in proxies:
                        # Check if the proxy is working
                        try:
                            if 'http' in proxy:
                                proxy_dict = {'http': proxy, 'https': proxy}
                            elif 'socks' in proxy:
                                proxy_dict = {'socks': proxy}
                            else:
                                proxy_dict = {'http': proxy, 'https': proxy}
                            # Send a request to a test site using the proxy
                            test_site = 'https://httpbin.org/ip'
                            r = requests.get(test_site, proxies=proxy_dict)
                            # If the request was successful, the proxy is working
                            if r.status_code == 200:
                                # Append the proxy to the file
                                proxies_file.write(proxy + "\n")
                                print("\033[32m[+]\033[0m", proxy)
                        except:
                            # If the request failed, the proxy is not working
                            print("\033[31m[-]\033[0m", proxy)
            except:
                # If the request was not successful, print an error message
                print("\033[31m[-]\033[0m", site)
