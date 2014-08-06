'''
    Googleplus
    for Istream ONLY
    

    Coolwave

    A thank you to all members of the Xunity team.

    (c)2014 Xunity.

    This resolver IS NOT OPEN SOURCE, It is to be used as
    part of Istream ONLY.

    version 0.1
'''
from entertainment import jsunpack
from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay import Plugin
from entertainment import common

import xbmcgui
import xbmc
import os
                    


class googleplus(HostResolver):
    implements = [HostResolver]
    name = "googleplus"
    match_list = ['plus.google.com']
    profile_path = common.profile_path
    cookie_file = os.path.join(profile_path, 'cookies', '%s.cookies') % name
    puzzle_img = os.path.join(profile_path, 'captchas', '%s.png') % name
    icon = common.notify_icon
    try:
        os.makedirs(os.path.dirname(cookie_file))
    except OSError:
        pass

    
    def Resolve(self, url):

        from entertainment.net import Net
        import re
        import time

        net = Net()

        try:

            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                          'Resolving', 700, self.icon)
        
            result = net.http_GET(url).content

            res_name = []
            res_url = []

            r = re.findall('\,(\d+\,\d+)\,\"(http://redirector.googlevideo.com/videoplayback?.*?)\"',result)
            
            for quality, url in r:
                if '1920' in quality:
                    quality = '1080P'
                elif '1280' in quality:
                    quality = '720P'
                elif '852' in quality:
                    quality = 'SD'
                else:
                    quality ='LOW QUALITY'
                res_name.append(quality)                
                res_url.append(url)

            dialog = xbmcgui.Dialog()
            ret = dialog.select('Please Select Stream Quality.',res_name)

            if ret == 0:
                return None

            elif ret >1:
                print res_url[ret]
                return res_url[ret].replace('\u003d','=').replace('\u0026','&')

            

        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 700, self.icon)                
            return None

        
