'''
    g2g.fm  # OdrtKapH2dNRpVHxhBtg 
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


class g2g(MovieIndexer,TVShowIndexer,MovieSource,TVShowSource):
    implements = [MovieIndexer,TVShowIndexer,MovieSource,TVShowSource]
    
    name = "g2g"
    display_name = "g2g.fm"
    base_url = 'http://g2g.fm/'
    #img='https://raw.githubusercontent.com/Coolwavexunitytalk/images/92bed8a40419803f31f90e2268956db50d306997/flixanity.png'
    default_indexer_enabled = 'false'
    source_enabled_by_default = 'false'
    cookie_file = os.path.join(common.cookies_path, 'g2glogin.cookie')
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
                new_url = new_url + 'index.php?&page=' + page
                print new_url
            
            from entertainment.net import Net
            import re
            net = Net(cached=False)
            import urllib
            
            html = net.http_GET(new_url).content
            #total_pages = '7'
            
            if total_pages == '':
                r= 'title="Last Page - Results .+? to .+? of (.+?)">Last'
                total_pages = re.compile(r).findall(html)[0]
                   
                
            self.AddInfo(list, indexer, 'latest', url, type, str(page), total_pages)

            for item in re.finditer(r'<span class="leftgg"> <a href="(.+?)" id=".+?"><img onerror=.+?href=".+?" id=".+?">(.+?)(\([\d]{4}\)) .+?Online Streaming</a>',html,re.I|re.DOTALL):
                url='http://g2g.fm/forum/'+item.group(1)
                url=url.split('&')[0]
                print url
                name=item.group(2)
                item_year=item.group(3).replace('(','').replace(')','')
                name = self.CleanTextForSearch(name)
                self.AddContent(list,indexer,common.mode_File_Hosts,name+' ('+item_year+')','',type, url=url, name=name, year=item_year)

        if section == 'tvshows':
            
            new_url = url
                        
            from entertainment.net import Net
            import re
            net = Net(cached=False)
            import urllib
            
            html = net.http_GET(new_url).content 
                
            for item in re.finditer(r'<!--- <a href=".+?" target="_self"> ---><a href="(.+?)" target="_self"><img class="image" src=".+?" alt="(.+?)"',html,re.I):
                url='http://g2g.fm/tvseries/'+item.group(1)
                print url
                url=url.split('&')[0]
                print url
                name=item.group(2)
                name = self.CleanTextForSearch(name)
                self.AddContent(list,indexer,common.mode_Content,name,'','tv_seasons', url=url, name=name)

        if section == 'tvshowslatest':
            
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = new_url + 'index.php?&page=' + page
                print new_url
            
            from entertainment.net import Net
            import re
            net = Net(cached=False)
            import urllib
            
            html = net.http_GET(new_url).content
            total_pages='6'
            '''
            if total_pages == '':
                r= 'title="Last Page - Results .+? to .+? of (.+?)">Last'
                total_pages = re.compile(r).findall(html)[0]
            '''           
            self.AddInfo(list, indexer, 'tvshowslatest', url, type, str(page), total_pages)   
                                        
            for item in re.finditer(r'<!--- <a href=".+?" target="_self"> ---><a href="(.+?)" target="_self"><img class="image" src=".+?" alt="(.+?) S(\d+)E(\d+)"',html,re.I):
                url='http://g2g.fm/episodes/'+item.group(1)
                url=url.split('&')[0]
                print url
                name=item.group(2)
                season=item.group(3)
                episode=item.group(4)
                name = self.CleanTextForSearch(name)
                item_id = common.CreateIdFromString(name + '_season_' + season + '_episode_' + episode)
                
                self.AddContent(list, indexer, common.mode_File_Hosts, name+' S'+season+'E'+episode, item_id, 'tv_episodes', url=url, name=name, season=season, episode=episode)
                   
        else:
            
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = new_url + 'index.php?&page=' + page
                print new_url
            
            from entertainment.net import Net
            import re
            net = Net(cached=False)
            import urllib
            
            html = net.http_GET(new_url).content
            #total_pages='7'
            '''
            if total_pages == '':
                r= 'title="Last Page - Results .+? to .+? of (.+?)">Last'
                total_pages = re.compile(r).findall(html)[0]
            '''           
            #self.AddInfo(list, indexer, 'latest2', url, type, str(page), total_pages)   
                
            for item in re.finditer(r'<!--- <a href=".+?" target="_self"> ---><a href="(.+?)" target="_self"><img class="image" src=".+?" alt="(.+?)(\([\d]{4}\))"',html,re.I):
                url='http://g2g.fm/movies/'+item.group(1)
                print url
                url=url.split('&')[0]
                print url
                name=item.group(2)
                item_year=item.group(3).replace('(','').replace(')','')
                name = self.CleanTextForSearch(name)
                #url = net.http_GET(url).get_url()
                #print url
                self.AddContent(list,indexer,common.mode_File_Hosts,name+' ('+item_year+')','',type, url=url, name=name, year=item_year)
                
    def GetContent(self, indexer, url, title, name, year, season, episode, type, list):      
        import urllib
        url = urllib.unquote_plus(url)
        title = urllib.unquote_plus(title)
        name = urllib.unquote_plus(name)
        name = (name).lower()
        
        import re
        from entertainment.net import Net
        net = Net(cached=False)
        net.set_cookies(self.cookie_file)

        content = net.http_GET(url).content
        
        if type == 'tv_seasons':
            match=re.compile('<br><br><b>(.+?)x').findall(content)
            for seasonnumber in match:                
                item_title = 'Season ' + seasonnumber
                item_id = common.CreateIdFromString(title + ' ' + item_title)
                

                self.AddContent(list, indexer, common.mode_Content, item_title, item_id, 'tv_episodes', url=url, name=name, season=seasonnumber)
               
        elif type == 'tv_episodes':
            match=re.compile("<br><b>"+season+"x(.+?)\s-\s<a style=.+?color.+?\shref='/(.+?)'>(.+?)</a>").findall(content)
            for item_v_id_2,url,item_title  in match:
                season = "0%s"%season if len(season)<2 else season
                item_v_id_2 = "0%s"%item_v_id_2 if len(item_v_id_2)<2 else item_v_id_2
                item_url = self.base_url + url
                item_v_id_2 = str(int(item_v_id_2))
                
                self.AddContent(list, indexer, common.mode_File_Hosts, item_title, item_id, type, url=item_url, name=name, season=season, episode=item_v_id_2)
                    
       
    
    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''):
        
        from entertainment.net import Net
        import re
        
        net = Net()

        url_type = ''
        content_type = ''
        
        if indexer == common.indxr_Movies:#'[COLOR orange]'+year+'[/COLOR]'

            if section == 'main':
                self.AddSection(list, indexer,'latest','Latest Movies','http://g2g.fm/forum/forumdisplay.php?4-Movies&sort=lastpost&order=desc',indexer)
                self.AddSection(list, indexer,'latest','Number of Views','http://g2g.fm/forum/forumdisplay.php?4-Movies&s=&pp=25&daysprune=-1&sort=views&order=desc',indexer)
                self.AddSection(list, indexer,'latest','Thread Rating','http://g2g.fm/forum/forumdisplay.php?4-Movies&s=&pp=25&daysprune=-1&sort=voteavg&order=desc',indexer)
                self.AddSection(list, indexer,'latest','ABC','http://g2g.fm/forum/forumdisplay.php?4-Movies&sort=title&order=asc',indexer)
                self.AddSection(list, indexer,'genre','Genere','http://g2g.fm/movies/genre.php?showC=27',indexer)         
                           
            elif section == 'genre':
                r = re.findall(r'<!--- <a href=".+?" target="_self"> ---><a href="(.+?)" target="_self"><img class="image" src="http://g2g.fm/uploads/thumbnails/(.+?)-G2G.FM.jpg"', net.http_GET(url).content, re.I)
                for url,genres in r[0:]:
                    genres_title = genres.upper()
                    url='http://g2g.fm/movies/'+url
                    url=url.split('&')[0]
                    self.AddSection(list, indexer, 'genres_title', genres_title, url, indexer)              

            else:
                self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)

        elif indexer == common.indxr_TV_Shows:
            
            if section == 'main':
                self.AddSection(list, indexer,'tvshows','TV Shows (Coming soon)','http://g2g.fm/tvseries/',indexer)
                self.AddSection(list, indexer,'tvshowslatest','Latest Episodes','http://g2g.fm/episodes/',indexer)

            else:
                self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)

            
    
    def GetFileHosts(self, url, list, lock, message_queue):

        import re
        from entertainment.net import Net
        net = Net()

        #'Resolution: <font color=".+?">.+?x(.+?)</font><br />'
        content = net.http_GET(url).content
        
        match=re.compile('Resolution: <font color=".+?">.+?x(.+?)</font><br />').findall(content)
        urlselect  = []

        for res in match:
            if url not in urlselect:
                urlselect.append(url)

                quality = 'HD'
                if '720' in res:
                    quality = '720P'
                elif '1080' in res:
                    quality = '1080P'
                  
                self.AddFileHost(list, quality, url)       
        
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        from entertainment.net import Net
        import re
        #net = Net(cached=False)
        name = self.CleanTextForSearch(name)
        import urllib
        name = name.lower()
        
               
        if type == 'movies':
            
            net = Net()
            
            if os.path.exists(self.cookie_file):
                    try: os.remove(self.cookie_file)
                    except: pass
                    
            headers={'Host':'g2g.fm','Origin':'http://g2g.fm','Referer':'http://g2g.fm/forum/search.php','Connection':'keep-alive','Content-Type':'application/x-www-form-urlencoded','User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}

            title = self.CleanTextForSearch(title) 
            name = self.CleanTextForSearch(name)

            form_data={ 'query':name+' '+year,'titleonly':'1','dosearch':'Search','s':'','securitytoken':'guest','do':'process','searchthreadid':'' }
            content = net.http_POST('http://g2g.fm/forum/search.php', form_data, headers).content
            
            item_url=re.compile('<span class="leftgg"> <a href="(.+?)"').findall(content)[0]
            item_url= 'http://g2g.fm/forum/'+item_url
            
            self.GetFileHosts(item_url, list, lock, message_queue)

        elif type == 'tv_episodes':
            season_pull = "0%s"%season if len(season)<2 else season
            episode_pull = "0%s"%episode if len(episode)<2 else episode
            net = Net()
            
            if os.path.exists(self.cookie_file):
                    try: os.remove(self.cookie_file)
                    except: pass
                    
            headers={'Host':'g2g.fm','Origin':'http://g2g.fm','Referer':'http://g2g.fm/forum/search.php','Connection':'keep-alive','Content-Type':'application/x-www-form-urlencoded','User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}

            title = self.CleanTextForSearch(title) 
            name = self.CleanTextForSearch(name)

            form_data={ 'query':name+' S'+season_pull+'E'+episode_pull,'titleonly':'1','dosearch':'Search','s':'','securitytoken':'guest','do':'process','searchthreadid':'' }
            content = net.http_POST('http://g2g.fm/forum/search.php', form_data, headers).content
            item_url=re.compile('<span class="leftgg"> <a href="(.+?)"').findall(content)[0]
            item_url= 'http://g2g.fm/forum/'+item_url
            name_fix = name.title()
            name_fix = name_fix.replace(' ','-')
            
            if name_fix in item_url:
                self.GetFileHosts(item_url, list, lock, message_queue)
                        
            

    def Resolve(self, url):
        
        from entertainment.net import Net
        import re
        net = Net(cached=False)
        html = net.http_GET(url).content
        
        item_url=re.compile('<iframe src="(.+?)"').findall(html)[0]
        headers={'Host':'g2g.fm', 'Referer': url , 'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
        data=item_url.split('=')[1]
        form_data={ 'g2gmov': data }
                
        content = net.http_POST(item_url,form_data,headers).content
        
        new_url = re.compile('<iframe src="(.+?)"').findall(content)[0]
        
        headers.update({'Referer':item_url, 'Accept':'*/*', 'Accept-Encoding':'identity;q=1, *;q=0', 'Range':'bytes=0-'})
        content = net.http_GET(new_url,headers).content
        host_url = re.compile('<iframe src="(.+?)"').findall(content)[0] 
        
        headers={'Referer':str(host_url), 'Host':'docs.google.com','User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:27.0) Gecko/20100101 Firefox/27.0','Connection':'keep-alive','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.5','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
            
        html = net.http_GET(host_url, headers=headers).content.encode("utf-8").rstrip()
        video_url = re.compile('fmt_stream_map".+?(http.+?),').findall(html)[0]
        video_url=video_url.replace('|', '').replace('\u003d','=').replace('\u0026','&')
        
        return video_url
        
            
        
