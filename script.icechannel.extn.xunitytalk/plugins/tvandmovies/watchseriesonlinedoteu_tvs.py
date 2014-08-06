'''
    IStream
    Watchseries-online.eu
'''
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin

class Watchseriesonlinedoteu(TVShowSource):
    implements = [TVShowSource]
    name = "WatchSeries-Online.EU"
    display_name = "WatchSeries-Online.EU"
    base_url = 'http://watchserieshd.eu'
    source_enabled_by_default = 'true'
    
    def GetFileHosts(self, url, list, lock, message_queue):
        from entertainment.net import Net
        import re        
        
        net = Net()
        sources=[]
        links=re.compile('<a target="_blank" id="hovered" href="(http.+?)">(.+?)[ <]').findall(net.http_GET(url).content)
        for url, name in links:
             if 'http' in url:
                 self.AddFileHost(list,'SD',url,host=name.upper())

    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):
        from entertainment.net import Net
        import re        
        
        net = Net()
        sources=[]
        seasonshit = '0%s'%season if len(season)<2 else season
        episodeshit = '0%s'%episode if len(episode)<2 else episode
        valid_constructor='S%sE%s'%(seasonshit,episodeshit)
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)#http://watchserieshd.eu/?s=black+box+S01E06&search=
        search_url_title = "%s/?s=%s+%s"%(self.base_url,name.replace(' ','+').lower(),title.replace(' ','+').lower())
        search_url_digit = "%s/?s=%s+%s"%(self.base_url,name.replace(' ','+').lower(),valid_constructor.lower())
                
        try:
            link=re.compile('<span class="PostHeader"><a href="(.+?)" rel="bookmark" title="Permanent').findall(net.http_GET(search_url_digit).content)[0]
            if name.replace(' ','-').lower() and valid_constructor.lower() in link:
                sources.append(link)
        except: pass
        try:
            link2=re.compile('<span class="PostHeader"><a href="(.+?)" rel="bookmark" title="Permanent').findall(net.http_GET(search_url_title).content)[0]
            if title.replace(' ','-').lower() in link2:
                sources.append(link2)
        except:pass
        for url in sources:
            self.GetFileHosts(url, list, lock, message_queue)

    def Resolve(self, url):
        import re
        from entertainment.net import Net
        net = Net()

        url = net.http_GET(url).get_url()
        from entertainment import istream
        play_url = istream.ResolveUrl(url)
        return play_url





