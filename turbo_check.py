import datetime
import urllib3.exceptions
import urllib3
from instagrapi import exceptions
import functions
import requests
from urllib3 import exceptions
from bs4 import BeautifulSoup
import os
import random
import instagrapi
import os, sys, time
import threading
from threading import RLock
from instagrapi import Client
import logging

logger = logging.getLogger('instagrapi')
logger.setLevel(logging.CRITICAL)
free_name_lock = RLock()
user_app_free = []
check_freenames = dict()
free_usernames = []
true_rename = dict()
rlock_name = RLock()


def check_length_usernames_credertials():
    usernames = get_username()
    accounts = get_accounts()
    if len(usernames) != len(accounts):
        print('[>]number of file lines usernames.txt does not match the file credentials.txt')
        print('[>]Im stopping work.....')
        exit()


def get_username():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    path_dir = os.path.join(current_dir, 'accounts')
    path_file = os.path.join(path_dir, 'usernames.txt')
    with open(path_file) as f:
        lines = f.readlines()
    usernames = [line.strip() for line in lines]
    return usernames


usernames_queue = get_username()
usernames_list = usernames_queue.copy()


def get_accounts():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    path_dir = os.path.join(current_dir, 'accounts')
    path_file = os.path.join(path_dir, 'accounts.txt')
    with open(path_file) as f:
        lines = f.readlines()
    accounts = [line.strip() for line in lines]
    return accounts


accounts = get_accounts()


def check_username(username):
    url = f'https://www.instagram.com/{username}'
    folder_name = 'file_for_works'
    file_name = 'useragents.txt'
    current_dir = os.path.abspath(os.path.dirname(__file__))
    path_dir = os.path.join(current_dir, folder_name)
    path_file = os.path.join(path_dir, file_name)
    session = requests.Session()
    session.headers = {'User-Agent': functions.get_user_agent(path_file)}
    file_name = 'proxies_list.txt'
    prox1 = functions.get_proxy(path_file)
    path_file = os.path.join(path_dir, file_name)
    proxy_types = ["http", "https", "socks4", "socks5"]
    for proxy_type in proxy_types:
        session.proxies = {proxy_type: f"{proxy_type}://{prox1}"}
        while True:
            try:
                start = datetime.datetime.now()
                response = session.get(url=url, timeout=3)
                if response.status_code == 404:
                    print(f" Found available nickname {username}!")
                    end = datetime.datetime.now()
                    elapsed_time = (end - start).total_seconds() * 1000
                    print(f"Checking nickname {username}: {abs(elapsed_time):.3f} MS")
                    if username in check_freenames:
                        return
                    if username in free_usernames:
                        return
                    else:
                        free_usernames.append(username)
                if not response.text:
                    break
                else:
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        len_text = soup.text.strip()
                        words = len_text.split()
                        if len(words) == 1 or len(words) == 3:
                            end = datetime.datetime.now()
                            elapsed_time = (end - start).total_seconds() * 10
                            print(f" Found available nickname {username}!")
                            print(f"Checking nickname {username}: {abs(elapsed_time):.3f} MS")
                            if username in check_freenames:
                                return
                            else:
                                free_usernames.append(username)
                                if username in usernames_queue:
                                    usernames_queue.remove(username)
                                return
                    else:
                        session.close()
                        break
            except requests.ConnectionError:
                session.close()
            except requests.exceptions.RequestException:
                session.close()
            time.sleep(5)


def rename(freename, proxy, semaphore):
    with semaphore:
        try:
            if proxy == "true":
                folder_name = 'file_for_works'
                file_name = 'proxies_for_rename.txt'
                current_dir = os.path.abspath(os.path.dirname(__file__))
                path_dir = os.path.join(current_dir, folder_name)
                path_file = os.path.join(path_dir, file_name)
                prox1 = functions.get_proxy(path_file)
                proxy = f'http://{prox1}'
                cl = Client(request_timeout=10, proxy=proxy)
            else:
                cl = Client(request_timeout=10)
        except:
            return
        start = datetime.datetime.now()
        if freename in check_freenames:
            try:
                free_usernames.remove(freename)
            except ValueError:
                time.sleep(5)
                return
        i = usernames_list.index(freename)
        if i >= len(accounts):
            time.sleep(5)
            return
        log_pass = accounts[i].split(':')
        login = log_pass[0]
        password = log_pass[1]
        try:
            cl.login(login, password)
        except instagrapi.exceptions.BadPassword:
            print(f'problem renaming name {freename} wrong {login}:{password},  because of error')
            end = datetime.datetime.now()
            elapsed_time = (start - end).total_seconds() * 10
            print(f"nickname renaming {freename} for availability: {abs(elapsed_time):.3f} MS")
            check_freenames[freename] = {'login': login, 'password': password}
            try:
                free_usernames.remove(freename)
            except ValueError:
                pass
        except instagrapi.exceptions.UnknownError:
            print(f'problem renaming name {freename} wrong {login}:{password},  because of error')
            end = datetime.datetime.now()
            elapsed_time = (start - end).total_seconds() * 10
            print(f"nickname renaming {freename} for availability: {abs(elapsed_time):.3f} MS")
            check_freenames[freename] = {'login': login, 'password': password}
            if freename in check_freenames:
                try:
                    free_usernames.remove(freename)
                except ValueError:
                    time.sleep(5)
                    return
            try:
                free_usernames.remove(freename)
            except ValueError:
                pass
        except OSError:
            time.sleep(5)
            return
        except requests.exceptions.ConnectionError:
            time.sleep(5)
            return
        except instagrapi.exceptions.ClientConnectionError:
            time.sleep(5)
            return
        except urllib3.exceptions.MaxRetryError:
            time.sleep(5)
            return
        except ConnectionRefusedError:
            time.sleep(5)
            return
        except urllib3.exceptions.NewConnectionError:
            time.sleep(5)
            return
        except urllib3.exceptions.ReadTimeoutError:
            time.sleep(5)
            return
        try:
            cl.account_edit(username=freename)
            true_rename[freename] = {'login': login, 'password': password}
            print(f'Account’s {login}:{password} nickname was renamed to {freename}')
            end = datetime.datetime.now()
            elapsed_time = (start - end).total_seconds() * 10
            print(f"nickname renaming {freename} for availability: {abs(elapsed_time):.3f} MS")
            check_freenames[freename] = {'login': login, 'password': password}
            free_usernames.remove(freename)
            time.sleep(5)
        except:
            time.sleep(5)
            return
        try:
            free_usernames.remove(freename)
        except ValueError:
            time.sleep(5)
            pass


def run():
    question = input("\n[>] Would you like to use proxies from proxies_for_rename.txt? (Y/N): ")
    if question == "Y" or question == "y":
        proxies = "true"
        current_dir = os.path.abspath(os.path.dirname(__file__))
        path_dir = os.path.join(current_dir, 'file_for_works')
        path_file = os.path.join(path_dir, 'proxies_for_rename.txt')
        with open(path_file) as f:
            lines = f.readlines()
        proxi = [line.strip() for line in lines]
        if len(proxi) > 50:
            semaphore = threading.BoundedSemaphore(50)
        elif len(proxi) <= 0:
            semaphore = threading.BoundedSemaphore(1)
        else:
            semaphore = threading.BoundedSemaphore(len(proxi))
    else:
        proxies = "false"
        semaphore = threading.BoundedSemaphore(1)
    while True:
        for username in usernames_queue:
            if usernames_queue:
                th = threading.Thread(target=check_username, args=(username,))
                th.start()
            else:
                pass
        for freename in free_usernames:
            if free_usernames:
                th = threading.Thread(target=rename, args=(freename, proxies, semaphore))
                th.start()
            else:
                pass


def turbo():
    print("\n[!] Important Information:")
    print("make sure that the number of nicknames and accounts matches otherwise the program will not continue working")
    print("make sure you get the list of proxy servers, otherwise you risk getting banned")
    print("[>] put the names to be checked in the accounts.txt, usernames.txt folder to check for availability")

    while True:
        check_length_usernames_credertials()
        question = input("[>] Are you ready to continue? Y/N: ")
        if question == "Y" or question == "y":
            run()
        else:
            print("[!] Exiting")
            exit()
