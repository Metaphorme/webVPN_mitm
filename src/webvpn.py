import getpass

def is_exec():
    import sys
    if getattr(sys, 'frozen', False):
        return True
    else:
        return False

def get_dir(myfile=__file__):
    import os
    if is_exec():
        import sys
        mydir=os.path.dirname(os.path.abspath(sys.executable))
    else:
        mydir=os.path.dirname(os.path.abspath(myfile))
    return mydir

MYDIR = get_dir()

def get_credentials():
    cred = []
    try:
        with open(MYDIR + '/credentials.txt','r',encoding='utf-8') as f:
            cred = f.read().strip().split('\n')
    except FileNotFoundError:
        pass

    if len(cred) == 0:
        cred.append(input('请输入学号: '))
    else:
        print('学号为: %s' %(cred[0]))
    if len(cred) <= 1:
        cred.append(getpass.getpass('请输入密码: '))
    else:
        print('密码已提供')

    return cred

if __name__ == '__main__':
    # Test only
    print(get_credentials())
