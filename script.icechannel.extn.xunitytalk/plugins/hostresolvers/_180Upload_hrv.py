'''
    Ice Channel    
'''

from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay import Plugin
from entertainment import common
import xbmcgui

class _180Upload(HostResolver):
    implements = [HostResolver]
    
    name = '180upload'
    
    match_list = ['180upload.com']
    
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
            
            if dialog.iscanceled(): return url
            dialog.update(25)
            
            #Check page for any error msgs
            import re
            if re.search('>File Not Found', html):
                raise Exception ('File not found.__url')
                
            if re.search('\.(rar|zip)</b>', html):
                raise Exception ('File not found.__url')
                
            if dialog.iscanceled(): return url
            dialog.update(50)

            data = {}
            r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)

            if r:
                for name, value in r:
                    data[name] = value
            else:
                raise Exception ('Unable to resolve.')
            
            # Check for SolveMedia Captcha image
            captcha_result = common.handle_captcha(url, html)
            captcha_status = captcha_result.get('status', 'none')
            if captcha_status == 'error':
                captcha_message = captcha_result.get('message', 'Unable to resolve.')
                raise Exception (captcha_message + '__url')
            elif captcha_status == 'ok':
                for key,value in captcha_result.items():
                    if key not in ('status','message','captcha','captcha_type'):
                        data.update({key:value})
            
            if dialog.iscanceled(): return url
            dialog.update(75)
                
            html = net.http_POST(url, data).content
            
            if dialog.iscanceled(): return url
            dialog.update(100)
            
            link = re.search('id="lnk_download" href="([^"]+)"', html)
            if link:
                link = link.group(1)
            else:
                error = re.search('<div class="err">(.+?)</div>', html)
                if error:
                    raise Exception (error.group(1) + '__url')
                else:
                    raise Exception ('Unable to resolve.')

            return link
            
        except Exception, e:
            return_value = None
            ex = '%s' % e
            if ex.endswith('__url'):
                return_value = url
                ex = ex.replace('__url', '')
                
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % ex)
            
            if return_value:
                common.addon.show_small_popup('[B][COLOR white]' + self.name.upper() + '[/COLOR][/B]', '[COLOR red]%s[/COLOR]' % ex)                
            else:
                common.addon.show_small_popup('[B][COLOR white]' + self.name.upper() + '[/COLOR][/B]', '[COLOR red]Exception occured, check logs.[/COLOR]')
                
            return return_value
        
        finally:
            dialog.close()