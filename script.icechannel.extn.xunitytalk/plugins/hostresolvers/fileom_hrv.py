'''
    FileOM Source Resolver
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
    name = "fileom"
    resolverName = "FileOM ([COLOR blue]i[/COLOR]STREAM Resolver)"
    version = "0.1"
    match_list = ['fileom.com']
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

            fnf = re.search(r'page-title\"\>File Not Found\<',html)
            if fnf:
                raise Exception ('File not found.')
        
            t = re.search(r'down-btns\"\>(.+?)filebtndwns',html,re.I|re.DOTALL)
            postData = {}
            headers = {}

            headers.update({'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'Accept-Encoding':'gzip,deflate,sdch','Accept-Language':'en-GB,en-US;q=0.8,en;q=0.6',
                            'Connection':'keep-alive','Content-Type':'application/x-www-form-urlencoded',
                            'Host':'fileom.com','Origin':'http://fileom.com','Referer':str(url),
                            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'})



            for item in re.finditer(r'name=\"(.*?)\"\svalue=\"?(.*?)\"',str(t.groups())):
                postData.update({str(item.group(1)): str(item.group(2))})

            html = net.http_POST(url, postData, headers).content
            secs = re.search(r'Wait\s\<span\sid=\".*?\"\>(\d+)\<\/sp', html, re.I)

            if secs:
                captcha_result = common.handle_captcha(url, html)
                captcha_status = captcha_result.get('status', 'none')
                captcha_type = captcha_result['captcha_type']
            
                if captcha_status == 'error':
                    captcha_message = captcha_result.get('message', 'Unable to resolve.')
                    raise Exception (captcha_message)
                elif captcha_status == 'ok':                
                    if 'solvemedia' in captcha_type:
                        del postData

                        postData = {}
                        postData.update({'adcopy_challenge': captcha_result['challenge'],'adcopy_response': captcha_result['captcha']} )
                        temp = re.search(r'\"F1\"\smethod=\"POST\"(.*?)div\sstyle',html,re.DOTALL)
                        for item in re.finditer(r'name=\"(.*?)\"\svalue=\"?(.*?)\"',str(temp.group(1))):
                            postData.update({str(item.group(1)):str(item.group(2)),'down_direct':'1'})
                        common.addon.show_countdown(int(str(secs.group(1))), title='[COLOR blue][B]I[/COLOR][/B]stream: FileOM', text='')

                        html = net.http_POST(url, postData, headers).content
                        final = re.search(r'url2\s=\s\'(.*?)\'',html)
                        if final:
                            return final.group(1)

                        raise Exception ('Final Link Not Found')

                    

            elif not secs:
                error = re.search(r'err\"\>\<center\>(You have to wait \d+ minutes, \d+ seconds  till next download)\s+',html, re.I)
                if error:
                    common.addon.log(self.name.upper() +' '+error.group(1))

                    for item in re.finditer(r'\s(\d+)\sminutes\,\s(\d+)\s', error.group(1)):
                        error = 'You have to wait [COLOR red][B]%s[/COLOR][/B] minutes, [COLOR red][B]%s[/COLOR][/B] seconds untill next stream'%(item.group(1),item.group(2))

                    dialog = xbmcgui.Dialog()
                    ok = dialog.ok('XBMC', error)
                    return

        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 3000, self.icon)                
            return None
