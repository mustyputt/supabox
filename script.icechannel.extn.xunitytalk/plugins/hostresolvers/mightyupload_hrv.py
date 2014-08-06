'''
    Mightyupload Host resolver
    for Istream ONLY
    29/06/2014

    Jas0npc

    Big thanks to all that has guided me on my XBMC Journey.

    A thank you to all members of the Xunity team.

    (c)2014 Xunity.

    This resolver IS NOT OPEN SOURCE, It is to be used as
    part of Istream ONLY.

    version 0.2
'''
from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common

import xbmcgui
import xbmc
import os
                    


class Mightyupload(HostResolver, CustomSettings):
    implements = [HostResolver, CustomSettings]
    name = "Mightyupload"
    resolverName = name.title()+' (Resolver)'
    match_list = ['mightyupload.com']
    version = '0.6'
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
        
        common.addon.log( self.name.upper() + ' Link: %s' % url )
        common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                      'Resolving', 700, self.icon)

        try:
            html = net.http_GET(url).content
            net.save_cookies(self.cookie_file)
            net.set_cookies(self.cookie_file)

            r=re.search(r'\<b\>File Not Found\<\/b\>',html,re.I)
            if r:
                raise Exception ('File Not Found Or Removed')

            postData = {}

            r=re.search(r'\<b\>File Not Found\<\/b\>',html,re.I)
            if r:
                raise Exception ('File Not Found Or Removed')
                

            r = re.findall(r'idden\"\sname=\"(.*?)\"\svalue=\"?(.*?)\"',html,re.I)
            if r:
                for key,value in r:
                    postData.update({str(key):str(value)})
                    
                solvemedia=re.search(r'challenge\.noscript\?k\=(.*?)\"',html,re.I).group(1)

                html = net.http_GET('http://api.solvemedia.com/papi/challenge.noscript?k=%s'%solvemedia).content
                hugekey=re.search('id="adcopy_challenge" value="(.+?)">', html).group(1)
                open(self.puzzle_img, 'wb').write(net.http_GET("http://api.solvemedia.com%s" % re.search('<img src="(.+?)"', html).group(1)).content)

                img = xbmcgui.ControlImage(450,15,400,130, self.puzzle_img)
                wdlg = xbmcgui.WindowDialog()
                wdlg.addControl(img)
                wdlg.show()
        
                xbmc.sleep(3000)

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
                    raise Exception ('You must enter text in the image to access video')
                wdlg.close()

                if solution:
                    postData.update({'adcopy_challenge': hugekey,'adcopy_response': solution})

                    headers=({'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                              'Accept-Encoding':'gzip,deflate,sdch','Accept-Language':'en-GB,en-US;q=0.8,en;q=0.6',
                              'Cache-Control':'max-age=0','Connection':'keep-alive','Content-Type':'application/x-www-form-urlencoded',
                              'Host':'mightyupload.com','Origin':'http://mightyupload.com','Referer':str(url),
                              'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'})

                    html = net.http_POST(url,postData,headers).content

                    r= re.search(r'id=\"player_code\"\>\<script type=\'text\/javascript\'\>(eval\(function\(.*?\)\)\))',html,re.I)
                    if r:
                        from entertainment import jsunpack
                        unnpacked = jsunpack.unpack(r.group(1))

                        r = re.search(r'divx\"src\=\"(.*?)\"',unnpacked,re.I)
                        if r:
                            common.addon.log( self.name.upper() + ' Resolved Link: %s' % r.group(1) )
                            return str(r.group(1))
                        if not r:
                            r=re.search(r'param\sname=\"src\"value\=\"(.*?)\"',unnpacked,re.I)
                            if r:
                                common.addon.log( self.name.upper() + ' Resolved Link: %s' % r.group(1))
                                return str(r.group(1))

                        common.addon.log(self.name.upper() + ' Unpacked JS: %s' % unnpacked)
                    


                    if not r:
                        r=re.search(r'file\:\s\'(.*?)\'',html,re.I)
                        if r:
                            common.addon.log( self.name.upper() + ' Resolved Link: %s' % r.group(1))
                            return str(r.group(1))
                        


                    #raise Exception ('Link Not Found In Packed JS')
        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 3000, self.icon)                
            return None
