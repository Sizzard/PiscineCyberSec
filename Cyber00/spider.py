import requests
import re
import os

# url = "https://unsplash.com"
# url = "https://fr.wikipedia.org/wiki/Testost%C3%A9rone"
url = "https://www.google.com"

visited_sites = []

dir_path = "./data/"

if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
    os.makedirs(dir_path)

response = requests.get(url)

if response.status_code != 200:
    print("Invalid URL, exit code : ", response.status_code)
    exit(1)

page = response.text

# print(page)

pattern = r'<img[^>]*src=["\']([^"\']+)["\']'

image_urls = re.findall(pattern, page)

print(image_urls)
print()

for i, sub in enumerate(image_urls):
    if sub.startswith("http") is False:
        try:
            if requests.get(url + sub).status_code == 200:
                image_urls[i] = url + sub
            else:
                image_urls[i] = "https:" + sub        
        except:
            image_urls[i] = "https:" + sub    

print(image_urls)

for image in image_urls:
    try:
        response = requests.get(image)
        test = os.path.splitext(image)
        x = re.search("[^/]*." + test[1], image)
        file_path = os.path.join(dir_path, x.group(0))
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print("Successfully downloaded : ", image)
    except:
        print("Impossible to Download : ", image)
    print("")