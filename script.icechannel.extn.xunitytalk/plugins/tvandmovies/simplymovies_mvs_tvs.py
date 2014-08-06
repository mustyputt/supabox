'''
    Ice Channel
    simplymovies.net
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment.xgoogle.search import GoogleSearch

class SimplyMovies(MovieSource, TVShowSource):
    implements = [MovieSource, TVShowSource]
    
    name = "SimplyMovies"
    display_name = "Simply Movies"
    base_url = 'http://simplymovies.net/'
    
    source_enabled_by_default = 'true'
    
    def GetFileHosts(self, url, list, lock, message_queue): 
        
        import re
        from entertainment.net import Net
        net = Net(cached=False)
        
        quality_dict = {'1080':'HD', '720':'HD', '540':'SD', '480':'SD', '360':'LOW', '240':'LOW'}
        
        content = net.http_GET(url).content
        r = '<iframe class="videoPlayerIframe" src="(.+?)"></iframe>'
        match  = re.compile(r).findall(content)
        
        content = net.http_GET(match[0]).content
        r ='url(.+?)=(.+?)&amp'
        match  = re.compile(r).findall(content)
        
        urlselect  = []

        for res, url in match:            
            if url not in urlselect:
                urlselect.append(url)
                
                self.AddFileHost(list, quality_dict.get(res, 'NA'), url, host='SIMPLYMOVIES.NET')
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name) 
        
        search_term = name
        helper_term = ''
        ttl_extrctr = ''
        
        if type == 'tv_episodes':
            php = 'tv_shows.php'
        elif type == 'movies':
            search_term = search_term + '+' + year
            php = 'index.php'
        
        if type == 'movies':
            import re
            from entertainment.net import Net
            net = Net()
            movie_url = 'http://simplymovies.net/%s?searchTerm=%s' %(php,search_term.replace(' ','+'))
            
            content = net.http_GET(movie_url).content.encode("utf-8")
            
            link=content.split('<div class="movieInfoHolder"')
            if_p ='>%s</h3>' % name
            for p in link:
                if if_p in p:
                    if year in p:
	                    match=re.compile('<a href="movie.php\?id=(.+?)">').findall (p)[0]
	                    self.GetFileHosts('http://simplymovies.net/movie.php?id=%s'%match, list, lock, message_queue)
            
            
        elif type == 'tv_episodes':
            movie_url = self.GoogleSearchByTitleReturnFirstResultOnlyIfValid(self.base_url, search_term, helper_term, title_extrctr=['(.+?) \- simply movies', 'simply movies \- watch (.+?) online for free'])
            if movie_url != '':
                import re
                from entertainment.net import Net
                net = Net()
                
                content = net.http_GET(movie_url).content
                
                season_content = re.search('<h3>Season ' + season + '(.*)', content)
                if season_content:
                    season_content = season_content.group(1)
                    
                    episode_re = 'Episode ' + str(int(episode)  - 1) + '.+?<a href="(.+?)">'
                    if episode == '1':
                        episode_re = '<a href="(.+?)">Episode ' + episode
                    
                    episode_content = re.search(episode_re, season_content)
                    if episode_content:
                        episode_url = self.base_url + episode_content.group(1)
                        self.GetFileHosts(episode_url, list, lock, message_queue)
                        
                
            
    def Resolve(self, url):
        '''
        from entertainment import odict
        resolved_media_url = odict.odict()
        
        import re
        from entertainment.net import Net
        net = Net()
        
        content = net.http_GET(url).content
        r = '<iframe class="videoPlayerIframe" src="(.+?)"></iframe>'
        match  = re.compile(r).findall(content)
        
        content = net.http_GET(match[0]).content
        r ='url(.+?)=(.+?)&amp'
        match  = re.compile(r).findall(content)
        
        urlselect  = []

        for res, url in match:            
            if url not in urlselect:
                urlselect.append(url)
                resolved_media_url[res] = url
        '''        
        return url
            
                
