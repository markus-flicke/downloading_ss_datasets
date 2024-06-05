import requests
import json
import os

UPDATES_PATH = 'updates'
DELETIONS_PATH = 'deletions'

def dir_delete_all_files(path):
    files = os.listdir(path)
    for f in files:
        os.remove(os.path.join(path, f))

def download_updates(since_date="2024-05-21"):
    os.makedirs(UPDATES_PATH, exist_ok=True)
    os.makedirs(DELETIONS_PATH, exist_ok=True)
    dir_delete_all_files(UPDATES_PATH)
    dir_delete_all_files(DELETIONS_PATH)
    
    with open('api_key.txt', 'r') as f:
        api_key = f.read().strip()
        headers = {
            "x-api-key": api_key
        }
    latest_release_date = requests.get('https://api.semanticscholar.org/datasets/v1/release/latest', headers=headers).json()['release_id']
    difflist = requests.get(f'https://api.semanticscholar.org/datasets/v1/diffs/{since_date}/to/latest/papers', 
                            headers=headers).json()
    for diff in difflist['diffs']:
        for idx, url in enumerate(diff['update_files']):
            file_content = requests.get(url, headers=headers).content
            filepath = os.path.join(UPDATES_PATH, f'{idx}.zip')
            with open(filepath, 'wb') as f:
                f.write(file_content)

        for idx, url in enumerate(diff['delete_files']):
                file_content = requests.get(url, headers=headers).content
                filepath = os.path.join(DELETIONS_PATH, f'{idx}.zip')
                with open(filepath, 'wb') as f:
                    f.write(file_content)

if __name__=='__main__':
    download_updates()