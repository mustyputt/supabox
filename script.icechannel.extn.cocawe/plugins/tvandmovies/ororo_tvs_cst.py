# -*- coding: utf-8 -*-
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common
import os

class ororo(TVShowSource,CustomSettings):
    implements = [TVShowSource,CustomSettings]
    name = "ororo"
    display_name = "Ororo"
    base_url = 'http://ororo.tv'
    source_enabled_by_default = 'false'
    cookiejar = os.path.join(common.cookies_path, 'ororo') 
    
    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="Proxy">\n'
        xml += '<setting id="prxy" type="bool" label="Proxy(For people in the USA):" default="false" />\n'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.display_name, xml)

    def GetFileHosts(self, url, list, lock, message_queue):
        from entertainment.net import Net
        import re
        net = Net(cached=False)
        net.set_cookies(self.cookiejar)
        if self.Settings().get_setting('prxy')=='true':
            net.set_proxy('http://223.27.200.4:80')
        content = net.http_GET(url).content
        find = '<source src=\'(.+?)\' type=\'video/webm\'>'
        url = search_res = re.search(find, content).group(1) + '?video=true'
        res = 'DVD'
        host = 'ORORO.TV'
        self.AddFileHost(list, res, url, host)

    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        from entertainment.net import Net
        import re
        net = Net(cached=False)
        if self.Settings().get_setting('prxy')=='true':
            net.set_proxy('http://223.27.200.4:80')
        content = net.http_GET('http://ororo.tv/en').content
        net.save_cookies(self.cookiejar)
        name = self.CleanTextForSearch(name).strip(' ')
        rep = {' ':'-', ':':'', "'":'', '/':'', '.':'', '!':'', '?':''}
        for i, j in rep.iteritems():
            name = name.replace(i, j).lower()
        url = 'http://ororo.tv/en/shows/' + name
        #<a href="#1-13" class="episode" data-href="/en/shows/the-simpsons/videos/4216"
        net.set_cookies(self.cookiejar)
        content = net.http_GET(url).content
        find = '<a href="#%s-%s" class="episode" data\-href="(.+?)"' %(season, episode)
        end_url = search_res = re.search(find, content).group(1)
        url = self.base_url + end_url
        self.GetFileHosts(url, list, lock, message_queue)
