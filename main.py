import instagrapi
import urllib3
from instagrapi import exceptions
from functions import header as head
from functions import get_proxy_list
import turbo_check
import os, sys, time
import os.path
import requests
import threading
import datetime
import functions
import requests
from bs4 import BeautifulSoup
from requests import exceptions
import os
import random
import threading
import logging
from urllib3 import exceptions

if __name__ == '__main__':
    h = head
    exit_program = False
    while not exit_program:
        mode = input("[>] Please choose one of the following\n[>] 1 = get a list of proxy to work\n[>] 2 = start checking and renaming\n[>] 3 = exit program\n")
        if mode == "1":
            print("\n")
            get_proxy_list()
        elif mode == "2":
            print("\n")
            try:
                turbo_check.turbo()
            except requests.exceptions.RequestException:
                continue
        elif mode == "3":
            exit_program = True
        else:
            print("\n[?] Invalid option, try again.")
            time.sleep(3)
            pass

