# -*- coding: utf-8 -*-
import os


def clear():
    # For Windows Users
    if os.name == "nt":
        os.system('clr')
    # For other Users
    else:
        os.system('clear')


def find_cert(file_path='credentials.txt'):
    if os.path.exists(file_path):
        return True
    else:
        return False


def write_cert():
    from webVPN_mitm.cpu_webvpn import write_credentials
    import getpass

    username = input("请输入学号：")
    password = getpass.getpass("请输入密码：")

    write_credentials(username=username, password=password, file_path='credentials.txt')
    print("已创建凭证文件 credentials.txt")

    input("请按任意键继续...")
    main()


def verify_cert():
    from webVPN_mitm.cpu_webvpn import read_credentials
    from webVPN_mitm.cpu_webvpn import login

    username, password = read_credentials(file_path='credentials.txt')
    print("读取成功，学号：{} ，密码：{}".format(username, password))
    print("正在尝试登录...")
    my_cookie = login(username=username, password=password)
    print("获得 Cookie：{wengine_vpn_ticketwebvpn_cpu_edu_cn: " + my_cookie + "}")

    input("请按任意键继续...")
    main()


def url_encode():
    from webVPN_mitm.url_conversion import WebvpnUrl
    d = WebvpnUrl(inst_host="webvpn.cpu.edu.cn")

    try:
        while True:
            url = input("请输入待转换的普通url：")
            print("URL_Encoded: " + d.url_encode(url))
    except KeyboardInterrupt:
        main()


def url_decode():
    from webVPN_mitm.url_conversion import WebvpnUrl
    d = WebvpnUrl()

    try:
        while True:
            url = input("请输入webVPN 加密后的 URL：")
            print("URL_Decoded: " + d.url_decode(url))
    except KeyboardInterrupt:
        main()


def get_cookie():
    if find_cert():
        verify_cert()
    else:
        import getpass
        from webVPN_mitm.cpu_webvpn import login

        username = input("请输入学号：")
        password = getpass.getpass("请输入密码：")
        print("正在尝试登录...")
        my_cookie = login(username=username, password=password)
        print("获得 Cookie：{wengine_vpn_ticketwebvpn_cpu_edu_cn: " + my_cookie + "}")

        input("请按任意键继续...")
        main()


def start_http(port="8080"):
    try:
        input_port = int(input("请输入 HTTP/HTTPS 监听端口：（默认：8080）"))
    except ValueError:
        input_port = 8080
    if input_port in range(0, 65536):
        port = str(input_port)
    else:
        print("端口不合法，将使用8080")
    os.system("mitmdump -s webVPN_mitm/webvpn-mitm.py --listen-port " + port)


"""
def start_sock5(port="1080"):
    try:
        input_port = int(input("请输入 sock5 监听端口：（默认：1080）"))
    except ValueError:
        input_port = 1080
    if input_port in range(0, 65536):
        port = str(input_port)
    else:
        print("端口不合法，将使用1080")
    os.system("mitmdump -s webVPN_mitm/webvpn-mitm.py --mode socks5 --listen-port " + port)
"""


def main():
    clear()
    print()
    print()
    print("                     _     _   _______ _   _                  _ _     ")
    print("                    | |   | | | | ___ \ \ | |                (_) |     ")
    print("       __      _____| |__ | | | | |_/ /  \| |______ _ __ ___  _| |_ _ __ ___     ")
    print("       \ \ /\ / / _ \ '_ \| | | |  __/| . ` |______| '_ ` _ \| | __| '_ ` _ \     ")
    print("        \ V  V /  __/ |_) \ \_/ / |   | |\  |      | | | | | | | |_| | | | | |     ")
    print("         \_/\_/ \___|_.__/ \___/\_|   \_| \_/      |_| |_| |_|_|\__|_| |_| |_|     ")
    print()
    print()
    print("{:^83}".format("webVPN_mitm, A Good Man In the Middle of You and webVPN"))
    print("{:^83}".format("Author: Metaphorme, github.com/Metaphorme, in CPU"))
    print("{:^83}".format("            Lucien Shaw, github.com/lucienshawls, in CPU"))
    print("{:^83}".format("Designed for webVPN in China Pharmaceutical University"))
    print("{:^83}".format("Licensed under Mozilla Public License 2.0"))
    print("{:^83}".format("Repo: https://github.com/Metaphorme/webVPN-mitm"))
    print()
    print()
    print("{:<83}".format("工具选项："))
    print("{:<83}".format("- 1. 创建凭证文件"))
    print("{:<83}".format("- 2. 验证凭证文件有效性"))
    print("{:<83}".format("- 3. 普通 URL -> webVPN 加密 URL"))
    print("{:<83}".format("- 4. webVPN 加密 URL -> 普通 URL"))
    print("{:<83}".format("- 5. 获取有效 Cookie"))
    print("{:<83}".format("- 6. 开启 HTTP/HTTPS 代理服务器"))
    print()

    try:
        choose = input("请输入所需工具前的序号（e.g, 1）：")
    except KeyboardInterrupt:
        exit()

    if choose == "1":
        write_cert()
    elif choose == "2":
        verify_cert()
    elif choose == "3":
        url_encode()
    elif choose == "4":
        url_decode()
    elif choose == "5":
        get_cookie()
    elif choose == "6":
        start_http()
    else:
        print("输入不合法，将退出...")
        exit()


if __name__ == '__main__':
    main()
