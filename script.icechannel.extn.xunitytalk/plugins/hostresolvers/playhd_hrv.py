'''
    PlayHD Host resolver
    for Istream ONLY
    24/07/2014

    Jas0npc

    Big thanks to all that has guided me on my XBMC Journey.

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
                    


class PlayHD(HostResolver, CustomSettings):
    implements = [HostResolver, CustomSettings]
    name = "PlayHD"
    resolverName = name.title()+' (Resolver)'
    match_list = ['playhd.eu']
    version = '0.1'
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
        from entertainment.net import Net
        import re

        net = Net(cached=False)
        
        common.addon.log( self.name.upper() + ' Link: %s' % url )
        common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                      'Resolving', 700, self.icon)

        try:
            html = net.http_GET(url).content
            net.save_cookies(self.cookie_file)
            net.set_cookies(self.cookie_file)

            postdata = {}

            for pd in re.finditer(r'den\"\sname=\"(.*?)\"\svalue=\"?(.*?)\"',html,re.I):
                postdata[str(pd.group(1))]=str(pd.group(2))
            postdata['imhuman']='Proceed to video'

            html=net.http_POST(url,postdata).content

            r = re.search(r'file\:\s\"(.*?)\"',html,re.I)
            if r:
                common.addon.log(self.name.upper() + ' Resolved Link: %s' % str(r.group(1)))
                return r.group(1)

            if not r:
                raise Exception ('Resolved Link Not Found')
        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 3000, self.icon)                
            return None
            
        
