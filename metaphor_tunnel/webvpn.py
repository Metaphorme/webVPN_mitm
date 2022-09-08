import requests

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

def cpu_webvpn_login(credentials,skip_check=False):
    s = requests.Session()
    headers = HEADERS.copy()

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
    cookies = {
        'wengine_vpn_ticketwebvpn_cpu_edu_cn': cookie,
    }
    headers = HEADERS.copy()
    response = requests.get(url, cookies=cookies, headers=headers)
    return response

def get_credentials(file_path='credentials.txt',force_password_input=False):
    cred = []
    import os
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
        import getpass
        cred.append(getpass.getpass('请输入密码: '))
    else:
        print('密码已由凭证文件提供')

    return cred

if __name__ == '__main__':
    pass
