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
    hostname_pln = url_info['target']['hostname_pln']
    if hostname_pln != '':
        hostname_encrypted = encrypt(hostname_pln)
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
        hostname_encrypted,
        url_info['target']['uri'],
    )
    return url

if __name__ == '__main__':
    # Test only
    # my_url_info = URL_INFO.copy()
    my_url_info = {
        'webvpn': {
            'protocol': 'https',
            'hostname': INST_HOSTNAME,
            'port':'',
        },
        'target': {
            'protocol': 'https',
            'hostname_pln': 'cn.bing.com',
            'port': '443',
            'uri': '/?mkt=zh-CN',
        }
    }
    print(get_url(my_url_info))
    