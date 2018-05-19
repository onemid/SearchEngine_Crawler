import os
import sys
import hashlib
from elasticsearch import Elasticsearch


class Store():

    def __init__(self, location='', filename=''):
        self.md5 = hashlib.md5()
        self.location = location
        self.filename = filename

    def store(self, context):
        self.md5.update(self.filename.encode('utf-8'))
        with open(self.location + self.md5.hexdigest(), encoding='utf-8', mode='w+') as f:
            f.write('@url:' + self.filename + '\n')
            f.write(context)
        return

    def store_to_es(self, index, doc_type, body):
        es = Elasticsearch()
        res = es.index(index=index, doc_type=doc_type, body=body)
        return res
