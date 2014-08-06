'''
    Kingfiles Source Resolver
    For iStream Only,
    05/01/2014

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
                    


class Kingfiles(HostResolver, CustomSettings):
    implements = [HostResolver, CustomSettings]
    name = "kingfiles"
    version = "0.2"
    resolverName = name.title()+" ([COLOR blue]i[/COLOR]STREAM Resolver)"
    match_list = ['kingfiles.net']
    profile_path = common.profile_path
    cookie_file = os.path.join(common.cookies_path, '%s.cookies') % name
    puzzle_img = os.path.join(common.captchas_path, '%s.jpg') % name
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
        from entertainment.net import Net
        import re
        net = Net(cached=False)
        Referer = url

        common.addon.log( self.name.upper() + ' - Link: %s' % url )
        common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                      'Resolving', 700, self.icon)

        try:
            html = net.http_GET(url).content
            net.save_cookies(self.cookie_file)
            net.set_cookies(self.cookie_file)

            if not re.search(r'hidden',html):
                raise Exception ('File not found.')

            postData = {}

            for items in re.finditer(r'\"hidden\"\sname=\"(.*?)\"\svalue=\"?(.*?)\"',html):
                postData.update({str(items.group(1)): str(items.group(2)), 'referer': '', 'method_free': '+'})

            captcha = {}
            code = ''
            html = net.http_POST(url,postData).content

            r = re.findall(r'padding-left:(\d+)px;padding-top:\d+px\;\'\>(.*?)\<\/span\>',html)
            from entertainment import htmlcleaner

            for key, value in r:
                value2 = htmlcleaner.unescape(value)
                captcha.update({int(key): str(value2)})
            for key in sorted(captcha.iterkeys()):
                code = code+captcha[key]

            postData.update({'code': str(code)})
            del postData['usr_login']

            r = re.findall(r'hidden\"\sname=\"(.*?)\"\svalue=\"?(.*?)\"',html, re.I)

            for key, value in r:
                postData.update({str(key): str(value)})

            r = re.findall(r'div\sclass=\"err\"\>(.*?)\<',html)
            if r:
                dialog = xbmcgui.Dialog()
                dialog.ok('[COLOR red]ERROR[/COLOR]',str(r[0]),'')
                return
        
            secs = re.search(r'\"\>Wait\s\<span\sid=\".*?\"\>(\d+)\<\/', html, re.I).group(1)
            common.addon.show_countdown(int(str(secs)), title='Kingfiles', text='please wait')

            html = net.http_POST(url,postData,headers={'Content-Type':'application/x-www-form-urlencoded',
                                                       'Referer':str(url),'Origin':'http://www.kingfiles.net',
                                                       'Host':'www.kingfiles.net'}).content

            final = re.search(r'var\sdownload_url\s=\s\'(.*?)\'\;',html)
            if final:
                return final.group(1)

            if not final:
                raise Exception ('Streaming Media Not Found') 
        
        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 3000, self.icon)                
            return None
        
