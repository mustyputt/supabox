'''
    Nosvideo Host resolver
    for Istream ONLY
    18/01/2014

    Jas0npc, the-one

    A thank you to all members of the Xunity team,
    Voinage, Candita, Mikey1234, Coolwave, R3boot, WhufcLee,
    Krankie882, Dlrtybirdz, Hawk

    (c)2014 Xunity.

    This resolver IS NOT OPEN SOURCE, It is to be used as
    part of Istream ONLY.

    version 0.2
'''
from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay import Plugin
from entertainment import common

import xbmcgui
import xbmc
import os
                    


class Nosvideo(HostResolver):
    implements = [HostResolver]
    name = "nosvideo"
    match_list = ['nosvideo.com']
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

        common.addon.log( self.name.upper() + ' - Link: %s' % url )
        postData = {}
        referer = url
        
        net = Net(cached=False)
        html = net.http_GET(url).content

        if re.search(r'<b>File Not Found</b>', html, re.I):
            raise Exception ('File Not Found')

        try:
            url = re.search(r'top.location.href\s\=\s\'(.*?)\'\<\/script',
                            html, re.I).group(1)
            html = net.http_GET(url).content

            wait = re.search(r'var countdownNum =(.*?)\;', html, re.I)

            r = re.findall('hidden\"\sname=\"(.*?)\"\svalue=\"?(.*?)\"',
                           html, re.I)

            for name, value in r:
                postData.update({str(name): str(value)})
            postData.update({'referer': str(referer), 'method_free': 'Continue to Video'})

            common.addon.show_countdown(int(wait.group(1)), title='[COLOR blue][B]I[/COLOR][/B]stream: [COLOR white]'+self.name.title()+
                                        '[/COLOR]', text='')     

            r = re.search(r'cript\'\>(eval\(function\(p\,a\,c\,k\,e\,d\).*?\)\)\))',
                         net.http_POST(url, postData).content, re.I)

            if r:
                from entertainment import jsunpack
                lUrl = re.search('playlist\=(.*?)\&config', jsunpack.unpack(r.group(1)), re.I).group(1)
                url = re.search('\<file\>(.*?)\<\/file>', net.http_GET(lUrl).content, re.I).group(1)
                return url

            if not r:
                raise Exception ('File Not Found')

        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 700, self.icon)                
            return None
            
