from Crypto.Cipher import AES
from binascii import hexlify

KEY_ = b'wrdvpnisthebest!'
IV_  = b'wrdvpnisthebest!'
INST_HOSTNAME = 'webvpn.cpu.edu.cn'

URL_INFO = {
    'webvpn': {
        'protocol': 'https',
        'hostname': INST_HOSTNAME,
        'port':'',
    },
    'target': {
        'protocol': 'https',
        'hostname_pln': '',
        'port': '',
        'uri': '/',
    }
}

def encrypt(text_pln, key = KEY_, cfb_iv = IV_, size = 128):
    cfb_cipher_encrypt = AES.new(key, AES.MODE_CFB, cfb_iv, segment_size = size)

    message = text_pln.encode('utf-8')
    mid = cfb_cipher_encrypt.encrypt(message)
    res = hexlify(cfb_iv).decode('utf-8') + hexlify(mid).decode()

    return res

def get_url(url_info):
    hostname_pln_target = url_info['target']['hostname_pln']
    if hostname_pln_target != '':
        hostname_encrypted_target = encrypt(hostname_pln_target)
    else:
        return ''

    port_webvpn = str(url_info['webvpn']['port'])
    if port_webvpn != '':
        port_webvpn = ':' + port_webvpn

    port_target = str(url_info['target']['port'])
    if port_target != '':
        port_target = '-' + port_target

    url = '%s://%s%s/%s%s/%s%s' %(
        url_info['webvpn']['protocol'],
        url_info['webvpn']['hostname'],
        port_webvpn,
        url_info['target']['protocol'],
        port_target,
        hostname_encrypted_target,
        url_info['target']['uri'],
    )
    return url

def get_url_info(url):
    url_info = URL_INFO.copy()

    st1 = url.split('://')
    url_info['target']['protocol'] = st1[0]

    index = st1[1].find('/')
    if index == -1:
        st2 = st1[1][0:]
        url_info['target']['uri'] = ''
    else:
        st2 = st1[1][0:index]
        url_info['target']['uri'] = st1[1][index:]

    if st2.find(':') != -1:
        st3 = st2.split(':')
        url_info['target']['hostname_pln'] = st3[0]
        url_info['target']['port'] = st3[1]
    else:
        url_info['target']['hostname_pln'] = st2

    return url_info

if __name__ == '__main__':
    # Test only
    my_url_info = get_url_info('https://www.cpu.edu.cn/')
    # print(my_url_info)
    # my_url_info = {
    #     'webvpn': {
    #         'protocol': 'https',
    #         'hostname': INST_HOSTNAME,
    #         'port':'',
    #     },
    #     'target': {
    #         'protocol': 'https',
    #         'hostname_pln': 'cn.bing.com',
    #         'port': '443',
    #         'uri': '/?mkt=zh-CN',
    #     }
    # }
    print(get_url(my_url_info))
    