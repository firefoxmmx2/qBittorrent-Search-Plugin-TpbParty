#VERSION 1.0
#Author: firefoxmmx (firefoxmmx@163.com)

try:
    #python3
    from html.parser import HTMLParser
except ImportError:
    #python2
    from HTMLParser import HTMLParser

from re import compile as re_compile

#qBt
from novaprinter import prettyPrinter
from helpers import download_file, retrieve_url


class tpbparty(object): 
    url = 'https://tpb.party'

    def __init__(self):
        self.name = 'tpb.party(thepiratebay proxy site)'


