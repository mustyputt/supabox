'''
    Xvidstage Host resolver
    for Istream ONLY
    24/07/2014

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
                    


class Xvidstage(HostResolver, CustomSettings):
    implements = [HostResolver, CustomSettings]
    name = "Xvidstage"
    resolverName = name.title()+' (Resolver)'
    match_list = ['xvidstage.com']
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
        
        common.addon.log( self.name.upper() + ' Link: %s' % url )
        common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                      'Resolving', 700, self.icon)

        try:
            html = net.http_GET(url).content
            net.save_cookies(self.cookie_file)
            net.set_cookies(self.cookie_file)

            postdata = {}

            for pd in re.finditer(r'dden\"\sname=\"(id|fname)\"\svalue=\"?(.*?)\"',html,re.I):
                postdata[str(pd.group(1))]=str(pd.group(2))
            postdata['op']='download1'
            postdata['usr_login']=''
            postdata['method_free']='Continue to video / Continue to Free Download'

            html = net.http_POST(url,postdata).content

            captcha = {}
            code = ''

            r = re.findall(r'padding-left:(\d+)px;padding-top:\d+px\;\'\>(.*?)\<\/span\>',html)
            from entertainment import htmlcleaner

            for key, value in r:
                value2 = htmlcleaner.unescape(value)
                captcha.update({int(key): str(value2)})
            for key in sorted(captcha.iterkeys()):
                code = code+captcha[key]

            common.addon.log( self.name.upper() + ' Captcha Code: %s' % value )
            common.addon.log( self.name.upper() + ' Captcha Code: %s' % code )
        

            secs = re.search(r'down_str\"\>.*?\<span\sid=\".*?\"\>(\d+)\<\/sp',html,re.I)
            if secs:
                common.addon.show_countdown(int(str(secs.group(1))), title=self.name.title(), text='please wait')
            
                rand = re.search(r'den\"\sname=\"rand\"\svalue=\"(.*?)\"',html,re.I)
                del postdata['usr_login']
                del postdata['fname']
                postdata['op']='download2'
                postdata['referer']=str(url)
                postdata['rand']=str(rand.group(1))
                postdata['method_premium']=''
                postdata['down_direct']='1'
                postdata['code']=code

                html = net.http_POST(url,postdata).content


                r = re.search(r'\"\>(http\:\/\/\d+\.\d+\.\d+\.\d+\:\d+\/.*?)\<\/a\>',html,re.I)
                if r:
                    common.addon.log(self.name.upper() + ' Resolved Link: %s' % str(r.group(1)))
                    return str(r.group(1))
            raise Exception ('Not Found')
        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 3000, self.icon)                
            return None
