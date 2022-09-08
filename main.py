import os
import sys
from metaphor_tunnel import url_conversion as urlc
from metaphor_tunnel import webvpn as wvpn

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
MYDIR = get_dir(__file__)

def main():
    url = urlc.get_url(urlc.get_url_info('https://cn.bing.com'))
    print(url)
    cred = wvpn.get_credentials()
    mycookie = wvpn.cpu_webvpn_login(cred)
    print(mycookie)

if __name__ == '__main__':
    main()
