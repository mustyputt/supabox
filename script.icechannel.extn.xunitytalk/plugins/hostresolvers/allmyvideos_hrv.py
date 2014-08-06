'''
    Allmyvideos.me Host resolver
    for Istream ONLY
    18/01/2014

    Jas0npc, the-one

    A thank you to all members of the Xunity team, Voinage,
    Mikey1234, Coolwave, R3boot, Krankie882, Hawk

    (c)2014 Xunity.

    This resolver IS NOT OPEN SOURCE, It is to be used as
    part of Istream ONLY.

    version 0.2
'''
from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common

import xbmcgui
import xbmc
import os
                    


class Almyvideos(HostResolver, CustomSettings):
    implements = [HostResolver, CustomSettings]
    name = "allmyvideos"
    resolverName = "Allmyvideos ([COLOR blue]i[/COLOR]STREAM Resolver)"
    match_list = ['allmyvideos.net']
    version = "0.2"
    icon = common.notify_icon

    
    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="">\n'
        xml += '<setting id="version" type="bool" label="'
        xml += '[COLOR blue]Version: '+self.version+'[/COLOR]" />\n'
        xml += '<setting type="sep"/>\n'
        xml += '<setting id="quality" type="enum" label="Quality"'
        xml += 'values="480p|720p" default="0" />\n'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.resolverName, xml)
        
        
    def Resolve(self, url):
        import requests2
        import re

        fileid = re.search(r'net\/([a-zA-Z0-9]+)', url, re.I)

        if fileid:
            url = 'http://allmyvideos.net/embed-'+fileid.group(1)+'-650x360.html'
        
        common.addon.log( self.name.upper() + ' - Link: %s' % url )
        common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                      'Resolving', 700, self.icon)
        
        quality = self.Settings().get_setting('quality')

        try:
            if quality == '0':
                quality = '480'
            elif quality == '1':
                quality = '720'

            r = requests2.get(url)
            r = re.findall(r'\"file\"\s\:\s\"(http.+?)\".+?\"label\"\s\:\s\"(\d+)\"', str(r.text), re.I|re.DOTALL)

            if not r:
                raise Exception ('Video Not Found.')
            
            if r:
                for url, qual in r:
                    if quality == qual:
                        common.addon.log( self.name.upper() + ' - Link: %s Quality: %s' % (url, quality))
                        return url
            

        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 700, self.icon)                
            return None
