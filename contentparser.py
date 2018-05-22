from bs4 import BeautifulSoup
import bcolors
import sys


class ContentParser():
    def __init__(self):
        self.title = ''

        self.property_og_title = ''
        self.property_og_url = ''
        self.property_og_description = ''
        self.property_og_image = ''

        self.itemprop_name = ''
        self.itemprop_img = ''
        self.itemprop_description = ''

        self.name_img = ''
        self.name_description = ''
        self.name_author = ''

        self.body = ''

    def content_parsing(self, context):
        bc = bcolors.bcolors()
        r = BeautifulSoup(context, 'lxml')
        sys.stdout.write("\033[K")
        sys.stdout.write('[*] Parsing Contents...\r')
        sys.stdout.flush()
        try:
            self.title = r.title.string
            title = r.find("meta",  attrs={"property":"og:title"})
            url = r.find("meta",  attrs={"property":"og:url"})
            description = r.find("meta",  attrs={"property":"og:description"})
            image = r.find("meta",  attrs={"property":"og:image"})

            self.property_og_title = title["content"] if title else ""
            self.property_og_url = url["content"] if url else self.property_og_url
            self.property_og_description = description["content"] if description else self.property_og_description
            self.property_og_image = image["content"] if image else self.property_og_image

            name = r.find("meta",  attrs={"itemprop":"name"})
            description = r.find("meta",  attrs={"itemprop":"description"})
            image = r.find("meta",  attrs={"itemprop":"og:image"})

            self.itemprop_name = name["content"] if name else self.itemprop_name
            self.property_og_description = description["content"] if description else self.property_og_description
            self.property_og_image = image["content"] if image else self.property_og_image

            author = r.find("meta",  attrs={"name":"author"})
            description = r.find("meta",  attrs={"name":"description"})
            image = r.find("meta",  attrs={"name":"image"})

            self.name_author = author["content"] if author else self.name_author
            self.property_og_description = description["content"] if description else self.property_og_description
            self.property_og_image = image["content"] if image else self.property_og_image
        except:
            print('%s[!] Content Parsing Error - Unknown Elements%s\r' %
                  (bc.OKBLUE, bc.ENDC))
            self.title = ''

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

        return {'title': self.title,
                'property_og_title': self.property_og_title,
                'property_og_url': self.property_og_url,
                'property_og_description': self.property_og_description,
                'property_og_image': self.property_og_image,
                'itemprop_name': self.itemprop_name,
                'name_author': self.name_author,
                'body': self.body}
