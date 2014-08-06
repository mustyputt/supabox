'''
    Upafile Host resolver
    for Istream ONLY
    18/01/2014

    Jas0npc

    Big thanks to all that has guided me on my XBMC Journey.

    A thank you to all members of the Xunity team.

    (c)2014 Xunity.

    This resolver IS NOT OPEN SOURCE, It is to be used as
    part of Istream ONLY.

    version 0.1
'''
from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common

import xbmcgui
import xbmc
import os
                    


class Upafile(HostResolver, CustomSettings):
    implements = [HostResolver, CustomSettings]
    name = "Upafile"
    resolverName = name.title()+' (Resolver)'
    match_list = ['upafile.com']
    version = '0.1'
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
        xml += '<setting id="version" type="bool" label="'
        xml += '[COLOR blue]Version: '+self.version+'[/COLOR]" />\n'
        xml += '<setting type="sep"/>\n'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.resolverName, xml)
    
    def Resolve(self, url):
        from entertainment.net import Net
        import re

        net = Net(cached=False)
        
        common.addon.log( self.name.upper() + ' - Link: %s' % url )
        common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                      'Resolving', 700, self.icon)

        html = net.http_GET(url).content

        print html.encode('ascii','ignore')
        
        pattern = r'(op|id|rand|referer|method_free|method_premium|down_direct)"'
        pattern += '\svalue=\"?(.*?)\"'

        postData=dict(re.findall(pattern,html,re.I))

        captcha = re.search('api\/challenge\?k\=(.*?)\"',html,re.I)

        print html.encode('ascii','ignore')

        packed = re.search(r'script\'\>(eval\(function\(p\,a\,c\,k\,e.*?\)\)\))',html,re.I)
        print 'packed'
        print packed.groups()

        if packed:
            from entertainment import jsunpack

            unpacked=jsunpack.unpack(packed.group(1))

            print unpacked
            final = re.search(r"file\\',\\'(http\:.*?\:.*?)\'",unpacked,re.I)

            print final.group(1)
            if unpacked:
                return re.search(r"file\\',\\'(http\:.*?\:.*?)\\'",unpacked,re.I).group(1)

         
        #if captcha:

        #    thtml = net.http_GET('http://www.google.com/recaptcha/api/noscript?k='+captcha.group(1)).content

        #    img = re.search(r'src=\"(image.*?)\"',thtml)
        #    challange = re.search(r'recaptcha_challenge_field\"\svalue=\"(.*?)\"',thtml)

        #    print thtml.encode('ascii','ignore')

        #    print challange.groups()
        #    captchaimg = 'http://www.google.com/recaptcha/api/'+img.group(1)

        #    open(self.puzzle_img, 'wb').write(net.http_GET(captchaimg).content)

        #    img = xbmcgui.ControlImage(450,29,400,130,self.puzzle_img)
        #    wdlg = xbmcgui.WindowDialog()
        #    wdlg.addControl(img)
        #    wdlg.show()

        #    kb = xbmc.Keyboard('', 'Type the letters in the image', False)
        #    kb.doModal()
        #    capcode = kb.getText()

        #    if (kb.isConfirmed()):
        #        userInput = kb.getText()
        #        if userInput != '':
        #            solution = kb.getText()
        #        elif userInput == '':
        #            raise Exception ('You must enter text in the image to access video')
        #    else:
        #        return None
        #    wdlg.close()

        #    if solution:
        #        pattern = r'(op|id|rand|referer|method_free|method_premium|down_direct)"\svalue=\"?(.*?)\"'

        #        postData = {}
        #        r=re.findall(pattern,html,re.I)

        #        print r

        #        for key, value in r:
        #            postData.update({str(key): str(value),'recaptcha_challenge_field':str(challange.group(1)),'recaptcha_response_field':str(solution)})
       
        #        #print html.encode('ascii','ignore')
        #        #print postData

        #        #,'recaptcha_challenge_field':str(challange.group(1)),'recaptcha_response_field':str(solution)})
        #        #postData['recaptcha_challenge_field'] = challange.group(1)
        #        #postData['recaptcha_response_field'] = solution

        #        html = net.http_POST(url,postData,headers={'Content-Type':'application/x-www-form-urlencoded','Referer':url}).content

        #        print html.encode('ascii','ignore')
