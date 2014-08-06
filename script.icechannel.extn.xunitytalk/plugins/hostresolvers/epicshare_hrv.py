'''
    EpicShare Host resolver
    for Istream ONLY
    18/01/2014

    Jas0npc, the-one

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
                    


class Epicshare(HostResolver):
    implements = [HostResolver]
    name = "Epicshare"
    match_list = ['epicshare.net']
    profile_path = common.profile_path
    cookie_file = os.path.join(common.cookies_path, '%s.cookies') % name
    puzzle_img = os.path.join(common.captchas_path, '%s.jpg') % name
    icon = common.notify_icon
    try:
        os.makedirs(os.path.dirname(cookie_file))
    except OSError:
        pass

    
    def Resolve(self, url):
        from entertainment.net import Net
        import re
        net = Net(cached=False)
        Referer = url

        common.addon.log( self.name.upper() + ' - Link: %s' % url )
        common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                      'Resolving', 700, self.icon)

        try:
            postData = {}
            html = net.http_GET(url).content

            #file not found check goes here

            r = re.findall(r'hidden\"\sname=\"(.*)\"\svalue=\"?(.*?)\"', html, re.I)
            for name, value in r:
                postData.update({str(name): str(value)})

            solvemedia = re.search('<iframe src="(http://api.solvemedia.com.+?)"', html)

            if not solvemedia:
                raise Exception ('File Not Found.')

            if solvemedia:
                html = net.http_GET(solvemedia.group(1)).content
                hugekey=re.search('id="adcopy_challenge" value="(.+?)">', html).group(1)
                open(self.puzzle_img, 'wb').write(net.http_GET("http://api.solvemedia.com%s" %
                                                               re.search('<img src="(.+?)"', html).group(1)).content)

                img = xbmcgui.ControlImage(450,15,400,130, self.puzzle_img)
                wdlg = xbmcgui.WindowDialog()
                wdlg.addControl(img)
                wdlg.show()

                kb = xbmc.Keyboard('', 'Please enter the text in the image', False)
                kb.doModal()
                capcode = kb.getText()

                if (kb.isConfirmed()):
                    userInput = kb.getText()
                    if userInput != '':
                        solution = kb.getText()
                    elif userInput == '':
                        raise Exception ('Image Text not entered')
                else:
                    return None
                   
                wdlg.close()

                if solution:
                    postData.update({'adcopy_challenge': hugekey,'adcopy_response': solution})


                html = net.http_POST(url, postData).content

                if re.search(r'err\"\>Wrong captcha\<\/div\>', html, re.I):
                    raise Exception ('Wrong Captcha Entered.')

                r = re.search(r'href="(.*?)\"(?=\>Regular\sDownload)', html, re.I)
                if r:
                    return r.group(1)
                
        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 700, self.icon)                
            return None
        
