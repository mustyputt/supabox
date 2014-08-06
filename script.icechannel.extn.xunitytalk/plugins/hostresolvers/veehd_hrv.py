'''
    VeeHD Host resolver
    for Istream ONLY
    18/01/2014

    Jas0npc, the-one

    A thank you to all members of the Xunity team.

    (c)2014 Xunity.

    This resolver IS NOT OPEN SOURCE, It is to be used as
    part of Istream ONLY.

    Big thank you to T0mm0/Voinage, Without you guys, This would not have been possible.
    But some people cant figure out, How to add their login and password.
    (cough)Lee

    version 0.4
'''
from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay import Plugin
from entertainment import common

import xbmcgui
import xbmc
import os
                    


class VeeHD(HostResolver):
    implements = [HostResolver]
    name = "VeeHD"
    match_list = ['veehd.com']
    profile_path = common.profile_path
    cookie_file = os.path.join(profile_path, 'cookies', '%s.cookies') % name
    icon = common.notify_icon


    

    
    def Resolve(self, url):
        from entertainment.net import Net
        import re

        common.addon.log( self.name.upper() + ' - Link: %s' % url )
        net = Net(cached=False)

        postData = {}
        postData.update({'ref': 'http://veehd.com/login', 'uname': '101stream',
                         'pword': 'pass101', 'submit': 'Login', 'terms': 'on',
                         'remember_me': 'on'})

        #try:

        try:
            html = net.http_POST('http://veehd.com/login', postData).content
            net.save_cookies(self.cookie_file)
            net.set_cookies(self.cookie_file)
        except Exception, e:
            raise Exception (str(e))

        
        common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                      'Resolving', 700, self.icon)

        try:    
            html = net.http_GET(url).content
            r = re.search(r'playeriframe".+?attr.+?src : "(.+?)"', html)
            if r:
                frag = 'http://veehd.com'+r.group(1)
                html = net.http_GET(frag).content

            r = re.search(r'video\/divx\"\ssrc=\"(.*?)"', html, re.I)
            if r:
                return r.group(1)
            if not r:
                r = re.search(r'url\"\:\"(.*?)\"',html, re.I)
                if r:
                    import urllib
                    return urllib.unquote_plus(r.group(1))
                
        
            r = re.search(r'\"(\/embed\?v.*?)\"', html, re.I)

            if r:
                html = net.http_GET('http://www.veehd.com'+r.group(1)).content

                r = re.search(r'video\/divx\"\ssrc=\"(.*?)"', html, re.I)

                if r:
                    return r.group(1)
                else:
                    a = re.search('"url":"(.+?)"', html)
                    r = urllib.unquote(a.group(1))

                    if r:
                        return r

            raise Exception ('File Not Found or removed')

        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 700, self.icon)                
            return None
