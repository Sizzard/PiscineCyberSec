import os
import sys
import requests
import re
from bs4 import BeautifulSoup
from termcolor import colored
from urllib.parse import urlparse

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
        }
        self.recurse(self.given_url, 1)

    def createFolder(self):
        try:
            if not os.path.exists(self.path) or not os.path.isdir(self.path):
                os.mkdir(self.path)
            if not os.access(self.path, os.W_OK):       
                raise Exception
        except:
            print("Error on creating folder, it might not work")

    def recurse(self, url, level):
        print(colored('Level is : ' + str(level), 'cyan'))
        print(colored('URL is : ' + str(url), 'yellow'))
        print(colored('visited : ' + str(self.visited), 'cyan'))
        print()

        if level == self.max_depth or url in self.visited:
            return

        self.visited.append(url)
        
        soup = self.requestSite(url)
        images_url = []
        self.parseImages(soup, url,images_url)
        for image in images_url:
            print(image)
        sites_url = []
        self.parseLinks(soup, url, sites_url)
        self.saveImages(images_url)

        level += 1
        
        for site_url in sites_url:
            self.recurse(site_url, level)

    def requestSite(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            print("Invalid URL, status code : ", response.status_code)
            raise Exception("Invalid URL")
        self.soup = BeautifulSoup(response.text, 'html.parser')
        return self.soup

    def parseImages(self, soup, url, images_url):
        for img_url in self.soup.find_all('img'):
            if img_url.get('src'):
                images_url.append(img_url.get('src'))
        for i, sub in enumerate(images_url):
            if sub.startswith("//") is True:
                images_url[i] = "https:" + sub
            elif sub.startswith("/") is True:
                images_url[i] = url + sub
            else:
                continue

    def parseLinks(self, soup, base_url, sites_url):
        for site_url in soup.find_all('a'):
            url = site_url.get('href')
            if url and url.startswith('#') is False:
                if url.startswith('/') and not url.startswith('//'):
                    parsed_url = urlparse(base_url)
                    base_url = parsed_url.scheme + "://" + parsed_url.netloc
                    sites_url.append(base_url + '/' + url)
                else:
                    sites_url.append(url)

    def saveImages(self, images_url):
        for image in images_url:
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
                        print(colored("Successfully downloaded : " + str(image), 'green'))
                except Exception as e:
                    print(colored("Error: " + str(e), 'red'))
            else:
                print(colored("Wrong format of image : " + str(image), 'red'))
            print()