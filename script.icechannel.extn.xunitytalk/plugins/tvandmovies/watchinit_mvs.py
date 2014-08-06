'''
    Ice Channel    
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment.xgoogle.search import GoogleSearch
ooOOOoo = ''


class WatchinIt(MovieSource):
    implements = [MovieSource]
    
    name = "WatchinIt"
    display_name = "Watch-In-It"
    def ttTTtt(i, t1, t2=[]):
     t = ooOOOoo
     for c in t1:
      t += chr(c)
      i += 1
      if i > 1:
       t = t[:-1]
       i = 0  
     for c in t2:
      t += chr(c)
      i += 1
      if i > 1:
       t = t[:-1]
       i = 0
     return t
    
    base_url=ttTTtt(0,[104,60,116,5,116,162,112,254,58,34,47,77,47,186,119],[86,97,215,116,154,99,75,104,45,105,65,110,4,45,7,105,110,116,212,46,192,110,234,117,175,47])
    
    def GetFileHosts(self, url, list, lock, message_queue): 
        
        import re
        
        from entertainment.net import Net
        
        net = Net()
        
        content = net.http_GET(url).content
        
        match=re.compile('<a class="image.+?" href="(.+?)" target=".+?"><img src=".+?" title=".+?" /><br />(.+?)</a>',re.DOTALL).findall(content)
        
        for host_url, name in match:
            
            self.AddFileHost(list, 'SD', host_url)
            
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name) 
        
        search_term = name + ' ' + year
        helper_term = 'movies'
        
        movie_url = self.GoogleSearchByTitleReturnFirstResultOnlyIfValid(self.base_url, search_term, helper_term, title_extrctr='(.+?) \(')
        
        self.GetFileHosts(movie_url, list, lock, message_queue)
