'''
    http://afdah.com/    
    Copyright (C) 2013 Coolwave
'''

#from entertainment.plugnplay.interfaces import MovieIndexer
#from entertainment.plugnplay.interfaces import TVShowIndexer
from entertainment.plugnplay.interfaces import MovieSource
#from entertainment.plugnplay.interfaces import TVShowSource
#from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common
import os
from entertainment.xgoogle.search import GoogleSearch
import xbmc
import xbmcgui


class afdah(MovieSource):
    implements = [MovieSource]
    
    name = "afdah"
    display_name = "afdah"
    base_url = 'http://afdah.com/'
    #img=''
    source_enabled_by_default = 'false'
    icon = common.notify_icon
    
        
    def GetFileHosts(self, url, list, lock, message_queue):#<b>Notice:</b>(.+?)<a

        import re
        from entertainment.net import Net
        net = Net()      

        content = net.http_GET(url).content
        r = '<a rel="nofollow" href="(.+?)"'
        match  = re.compile(r).findall(content)

        r2 = '<b>Notice:</b>(.+?)<a'
        match2  = re.compile(r2).findall(content)

        for url in match:
            for res in match2:
                quality = 'SD'
                res_lower = '.' + res.lower() + '.'
                for quality_key, quality_value in common.quality_dict.items():
                    if re.search('[^a-zA-Z0-0]' + quality_key + '[^a-zA-Z0-0]', res_lower):
                        quality = quality_value
                        break 
                self.AddFileHost(list, quality, url)
        
        
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        from entertainment.net import Net
        import re
        net = Net(cached=False)
        name = self.CleanTextForSearch(name)
        import urllib
        name = name.lower()
        season_pull = "0%s"%season if len(season)<2 else season
        episode_pull = "0%s"%episode if len(episode)<2 else episode
        
        movie_url='http://afdah.com/?s=%s+%s&x=0&y=0&type=title' %(name.replace(' ','+'),'('+year+')')
        tv_url='http://afdah.com/?s=%s+S%sE%s&x=0&y=0&type=title' %(name.replace(' ','+'),season_pull,episode_pull)
        
        if type == 'movies':
            name=name.lower()
            html = net.http_GET(movie_url).content
            name_lower = common.CreateIdFromString(name)
            r = '<h3 class="entry-title"><a href="(.+?)"'
            match  = re.compile(r).findall(html)

            for item_url in match:
                print item_url
                self.GetFileHosts(item_url, list, lock, message_queue)

        '''
        elif type == 'tv_episodes':
            name=name.lower()
            html = net.http_GET(tv_url).content
            name_lower = common.CreateIdFromString(name)
            r = '<h3 class="entry-title"><a href="(.+?)"'
            match  = re.compile(r).findall(html)

            for item_url in match:
                print item_url
                self.GetFileHosts(item_url, list, lock, message_queue)
        '''

                
