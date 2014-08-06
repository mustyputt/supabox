'''
    Vidto Host resolver
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
from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common

import xbmcgui
import xbmc
import os
                    


class Vidto(HostResolver, CustomSettings):
    implements = [HostResolver, CustomSettings]
    name = "Vidto"
    resolverName = name.title()+' (Resolver)'
    match_list = ['vidto.me']
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

        if re.search(r'\/embed\-',url):
            items = re.search(r'(http\:\/\/vidto\.me\/)embed\-(.*?)-\d+x',url,re.I)
            url=items.group(1)+items.group(2)+'.html'

        try:
            
            html = net.http_GET(url).content
            net.save_cookies(self.cookie_file)
            net.set_cookies(self.cookie_file)

            postData = {}
            secs = re.search(r'\"cxc\"\>(\d+)\<',html,re.I)

            if secs:
                for items in re.finditer(r'n\"\sname=\"(.*?)\"\svalue=\"?(.*?)\"',html,re.I):
                    postData.update({str(items.group(1)):str(items.group(2))})

                common.addon.show_countdown(int(str(secs.group(1))), title='[COLOR blue][B]I[/COLOR][/B]stream: '+self.name.title(), text='')
                html=net.http_POST(url,postData).content

                r = re.search(r'script\'\>(eval\(function\(p\,a.*?\)\)\))',html,re.I)

                if r:
                    from entertainment import jsunpack
                    unpacked = jsunpack.unpack(r.group(1))

                    r = re.search(r'label\:\"360p\"\,file\:\"(.*?)\"',unpacked,re.I)

                    if r:
                        return r.group(1)

                    if not r:
                        return re.search(r'label\:\"240p\"\,file\:\"(.*?)\"',unpacked,re.I).group(1)

            raise Exception ('Media Not Found')

        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 3000, self.icon)                
            return None
