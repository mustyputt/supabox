'''
    iStream
    Solar Movie - by Cocawe
    Ver 0.4.1
'''

from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.xgoogle.search import GoogleSearch

class solarmovie(MovieSource, TVShowSource, CustomSettings):
    implements = [MovieSource, TVShowSource, CustomSettings]
    
    name = "solarmovie"
    display_name = "Solar Movie"
    base_url = 'http://www.solarmovie.so/'
    source_enabled_by_default = 'false'

    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="General">\n'
        xml += '<setting id="custom_url" type="labelenum" label="URL" default="http://www.solarmovie.so/" values="Custom|http://www.solarmovie.so/|http://www.solarmovie.tl/|http://solarmovie.occupyuk.co.uk/" />\n'
        xml += '<setting id="custom_text_url" type="text" label="     Custom" default="" enable="eq(-1,0)" />\n'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.display_name, xml)
        
    def get_url(self):
        custom_url = self.Settings().get_setting('custom_url')
        if custom_url == 'Custom':
            custom_url = self.Settings().get_setting('custom_text_url')
        if not custom_url.startswith('http://'):
            custom_url = ('http://' + custom_url)
        if not custom_url.endswith('/'):
            custom_url += '/'
        return custom_url
    
    def GetFileHosts(self, url, list, lock, message_queue):
        import re
        from entertainment.net import Net
        net = Net()
        #needfix = [sockshare.com, gorrilavid.in, allmyvideos.net, filedrive  a lot more
        #ok = [sharesix.com, mightyupload.com, sharevid.org]
        #good = [vodlocker.com, vidbull.com, ishared.eu, played.to, 'movreel']
        #goodbut_needresolvers = ['cloudyvideos.com', 'filehoot.com']

        custom_url = self.get_url()
        
        content = net.http_GET(url).content
        hostlink  = re.compile('<a href="/link/show/(.+?)">\n                        (.+?)</a>').findall(content)
        quality = re.compile('<td class="qualityCell">\n                                    (.+?)                </td>').findall(content)
        qhl = zip(hostlink, quality)
        
        for (url, host), res in qhl:
            good = ['vodlocker.com', 'vidbull.com', 'ishared.eu', 'played.to', 'movreel.com']
            if host in good:
                url = custom_url + 'link/play/' + url
                if res == 'LQ DVD':
                    res = 'SD'
                self.AddFileHost(list, res, url, host=host.upper())
            
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):
        import re
        from entertainment.net import Net
        net = Net()

        custom_url = self.get_url() 

        if type == 'movies':
            search_url = custom_url + 'movie/search/' + name + ' ' + year
            content = net.http_GET(search_url).content
            search_result = re.compile('<a title=".+?"\n            href="/(.+?)">').findall(content)
            for movie_url in search_result:
                url = custom_url + movie_url
                self.GetFileHosts(url, list, lock, message_queue)

        elif type == 'tv_episodes':
            search_term = 'Watch %s Series Online for Free' %(name)
            helper_term = year
            url = self.GoogleSearchByTitleReturnFirstResultOnlyIfValid(custom_url, search_term, helper_term, title_extrctr='(.+?) \-', item_count=5)
            url = re.sub('\?page=[0-9]+', '', url) + 'season-%s/episode-%s/' %(season, episode)
            self.GetFileHosts(url, list, lock, message_queue)

    def Resolve(self, url):
        import re
        from entertainment.net import Net
        net = Net()
        content = net.http_GET(url).content
        
        final = re.compile('<iframe name="service_frame" class="service_frame" src="(.+?)"').findall(content)[0]
        return MovieSource.Resolve(self, final)
    


