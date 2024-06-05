import os
from subprocess import call
def unzip(filepath):
    # inplace
    cmd = f'file-roller -h {filepath}'
    print(cmd)
    call(cmd, shell=True)

if __name__=='__main__':
    unzip('/home/scholar/Desktop/download_ss_dataset/updates/0.zip')