'''
    Thevideo Host resolver
    for Istream ONLY
    05/01/2014

    A thank you to all members of the Xunity team.

    (c)2014 Xunity.

    This resolver IS NOT OPEN SOURCE, It is to be used as
    part of Istream ONLY.

    version 0.1
'''

from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common

import xbmcgui
import xbmc
import os


class Thevideo(HostResolver, CustomSettings):
    implements = [HostResolver, CustomSettings]
    name = "TheVideo"
    resolverName = name.title()+" ([COLOR blue]i[/COLOR]STREAM Resolver)"
    version = "0.1"
    match_list = ['thevideo.me']
    profile_path = common.profile_path
    cookie_file = os.path.join(profile_path, 'cookies', '%s.cookies') % name
    puzzle_img = os.path.join(profile_path, 'captchas', '%s.png') % name
    icon = common.notify_icon
    try:
        os.makedirs(os.path.dirname(cookie_file))
    except OSError:
        pass

    
    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="">\n'
        xml += '<setting id="version" type="bool" label="'
        xml += '[COLOR blue]Version: '+self.version+'[/COLOR]" />\n'
        xml += '<setting type="sep"/>\n'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.resolverName, xml)

    
    def Resolve(self, url):
        import re
        from entertainment.net import Net
        net = Net(cached=False)

        common.addon.log( self.name.upper() + ' - Link: %s' % url )
        common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                      'Resolving', 700, self.icon)
        try:
            
            html = net.http_GET(url).content
            net.save_cookies(self.cookie_file)
            net.set_cookies(self.cookie_file)

        
            postData={}
            for items in re.finditer(r'\"\sname\=\"(.*?)\"\svalue\=\"?(.*?)\"',html,re.I):
                postData.update({str(items.group(1)):str(items.group(2))})

            if items:
                return re.search(r'config\:\{file\:\'(.*?)\'',net.http_POST(url,postData).content,re.I).group(1)

            else:
                raise Exception ('File Not Found')
            
        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 3000, self.icon)                
            return None   
        
