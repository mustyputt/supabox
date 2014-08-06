'''
    PandaPlanet Source Resolver
    For iStream Only,
    15/05/2014

    Jas0npc, the-one

    A thank you to all members of the Xunity team.

    (c)2014 Xunity.

    This resolver IS NOT OPEN SOURCE, It is to be used as
    part of Istream ONLY.

    
'''

from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common

import xbmcgui
import xbmc
import os


class Pandaplanet(HostResolver, CustomSettings):
    implements = [HostResolver, CustomSettings]
    name = "Pandaplanet"
    resolverName = "PandaPlanet ([COLOR blue]i[/COLOR]STREAM Resolver)"
    version = "0.1"
    match_list = ['pandapla.net']
    icon = common.notify_icon


    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="">\n'
        xml += '<setting type="sep"/>\n'
        xml += '<setting label="[COLOR blue]Version: '+self.version+'[/COLOR]" type="lsep" />\n'
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

            postData = {}
            for item in re.finditer(r'hidden\"\sname=\"(.*?)\"\svalue=\"?(.*?)\"',html):
                postData.update({str(item.group(1)):str(item.group(2))})

            html = net.http_POST(url,postData).content

            finalLink = re.search(r'download\_url\=(.*?)\'',html,re.I)
            if finalLink:
                return str(finalLink.group(1))

            else:
                raise Exception ('Playable Link Not Found')

        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 3000, self.icon)                
            return None
