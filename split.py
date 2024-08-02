import os
from subprocess import call
from tqdm import tqdm

def split(filepath, target_path = None):
    max_lines = 10**6
    cmd = f'split -l {max_lines} {filepath}'
    if target_path is not None:
        cmd += f' {target_path}'
    print(cmd)
    call(cmd, shell=True)


def split_all(folderpath):
    os.makedirs(os.path.join(folderpath, 'shards'), exist_ok=True)
    for filename in tqdm(os.listdir(folderpath)):
        if not os.path.isfile(os.path.join(folderpath, filename)):
            continue
        filepath = os.path.join(folderpath, filename)
        if filename.endswith('.zip') or filename.endswith('.gz'):
            continue
        split(filepath, target_path = os.path.join(folderpath, 'shards', filename + '_'))

if __name__=='__main__':
    split_all('/media/scholar/cca30a4f-fb5b-4ec5-9bca-8f51dad1364c/citations')