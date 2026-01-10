import sys
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# python3 download_pubmed.py https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/    /group/cits5017/sji/cits5553/datasets/pubmed
# python3 download_pubmed.py https://ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/ /group/cits5017/sji/cits5553/datasets/pubmed


def download_files_from_url(url, download_directory):
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error accessing the URL: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    all_links = soup.find_all('a', href=True)
    
    file_extensions = ['.gz']

    downloaded_count = 0
    for link in all_links:
        href = link['href']
        full_url = urljoin(url, href)
        
        if any(full_url.lower().endswith(ext) for ext in file_extensions):
            file_name = os.path.basename(urlparse(full_url).path)
            file_path = os.path.join(download_directory, file_name)

            print(f"Downloading {full_url}...")
            
            try:
                file_response = requests.get(full_url, stream=True)
                file_response.raise_for_status()
                
                with open(file_path, 'wb') as f:
                    for chunk in file_response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f"Successfully downloaded {file_name}")
                downloaded_count += 1
            except requests.exceptions.RequestException as e:
                print(f"Failed to download {full_url}: {e}")
            
    print(f"\nCompleted. Total files downloaded: {downloaded_count}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"{sys.argv[0]} [web_page_url] [save_location]", file=sys.stderr)
        sys.exit(1)
    web_page_url = sys.argv[1]
    save_location = sys.argv[2]
    download_files_from_url(web_page_url, save_location)
