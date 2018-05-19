class DupURLDel():
    def __init__(self, urls_seen=set()):
        self.urls_seen = urls_seen

    def verify_seen_filter(self, urls):
        if type(urls) == list:
            urls = set(urls)
        elif type(urls) == str:
            urls = set([urls])

        return list(urls - self.urls_seen)

    def check_if_seen(self, url):
        return url in self.urls_seen

    def add_to_urls_seen(self, url):
        self.urls_seen.add(url)
        return

    def get_urls_seen(self):
        return self.urls_seen
