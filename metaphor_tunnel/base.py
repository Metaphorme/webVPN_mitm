import os
import sys
import requests

def is_exec():
    if getattr(sys, 'frozen', False):
        return True
    else:
        return False

def get_dir(myfile=__file__):
    if is_exec():
        mydir=os.path.dirname(os.path.abspath(sys.executable))
    else:
        mydir=os.path.dirname(os.path.abspath(myfile))
    return mydir

HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27',
        'sec-ch-ua': '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"105.0.1343.27"',
        'sec-ch-ua-full-version-list': '"Microsoft Edge";v="105.0.1343.27", " Not;A Brand";v="99.0.0.0", "Chromium";v="105.0.5195.96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"14.0.0"',
    }
