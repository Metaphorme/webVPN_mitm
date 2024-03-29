import re
import copy
from binascii import hexlify, unhexlify
from Crypto.Cipher import AES


class WebvpnUrl:
    KEY_ = b'wrdvpnisthebest!'
    IV_ = b'wrdvpnisthebest!'
    SIZE = 128
    PREFIX = '77726476706e69737468656265737421'
    PREFIX_LEN = len(PREFIX)
    URL_INFO = {
        'webvpn': {
            'protocol': 'https',
            'host': '',
            'port': '',
        },
        'target': {
            'protocol': '',
            'host': '',
            'port': '',
            'url': '/',
        }
    }

    def __init__(self, inst_host=''):
        self.INST_HOST = inst_host
        self.url_info = copy.deepcopy(WebvpnUrl.URL_INFO)

    def __encrypt(self, text):
        key = WebvpnUrl.KEY_
        cfb_iv = WebvpnUrl.IV_
        size = WebvpnUrl.SIZE
        cfb_cipher_encrypt = AES.new(key, AES.MODE_CFB, cfb_iv, segment_size=size)

        message = text.encode('utf-8')
        mid = cfb_cipher_encrypt.encrypt(message)
        return hexlify(mid).decode()

    def __decrypt(self, ciphertext):
        key = WebvpnUrl.KEY_
        cfb_iv = WebvpnUrl.IV_
        size = WebvpnUrl.SIZE

        message = unhexlify(ciphertext.encode('utf-8'))
        cfb_cipher_decrypt = AES.new(key, AES.MODE_CFB, cfb_iv, segment_size=size)
        return cfb_cipher_decrypt.decrypt(message).decode('utf-8')

    def __get_url(self, mode):
        host_encrypted_target, url = None, None
        host_target = self.url_info['target']['host']
        if host_target != '' and mode == 'encode':
            host_encrypted_target = WebvpnUrl.PREFIX + self.__encrypt(host_target)
        elif host_target == '':
            return ''

        port_webvpn = str(self.url_info['webvpn']['port'])
        if port_webvpn != '' and mode == 'encode':
            port_webvpn = ':' + port_webvpn

        port_target = str(self.url_info['target']['port'])
        if port_target != '':
            if mode == 'encode':
                port_target = '-' + port_target
            elif mode == 'decode':
                port_target = ':' + port_target
        if mode == 'encode':
            url = '%s://%s%s/%s%s/%s%s' % (
                self.url_info['webvpn']['protocol'],
                self.url_info['webvpn']['host'],
                port_webvpn,
                self.url_info['target']['protocol'],
                port_target,
                host_encrypted_target,
                self.url_info['target']['url'],
            )
        elif mode == 'decode':
            url = '%s://%s%s%s' % (
                self.url_info['target']['protocol'],
                host_target,
                port_target,
                self.url_info['target']['url'],
            )
        return url

    def __get_url_info_from_plain(self, url):
        self.url_info = copy.deepcopy(WebvpnUrl.URL_INFO)

        self.url_info['webvpn']['host'] = self.INST_HOST

        st1 = url.split('//')
        self.url_info['target']['protocol'] = st1[0][:-1]
        if st1[0] == '' or st1[0] == 'http:':
            self.url_info['webvpn']['protocol'] = 'https'
        else:
            self.url_info['webvpn']['protocol'] = st1[0][:-1]

        host = re.match('[0-9,a-z,A-Z,\.\-\:]*', st1[1]).group(0)
        my_url = st1[1][len(host):]
        if my_url == '' or my_url[0] != '/':
            my_url = '/' + my_url
        self.url_info['target']['url'] = my_url

        if host.find(':') != -1:
            host, port = host.split(':')
            self.url_info['target']['host'] = host
            self.url_info['target']['port'] = port
        else:
            self.url_info['target']['host'] = host

    def __get_url_info_from_encrypted(self, url):
        self.url_info = copy.deepcopy(WebvpnUrl.URL_INFO)

        self.url_info['webvpn']['host'] = self.INST_HOST

        st1 = url.split('//')
        if st1[0] == '':
            st1[0] = 'https:'
        self.url_info['webvpn']['protocol'] = st1[0][:-1]

        index1 = st1[1].find('/')
        st2 = st1[1][0:index1]

        if st2.find(':') != -1:
            st2_1 = st2.split(':')
            self.url_info['webvpn']['port'] = st2_1[1]

        st3 = st1[1][index1 + 1:]
        index2 = st3.find('/')
        st4 = st3[0:index2]

        if st4.find('-') != -1:
            st4_1 = st4.split('-')
            self.url_info['target']['protocol'] = st4_1[0]
            self.url_info['target']['port'] = st4_1[1]
        else:
            self.url_info['target']['protocol'] = st4

        st5 = st3[index2 + 1:]
        host_encrypted_target = re.match('[0-9,a-f]*', st5).group(0)
        my_url = st5[len(host_encrypted_target):]
        if my_url == '' or my_url[0] != '/':
            my_url = '/' + my_url
        self.url_info['target']['url'] = my_url

        host_target = self.__decrypt(host_encrypted_target[WebvpnUrl.PREFIX_LEN:])
        self.url_info['target']['host'] = host_target

    def url_encode(self, url=''):
        if url != '':
            self.__get_url_info_from_plain(url)
        return self.__get_url(mode='encode')

    def url_decode(self, url=''):
        if url != '':
            self.__get_url_info_from_encrypted(url)
        return self.__get_url(mode='decode')


if __name__ == '__main__':
    d = WebvpnUrl("webvpn.cpu.edu.cn")
    print("-----------调试-----------")
    print("加密 http（为支持 webVPN，将升为 HTTPS）：")
    print(d.url_encode("http://www.baidu.com"))
    print("加密 ws：")
    print(d.url_encode("ws://121.40.165.18:8800"))
    print("加密 https：")
    print(d.url_encode("https://www.baidu.com"))
    print("加密 wss：")
    print(d.url_encode("wss://121.40.165.18:8800"))
    print()

    print("解密 http：")
    print(d.url_decode(d.url_encode("http://www.baidu.com")))
    print("解密 ws：")
    print(d.url_decode(d.url_encode("ws://121.40.165.18:8800")))
    print("解密 https：")
    print(d.url_decode(d.url_encode("https://www.baidu.com")))
    print("解密 wss：")
    print(d.url_decode(d.url_encode("wss://121.40.165.18:8800")))
    print()

    print("相对路径加密（将以 HTTPS 填充）：")
    print(d.url_encode("//www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"))
    print("相对路径解密：")
    print(d.url_decode(
        "//webvpn.cpu.edu.cn/https/77726476706e69737468656265737421e7e056d2253161546b468aa395/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"))
    print()

    print("不合法 HTTP/HTTPS 加密链接自动补全：")
    print(d.url_encode('https://www.maj-soul.com:443?query=value'))
