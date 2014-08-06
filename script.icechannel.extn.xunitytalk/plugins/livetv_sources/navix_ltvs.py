'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveTVSource
from entertainment.plugnplay import Plugin
from entertainment import common

class navix(LiveTVSource):
    implements = [LiveTVSource]
    
    display_name = "NAVI X"
    
    name = 'NAVI X'
    
    source_enabled_by_default = 'true'
    
    base_url = 'http://www.navixtreme.com/playlist/search/'
    
    second_url = 'http://www.navixtreme.com/cgi-bin/boseman/Scrapers/ct_gsearchv20?q=basic/on/'

    def GetFileHosts(self, id, other_names, region, language, list, lock, message_queue):
        


        from entertainment.net import Net
        net = Net()

        clean_id= id.replace('_',' ').lower()
        
        r = self.base_url + id.replace('_','%20')+'%20rtmp'
        
        content = net.http_GET(r).content

        link = content.split('type')
        
        for p in link:
            
            if '=video' in p:
                
                if clean_id in p.lower():
                    
                    import re
                    
                    d    =  p.split('player=')[0]
                  
                    name =  re.compile('name=(.+?)\n').findall(d)[0]
                    
                    url  =  re.compile('URL=(.+?)\n').findall(d)[0]

                    if not re.search('\.[a-zA-z]{3}$', url):
                        
                        if re.search('(rtmp|mms|rtmpe|rtsp.*)', url):
                            if 'HD' in name:
                                res='HD'
                            else:
                                res='SD' 
                            url=url.replace('%20',' ')
                            self.AddLiveLink( list, name, url, host='NAVIX',quality=res)
                            


    def Resolve(self, url):

        
        return url
        
        
    def Search(self, srcr, keywords, type, list, lock, message_queue, page='', total_pages=''): 
        
        self.GetFileHosts(keywords, '', '', '', list, lock, message_queue)
