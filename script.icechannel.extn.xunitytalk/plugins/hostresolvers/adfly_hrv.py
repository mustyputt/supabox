'''
    adf.ly
    for Istream ONLY
    26/03/2014

    Jas0npc, Coolwave, The-One

    A thank you to all members of the Xunity team.

    (c)2014 Xunity.

    This resolver IS NOT OPEN SOURCE, It is to be used as
    part of Istream ONLY.

    version 0.1
'''
from entertainment import jsunpack
from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay import Plugin
from entertainment import common

import xbmcgui
import xbmc
import os
                    


class adfly(HostResolver):
    implements = [HostResolver]
    name = "adfly"
    match_list = ['adf.ly']
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
        import time

        net = Net()

        try:

            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                          'Resolving', 700, self.icon)
        
            content = net.http_GET(url).content
            time.sleep(9)
            encoded_url = re.compile("var ysmm = '(.+?)';").findall(content)[0]
            encoded_url_length = len(encoded_url)
            encdd_url_part_1 = ''
            encdd_url_part_2 = ''
            for x in range(0, encoded_url_length):
                enc_char = encoded_url[x]
                if not re.match("[a-zA-Z0-9\+/=]", enc_char):
                    break;
                if x % 2 == 0:
                    encdd_url_part_1 = encdd_url_part_1 + enc_char
                else:
                    encdd_url_part_2 = enc_char + encdd_url_part_2
            encoded_url = encdd_url_part_1 + encdd_url_part_2
            import base64
            new_url = (base64.b64decode(encoded_url))[2:]
            from entertainment import istream
            play_url = istream.ResolveUrl(new_url)
            return play_url

            

        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 700, self.icon)                
            return None

        
