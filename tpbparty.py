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
    url = 'https://pirateproxy.live'

    def __init__(self):
        self.name = 'tpb.party(thepiratebay proxy site)'
        self.supported_categories = {'all': '0'}

    def search(self, query, cat='all'):
        query = query.replace(' ', '%20')
        parser = self.TpbPartyHtmlParser(self.url)

        def _search(url,query,cat,page):
            torrent_list = re_compile('(?s)<table id="searchResult">(.*)</table>')
            request_url = '{0}/search/{1}/{2}/99/{3}'.format(url,query,page,self.supported_categories[cat])
            print('retrieve_url and return data..')
            data = retrieve_url(request_url)
            print('>> ',data)
            data = torrent_list.search(data).group(0)
            print('start parse feed data')
            parser.feed(data)
            parser.close()
            return data
        
        search_data = None
        page = 1
        
        while True:
            if search_data == None or search_data.find('searchResult') != -1:
                search_data = _search(self.url, query, cat, page)
                print(">> page ", page)
                page += 1
            else:
                break


    def download_torrent(self,info):
        print(download_file(info))

    class TpbPartyHtmlParser(HTMLParser):
        def __init__(self,url):
            HTMLParser.__init__(self)
            self.url = url
            self.item = None
            self.item_found = False
            self.size_found = False
            self.size_regex = re_compile('.*Size\s([^ ]*),.*')
            self.name_found = False
            self.stats_found = False 
            self.stats = ['seed','leech']
            self.stats_count = -1

        def handle_starttag(self,tag,attrs):
            attrsMap = dict(attrs)
            if tag == 'tbody':
                self.item_found = True
            elif self.item_found: 
                if tag == 'tr':
                   self.item = dict() 
                   self.item['engine_url'] = self.url
                elif self.item:
                    if tag == 'a':
                        if attrsMap['class'] == 'detLink':
                           self.item['desc_link'] = attrsMap['href']
                           self.name_found = True
                        elif attrsMap['href'].startswith('magnet'):
                           self.item['link']=attrsMap['href']
                    elif tag == 'font' and attrsMap['class'] == 'detDesc':
                        self.size_found = True
                    if tag == 'td' and attrsMap['align'] == 'right':
                       self.stats_found = True
                       self.stats_count += 1
        def handle_data(self,data):
            if self.name_found:
                self.item['name']=data
                self.name_found = False
            elif self.size_found:
                result = self.size_regex.search(data)
                if result:
                    self.item['size']=result.group(1)
                    self.size_found = False
            elif self.stats_found:
                self.item[self.stats[self.stats_count]]=data
                if self.stats_count == len(self.stats):
                    self.stats_count = -1
                    self.stats_found = False
        def handle_endtag(self,tag):
            if tag == 'tr' and self.item and len(self.item) == 7:
                prettyPrinter(self.item)
                self.item = None
if __name__ == '__main__':
    tpb = tpbparty()
    tpb.search('sweetie fox')
