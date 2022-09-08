import os
import sys

def is_exec():
    if getattr(sys, 'frozen', False):
        return True
    else:
        return False

def get_dir(myfile=__file__):
    if is_exec():
        mydir=os.path.dirname(os.path.abspath(sys.executable))
    else:
        mydir=os.path.dirname(os.path.abspath(myfile))
    return mydir
