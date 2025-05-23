# https://github.com/allenai/s2-folks/blob/main/examples/Webinar%20Code%20Examples/Datasets_Download_a_Dataset.py

import os
import requests
from tqdm import tqdm



def download_dataset(dataset_name, dataset_savepath, start_save_idx=1):
    dataset_savepath = os.path.join(dataset_savepath, dataset_name)
    os.makedirs(dataset_savepath, exist_ok=True)

    # Fetch API key from environment variables
    api_key = os.getenv("S2_API_KEY")
    with open('api_key.txt', 'r') as f:
        api_key = f.read().strip()
    headers = {
        "x-api-key": api_key
    }

    # Fetch the ID of the latest release
    response_latest_release = requests.get('https://api.semanticscholar.org/datasets/v1/release/latest', headers=headers)
    latest_release_id = response_latest_release.json()['release_id']
    print(f"Latest Release ID: {latest_release_id}")

    # Fetch the download links for the specified dataset in the latest release
    response_dataset = requests.get(f'https://api.semanticscholar.org/datasets/v1/release/{latest_release_id}/dataset/{dataset_name}', headers=headers)

    # Check if the request was successful
    if response_dataset.status_code == 200:
        data = response_dataset.json()
        # Check if the 'files' key exists in the response
        if 'files' in data:
            download_links = data['files']

            # Download the dataset
            # Note: Datasets might be split into multiple parts. Loop through each part and download.

            for idx, link in tqdm(enumerate(download_links[start_save_idx-1:], start=start_save_idx)):
                response = requests.get(link, headers=headers)
                print(link)
                filepath = os.path.join(dataset_savepath, f'{dataset_name}_part{idx}.gz')
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded part {idx} of the {dataset_name} dataset.")
            
            print("Download completed!")
        else:
            print("No files found for the specified dataset in the latest release.")
    else:
        print(f"Failed to fetch data for the {dataset_name} dataset in the latest release. HTTP status code: {response_dataset.status_code}")


if __name__=='__main__':
    download_dataset(dataset_name = "papers", 
                     dataset_savepath = '/home/scholar/s2orc/papers', 
                     start_save_idx=1)
    # Downloaded papers, authors, abstracts and citations