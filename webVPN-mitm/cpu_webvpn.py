import getpass

import requests


class GetCred:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.HEADERS = {
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

    def login(self, credentials, skip_check=False):
        s = requests.Session()
        headers = self.HEADERS.copy()

        response = s.get('https://webvpn.cpu.edu.cn/portal', headers=headers)
        my_cookie = response.history[0].cookies.get_dict()['wengine_vpn_ticketwebvpn_cpu_edu_cn']

        headers['Origin'] = 'https://webvpn.cpu.edu.cn'
        headers['Referer'] = 'https://webvpn.cpu.edu.cn/https' \
                             '/77726476706e69737468656265737421f9f30f9f372526557a1dc7af96/sso/login?service=https%3A' \
                             '%2F%2Fwebvpn.cpu.edu.cn%2Flogin%3Fcas_login%3Dtrue '
        params = {'service': 'https://webvpn.cpu.edu.cn/login?cas_login=true', }
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

        response = s.post('https://webvpn.cpu.edu.cn/https/77726476706e69737468656265737421f9f30f9f372526557a1dc7af96'
                          '/sso/login', params=params, headers=headers, data=data)
        if response.url == 'https://webvpn.cpu.edu.cn/portal' or skip_check:
            return my_cookie
        else:
            raise RuntimeError('登录失败，请检查学号密码或选择跳过验证')

    def get_credentials(self, file_path='credentials.txt', force_password_input=False):
        cred = []
        import os
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                cred = f.read().strip().split('\n')
            is_exist = True
        else:
            print('找不到凭证文件，将采用学号/密码方式登录')
            is_exist = False

        if len(cred) == 0 or cred[0] == '':
            cred.append(self.username)
        else:
            print('学号已由凭证文件提供: %s' % (cred[0]))
        if len(cred) <= 1 or force_password_input:
            if is_exist:
                print('未从凭证文件处获得密码或设置了强制密码输入')
            cred.append(self.password)
        else:
            print('密码已由凭证文件提供')

        return self.login(cred)


if __name__ == '__main__':
    g = GetCred(username=input('请输入学号: '),
                password=getpass.getpass('请输入密码：'))
    print(g.get_credentials())
