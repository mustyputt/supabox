'''
    Movpod.in Host resolver
    for Istream ONLY
    18/01/2014

    Jas0npc, the-one

    A thank you to all members of the Xunity team, Voinage,
    Candita, Mikey1234, Coolwave, R3boot, Krankie882, Hawk

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
                    


class Movpod(HostResolver, CustomSettings):
    implements = [HostResolver, CustomSettings]
    name = "Movpod"
    resolverName = "Movpod.in (Resolver)"
    match_list = ['movpod.in']
    version = "0.1"
    
    profile_path = common.profile_path
    cookie_file = os.path.join(profile_path, 'cookies', '%s.cookies') % name
    puzzle_img = os.path.join(profile_path, 'captchas', '%s.jpg') % name
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
        import requests2
        import re

        common.addon.log( self.name.upper() + ' - Link: %s' % url )
        common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.title() + '[/B][/COLOR]',
                                      'Resolving', 700, self.icon)

        Host = re.search(r'//(.*?)/', url, re.I).group(1)
        Origin = 'http://'+Host
        Referer = url

        headers = {}
        postData = {}
        headers.update({'Connection': 'keep-alive'})

        try:
            r = requests2.get(url)

            secs = re.search(r'Wait\s(\d+)\sseconds', r.text, re.I)

            headers.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'Accept-Encoding': 'gzip,deflate,sdch', 'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
                            'Content-Type': 'application/x-www-form-urlencoded', 'Host': str(Host),
                            'Origin': str(Origin), 'Referer': str(url),
                            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36'})
            if secs:
                common.addon.show_countdown(int(secs.group(1)), title='[COLOR blue][B]I[/COLOR][/B]stream: '+self.name.upper(), text='')

                result = re.findall(r'hidden\"\sname=\"(.*?)\"\svalue=\"?(.*?)\"', r.text, re.I)
                for name, value in result:
                    postData.update({str(name): str(value)})
            
                r = requests2.post(url, data=postData, headers=headers)

                if r:
                    url = re.search(r'file\:\s\'(.*?)\'', r.text, re.I)
                    if url:
                        return url.group(1)

            raise Exception ('File Not Found.')
        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 3000, self.icon)                
            return None
                
            
            
