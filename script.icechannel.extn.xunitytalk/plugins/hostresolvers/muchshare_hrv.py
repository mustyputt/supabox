'''
    Muchshare Host resolver
    for Istream Only 
    23/01/2014

    Jas0npc, the-one

    version 0.1

    A thank you to all members of the Xunity team.

    (c)2014 Xunity.

    This resolver IS NOT OPEN SOURCE, It is to be used as
    part of Istream ONLY.
'''
from entertainment import jsunpack
from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay import Plugin
from entertainment import common

import xbmcgui
import xbmc
import os
                    


class Muchshare(HostResolver):
    implements = [HostResolver]
    name = "muchshare"
    match_list = ['muchshare.net']
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

        
        headers = {}
        postData = {}
        referer = url
        
        net = Net(cached=False)
        common.addon.log( self.name.upper() + ' - Link: %s' % url )

        try:
            html = net.http_GET(url).content
            net.save_cookies(self.cookie_file)
            net.set_cookies(self.cookie_file)

            r = re.findall(r'hidden\"\sname=\"(.*?)\"\svalue=\"?(.*?)\"\>', html, re.I)
            for name, value in r:
                postData.update({str(name): str(value), 'method_free': 'Proceed to Video'})

            html = net.http_POST(url, postData).content

            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                          'Resolving', 700, self.icon)

            secs = re.search(r'\>Wait \<span id=\"\w+\"\>(\d+)\<\/', html, re.I)
            if not secs:
                message = re.search(r'err\"\>(.*?)till next', html, re.I)
                raise Exception (message.group(1)+' to try again.')

            common.addon.show_countdown(int(secs.group(1)), title='[COLOR blue][B]I[/B][/COLOR]stream: Muchshare', text='')

            postData.clear()
            r = re.findall(r'hidden\"\sname=\"(.*?)\"\svalue=\"(.*?)\"\>', html, re.I)

            for name, value in r:
                postData.update({str(name): str(value)})
            postData.update({'referer': referer})

            html = net.http_POST(url, postData).content

            url = re.search(r'lnk_download\"\shref=\"(.*?)\"\>', html, re.I)

            if url:
                return url.group(1)
            if not url:
                raise Exception ('Link Not Found.')
                

        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 700, self.icon)                
            return None
