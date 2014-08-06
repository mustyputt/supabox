'''
    Megarelease Host resolver
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
                    


class Megarelease(HostResolver):
    implements = [HostResolver]
    name = "megarelease"
    match_list = ['megarelease.org']
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

        Referer = url
        Host = re.search(r'//(.*?)/', url, re.I).group(1)
        Origin = 'http://'+Host

        common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                      'Resolving', 700, self.icon)

        try:
            html = net.http_GET(url).content
            net.save_cookies(self.cookie_file)
            net.set_cookies(self.cookie_file)

            headers = {}
            headers.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'Accept-Encoding': 'gzip,deflate,sdch', 'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
                            'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'Host': str(Host),
                            'Content-Type': 'application/x-www-form-urlencoded', 'Origin': str(Origin),
                            'Referer': str(Referer), 'User-Agent':
                            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36'})
        

            postData = {}

            r = re.findall(r'hidden\"\sname=\"(.*?)\"\svalue=\"?(.*?)\"', html, re.I)
            for name, value in r:
                postData.update({str(name): str(value)})

            captchaimg = re.search('<script type="text/javascript" src="(http://www.google.com.+?)">', html)

            if captchaimg:
                html = net.http_GET(captchaimg.group(1)).content
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

                postData.update({'recaptcha_challenge_field':part.group(1),
                                 'recaptcha_response_field': str(solution)})

                html = net.http_POST(url, postData, headers).content

                if re.search(r'err\"\>Wrong captcha\<\/div\>', html, re.I):
                    raise Exception ('Wrong captcha Entered')

                r = re.search(r'\<div id=\"player_code.*?script\'\>(eval\(function\(p\,a\,c\,k\,e\,d.*?\)\)\))', html, re.I|re.DOTALL)

                if r:
                    from entertainment import jsunpack
                    unpacked = jsunpack.unpack(r.group(1))
                    url = re.search(r"file\\',\\'(.*?)\\'", unpacked, re.I).group(1)
                    return url
            
                raise Exception ('Media Not Found')
            raise Exception ('Captcha Not Found')
        
        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 700, self.icon)                
            return None
