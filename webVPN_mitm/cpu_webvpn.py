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


def login(username, password, skip_check=False) -> str or RuntimeError:
    s = requests.Session()
    headers = HEADERS.copy()

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
        'username': username,
        'password': password,
        'rememberpwd': 'on',
    }

    response = s.post('https://webvpn.cpu.edu.cn/https/77726476706e69737468656265737421f9f30f9f372526557a1dc7af96'
                      '/sso/login', params=params, headers=headers, data=data)
    if response.url == 'https://webvpn.cpu.edu.cn/portal' or skip_check:
        return my_cookie
    else:
        raise RuntimeError('登录失败，请检查学号密码或选择跳过验证')


def read_credentials(file_path='credentials.txt') -> tuple or Exception:
    import os
    import base64
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            username, password = str(base64.b64decode(f.read()), encoding="utf-8").split(':')
    else:
        raise Exception("找不到凭证文件")
    return username, password


def write_credentials(username="", password="", file_path='credentials.txt') -> None:
    import os
    import base64
    if os.path.exists(file_path):
        choose = input("credentials.txt 已存在，继续操作将覆盖原文件，要继续操作吗？(y/n) ")
        if choose != "Y" or "y":
            return None
    else:
        print("将创建 credentials.txt 加密保存学号/密码")

    with open(file_path, "wb") as f:
        f.write(base64.b64encode(bytes(username + ":" + password, encoding="utf-8")))
    return None


def logout(cookie):
    requests.get(
        url="https://webvpn.cpu.edu.cn/http/77726476706e69737468656265737421fdee0f9f372526557a1dc7af96/EIP/login"
            "/logout.htm",
        headers=HEADERS,
        cookies={"wengine_vpn_ticketwebvpn_cpu_edu_cn": cookie}
    )
    return None


if __name__ == '__main__':
    """
    方式一：手动输入学号/密码登录
    """
    import getpass

    print("Cookie: {wengine_vpn_ticketwebvpn_cpu_edu_cn: " +
          login(username=input('请输入学号: '),
                password=getpass.getpass('请输入密码：'))
          + "}")

    """
    方式二：通过凭证文件登录
    """
    write_credentials(username="2020502032", password="CVu03CHU+sJz4w==")
    cred = read_credentials()
    print("Cookie: {wengine_vpn_ticketwebvpn_cpu_edu_cn: " +
          login(username=cred[0],
                password=cred[1])
          + "}")
