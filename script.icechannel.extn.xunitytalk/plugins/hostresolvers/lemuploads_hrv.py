'''
    Ice Channel    
'''

from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay import Plugin
from entertainment import common
import xbmcgui

class LemUploads(HostResolver):
    implements = [HostResolver]
    
    name = 'lemuploads'
    
    match_list = ['lemuploads.com']
    
    def Resolve(self, url):
    
        try:
            
            #Show dialog box so user knows something is happening
            dialog = xbmcgui.DialogProgress()
            dialog.create('Resolving', 'Resolving ' + self.name.upper() + ' Link...')
            dialog.update(0)
            
            common.addon.log( self.name.upper() + ' - Link: %s' % url )
            
            from entertainment.net import Net
            net = Net(cached=False)
            html = net.http_GET(url).content
            
            if dialog.iscanceled(): return None
            dialog.update(25)
            
            #Check page for any error msgs
            import re
            if re.search('This server is in maintenance mode', html):
                common.addon.log(self.name.upper() + ' - Site in maintenance mode')
                common.addon.show_small_popup('[B][COLOR white]' + self.name.upper() + '[/COLOR][/B]', '[COLOR red]Site is in maintenance mode.[/COLOR]')
                return None
            if re.search('<b>File Not Found</b>', html):
                common.addon.log(self.name.upper() + ' - File not found')
                common.addon.show_small_popup('[B][COLOR white]' + self.name.upper() + '[/COLOR][/B]', '[COLOR red]File not found.[/COLOR]')                
                return None
            
            if dialog.iscanceled(): return None
            dialog.update(50)

            filename = re.search('<h2>(.+?)</h2>', html).group(1)
            extension = re.search('(\.[^\.]*$)', filename).group(1)
            
            guid = re.search('http://lemuploads.com/(.+)$', url).group(1)
            
            vid_embed_url = 'http://lemuploads.com/vidembed-%s%s' % (guid, extension)
            headers = {'Referer':url}
            
            if dialog.iscanceled(): return None
            dialog.update(75)
            
            response = net.http_HEAD(vid_embed_url, headers=headers, auto_read_response=False)
            redirect_url = re.search('(http://.+?)video', response.get_url()).group(1)
            download_link = redirect_url + filename
            
            if dialog.iscanceled(): return None
            dialog.update(100)

            return download_link
            
        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR white]' + self.name.upper() + '[/COLOR][/B]', '[COLOR red]Exception occured, check logs.[/COLOR]')                
            return None
        finally:
            dialog.close()