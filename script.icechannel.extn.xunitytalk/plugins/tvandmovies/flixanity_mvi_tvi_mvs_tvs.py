'''
    Flixanity    
    Copyright (C) 2013 Coolwave
'''

from entertainment.plugnplay.interfaces import MovieIndexer
from entertainment.plugnplay.interfaces import TVShowIndexer
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
#from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common
import os
from entertainment.xgoogle.search import GoogleSearch
import xbmc
import xbmcgui


class flixanity(MovieIndexer,TVShowIndexer,MovieSource,TVShowSource):
    implements = [MovieIndexer,TVShowIndexer,MovieSource,TVShowSource]
    
    name = "flixanity"
    display_name = "Fli[COLOR yellow]X[/COLOR]anity"
    base_url = 'http://www.flixanity.com/'
    img='https://raw.githubusercontent.com/Coolwavexunitytalk/images/92bed8a40419803f31f90e2268956db50d306997/flixanity.png'
    default_indexer_enabled = 'false'
    source_enabled_by_default = 'false'
    #cookie_file = os.path.join(common.cookies_path, 'NRlogin.cookie')
    icon = common.notify_icon
    
    '''
    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="Account">\n'
        xml += '<setting id="tv_user" type="text" label="Email" default="Enter your noobroom email" />\n'
        xml += '<setting id="tv_pwd" type="text" option="hidden" label="Password" default="xunity" />'
        xml += '<setting label="Premium account will allow for 1080 movies and the TV Shows section" type="lsep" />\n'
        xml += '<setting id="premium" type="bool" label="Enable Premium account" default="false" />\n'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.display_name, xml)
    '''

    def ExtractContentAndAddtoList(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 
        if section == 'latest':
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = new_url + page
            
            from entertainment.net import Net
            import re
            net = Net(cached=False)
            import urllib
            
            html = net.http_GET(new_url).content
            if total_pages == '':
                r= '<li><a href="javascript.+?">...</a></li>  <li><a href=".+?">.+?</a></li>\s*<li><a href=".+?">(.+?)</a></li>'
                total_pages = re.compile(r).findall(html)[0]
                
            self.AddInfo(list, indexer, 'latest', url, type, str(page), total_pages)

            for item in re.finditer(r'<img class="img-preview spec-border"  src=(.+?)\&.+?" alt=" " style=".+?"/>.+?<p><strong>(.+?)</strong></p>\s*<p>(.+?)</p>.+?class="left" /> <a href="(.+?)" class="left">Watch this</a></li>',html,re.I|re.DOTALL):
                image=item.group(1)
                image=image.replace('http://www.flixanity.com/templates/trakt/timthumb.php?src=','')
                name=item.group(2)
                plot=item.group(3)
                url=item.group(4)
                name = self.CleanTextForSearch(name)
                self.AddContent(list,indexer,common.mode_File_Hosts,name,'',type, url=url, name=name, img=image, plot=plot)
                

        elif section == 'box':
            
            from entertainment.net import Net
            import re
            net = Net(cached=False)
            import urllib
            
            html = net.http_GET(url).content

            for item in re.finditer(r'<img class="img-preview spec-border"  src="(.+?)\&.+?" alt=" " />.+?<p><strong>(.+?)</strong></p>\s*<p>(.+?)</p>.+?<a href="(.+?)" class="left">Watch this</a></li>',html,re.I|re.DOTALL):
                image=item.group(1)
                image=image.replace('http://www.flixanity.com/templates/trakt/timthumb.php?src=','')
                name=item.group(2)
                plot=item.group(3)
                url=item.group(4)
                name = self.CleanTextForSearch(name)
                self.AddContent(list,indexer,common.mode_File_Hosts,name,'',type, url=url, name=name, img=image, plot=plot)

        elif section == 'tvshows2':
            
            from entertainment.net import Net
            import re
            net = Net(cached=False)
            import urllib
            
            html = net.http_GET(url).content

            for item in re.finditer(r'<a href="(.+?)" class="item" title="">\s*<img class="img-preview spec-border show-thumbnail" src="(.+?)\&.+?" alt=" "/>\s*</a>\s*<div class="rating-pod">\s*<p><strong>(.+?)</strong></p>\s*<p>(.+?)</p>\s*<div class="right">',html,re.I):
                image=item.group(2)
                image=image.replace('http://www.flixanity.com/templates/trakt/timthumb.php?src=','')
                print image
                name=item.group(3)
                plot=item.group(4)
                url=item.group(1)
                name = self.CleanTextForSearch(name)
                self.AddContent(list, indexer, common.mode_Content, name, '', 'tv_seasons', url=url, name=name, img=image, plot=plot)

        elif section == 'tvshows':
            
            new_url = url
            
            from entertainment.net import Net
            import re
            net = Net(cached=False)
            import urllib
            
            html = net.http_GET(new_url).content

            match=re.compile('<a href="(.+?)" class="item" title="">\s*<img class="img-preview spec-border"  src="(.+?)\&.+?" alt=" " />\s*</a>\s*<div class="rating-pod">\s*<div class="left">\s*<p><strong>(.+?)</strong></p>\s*<p>(.+?)</p>\s*</div>',re.I).findall(html)

            ''' Pagination Code Start '''
            num_items_on_a_page = 25
            if page == '':                
                page = '1'
                total_items = len(match)
                total_pages = str ( ( total_items / num_items_on_a_page ) + ( 1 if total_items % num_items_on_a_page >= 1 else 0) )
                
            self.AddInfo(list, indexer, section, url, type, page, total_pages, sort_by, sort_order)
            
            start_index = ( int(page) - 1 ) * num_items_on_a_page
            match = match[ start_index : start_index + num_items_on_a_page  ]
            ''' Pagination Code End '''

            for url,image,name,plot in match:
                image=image.replace('http://www.flixanity.com/templates/trakt/timthumb.php?src=','')
                name = self.CleanTextForSearch(name)
                self.AddContent(list, indexer, common.mode_Content, name, '', 'tv_seasons', url=url, name=name, img=image, plot=plot)
                

        
        else:
            
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = new_url + page
            
            from entertainment.net import Net
            import re
            net = Net(cached=False)
            import urllib
            
            html = net.http_GET(new_url).content
            if total_pages == '':
                r= '<li><a href="javascript.+?">...</a></li>  <li><a href=".+?">.+?</a></li>\s*<li><a href=".+?">(.+?)</a></li>'
                total_pages = re.compile(r).findall(html)[0]
                
            self.AddInfo(list, indexer, 'latest', url, type, str(page), total_pages)

            for item in re.finditer(r'<img class="img-preview spec-border"  src=(.+?)\&.+?" alt=" " style=".+?"/>.+?<p><strong>(.+?)</strong></p>\s*<p>(.+?)</p>.+?class="left" /> <a href="(.+?)" class="left">Watch this</a></li>',html,re.I|re.DOTALL):
                image=item.group(1)
                image=image.replace('http://www.flixanity.com/templates/trakt/timthumb.php?src=','')
                name=item.group(2)
                plot=item.group(3)
                url=item.group(4)
                name = self.CleanTextForSearch(name)
                self.AddContent(list,indexer,common.mode_File_Hosts,name,'',type, url=url, name=name, img=image, plot=plot)           

                    
       
    def GetContent(self, indexer, url, title, name, year, season, episode, type, list):      
        import urllib
        url = urllib.unquote_plus(url)
        title = urllib.unquote_plus(title)
        name = urllib.unquote_plus(name)
        name = (name).lower()
        
        import re
        from entertainment.net import Net
        net = Net(cached=False)
        
        content = net.http_GET(url).content
        
        if type == 'tv_seasons':
            match=re.compile("href='http://www.flixanity.com/show/.+?'>Season (.+?)</a></li>").findall(content)
            for seasonnumber in match:                
                item_title = 'Season ' + seasonnumber
                item_id = common.CreateIdFromString(title + ' ' + item_title)
                

                self.AddContent(list, indexer, common.mode_Content, item_title, item_id, 'tv_episodes', url=url, name=name, season=seasonnumber)
               
        elif type == 'tv_episodes':#<a class="link" href="(.+?)" title="Season '+season+', Episode (.+?) - (.+?)">
            match=re.compile('<a class="link" href="(.+?)" title="Season '+season+', Episode (.+?) - (.+?)">').findall(content)
            for url,item_v_id_2,item_title  in match:
                season = "0%s"%season if len(season)<2 else season
                item_v_id_2 = "0%s"%item_v_id_2 if len(item_v_id_2)<2 else item_v_id_2
                item_url = url
                item_v_id_2 = str(int(item_v_id_2))
                item_id = common.CreateIdFromString(name + '_season_' + season + '_episode_' + item_v_id_2)
                self.AddContent(list, indexer, common.mode_File_Hosts, item_title, item_id, type, url=item_url, name=name, season=season, episode=item_v_id_2)
            

        
    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''):
        
        from entertainment.net import Net
        import re
        
        net = Net()

        url_type = ''
        content_type = ''
        
        if indexer == common.indxr_Movies:#'[COLOR orange]'+year+'[/COLOR]'

            if section == 'main':
                self.AddSection(list, indexer,'latest','[COLOR red]Ordered[/COLOR] [COLOR white]by Latest[/COLOR]',self.base_url +'movies/date/',indexer)
                self.AddSection(list, indexer,'box','[COLOR red]Ordered[/COLOR] [COLOR white]by Featured Movies[/COLOR]',self.base_url +'featuredmovies',indexer)
                self.AddSection(list, indexer,'azlist','[COLOR red]Ordered[/COLOR] [COLOR white]by ABC[/COLOR]',self.base_url +'movies/abc/',indexer)
                self.AddSection(list, indexer,'rating','[COLOR red]Ordered[/COLOR] [COLOR white]by IMDb Rating[/COLOR]',self.base_url +'movies/imdb_rating/',indexer)
                self.AddSection(list, indexer,'genre','[COLOR red]Ordered[/COLOR] [COLOR white]by Genre[/COLOR]',self.base_url,indexer)
                self.AddSection(list, indexer,'popular','[COLOR red]Ordered[/COLOR] [COLOR white]by Popular[/COLOR]',self.base_url +'movies/favorites/',indexer)         
                           
            elif section == 'genre':
                r = re.findall(r'<li><a href="http://www.flixanity.com/movie-tags/(.+?)">.+?</a></li>', net.http_GET(url).content, re.I)
                for genres in r[0:]:
                    genres_title = genres.replace('-',' ')
                    genres_title = genres_title.replace('and','&')
                    genres_title = genres_title.upper()
                    self.AddSection(list, indexer, 'genres_title', genres_title, 'http://www.flixanity.com/movie-tags/'+genres+'/date/', indexer)
                
                

            else:
                self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)

        elif indexer == common.indxr_TV_Shows:
            if section == 'main':
                self.AddSection(list, indexer,'tvshows','[COLOR red]Ordered[/COLOR] [COLOR white]by Latest[/COLOR]',self.base_url +'tv-shows/date/',indexer)
                self.AddSection(list, indexer,'tvshows','[COLOR red]Ordered[/COLOR] [COLOR white]by ABC[/COLOR]',self.base_url +'tv-shows/abc',indexer)
                self.AddSection(list, indexer,'tvshows','[COLOR red]Ordered[/COLOR] [COLOR white]by IMDb Rating[/COLOR]',self.base_url +'tv-shows/imdb_rating',indexer)
                self.AddSection(list, indexer,'genre','[COLOR red]Ordered[/COLOR] [COLOR white]by Genre[/COLOR]',self.base_url,indexer)
                self.AddSection(list, indexer,'livetv','[COLOR red]Live[/COLOR] [COLOR white]TV - Coming Soon[/COLOR]',self.base_url + 'pages/live-tv',indexer)

            elif section == 'genre':
                r = re.findall(r'<li><a href="http://www.flixanity.com/tv-tags/(.+?)">.+?</a></li>', net.http_GET(url).content, re.I)
                for genres in r[0:]:
                    genres_title = genres.replace('-',' ')
                    genres_title = genres_title.replace('and','&')
                    genres_title = genres_title.upper()
                    self.AddSection(list, indexer, 'tvshows2', genres_title, 'http://www.flixanity.com/tv-tags/'+genres+'/date/', indexer)

            elif section == 'Live Tv':
                self.AddSection(list, indexer,'live_tv','[COLOR white]Coming Soon!!!![/COLOR]',self.base_url +'pages/live-tv',indexer)


            else:
                self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)
            
    
    def GetFileHosts(self, url, list, lock, message_queue):

        import re
        from entertainment.net import Net
        net = Net()
        print url
     
        content = net.http_GET(url).content
        r = 'embeds.+?<iframe.+?src.+?"(http://.+?)"'
        match  = re.compile(r,re.I).findall(content)

        for url in match:
            quality = 'SD'
            try:
                r4 = '<span>Picture Quality:</span>\s*<img src=".+?" style=".+?" class="(.+?)" />'
                match3  = re.compile(r4).findall(content)
                    
                for res in match3:
                    
                    res_lower = '.' + res.lower() + '.'
                    for quality_key, quality_value in common.quality_dict.items():
                        if re.search('[^a-zA-Z0-0]' + quality_key + '[^a-zA-Z0-0]', res_lower):
                            quality = quality_value
                        
            except:
                continue
            
            url = common.CleanText(url, True, True)
            url = url.replace('http://www.flixanity.com/jwplayer/gkplugins/player.php?','')
                  
            self.AddFileHost(list, quality, url)
        
        
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        from entertainment.net import Net
        import re
        net = Net(cached=False)
        name = self.CleanTextForSearch(name)
        import urllib
        name = name.lower()
        
        main_url='http://www.flixanity.com/index.php?menu=search&query=%s' %(name.replace(' ','+'))
        
        if type == 'movies':
            name=name.lower()
            print name
            name=name.replace(':','').replace('&','').replace('.','').replace('mr peabody   sherman','mr peabody sherman').replace('\'','').replace(',','')
            item_url = 'http://www.flixanity.com/movie/%s' %(name.replace(' ','-'))
            print item_url
            self.GetFileHosts(item_url, list, lock, message_queue)

            '''
            html = net.http_GET(main_url).content
            name_lower = common.CreateIdFromString(name)
            r = '<div class="item" style="text-align:center">\s*<a href="(.+?)"'
            match  = re.compile(r,re.DOTALL).findall(html)

            for item_url in match:
                self.GetFileHosts(item_url, list, lock, message_queue)
            '''


        elif type == 'tv_episodes':
            name=name.lower()
            item_url = 'http://www.flixanity.com/show/%s/season/%s/episode/%s' %(name.replace(' ','-'),season,episode)
            
            self.GetFileHosts(item_url, list, lock, message_queue)
         

    
