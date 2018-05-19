import socket
import re

class DNSResolver():
    def __init__(self):
        pass

    def resolve_url(self, domain_name):
        return socket.gethostbyname(domain_name)