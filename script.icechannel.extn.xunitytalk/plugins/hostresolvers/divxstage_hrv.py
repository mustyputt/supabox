'''
    DivxStage Host resolver
    for Istream ONLY
    15/03/2014

    Jas0npc, the-one

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
                    

class Divxstage(HostResolver, CustomSettings):
    implements = [HostResolver, CustomSettings]
    name = "divxstage"
    resolverName = "divxstage ([COLOR blue]i[/COLOR]STREAM Resolver)"
    version = "0.1"
    match_list = ['divxstage.eu']
    icon = common.notify_icon
    

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

        try:

            headers = {}
            headers.update({'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'Accept-Encoding':'gzip,deflate,sdch','Accept-Language':'en-GB,en-US;q=0.8,en;q=0.6',
                            'Connection':'keep-alive','Host':'www.divxstage.eu',
                            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36'})

            html = net.http_GET(url, headers=headers).content
            cid = re.search(r'flashvars\.cid\=\"(.*?)\"', html, re.I)
            if cid:
                cid = cid.group(1)
                key = re.search(r'flashvars\.filekey\=\"(.*?)\"', html, re.I).group(1)
                fileId = re.search(r'flashvars\.file\=\"(.*?)\"', html, re.I).group(1)
                cid2 = re.search(r'flashvars\.cid2\=\"(.*?)\"', html, re.I)
                if cid2:
                    cid2 = cid2.group(1)
                    url = 'http://www.divxstage.eu/api/player.api.php?key=%s&cid2=%s&cid=%s'%(key,cid2,cid)
                    url +='&pass=undefined&user=undefined&numOfErrors=0&cid3=undefined&file=%s'%fileId
                if not cid2:
                    url = 'http://www.divxstage.eu/api/player.api.php?key=%s&pass=undefined&'%key
                    url +='cid=%s&file=%s&user=undefined&cid3=undefined&numOfErrors=0&cid2=undefined'%(cid,fileId)
            
                html = net.http_GET(url, headers=headers).content
                url = re.search(r'url=(.*?)\&', html)
                if url:
                    return url.group(1)

            raise Exception ('Unable To Resolve')
            
        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 3000, self.icon)                
            return None
