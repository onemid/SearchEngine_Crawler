import requests
import re
from urllib.parse import urlparse
import dnsresolver
import time
import random
import sys
import json
import bcolors


from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class HTTPFetcher():
    def __init__(self, url, encoding='', render='requests'):
        self.__url = url
        self.__render = render
        self.__encoding = encoding
        self.__text = ''
        self.__status_code = 0
        self.__d = DesiredCapabilities.CHROME
        self.__d['loggingPrefs'] = {'performance': 'ALL'}

    def _be_a_good_bot(self, waiting_time=-1):
        if waiting_time == -1:
            time.sleep(random.randint(3, 10))
        else:
            time.sleep(waiting_time)
        return

    def _get_http_status(self, browser):
        for responseReceived in browser.get_log('performance'):
            try:
                response = json.loads(responseReceived[u'message'])[
                    u'message'][u'params'][u'response']
                if response[u'url'] == browser.current_url:
                    return response[u'status']
            except:
                pass
        return None

    def fetch_page(self):
        self._be_a_good_bot()
        bc = bcolors.bcolors()
        sys.stdout.write('[>] Fetching: %s\r' % (self.__url))

        if self.__render == 'requests':
            try:
                r = requests.get(self.__url)
                self.__status_code = r.status_code
                r.encoding = self.__encoding if self.__encoding != '' else r.encoding
                self.__text = r.text if self.__status_code == 200 else ''
            except Exception:
                pass
        elif self.__render == 'selenium':
            r = webdriver.Chrome(
                './crawler/driver/chromedriver', desired_capabilities=self.__d)
            try:
                r.get(self.__url)
                self.__status_code = self._get_http_status(r)
                self.__status_code = self.__status_code if type(
                    self.__status_code) is int else 0
                self.__text = r.page_source if self.__status_code == 200 else ''
            except Exception:
                pass
            r.close()

        if self.__status_code != 200:
            print('%s[!] Response [%d]%s: %s\r' %
                  (bc.OKBLUE, self.__status_code, bc.ENDC, self.__url))
            if self.__status_code == 429:
                self._be_a_good_bot(300)

        return self.__text, self.__status_code

    def parse_url(self):
        url_parse = urlparse(self.__url)
        return {'scheme': url_parse.scheme,
                'domain_name': url_parse.netloc,
                'web_path': url_parse.path,
                'query': url_parse.query}

    def get_domain_ip(self):
        parsed = self.parse_url()
        r_dns = dnsresolver.DNSResolver()
        return r_dns.resolve_url(parsed['domain_name'])
