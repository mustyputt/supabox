'''
    Filecloud Host resolver
    for Istream ONLY
    18/01/2014

    Jas0npc, the-one

    A thank you to all members of the Xunity team.

    (c)2014 Xunity.

    This resolver IS NOT OPEN SOURCE, It is to be used as
    part of Istream ONLY.

    version 0.3
'''
from entertainment import jsunpack
from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay import Plugin
from entertainment import common

import xbmcgui
import xbmc
import os
                    


class Filecloud(HostResolver):
    implements = [HostResolver]
    name = "Filecloud"
    match_list = ['filecloud.io']
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
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                          'Resolving', 700, self.icon)

            html = net.http_GET(url).content
            net.save_cookies(self.cookie_file)
            net.set_cookies(self.cookie_file)
            headers = {}

            url = re.search(r'__requestUrl\s+\=\s+\'(.*?)\'', html, re.I).group(1)
            ukey = re.search(r'ukey\'\s+\:\s+\'(.*?)\'', html, re.I).group(1)
            __ab1 = re.search(r'\{var\s__ab1\s=\s(\d+)\;\}', html, re.I).group(1)
        
            captcha = re.search(r'recaptcha_public  =	\'(.*?)\'', html, re.I).group(1)
            ctype = re.search(r'\'ctype\'\s+\:\s+\'(.*?)\'', html, re.I).group(1)

            headers.update({'Accept': 'application/json, text/javascript, */*; q=0.01',
                            'Accept-Encoding': 'gzip,deflate,sdch', 'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
                            'Connection': 'keep-alive', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                            'Host': 'filecloud.io', 'Origin': 'http://filecloud.io', 'Referer': 'http://filecloud.io/download.html',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36',
                            'X-Requested-With': 'XMLHttpRequest'})
        
            html = net.http_POST(url, {'ukey': str(ukey), '__ab1': str(__ab1)}, headers).content

        
            if captcha:
                captchUrl = 'http://www.google.com/recaptcha/api/challenge?k='+captcha
                html = net.http_GET(captchUrl).content
                part = re.search("challenge \: \\'(.+?)\\'", html)
                captchaimg = 'http://www.google.com/recaptcha/api/image?c='+part.group(1)
                open(self.puzzle_img, 'wb').write(net.http_GET(captchaimg).content)
            
        
                img = xbmcgui.ControlImage(450,29,400,130,self.puzzle_img)
                wdlg = xbmcgui.WindowDialog()
                wdlg.addControl(img)
                wdlg.show()

                kb = xbmc.Keyboard('', 'Type the letters in the image', False)
                kb.doModal()
                capcode = kb.getText()

                if (kb.isConfirmed()):
                    userInput = kb.getText()
                    if userInput != '':
                        solution = kb.getText()
                    elif userInput == '':
                        raise Exception ('You must enter text in the image to access video')
                else:
                    return None
                wdlg.close()

                if solution:
                    postData = {}
                    postData.update({'ukey': str(ukey), '__ab1': str(__ab1), 'ctype': str(ctype),
                                     'recaptcha_response': str(solution), 'recaptcha_challenge': str(part.group(1))})

                    html = net.http_POST(url, postData).content

                    r = re.search(r'\"retry\"\:[1:9]', html, re.I)
                    if r:
                        raise Exception ('Incorrect Captcha Entered.')

                
                    html = net.http_GET('http://filecloud.io/download.html').content

                    r = re.search(r'href=\"(.*?)\"(?=\sclass=\"btn\")', html, re.I)
                    if r:
                        del headers
                        host = re.search(r'//(.*?)/', r.group(1)).group(1)

                        headers = {}
                        headers.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                        'Accept-Encoding': 'gzip,deflate,sdch', 'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
                                        'Connection': 'keep-alive', 'Host': str(host),
                                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36'})
            
                        #h = net.http_GET(r.group(1), headers, auto_read_response=False).get_headers()

                        #print h
                        #print url
                        return r.group(1)
                        #print html.encode('ascii', 'ignore')

                    raise Exception ('Playable Link Not Found.')
                
        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 700, self.icon)                
            return None
