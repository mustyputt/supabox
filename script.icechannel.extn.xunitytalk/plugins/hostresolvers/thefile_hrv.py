'''
    Thefile.me Host resolver
    for Istream ONLY
    18/01/2014

    Jas0npc, the-one

    A thank you to all members of the Xunity team,
    Voinage, Candita, Mikey1234, Coolwave, R3boot, WhufcLee,
    Krankie882, Dlrtybirdz, Hawk

    (c)2014 Xunity.

    This resolver IS NOT OPEN SOURCE, It is to be used as
    part of Istream ONLY.

    version 0.1
'''
from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay import Plugin
from entertainment import common

import xbmcgui
import xbmc
import os
                    


class Thefile(HostResolver):
    implements = [HostResolver]
    name = "thefile"
    match_list = ['thefile.me']
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
        net = Net(cached=False)

        try:
            html = net.http_GET(url).content

            if re.search(r'\<b\>Free\<\/b\>', html, re.I):
                postData = {}
                r = re.findall(r'hidden\"\sname=\"(.*?)\"\svalue=\"?(.*?)\"', html, re.I)
                for name, value in r:
                    postData.update({str(name): str(value), 'op': 'download1',
                                     'method_free': 'Free Download'})

                html = net.http_POST(url, postData).content

            pattern = 'me\/player\/jwplayer\.js\'\>\<\/script\>.*?\<script\stype=\''
            pattern +='text\/javascript\'\>(eval\(function\(p\,a\,c\,k\,e\,d\).*?'
            pattern +='\)\)\))'
            packed = re.search(r''+pattern+'', html, re.I|re.DOTALL).group(1)

            if packed:
                from entertainment import jsunpack

                common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                              'Resolving', 700, self.icon)                
            
                unpacked = jsunpack.unpack(packed)
                r = re.search(r'\{file\:\"(.*?)\"', unpacked, re.I)

                if r:
                    html = net.http_GET(r.group(1)+'?start=0',auto_read_response=False).get_url()
                    return r.group(1)+'?start=0'

            raise Exception ('Link Not Found')

            
        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 700, self.icon)                
            return None
