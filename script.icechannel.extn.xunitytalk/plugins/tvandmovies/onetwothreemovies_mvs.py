'''
    Ice Channel
    123 Movies.me
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common


class onetwothreemovies(MovieSource):
    implements = [MovieSource]
    
    name = "123Movies"
    display_name = "123Movies"
    base_url = 'http://www.123movies.me'
    
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
        url='http://www.123movies.me/search/'+search_term
        link=net.http_GET(url).content.replace('\n','')
        
        match = re.compile('<a href="/movies/(.+?)">').findall(link)
        
        for movie_url  in match:
            self.GetFileHosts('http://www.123movies.me/movies/'+movie_url, list, lock, message_queue)
                
            
    def Resolve(self, url):
        
        import re        
        from entertainment.net import Net
        net = Net(user_agent='Apple-iPhone/')
        
        content = net.http_GET(url).content
       
        link=content.split('href=')
        for p in link:
            if '.mp4' in p:
                resolved_media_url = re.compile('"(.+?)"').findall(p)[0]
                
        return resolved_media_url
            
                
                
