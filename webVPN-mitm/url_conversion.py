from binascii import hexlify, unhexlify
import copy

from Crypto.Cipher import AES


class WebVPN_URL:
    KEY_ = b'wrdvpnisthebest!'
    IV_ = b'wrdvpnisthebest!'
    SIZE = 128
    PREFIX = '77726476706e69737468656265737421'
    PREFIX_LEN = len(PREFIX)
    URL_INFO = {
        'webvpn': {
            'protocol': 'https',
            'hostname': '',
            'port': '',
        },
        'target': {
            'protocol': '',
            'hostname': '',
            'port': '',
            'url': '/',
        }
    }
    def __init__(self, inst_hostname):
        self.INST_HOSTNAME = inst_hostname
        self.url_info = copy.deepcopy(WebVPN_URL.URL_INFO)

    def __encrypt(self, text):
        key = WebVPN_URL.KEY_
        cfb_iv = WebVPN_URL.IV_
        size = WebVPN_URL.SIZE
        cfb_cipher_encrypt = AES.new(key, AES.MODE_CFB, cfb_iv, segment_size=size)

        message = text.encode('utf-8')
        mid = cfb_cipher_encrypt.encrypt(message)
        return hexlify(mid).decode()

    def __decrypt(self, ciphertext):
        key = WebVPN_URL.KEY_
        cfb_iv = WebVPN_URL.IV_
        size = WebVPN_URL.SIZE

        message = unhexlify(ciphertext.encode('utf-8'))
        cfb_cipher_decrypt = AES.new(key, AES.MODE_CFB, cfb_iv, segment_size=size)
        return cfb_cipher_decrypt.decrypt(message).decode('utf-8')

    def __get_url(self,mode):
        hostname_target = self.url_info['target']['hostname']
        if hostname_target != '' and mode == 'encode':
            hostname_encrypted_target = WebVPN_URL.PREFIX + self.__encrypt(hostname_target)
        elif hostname_target == '':
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
                self.url_info['webvpn']['hostname'],
                port_webvpn,
                self.url_info['target']['protocol'],
                port_target,
                hostname_encrypted_target,
                self.url_info['target']['url'],
            )
        elif mode == 'decode':
            url = '%s://%s%s%s' % (
                self.url_info['target']['protocol'],
                hostname_target,
                port_target,
                self.url_info['target']['url'],
            )
        return url

    def __get_url_info_from_plain(self, url):
        self.url_info = copy.deepcopy(WebVPN_URL.URL_INFO)

        self.url_info['webvpn']['hostname'] = self.INST_HOSTNAME

        st1 = url.split('//')
        self.url_info['target']['protocol'] = st1[0][:-1]
        if st1[0] == 'ws:' or st1[0] == 'wss:':
            self.url_info['webvpn']['protocol'] = 'wss'
        index = st1[1].find('/')
        if index == -1:
            st2 = st1[1][0:]
            self.url_info['target']['url'] = '/'
        else:
            st2 = st1[1][0:index]
            self.url_info['target']['url'] = st1[1][index:]

        if st2.find(':') != -1:
            st2_1 = st2.split(':')
            self.url_info['target']['hostname'] = st2_1[0]
            self.url_info['target']['port'] = st2_1[1]
        else:
            self.url_info['target']['hostname'] = st2

    def __get_url_info_from_encrypted(self, url):
        self.url_info = copy.deepcopy(WebVPN_URL.URL_INFO)

        self.url_info['webvpn']['hostname'] = self.INST_HOSTNAME

        st1 = url.split('//')
        if st1[0] == '':
            st1[0] = 'https:'
        self.url_info['webvpn']['protocol'] = st1[0][:-1]
        
        index1 = st1[1].find('/')
        st2 = st1[1][0:index1]

        if st2.find(':') != -1:
            st2_1 = st2.split(':')
            self.url_info['webvpn']['port'] = st2_1[1]
        
        st3 = st1[1][index1+1:]
        index2 = st3.find('/')
        st4 = st3[0:index2]

        if st4.find('-') != -1:
            st4_1 = st4.split('-')
            self.url_info['target']['protocol'] = st4_1[0]
            self.url_info['target']['port'] = st4_1[1]
        else:
            self.url_info['target']['protocol'] = st4

        st5 = st3[index2+1:]
        index3 = st5.find('/')
        if index3 != -1:
            hostname_encrypted_target = st5[:index3]
            self.url_info['target']['url'] = st5[index3:]
        else:
            hostname_encrypted_target = st5
            self.url_info['target']['url'] = '/'

        hostname_target = self.__decrypt(hostname_encrypted_target[WebVPN_URL.PREFIX_LEN:])
        self.url_info['target']['hostname'] = hostname_target

    def url_encode(self, url=''):
        if url != '':
            self.__get_url_info_from_plain(url)
        return self.__get_url(mode = 'encode')

    def url_decode(self, url):
        if url != '':
            self.__get_url_info_from_encrypted(url)
        return self.__get_url(mode = 'decode')

if __name__ == '__main__':
    d = WebVPN_URL("webvpn.cpu.edu.cn")
    print(d.url_encode("ws://1.1.1.1:8800"))
    print(d.url_decode(d.url_encode("ws://1.1.1.1:8800")))
    print(d.url_decode(
        "//webvpn.cpu.edu.cn/https/77726476706e69737468656265737421e7e056d2253161546b468aa395/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"))
