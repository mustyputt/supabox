'''
    Ice Channel
    MoviesHD
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment.xgoogle.search import GoogleSearch

class MoviesHD(MovieSource):
    implements = [MovieSource]
    
    name = "MoviesHD"
    display_name = "Movies HD"
    
    
    source_enabled_by_default = 'true'
    
    def GetFileHosts(self, url, list, lock, message_queue): 
        self.AddFileHost(list, 'HD', url)
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):  
    
        from entertainment.net import Net
        
        net = Net()        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name) 
        
        search_term = name.replace(' ','+')
        
        import re
        url='http://movieshd.co/?s='+search_term
        link=net.http_GET(url).content
        if 'Sorry, but nothing matched your search criteria' in link:
            return None
        match = re.compile('<ul class="listing-videos listing-tube">.+?<a href="(.+?)" title="(.+?)"><span>.+?</span></a>',re.DOTALL).findall(link)
        
        for movie_url , title  in match:
            if year in title: 
                self.GetFileHosts(movie_url, list, lock, message_queue)
                
            
    def Resolve(self, url):
        
        import re        
        from entertainment.net import Net
        import urllib 
        net = Net()
        
        link = net.http_GET(url).content  
        
        match = re.compile("'text/rocketscript'>ref='(.+?)';width.*iframe").findall(link)
        if (len(match) == 1):
                videomega_url = "http://videomega.tv/iframe.php?ref=" + match[0] 
        if (len(match) < 1):
                match=re.compile("frameborder='.+?' src='(.+?)&").findall(link)
                videomega_url = match[0]

        link = net.http_GET(videomega_url).content
        match=re.compile("document.write.unescape.\"(.+?)\"").findall(link)
        if (len(match) < 1):
            return
        encoded=match[0]
        link = urllib.unquote(encoded)
        match=re.compile("file: \"(.+?)\",flash").findall(link)
        if (len(match) < 1):
            return
        print match
        stream_url = match[0]
        print stream_url
            
        return stream_url
        
