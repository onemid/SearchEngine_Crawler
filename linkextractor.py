from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import httpfetcher
import sys
import random


class LinkExtractor():
    def __init__(self, url):
        self.__url = url
        self.__extract_url = list()

    def parse_page_links(self, context):
        sys.stdout.write("\033[K")
        sys.stdout.write('[*] Parsing URLs: %s\r' % (self.__url))
        sys.stdout.flush()

        fetcher = httpfetcher.HTTPFetcher(self.__url)
        parsed = fetcher.parse_url()
        c = BeautifulSoup(context, 'lxml')
        parsed['scheme'] = parsed['scheme'] + \
            ':' if parsed['scheme'] != '' else parsed['scheme']
        parsed['web_path'] = parsed['web_path'] + \
            '/' if parsed['web_path'] != '' else parsed['web_path']

        for link in c.find_all('a'):
            link = link.get('href')
            if type(link) == str:
                self.__extract_url.append(urljoin(self.__url, link))
                # if link.lstrip().startswith('https://') or link.lstrip().startswith('http://'):
                #     # self.__extract_url.append(link)
                #     self.__extract_url.append()
                # elif link.lstrip().startswith('//'):
                #     self.__extract_url.append(
                #         parsed['scheme'] + link)
                # elif link.lstrip().startswith('/'):
                #     self.__extract_url.append(
                #         parsed['scheme'] + '//' + parsed['domain_name'] + link)
                # elif link.lstrip().startswith('javascript:'):
                #     pass
                # elif link.lstrip().startswith('mailto:'):
                #     pass
                # else:
                #     self.__extract_url.append(
                #         parsed['scheme'] + '//' + parsed['domain_name'] + parsed['web_path'] + link + '?' + parsed['query'])

        random.shuffle(self.__extract_url)

        return self.__extract_url
