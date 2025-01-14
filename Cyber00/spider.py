import os
import sys
import requests
import re
from bs4 import BeautifulSoup

# url = "https://unsplash.com"
# url = "https://pixabay.com/fr/"
# url = "https://fr.wikipedia.org/wiki/Testost%C3%A9rone"
url = "https://www.google.com"
# url = "https://www.gettyimages.fr/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': url,
}

visited_sites = []

dir_path = "./data/"

if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
    os.makedirs(dir_path)

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("Invalid URL, status code : ", response.status_code)
    exit(1)

page = response.text

soup = BeautifulSoup(page, 'html.parser')

image_urls = []

for img in soup.find_all('img'):
    image_urls.append(img.get('src')) 

for i, sub in enumerate(image_urls):
    if sub.startswith("//") is True:
       image_urls[i] = "https:" + sub
    elif sub.startswith("/") is True:
        image_urls[i] = url + sub
    else:
        continue

for image in image_urls:
    if image.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        try:
            response = requests.get(image, headers=headers)
            x = re.search(r"[^/]+$", image)
            if x:
                file_name = x.group(0)
                file_path = os.path.join(dir_path, file_name)
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                print("Successfully downloaded : ", image)
        except Exception as e:
            print("Impossible to Download : ", image)
            print("Error: ", str(e))
    else:
        print("Wrong format of image: ", image)
    print()