'''
    Ice Channel    
'''

from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common
import re
from entertainment.xgoogle.search import GoogleSearch
import xbmc,os
datapath = xbmc.translatePath(os.path.join('special://home/userdata/addon_data','script.icechannel'))
cookie_path = os.path.join(datapath, 'cookies')

ooOOOoo = ''

do_no_cache_keywords_list = ["alert('Please Login!');"]

class TvOnline(TVShowSource,CustomSettings):
    implements = [TVShowSource,CustomSettings]
    
    name = "TvOnline"
    display_name = "TV Online"
    base_url = 'http://tvonline.cc'
    source_enabled_by_default = 'true'
    
    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="Account">\n'
        xml += '<setting id="tv_user" type="text" label="Username" default="xunity" />\n'
        xml += '<setting id="tv_pwd" type="text" option="hidden" label="Password" default="xunity" />'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.display_name, xml)

            
    
    def GetFileHosts(self, url, list, lock, message_queue,scrape): 
        
        import re
        
        from entertainment.net import Net
        
        base_url = 'http://tvonline.cc'
        net = Net(do_not_cache_if_any=do_no_cache_keywords_list)
        content = net.http_GET(url).content
        
        r='%s.+?href="(.+?)">'%scrape
        match=re.compile(r).findall(content)
        
        self.AddFileHost(list, 'HD', base_url+match[0])
            
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        name = self.CleanTextForSearch(name) 
        season = self.CleanTextForSearch(season) 
        episode = self.CleanTextForSearch(episode)
        if len(episode)< 2:
            episode = '0'+episode
            
        scrape ='S' + season+ ', Ep' + episode+':'
        search_term = name
        helper_term = 'tvshow'
        
        movie_url = self.GoogleSearchByTitleReturnFirstResultOnlyIfValid(self.base_url, search_term, helper_term, title_extrctr='(.+?) \|.+?\|.+?\|tvonline.cc', item_count=5)
        
        self.GetFileHosts(movie_url, list, lock, message_queue,scrape)

    def Resolve(self, url):
        print url
        import re        
        from entertainment.net import Net
        net = Net(cached=False, do_not_cache_if_any=do_no_cache_keywords_list)
        tv_user = self.Settings().get_setting('tv_user')
        tv_pwd = self.Settings().get_setting('tv_pwd')
        loginurl = 'http://tvonline.cc/reg.php'
        html = net.http_GET(loginurl).content
        match=re.compile('name="Token(.+?)" value="(.+?)"').findall(html)
        data     = {'subscriptionsPass': tv_pwd,
                                            'UserUsername': tv_user,
                                            'Token'+match[0][0]:'login'}
        headers  = {'Host':'tvonline.cc',
                                            'Origin':'http://tvonline.cc',
                                            'Referer':'http://tvonline.cc/login.php',
                                                    'X-Requested-With':'XMLHttpRequest'}
        html = net.http_POST(loginurl, data, headers)
        cookie_jar = os.path.join(cookie_path, "tvonline.lwp")
        if os.path.exists(cookie_path) == False:
                os.makedirs(cookie_path)
        net.save_cookies(cookie_jar)
        net.set_cookies(cookie_jar)
        html = net.http_GET(url).content

        match=re.compile('"flow-(.+?)"',re.DOTALL).findall(html)
                
        return ( match[0] if match else '' )
