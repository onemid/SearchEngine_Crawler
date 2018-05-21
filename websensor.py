import urllib.robotparser
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import httpfetcher
import sys
import random
import re


class WebSensor():
    def __init__(self):
        pass

    def redirect_detect(self, context):

        r = BeautifulSoup(context, 'lxml')
        meta_refresh = r.find('meta', attrs={"http-equiv": "refresh"})
        if meta_refresh is not None:
            meta_refresh = meta_refresh.get('content')
            meta_refresh = meta_refresh.split(';')
            return min(int(meta_refresh[0]), 15)
        if "window.location" in context:
            return 10
        return 0
