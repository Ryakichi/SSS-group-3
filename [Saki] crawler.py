import pandas as pd


import requests
from concurrent.futures import ThreadPoolExecutor
import os
import json


# Function to download HTML and save it to a file
def download_html(link_filename_pair):
    link, filename = link_filename_pair
    try:
        response = requests.get(link, timeout=20)  # Set timeout to prevent hanging
        if response.status_code == 200:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(response.text)
            return f"Successfully saved: {filename}"
        else:
            return f"Failed to download {link}: Status code {response.status_code}"
    except requests.RequestException as e:
        return f"Error downloading {link}: {e}"

# Parallelized downloading
def download_all(links, app_names):
    if len(links) != len(app_names):
        raise ValueError("The number of links and filenames must match.")
    
    # Create pairs of links and filenames
    link_filename_pairs = zip(links, app_names)

    # Use ThreadPoolExecutor for parallel requests
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(download_html, link_filename_pairs))

    return results


def crawl():
    df = pd.read_csv('flows.csv', names=['1', '2', '3', '4','5','6','7','8','9'])
    links = []
    app_names = []
    for i in range(len(df.index)):
        link = df.iloc[i]['9']
        if isinstance(link, str):
            if link not in links:
                links.append(link)
                app_name = df.iloc[i]['1']
                if '+' in app_name:
                    app_name = app_name.split('+')[1]
                app_names.append('plaintext_policies/' + app_name + '.txt')

    print('Crawling {} policies.'.format(len(links)))

    results = download_all(links, app_names)
    with open('download_result.txt', 'w') as file:
        file.write(json.dumps(results))


if __name__ == '__main__':
    crawl()

