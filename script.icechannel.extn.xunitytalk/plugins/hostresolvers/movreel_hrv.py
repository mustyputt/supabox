'''
    Movreel.com Host resolver
    for Istream ONLY
    18/01/2014

    Jas0npc

    Big thanks to all that has guided me on my XBMC Journey.

    A thank you to all members of the Xunity team.

    (c)2014 Xunity.

    This resolver IS NOT OPEN SOURCE, It is to be used as
    part of Istream ONLY.

    version 0.3
'''
from entertainment import jsunpack
from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common

import xbmcgui
import xbmc
import os
                    


class Movreel(HostResolver, CustomSettings):
    implements = [HostResolver, CustomSettings]
    name = "Movreel"
    resolverName = name.title()+' (Resolver)'
    match_list = ['movreel.com']
    version = '0.1'
    profile_path = common.profile_path
    cookie_file = os.path.join(profile_path, 'cookies', '%s.cookies') % name
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
        
        common.addon.log( self.name.upper() + ' - Link: %s' % url )
        common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                      'Resolving', 700, self.icon)

        try:

            html = net.http_GET(url).content
            postData = {}
            for item in re.finditer(r'\"\sname\=\"(.*?)\"\svalue=\"?(.*?)\"',html,re.I):
                postData.update({str(item.group(1)):str(item.group(2))})

            if postData:
                finalLink=re.search(r'\"(.*?)\"\>Down',net.http_POST(url,postData,headers={'Content-Type':'application/x-www-form-urlencoded',
                                                                                           'Referer':str(url),'Origin':'http://movreel.com',
                                                                                           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}).content,
                                    re.I)
                if finalLink:
                    return finalLink.group(1)

                if not finalLink:
                    raise Exception ('Streaming Media Not Found')

        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 700, self.icon)                
            return None
        
