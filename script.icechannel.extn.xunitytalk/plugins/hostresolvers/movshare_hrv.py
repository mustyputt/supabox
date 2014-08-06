'''
    Movshare.net Host resolver
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


class Movshare(HostResolver, CustomSettings):
    implements = [HostResolver, CustomSettings]
    name = "Movshare.net"
    resolverName = name.title()+" ([COLOR blue]i[/COLOR]STREAM Resolver)"
    version = "0.1"
    match_list = ['movshare.net','movshare.sx']
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

            jsvars=dict(re.findall(r'flashvars\.(.*?)\=\"(.*?)\"\;',html,re.I))

            if not jsvars:
                raise Exception ('File Not Found')

            if  'cid3' not in jsvars:
                jsvars['cid3']='undefined'
            if 'cid2' not in jsvars:
                jsvars['cid2']='undefined'
                
            url=jsvars['domain']+'/api/player.api.php?cid='+jsvars['cid']+'&cid2='+jsvars['cid2']
            url+='&key='+jsvars['filekey']+'&cid3='+jsvars['cid3']+'&numOfErrors=0&file='+jsvars['file']
            url+='&user=undefined&pass=undefined'

            finallink=re.search(r'url=(.*?)\&',net.http_GET(url).content).group(1)+'?client=FLASH'
            if finallink:
                return finallink

            raise Exception ('Media To Stream Not Found')

        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 3000, self.icon)                
            return None
        
                    
