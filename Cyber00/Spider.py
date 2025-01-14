import os
import sys
import requests
import re
from bs4 import BeautifulSoup

class Spider:
    def __init__(self, given_url, recursive, length, path):
        self.given_url = given_url
        self.recursive = recursive
        if not recursive:
            self.max_depth = 1
        else:
            self.max_depth = 5
        self.path = path
        self.images_url = []
        self.sites_url = []
        self.visited = []
        print("Base URL = ", self.given_url)
        print("Recursive = ", self.recursive)
        print("Max depth = ", self.max_depth)
        print("Folder = ", self.path)
        self.createFolder()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': self.given_url,
        }
        self.launch()
        # self.recurse(self.given_url, 1)

    def createFolder(self):
        try:
            if not os.path.exists(self.path) or not os.path.isdir(self.path):
                os.mkdir(self.path)
            if not os.access(self.path, os.W_OK):       
                raise Exception
        except:
            print("Error on creating folder, it might not work")

    def launch(self):
        for x in range(self.max_depth):
            self.requestSite(self.given_url)
            self.parseImages()
            self.parseLinks()
            self.addSuffix()
            self.saveImages()

    # def recurse(self, url, level):
    #     if level == self.level
    #         return
        
    #     level += 1
    #     recurse(level)

    def requestSite(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            print("Invalid URL, status code : ", response.status_code)
            exit(1)
        self.soup = BeautifulSoup(response.text, 'html.parser')

    def parseImages(self):
        for img_url in self.soup.find_all('img'):
            if img_url.get('src'):
                self.images_url.append(img_url.get('src'))

    def parseLinks(self):
        for site_url in self.soup.find_all('a'):
            if site_url.get('href'):
                self.sites_url.append(site_url.get('href')) 

        for line in self.sites_url:
            print(line)
    
    def addSuffix(self):
        for i, sub in enumerate(self.images_url):
            if sub.startswith("//") is True:
                self.images_url[i] = "https:" + sub
            elif sub.startswith("/") is True:
                self.images_url[i] = self.given_url + sub
            else:
                continue

    def saveImages(self):
        for image in self.images_url:
            if image.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                try:
                    response = requests.get(image, headers=self.headers)
                    if response.status_code != 200:
                        raise Exception("Can't get image") 
                    x = re.search(r"[^/]+$", image)
                    if x:
                        file_name = x.group(0)
                        file_path = os.path.join(self.path, file_name)
                        with open(file_path, 'wb') as file:
                            file.write(response.content)
                        print("Successfully downloaded : ", image)
                except Exception as e:
                    print("Error: ", str(e))
            else:
                print("Wrong format of image: ", image)
            print()