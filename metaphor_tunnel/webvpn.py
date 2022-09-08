import base
from base import *
import getpass

MYDIR = base.get_dir()

def cpu_webvpn_login(credentials,skip_check=False):
    s = requests.Session()
    headers = base.HEADERS.copy()

    response = s.get('https://webvpn.cpu.edu.cn/portal', headers=headers)
    mycookie = response.history[0].cookies.get_dict()['wengine_vpn_ticketwebvpn_cpu_edu_cn']

    headers['Origin'] = 'https://webvpn.cpu.edu.cn'
    headers['Referer'] = 'https://webvpn.cpu.edu.cn/https/77726476706e69737468656265737421f9f30f9f372526557a1dc7af96/sso/login?service=https%3A%2F%2Fwebvpn.cpu.edu.cn%2Flogin%3Fcas_login%3Dtrue'
    params = {'service': 'https://webvpn.cpu.edu.cn/login?cas_login=true',}
    data = {
        'lt': '${loginTicket}',
        'useVCode': '',
        'isUseVCode': 'true',
        'sessionVcode': '',
        'errorCount': '',
        'execution': 'e1s1',
        'service': 'https://webvpn.cpu.edu.cn/login?cas_login=true',
        '_eventId': 'submit',
        'geolocation': '',
        'username': credentials[0],
        'password': credentials[1],
        'rememberpwd': 'on',
    }
    
    response = s.post('https://webvpn.cpu.edu.cn/https/77726476706e69737468656265737421f9f30f9f372526557a1dc7af96/sso/login', params=params,headers=headers, data=data)
    
    if response.url == 'https://webvpn.cpu.edu.cn/portal' or skip_check:
        return mycookie
    else:
        raise RuntimeError('登录失败，请检查学号密码或选择跳过验证')

def web_go(url,cookie):
    import requests
    cookies = {
        'wengine_vpn_ticketwebvpn_cpu_edu_cn': cookie,
    }
    headers = base.HEADERS.copy()
    response = requests.get(url, cookies=cookies, headers=headers)
    return response

def get_credentials(force_password_input=False):
    cred = []
    file_path = MYDIR + '/credentials.txt'
    if os.path.exists(file_path):
        with open(file_path,'r',encoding='utf-8') as f:
            cred = f.read().strip().split('\n')
        isexist = True
    else:
        print('找不到凭证文件')
        isexist = False
    
    if len(cred) == 0 or cred[0] == '':
        cred.append(input('请输入学号: '))
    else:
        print('学号已由凭证文件提供: %s' %(cred[0]))
    if isexist:
        print('凭证文件未提供密码或设置了强制密码输入')
    if len(cred) <= 1 or force_password_input:
        cred.append(getpass.getpass('请输入密码: '))
    else:
        print('密码已由凭证文件提供')

    return cred

if __name__ == '__main__':
    # Test only
    url = 'https://webvpn.cpu.edu.cn/https/77726476706e69737468656265737421f3f90f9e2e3e6f1e7d0784/' # bing
    # url = 'https://webvpn.cpu.edu.cn/https/77726476706e69737468656265737421e7e056d224207d1e7b0c9ce29b5b/' # cpu
    cred = get_credentials(force_password_input=False)
    mycookie = cpu_webvpn_login(cred,skip_check=False)
    # resp = web_go(url,mycookie)
    # print(resp.text)
    print(mycookie)
