'''
    animeultimahost Host resolver
    for Istream ONLY
    26/03/2014

    Jas0npc, Coolwave, The-One

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
                    


class animeultimahost(HostResolver):
    implements = [HostResolver]
    name = "animeultimahost"
    match_list = ['animeultima.tv']
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

        net = Net()

        try:

            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                          'Resolving', 700, self.icon)
        
            new_url = url.upper()
            if 'MP4UPLOAD' in new_url:
                try:
                    #url = 'http://www.animeultima.tv'+url
                    content = net.http_GET(url).content
                    mp4upload=re.compile('<iframe title="MP4Upload" type="text/html" frameborder="0" scrolling="no" width=".+?" height=".+?" src="(.+?)">').findall(content)[0]
                    content2 = net.http_GET(mp4upload).content
                    mp4=re.compile("file: '(.+?)',").findall(content2)[0]
                    url = net.http_GET(mp4, auto_read_response=False).get_url()
                except:pass

            if 'NOVAMOV' in new_url:
                try:
                    #url = 'http://www.animeultima.tv'+url
                    content = net.http_GET(url).content
                    nova="http://www.novamov.com/video/%s"%re.compile('<div class="player-embed" id="pembed".+?iframe src="http://embed.+?novamov.+?com/embed.+?v=(.+?)&.+?" frameborder="0"').findall(content)[0]
                    content2 = net.http_GET(nova).content
                    key=re.compile('flashvars.filekey="(.+?)"').findall(str(content2))[0].replace('.','%2e').replace('-','%2d')
                    content3 = net.http_GET('http://www.novamov.com/api/player.api.php?pass=undefined&codes=1&user=undefined&file=%s&key=%s'%(nova.replace('http://www.novamov.com/video/',''),key)).content
                    vid=re.compile('url=(.+?)&title').findall(content3)[0]
                    url = net.http_GET(vid, auto_read_response=False).get_url()
                except:pass

            if 'VIDEOWEED' in new_url:
                try:
                    #url = 'http://www.animeultima.tv'+url
                    content = net.http_GET(url).content
                    videoweed="http://www.videoweed.es/file/%s"%re.compile('<div class="player-embed" id="pembed".+?iframe src="http://embed.+?videoweed.+?com/embed.+?v=(.+?)&.+?" frameborder="0"').findall(net().http_GET(url).content)[0]
                    content2 = net.http_GET(videoweed).content
                    key=re.compile('flashvars.filekey="(.+?)"').findall(str(content2))[0].replace('.','%2e').replace('-','%2d')
                    content3 = net.http_GET('http://www.videoweed.es/api/player.api.php?pass=undefined&codes=1&user=undefined&file=%s&key=%s'%(videoweed.replace('http://www.videoweed.es/file/',''),key)).content
                    vid=re.compile('url=(.+?)&title').findall(content3)[0]
                    url = net.http_GET(vid, auto_read_response=False).get_url()
                except:pass

            if 'DAILYMOTION' in new_url:
                try:
                    import urllib
                    #url = 'http://www.animeultima.tv'+url
                    content = net.http_GET(url).content
                    daily=re.compile('<div class="player-embed" id="pembed"><embed src="(.+?)" type="application/x-shockwave-flash"').findall(content)[0]
                    #redirect = urllib.unquote(net.http_GET(net.http_GET(daily).get_url().replace('swf/','')).content)
                    #dail = urllib.unquote(re.compile('"video_url":"(.+?)"',re.DOTALL).findall(redirect)[0])
                    url = net.http_GET(daily, auto_read_response=False).get_url()
                except:pass

            if 'YOURUPLOAD' in new_url:
                try:
                    #url = 'http://www.animeultima.tv'+url
                    content = net.http_GET(url).content
                    yu=re.compile('<iframe title="YourUpload" type="text/html" frameborder="0" scrolling="no" width="650" height="370" src="(.+?)">').findall(content)[0]
                    data2 = net.http_GET(yu).content
                    yupload=re.compile('var video =\s*{file: "(.+?)"').findall(data2)[0]
                    url = net.http_GET(yupload, auto_read_response=False).get_url()
                except:pass

            if 'UPLOADC' in new_url:
                try:
                    #url = 'http://www.animeultima.tv'+url
                    content = net.http_GET(url).content
                    uploadc=re.compile('<iframe src="(.+?)" frameborder="0"',re.DOTALL).findall(content)[0]
                    content2 = net.http_GET(uploadc).content
                    c = re.compile("'file','(.+?)'",re.DOTALL).findall(content2)[0]
                    url = net.http_GET(c, auto_read_response=False).get_url()
                except:pass

            if 'VIDBOX' in new_url: #VIDBOX IS NOT WORKING
                try:            
                    #url = 'http://www.animeultima.tv'+url
                    content = net.http_GET(url).content
                    box=re.compile('<iframe title="VidBox" type="text/html" frameborder="0" scrolling="no" width="650" height="370" src="(.+?)"').findall(content)[0]
                    content2 = net.http_GET(box).content
                    vidb=re.compile("url: '(.+?)'").findall(content2)[0]
                    url = net.http_GET(vidb, auto_read_response=False).get_url()
                except:pass

            if 'VEEVR' in new_url:
                try:
                    #url = 'http://www.animeultima.tv'+url
                    content = net.http_GET(url).content
                    veevr=re.compile('<div class="player-embed" id="pembed"><iframe src="(.+?)"').findall(content)[0]
                    url = net.http_GET(veevr, auto_read_response=False).get_url()
                except:pass

            return url

        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 700, self.icon)                
            return None

        
