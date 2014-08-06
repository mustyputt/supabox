'''
    Ice Channel
    yify.tv
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay import Plugin
from entertainment import common

class yifytv(MovieSource,HostResolver):
    implements = [MovieSource,HostResolver]
    
    name = "Yify.tv"
    display_name = "Yify TV"

    base_url='http://yify.tv'
    
    source_enabled_by_default = 'false'
    
    match_list = ['yify.tv']
    
    def GetFileHosts(self, url, list, lock, message_queue):
        import re
        from entertainment.net import Net
        
        net = Net()
        url = url.replace('\/', '/')
        html = net.http_GET(url, headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Host':'yify.tv','Pragma':'no-cache', 'Referer':'http://yify.tv/'}).content
        
        net._cached = False
        
        video_request_param = re.search('showPkPlayer\("(.+?)"\)', html)
        if video_request_param:
            video_request_param = video_request_param.group(1)
        else:
            return
            
        video_reqest_dict = 'url=https%3A//picasaweb.google.com/' + video_request_param + '&_' + common.GetEpochStr()
        
        import urllib
        
        try:
            video_request_url = self.base_url + '/reproductor2/pk/pk/plugins/player_p.php?url=' + video_request_param
            videos = net.http_GET(video_request_url).content
        except:
            video_request_url = self.base_url + '/reproductor2/pk/pk/plugins/player_p2.php'
            videos = net.http_POST(video_request_url, {'url':video_request_param}).content
        quality_dict = {'1920':'HD', '1280':'HD', '854':'SD', '640':'LOW', '426':'LOW'}
        
        import json
        video_links = json.loads(videos)
        for video_link in video_links:
            if 'videoplayback' in video_link['url']:
                # print video_link['url']
                self.AddFileHost(list, quality_dict.get(str(video_link['width']), 'NA'), video_link['url'], host='YIFY.TV')
        
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        import re
        from entertainment.net import Net
        
        net = Net()
        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name) 
        name_lower = name.lower()
        name_id = common.CreateIdFromString(name)
            
        import urllib
        from entertainment import odict
        search_dict = odict.odict({'years':year, 's':name})
        search_dict.sort(key=lambda x: x[0].lower())
        
        search_for_url = self.base_url + '/?' + urllib.urlencode(search_dict)
        #print search_for_url
        search_content = net.http_GET(search_for_url).content
        for search_item in re.finditer(',"title":"(.+?)","link":"(.+?)",.+?,"year":"(.+?)",', search_content):
            item_link = search_item.group(2)
            item_name_id = common.CreateIdFromString( search_item.group(1).lower() )
            if name_id == item_name_id and year == search_item.group(3):
                self.GetFileHosts(item_link, list, lock, message_queue)
                break
                
    def Resolve(self, url):
        if 'videoplayback' in url: return url   
        
        resolved_url = ''
        
        import re
        from entertainment.net import Net        
        net = Net()
        url = url.replace('\/', '/')
        html = net.http_GET(url, headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Host':'yify.tv','Pragma':'no-cache', 'Referer':'http://yify.tv/'}).content
        
        net._cached = False
        
        video_request_param = re.search('showPkPlayer\("(.+?)"\)', html)
        if video_request_param:
            video_request_param = video_request_param.group(1)
        else:
            return
            
        video_reqest_dict = 'url=https%3A//picasaweb.google.com/' + video_request_param + '&_' + common.GetEpochStr()
        
        import urllib
        try:
            video_request_url = self.base_url + '/reproductor2/pk/pk/plugins/player_p.php?url=' + video_request_param
            videos = net.http_GET(video_request_url).content
        except:
            video_request_url = self.base_url + '/reproductor2/pk/pk/plugins/player_p.php'
            videos = net.http_POST(video_request_url, {'url':video_request_param}).content
        
        quality_dict = {'1920':'HD', '1280':'HD', '854':'SD', '640':'LOW', '426':'LOW'}
        
        import json
        video_links = json.loads(videos)
        quality_width = 0
        for video_link in video_links:
            if 'videoplayback' in video_link['url'] and video_link['width'] >= quality_width:
                quality_width = video_link['width']
                resolved_url = video_link['url']
            
        return resolved_url
