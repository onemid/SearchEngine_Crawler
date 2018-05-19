from bs4 import BeautifulSoup
import bcolors


class ContentParser():
    def __init__(self):
        self.title = ''
        self.body = ''

    def content_parsing(self, context):
        bc = bcolors.bcolors()
        r = BeautifulSoup(context, 'lxml')
        try:
            self.title = r.title.string
        except:
            print('%s[!] Content Parsing Error - Unknown Title%s\r' %
                  (bc.OKBLUE, bc.ENDC))
            self.title = 'unknown'

        for script in r(["script", "style", "nav", "form", "footer", "noscript", "header"]):
            script.decompose()  # rip it out

        # for code in r()
        self.body = r.get_text()

        # break into lines and remove leading and trailing space on each
        self.body = (line.strip() for line in self.body.splitlines())
        # break multi-headlines into a line each
        self.body = (phrase.strip()
                     for line in self.body for phrase in line.split("  "))
        # drop blank lines
        self.body = ' '.join(chunk for chunk in self.body if chunk)

        return {'title': self.title, 'body': self.body}
