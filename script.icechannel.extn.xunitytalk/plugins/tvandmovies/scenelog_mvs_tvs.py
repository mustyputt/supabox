'''
    Istream
    Scenelog.org
    Copyright (C) 2013 Coolwave, Jas0npc, the-one, voinage

    version 0.2

'''


from entertainment.plugnplay import Plugin
from entertainment import common

from entertainment.plugnplay.interfaces import TVShowSource
#from entertainment.plugnplay.interfaces import MovieSource

class scenelog(TVShowSource):
    implements = [TVShowSource]
	
    #unique name of the source
    name = "scenelog"
    source_enabled_by_default = 'false'
    #display name of the source
    display_name = "SceneLog"
    
    #base url of the source website
    base_url = 'http://scnlog.eu/'
    
    def GetFileHosts(self, url, list, lock, message_queue):
        import re

        from entertainment.net import Net
        net = Net()

        content = net.http_GET(url).content
        #print content.encode('utf-8')
        r = '<p><a href="(.+?)".+?rel="nofollow">(.+?)</a>' # title="(.+?)" target="_blank" rel="nofollow">(.+?)</a>
        match  = re.compile(r).findall(content)
        
        urlselect  = []

        for res, url in match:            
            
            quality = 'SD'
            res_lower = '.' + res.lower() + '.'
            for quality_key, quality_value in common.quality_dict.items():
                if re.search('[^a-zA-Z0-0]' + quality_key + '[^a-zA-Z0-0]', res_lower):
                    quality = quality_value
                    break
                
            self.AddFileHost(list, quality, url)



    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        import urllib2
        import re
        from entertainment.net import Net
        net = Net()

        search_term = name
        category = ''
        if type == 'tv_episodes':
            category = 'cat=5'
        elif type == 'movies':
            category = 'cat=4'
        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)

        #Movies = http://scenelog.org/?s=catching+fire&category=4
        #TV Shows = http://scenelog.org/?s=pawn+stars&category=5
        #http://scnlog.eu/?s=the+following+S02e08&cat=5
        #http://scnlog.eu/?s=The+Outsider+2014&cat=4

        season_pull = "0%s"%season if len(season)<2 else season
        episode_pull = "0%s"%episode if len(episode)<2 else episode

        tv_url='http://scenelog.org/?s=%s+S%s+E%s&%s' %(name.replace(' ','+'),season_pull,episode_pull,category)
        '''
        #movie_url='http://scenelog.org/?s=%s+%s&%s' %(name.replace(' ','+'),year,category)
        if type == 'movies':
            headers = ({'User-Agent': 'Magic Browser'})
            link = re.split('Start: Post', net.http_GET(movie_url).content)[0]
            url = re.findall(r'title=""/><a href="(.+?)" rel="bookmark" title=".+?">(.+?)</a></h1>', str(link), re.DOTALL)
            for url, res in url:
                self.GetFileHosts(url, list, lock, message_queue)
        '''    
        if type == 'tv_episodes':
            headers = ({'User-Agent': 'Magic Browser'})
            link = re.split('Start: Post', net.http_GET(tv_url).content)[0]
            r = re.findall('s\d+e', link, re.I)
            if r:
                url = re.findall(r'href=\"(\S+)\"\srel\=', str(link), re.I)
                for url in url:
                    self.GetFileHosts(url, list, lock, message_queue)
