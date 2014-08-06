'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveTVSource
from entertainment.plugnplay import Plugin
from entertainment import common

class iptvblog(LiveTVSource):
    implements = [LiveTVSource]
    
    display_name = "IPTV-BLOGS"
    
    name = 'IPTV-BLOGS'
    
    source_enabled_by_default = 'true'
    
    base_url = 'http://%s.blogspot.com/feeds/posts/default'
    
    BLOG=['iptv-free','iptv-list-updater','iptv-tv','links-iptv-playlist']

    def GetFileHosts(self, id, other_names, region, language, list, lock, message_queue):
        

        
        from entertainment.net import Net
        net = Net()

        clean_id= id.replace('_',' ').lower()
        
        for blogs in self.BLOG:
            
            r = self.base_url % blogs
            
            content = net.http_GET(r).content

            link = content.split('EXTINF')
            
            for p in link:
                
                if clean_id.replace(' ','') in p.replace(' ','').lower():
     
                    if 'raw=' in p:
                        
                        _url=p.split('raw=')[1]
                        url=_url.split('&lt;')[0]
                        
                    else:
                        d    =  p.split('&gt;')[1]
                        
                        url= d.split('&lt')[0]
                    if not '<?xml' in url:
                        if 'rtmp' in url:
                            url += ' timeout=10'
                        url=url.replace('&amp;','').replace('nbsp;','')    
                        self.AddLiveLink( list, clean_id.title(), url, host=blogs.upper())

        

    def Resolve(self, url):

        
        return url
        
        
    def Search(self, srcr, keywords, type, list, lock, message_queue, page='', total_pages=''): 
        
        self.GetFileHosts(keywords, '', '', '', list, lock, message_queue)
        
