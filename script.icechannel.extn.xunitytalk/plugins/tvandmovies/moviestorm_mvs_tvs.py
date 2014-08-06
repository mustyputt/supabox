'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment.xgoogle.search import GoogleSearch
from BeautifulSoup import BeautifulSoup as soup

class moviestorm(MovieSource, TVShowSource):
    implements = [MovieSource, TVShowSource]
    
    name = "MovieStorm"
    display_name = "Movie Storm"

    base_url='http://moviestorm.eu'
    
    source_enabled_by_default = 'false'
    
    def GetFileHosts(self, url, list, lock, message_queue,res):
        if 'CAM' in res:
            res='LOW'
        if 'HD' in res:
            res='HD'
        if 'DVD' in res:
            res='DVD'
        if 'BRRip' in res:
            res='HD'
        if 'R5' in res:
            res='DVD'
        if 'Unknown' in res:
            res='SD'
            
        self.AddFileHost(list, res, url)
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        import re
        from entertainment.net import Net
        
        net = Net(cached=False)
        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name) 

        
        if type == 'tv_episodes':
            search_term = '%s</h1>'%(re.sub('\A(a|A|the|THE|The)\s','',name))
            episode_get = '?season=%s&episode=%s#searialinks'%(season,episode)

            tv_url = 'http://moviestorm.eu/search?q=%s&go=Search' % name.replace(' ','+')
            
            content = net.http_GET(tv_url).content
            
            html=content.split('<div class="movie_box">')
            
            for p in html:
                if search_term in p:
                    
                    match=re.compile('<a href="(.+?)"').findall(p)
                    for url in match:
                        if 'http://moviestorm.eu/view' in url:
                            
                            new_tv_url= url+episode_get
                            
                            link = net.http_GET(new_tv_url).content

                            quality=link.split('<td class="quality_td">')
                            for p in quality:
                                res= p.split('</td>')[0]
                                ep=re.compile('<a target="_blank" href="(.+?)">WATCH</a>').findall(p)
                                for episode_link in ep:
                            
                                    self.GetFileHosts(episode_link,list, lock, message_queue,res)
                            
                
            

                

            
        elif type == 'movies':
            name = name.rstrip()
            search_term = '%s</h1>'%(re.sub('\A(a|A|the|THE|The)\s','',name))
  
            movie_url = 'http://moviestorm.eu/search?q=%s&go=Search' % name.replace(' ','+')
                        
            content = net.http_GET(movie_url).content
                      
            html=content.split('<div class="movie_box">')
            
            for p in html:
                if search_term in p:
                    
                    match=re.compile('<a href="(.+?)"').findall(p)
                    
                    for url in match:
                        
                        if 'http://moviestorm.eu/view' in url:
                            
                            link = net.http_GET(url).content
                            quality=link.split('<td class="quality_td">')
                            for p in quality:
                                res= p.split('</td>')[0]
                                movie_link=re.compile('href="(.+?)">WATCH</a>').findall(p)
                            
                                for new_movie_link in movie_link:
                                    
                                    if 'http://moviestorm.eu/exit/' in new_movie_link:
                                        link2 = net.http_GET(new_movie_link).content
                                        new_movie2=re.compile('<a class="real_link" href="(.+?)"').findall(link2)
                                        for new_movie_link in new_movie2:
                                            print new_movie_link
                                            print 'new movie link'
                                            
                                    self.GetFileHosts(new_movie_link, list, lock, message_queue,res)
                        
                
    #def Resolve(self, url):
        #import re
        #from entertainment.net import Net
        
        #net = Net(cached=False)
        #print net

        #html = net.http_GET(url).content
        #print url
        #print html
        #match = re.compile('var .+? = "(.+?)";').findall (html)
        #print match
        #return match[0]        
