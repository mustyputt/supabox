from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common

class putlockerbz(MovieSource):
    implements = [MovieSource]
    
    name = "putlocker.bz"
    display_name = "Putlocker.bz"
    source_enabled_by_default = 'false'
    
    def GetFileHosts(self, url, list, lock, message_queue):
        import re
        from entertainment.net import Net
        net = Net()
        
        content = net.http_GET(url).content
        match = re.compile('proxy.file\':\'(.+?)\',\n\t\t\t\t\t\t\t\tfile:\'(.+?)\'').findall(content)
        for player, stuff in match:
            content = net.http_POST(player, {'url': stuff}).content.replace('""','"null"')
            links = re.compile('"file":".+?"|"large.file":".+?"|"hd.file":".+?"').findall(content)
            for info in links:
                res_link = re.split(':', info.replace('\\','').replace('"',''), 1)
                res = res_link[0]
                url = res_link[1]
                if url != 'null':
                    if res == 'hd.file':
                        res = 'HD'
                    elif res == 'large.file':
                        res = 'DVD'
                    else:
                        res = 'SD'
                    host = 'GOOGLVIDEO.COM'
                    self.AddFileHost(list, res, url, host)
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        import re, urllib
        from entertainment.net import Net
        net = Net()
        
        name = self.CleanTextForSearch(name)
        helper ='%s (%s)' %(name, year)
        name = urllib.quote(name)
        search_url = 'http://putlocker.bz/search/search.php?q=' + name
        content = net.http_GET(search_url).content
        search_res = re.split('Search Results For: "<font color=red>', content)[1]
        match = re.compile('href="(.+?)" title="(.+?)"').findall(search_res)
        for url, title in match:
            if title == helper or title == helper.replace(':',' 2:'):
                self.GetFileHosts(url, list, lock, message_queue)
