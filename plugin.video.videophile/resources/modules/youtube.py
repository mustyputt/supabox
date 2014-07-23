#Youtube documentary module by o9r1sh
import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,main,urlresolver,xbmc,os

artwork = main.artwork
base_url = 'http://www.youtube.com'
settings = main.settings

def INDEX(url):
        next_page = ''
        inc = 0
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        np=re.compile('<a href="(.+?)" class="yt-uix-button  yt-uix-pager-button yt-uix-sessionlink yt-uix-button-default yt-uix-button-size-default" data-sessionlink="ei=.+?" data-page=".+?"><span class="yt-uix-button-content">Next \xc2\xbb </span></a>').findall(link)
        if len(np) > 0:
                next_page = base_url + np[0]
                if settings.getSetting('nextpagetop') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'youtubeIndex',artwork + '/main/next.png')
        match=re.compile('data-context-item-title="(.+?)"').findall(link)
        times=re.compile('data-context-item-time="(.+?)"').findall(link)
        ids=re.compile('data-context-item-id="(.+?)"').findall(link)
        thumbs=re.compile('<img alt=".+?" src="(.+?)" width=".+?" >').findall(link)
        thumb = ''
        for name in match:
                try:
                        name = match[inc]
                except:
                        name = ''
                
                try:
                        vid = ids[inc]
                except:
                        vid = ''
                #try:
                        #thumb = 'http:' + thumbs[inc]
                        #thumb = thumb[2:]
                #except:
                        #thumb = ''

                url = base_url + '/watch?v=' + vid
                if name != '__title__':
                        try:
                                main.addDir(name,url,'resolve',thumb)
                        except:
                                continue
                
                inc += 1
        if len(np) > 0:
                next_page = base_url + np[0]
                if settings.getSetting('nextpagetop') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'youtubeIndex',artwork + '/main/next.png')



