from bs4 import BeautifulSoup
from urllib.parse import urlparse
import httpfetcher
import sys
import random

class LinkExtractor():
    def __init__(self, url):
        self.__url = url
        self.__extract_url = list()

    def parse_page_links(self, context):

        sys.stdout.write('[*] Parsing URLs: %s\r' % (self.__url))
        sys.stdout.flush()

        fetcher = httpfetcher.HTTPFetcher(self.__url)
        parsed = fetcher.parse_url()
        c = BeautifulSoup(context, 'lxml')

        for link in c.find_all('a'):
            link = link.get('href')
            if type(link) == str:
                if link.lstrip().startswith('https://') or link.lstrip().startswith('http://'):
                    self.__extract_url.append(link)
                elif link.lstrip().startswith('//'):
                    self.__extract_url.append(
                        parsed['scheme'] + ':' + link)
                elif link.lstrip().startswith('/'):
                    self.__extract_url.append(
                        parsed['scheme'] + '://' + parsed['domain_name'] + link)
                else:
                    self.__extract_url.append(
                        parsed['scheme'] + '://' + parsed['domain_name'] + parsed['web_path'] + '/' + link + '?' + parsed['query'])

        random.shuffle(self.__extract_url)
        
        return self.__extract_url
