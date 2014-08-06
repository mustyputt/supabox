'''
    MegaFiles Source Resolver
    For iStream Only,
    10/0/2014

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


class FileOM(HostResolver, CustomSettings):
    implements = [HostResolver, CustomSettings]
    name = "Megafiles"
    resolverName = name.title()+" ([COLOR blue]i[/COLOR]STREAM Resolver)"
    version = "0.1"
    match_list = ['megafiles.se']
    profile_path = common.profile_path
    cookie_file = os.path.join(profile_path, 'cookies', '%s.cookies') % name
    puzzle_img = os.path.join(profile_path, 'captchas', '%s.png') % name
    icon = common.notify_icon
    try:
        os.makedirs(os.path.dirname(cookie_file))
    except OSError:
        pass

    
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
            net.save_cookies(self.cookie_file)
            net.set_cookies(self.cookie_file)

            postData = {}

            for item in re.finditer(r'hidden\"\sname=\"(.*?)\"\svalue=\"?(.*?)\"',html,re.I):
                postData.update({str(item.group(1)):str(item.group(2))})


            captcha_result = common.handle_captcha(url, html)
            captcha_status = captcha_result.get('status', 'none')
            captcha_type = captcha_result['captcha_type']

            if captcha_status == 'error':
                captcha_message = captcha_result.get('message', 'Unable to resolve.')
                raise Exception (captcha_message)
            elif captcha_status == 'ok':                
                if 'solvemedia' in captcha_type:
                    postData.update({'adcopy_challenge': captcha_result['challenge'],'adcopy_response': captcha_result['captcha'],'referer':str(url)} )

                html = net.http_POST(url,postData).content

                finalLink = re.search(r'var\sdownload_url\s\=\s\'(.*?)\'',html,re.I)
                if finalLink:
                    return str(finalLink.group(1))

                if not finalLink:
                    raise Exception ('Streaming Media not found.')
        
        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 3000, self.icon)                
            return None
