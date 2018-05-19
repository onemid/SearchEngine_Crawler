import re
import multiprocessing as mp
import sys


class URLFilter():
    def __init__(self, urls=list(), exc_rules=list(), inc_rules=list()):
        self.urls = list(urls)
        self.exc_rules = list(exc_rules)
        self.inc_rules = list(inc_rules)

    def filter(self):
        inc_filtered_urls = []
        exc_filtered_urls = []

        if self.inc_rules != []:
            for rule in self.inc_rules:
                rule = re.compile(rule)
                inc_filtered_urls.extend(
                    [url for url in self.urls if re.match(rule, url) != None])

        if self.exc_rules != []:
            for rule in self.exc_rules:
                rule = re.compile(rule)
                exc_filtered_urls.extend(
                    [url for url in inc_filtered_urls if re.match(rule, url) == None])

        if self.inc_rules == [] and self.exc_rules == []:
            return self.urls
        else:
            return inc_filtered_urls
