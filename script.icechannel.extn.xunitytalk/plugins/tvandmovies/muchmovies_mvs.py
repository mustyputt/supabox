'''
    Ice Channel
    muchmovies.org
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment.xgoogle.search import GoogleSearch

class MuchMovies(MovieSource):
    implements = [MovieSource]
    
    name = "MuchMovies"
    display_name = "Much Movies"
    base_url = 'http://www.muchmovies.org'
    
    source_enabled_by_default = 'true'
    
    def GetFileHosts(self, url, list, lock, message_queue): 
        self.AddFileHost(list, 'HD', url)
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):  
    
        from entertainment.net import Net
        
        net = Net(user_agent='Apple-iPhone/')        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name) 
        
        search_term = name.replace(' ','-')+'-'+year
        
        import re
        url='http://www.muchmovies.org/search/'+search_term
        link=net.http_GET(url).content.replace('\n','')
        match = re.compile('<div class=".+?"><a href="(.+?)">').findall(link)
        
        for movie_url  in match:
            self.GetFileHosts('http://www.muchmovies.org'+movie_url, list, lock, message_queue)
                
            
    def Resolve(self, url):
        
        import re        
        from entertainment.net import Net
        net = Net(user_agent='Apple-iPhone/')
        
        content = net.http_GET(url).content
        content = content.replace('\n','')
        
        link=content.split('href=')
        for p in link:
            if '.mp4' in p:
                resolved_media_url = re.compile('"(.+?)"').findall(p)[0]
                
        return resolved_media_url
            
                
                
