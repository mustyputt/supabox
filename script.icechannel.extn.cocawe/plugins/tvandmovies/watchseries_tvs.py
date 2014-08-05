'''
    iStream
    Watchseries.lt - by Cocawe
    Ver 0.0.1
'''

from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment.plugnplay.interfaces import TVShowSource

class watchseries(TVShowSource):
    implements = [TVShowSource]
    
    name = "watchseries"
    display_name = "Watchseries.lt"
    base_url = 'http://watchseries.lt/open/cale/'
    source_enabled_by_default = 'false'
    
    def GetFileHosts(self, url, list, lock, message_queue):
        
        import re
        from entertainment.net import Net
        net = Net()  
        content = net.http_GET(url).content
        r = '<span>(.+?)<\/span>.+?href="\/open\/cale\/(.+?)"'
        hostlink = re.compile(r).findall(content)
        for host, url in hostlink:
            url = self.base_url + url
            self.AddFileHost(list, 'SD', url, host=host.upper())
            
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):
        
        #http://watchseries.lt/episode/the_simpsons_s1_e1.html
        #http://watchseries.lt/episode/%s_s%s_e%s.html
        name = self.CleanTextForSearch(name)
        #Ill fix the overuse of replace later. I was lazy and it was an easy fix
        name = name.replace(' ','_').replace(':','').replace("'",'').replace('.','').lower()
        url = 'http://watchseries.lt/episode/%s_s%s_e%s.html' %(name,season,episode)
        self.GetFileHosts(url, list, lock, message_queue)

    def Resolve(self, url):

        import re
        from entertainment.net import Net
        net = Net()
        content = net.http_GET(url).content
        #<a class="myButton" href="http://www.movshare.net/video/5fd7f43d79e12">Click Here to Play</a>
        r = '<a class="myButton" href="(.+?)">Click Here to Play</a>'
        final = re.compile(r).findall(content)[0]
        return TVShowSource.Resolve(self, final)
    


