'''
    Bayfiles Host resolver
    for Istream ONLY
    05/01/2014

    A thank you to all members of the Xunity team.

    (c)2014 Xunity.

    This resolver IS NOT OPEN SOURCE, It is to be used as
    part of Istream ONLY.

    version 0.1
'''

from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay import Plugin
from entertainment import common

import cookielib
import xbmcgui
import xbmc
import re
import os


class Bayfiles(HostResolver):
    implements = [HostResolver]
    name = "bayfiles"
    match_list = ['bayfiles.net']
    profile_path = common.profile_path
    cookie_file = os.path.join(profile_path, 'cookies', '%s.cookies') % name
    icon = common.notify_icon
    try:
        os.makedirs(os.path.dirname(cookie_file))
    except OSError:
        pass


    def Resolve(self, url):
        from entertainment.net import Net
        net = Net(cached=False)

        try:
            html = net.http_GET(url).content

            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                          'Resolving', 700, self.icon)

            url = re.findall(r'ted-btn\"\shref=\"(.+?)\"\>Premium', html, re.I)

            if not url:
                raise Exception('file could not be found')

            return url[0]

        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 700, self.icon)                
            return None
