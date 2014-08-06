'''
    Ice Channel
    fanstash.eu
'''

from entertainment.plugnplay.interfaces import TVShowSource


class FanStash(TVShowSource):
    implements = [TVShowSource]
    
    name = "Fan-Stash"
    display_name = "Fan Stash"
    base_url = 'http://www.fanstash.eu'
    source_enabled_by_default = 'false'

    
    def GetFileHosts(self, url, list, lock, message_queue):
        from entertainment.net import Net
        import urllib
        import re
        net = Net()

        sources=[]
        html = net.http_GET(url,headers={'User-Agent':'Magic-Browser'}).content
        link=re.compile('<a target="_blank" href="(.+?)" class="play_link">').findall(html)
        page=re.compile('<td class="current_pagination">.+?</td><td><a href=javascript:Links.+?link_search.+?;>(.+?)</a></td>').findall(html)
        epid=re.compile(r'Episode.+?-(.+?).html').findall(url)
        for url in link:
            bits=re.compile("unescape.+?'(.+?)'").findall(net.http_GET('http://www.fanstash.eu%s'%url).content)
            sources.append(urllib.unquote(bits[0]))
        if page:
            html = net.http_GET('http://www.fanstash.eu/ajax.php?action=watch_links&epid=%s&cp=%s&mode=ajax&s=&sselect=undefined'%(epid[0],page[0])).content
            link=re.compile('<a target="_blank" href="(.+?)" class="play_link">').findall(html)
            for url in link:
                bits=re.compile("unescape.+?'(.+?)'").findall(net.http_GET('http://www.fanstash.eu%s'%url).content)
                sources.append(urllib.unquote(bits[0]))
        for url in sources:
            self.AddFileHost(list, 'SD', url)

    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):
        from entertainment.net import Net
        import re
        net = Net()
        
        search_term = '%s Season %s Episode %s'%(self.CleanTextForSearch(name),season,episode)
        url = self.GoogleSearchByTitleReturnFirstResultOnlyIfValid('http://www.fanstash.eu/', search_term, title_extrctr='watch (.+?) online free')

        if url: 
            self.GetFileHosts(url, list, lock, message_queue)
        
            
