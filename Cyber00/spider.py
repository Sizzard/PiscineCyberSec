import argparse
from Spider import Spider

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='This program scraps for image in the URL you give')

    parser.add_argument('-r', "--recursive", action="store_true", default=False)
    parser.add_argument('-l', "--length", nargs='?', default=5)
    parser.add_argument('-p', "--path", nargs='?', default="data")
    parser.add_argument('URL')
    args = parser.parse_args()

    spider = Spider(args.URL, args.recursive, args.length, args.path)

    urls = []

    # for site_url in soup.find_all('a'):
    #     if site_url.get('href'):
    #         urls.append(site_url.get('href')) 

    # for site_url in urls:
    #     print(site_url)

