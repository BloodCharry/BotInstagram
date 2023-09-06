import os
import random
import string
import requests


def header():
    print('''
   -*-*-*-   
            (__)  __  ___   _______   __     __ ___
            |  | |  \ |  | / ______| |  |_  / __`  | 
            |  | |   \|  | | |_____  |  __||  / |  |
            |  | |  \    | \___    \ |  |  |  | |  |
            |  | |  |\   |  ___/   / |  |_ |  \_|  |
            |__| |__| \__| |______/  \____| \___,__|  -*-*-*-
    ''')
    print("[+] Instagram Bot")
    print("[-] Developed by BloodCharry")
    print("-*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-")


def options():
    mode = input(
        "[>] would you like to start?\n[>] 1 = Yes\n[>] 2 = No\n[>] Selection: ")


def get_proxy_list():
    http = 'https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all'
    http1 = 'https://www.freeproxy-list.ru/api/proxy?anonymity=false&token=demo'
    https1 = 'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt'
    https2 = 'https://raw.githubusercontent.com/jetkai/proxy-list/main/archive/txt/proxies.txt'
    socks4 = 'https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=10000&country=all'
    socks5 = 'https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=10000&country=all'
    url_proxy = [http, http1, https1, https2, socks4, socks5]
    current_dir = os.path.abspath(os.path.dirname(__file__))
    folder_name = 'file_for_works'
    file_name = 'proxies_list.txt'
    path_dir = os.path.join(current_dir, folder_name)
    path_file = os.path.join(path_dir, file_name)
    with open(path_file, 'w') as file:
        for url in url_proxy:
            response = requests.get(url)
            if response.status_code == 200:
                proxy_list = response.text.strip().split('\n')
                for proxy in proxy_list:
                    file.write(proxy + '\n')
    with open(path_file, "r") as file:
        lines = file.readlines()
    lines = list(filter(lambda x: x.strip() != "", lines))
    with open(path_file, "w") as file:
        file.writelines(lines)
    print('[+]> the list of proxies has been received, you can start checking the names!\n')


def get_proxy(path_file):
    proxy = random.choice(list(open(path_file)))
    proxy = proxy.strip()
    proxy = proxy.replace("\n", "")
    return proxy


def get_user_agent(path_file):
    user_agent = random.choice(list(open(path_file)))
    user_agent = user_agent.strip()
    user_agent = user_agent.replace("\n", "")
    return user_agent


header()