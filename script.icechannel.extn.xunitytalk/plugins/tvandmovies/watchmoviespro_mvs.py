'''
    watchmoviespro
    Copyright (C) 2014 Coolwave
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common
import os

do_no_cache_keywords_list = ['Sorry for this interruption but we have detected an elevated amount of request from your IP']

class watchmoviespro(MovieSource):
    implements = [MovieSource]
    
    name = "watchmoviespro"
    display_name = "watchmoviespro"
    cookie_file = os.path.join(common.cookies_path, 'watchmoviespro')
    source_enabled_by_default = 'false'
    
    def GetFileHosts(self, url, list, lock, message_queue):
        import re
        from entertainment.net import Net
        net = Net(cached=False)
        content = net.http_GET(url).content
        r = "onclick=\"window.open\('(.+?)', '_blank'\);\">(.+?)\s(.+?)</a>" 
        match  = re.compile(r).findall(content)
        for url,host,res in match:      
        
            self.AddFileHost(list, res, url,host=host.upper())
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):
        import re
        from entertainment.net import Net
        
        net = Net(do_not_cache_if_any=do_no_cache_keywords_list)
        
        if os.path.exists(self.cookie_file):
                try: os.remove(self.cookie_file)
                except: pass
                
        headers={'Host':'www.watchmoviespro.us','Origin':'http://www.watchmoviespro.us','Referer':'http://www.watchmoviespro.us/search_movies','Connection':'keep-alive','Content-Type':'application/x-www-form-urlencoded'}

        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)

        form_data={ "q":"%s" % (name) }
        content = net.http_POST('http://www.watchmoviespro.us/search_movies', form_data, headers).content
        
        match=re.compile('<a href=".+?">\s*<img src=".+?" width="120" height="140" alt=".+?"/>\s*</a>\s*<br/>\s*<a href="(.+?)">.+?</a>\s*<br/>').findall(content)
        for url in match:
            url='http://www.watchmoviespro.us'+url
            print url
            self.GetFileHosts(url, list, lock, message_queue)
                    

    
