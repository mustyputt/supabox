'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common


class mkspot(MovieSource):
    implements = [MovieSource]
    
    name = "MkSpot"
    display_name = "MkSpot"

    base_url='http://mkspot.org'
    
    source_enabled_by_default = 'true'
    
    def GetFileHosts(self, url, list, lock, message_queue,res):

            
        self.AddFileHost(list, res, url)
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        import re
        from entertainment.net import Net
        
        net = Net(cached=False)
        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name) 
                

        movie_url = self.base_url+'/?s='+name.replace(' ','+')+'+'+year

        
                    
        content = net.http_GET(movie_url).content
                  
        html=content.split('<div class="moviefilm">')
        
        for p in html:
            if 'alt="'+name in p:

                url=re.compile('<a href="(.+?)"').findall(p)[0]

                                        
                link = net.http_GET(url).content

                match=re.compile('proxy.link=(.+?)&.+?captions.files=(.+?),').findall(link)
                
                for movie_link ,NAME in match:
                    if 'uptobox' in movie_link:
                        if '1080' in NAME:
                            res='1080P'
                        elif '3D' in NAME:
                            res='3D'    
                        elif '720' in NAME:
                            res='720P'
                        elif 'dvd' in NAME.lower():
                            res='DVD'
                        else:
                            res='SD'  
                    else:
                        if '1080' in NAME:
                            res='HD'
                        elif '3D' in NAME:
                            res='3D'  
                        elif '720' in NAME:
                            res='HD'
                        elif 'dvd' in NAME.lower():
                            res='DVD'
                        else:
                            res='SD'
                    self.GetFileHosts(movie_link, list, lock, message_queue,res)
                    
                
