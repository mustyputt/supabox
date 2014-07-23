import xbmc, xbmcgui, xbmcaddon, xbmcplugin, xbmcvfs
import urllib, urllib2
import re, string
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
import unicodedata
import traceback
import os.path
import sys
import time
import collections

net = Net()
pluginId = 'plugin.video.oneclickmoviez'
addon = Addon(pluginId, sys.argv)
settings = xbmcaddon.Addon(id=pluginId)
language = settings.getLocalizedString

Base_Url = "http://www.oneclickmoviez.ag/"
#Movie_Urls = collections.OrderedDict()
Movie_Urls = {}
Movie_Urls[1] = {'title': 'Featured Movies', 'mode': 'GetMovieTitles', 'url': Base_Url + "featuredmovies/date/1"}
Movie_Urls[2] = {'title': 'Movies', 'mode': 'GetMovieTitles', 'url': Base_Url + "movies/date/2"}
Movie_Urls[3] = {'title': 'Genres', 'mode': 'GetMovieGenres', 'url': Base_Url + "movies"}
Movie_Urls[4] = {'title': 'Search', 'mode': 'GetMovieSearch', 'url': Base_Url + "index.php?menu=search&query="}

TVShow_Urls = {}
TVShow_Urls[1] = {'title': 'TV Shows', 'mode': 'GetTVShowTitles', 'url': Base_Url + "tv-shows/date/1"}
TVShow_Urls[2] = {'title': 'Genres', 'mode': 'GetTVShowGenres', 'url': Base_Url + "tv-shows"}
TVShow_Urls[3] = {'title': 'Search', 'mode': 'GetTVShowSearch', 'url': Base_Url + "index.php?menu=search&query="}

language = settings.getLocalizedString

import HTMLParser
html_parser = HTMLParser.HTMLParser()

##### Queries ##########
mode = addon.queries['mode']
url = addon.queries.get('url', None)
regex = addon.queries.get('regex', None)
title = addon.queries.get('title', None)

# Ensure variable is defined
try:
    pDialog 
except NameError:
    pDialog = None

try:
    pFileName 
except NameError:
    pFileName = None

print 'Mode: %s, Url: %s' % (mode,url)

# database params
#try:
    #from sqlite3 import dbapi2 as orm
    #addon.log('Loading sqlite3 as DB engine')
#except:
    #from pysqlite2 import dbapi2 as orm
    #addon.log('pysqlite2 as DB engine')

#translated = xbmc.translatePath("special://database")
#DB_DIR = os.path.join(translated, 'online.oneclickmoviez.db')

def MainMenu():  #homescreen
    print 'oneclickmoviez home menu'
    addon.add_directory({'mode': 'SubMenu', 'url': 'Movies'}, {'title':  'Movies'})
    addon.add_directory({'mode': 'SubMenu', 'url': 'TVShows'}, {'title':  'TV Shows'})
    addon.add_directory({'mode': 'AddonSettings'}, {'title':  'Addon Settings'})
    addon.add_directory({'mode': 'ResolverSettings'}, {'title':  'Resolver Settings'})
    addon.add_directory({'mode': 'Help'}, {'title':  'Help'})
    addon.end_of_directory()

def SubMenu(url):  
    print 'oneclickmovies menu'
    urlDict = {};
    if url == 'Movies':
        urlDict = Movie_Urls
    elif url == 'TVShows':
        urlDict = TVShow_Urls

    for index, meta in urlDict.iteritems():
        addon.add_directory({'mode': meta['mode'], 'url': meta['url'], 'baseUrl': Base_Url}, {'title': meta['title']})
    addon.end_of_directory()

def GetTitles(url,movies): # Get Movie Titles
    print 'oneclickmoviez get Movie Titles Menu'
    print 'url: ' + str(url)
    html = net.http_GET(url).content
    #nextUrl = re.compile('<li><a href="(.+?)">&raquo;</a></li>').findall(html)
    #nextUrl = re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(html)
    try:
        html = html[re.search('<ul class="span-24" id="portfolio">', html).end():]
    except:
        pass
    match = re.compile('<img class="img-preview spec-border"  src="http://www.oneclickmoviez.ag/templates/svarog/timthumb.php\?src=(.+?)&amp;.+?" alt=" ".+?<a class="link" href="(.+?)" title="(.+?)">',re.DOTALL).findall(html)
    if not match:
        match = re.compile('<img class="img-preview spec-border show-thumbnail"  src="http://www.oneclickmoviez.ag/templates/svarog/timthumb.php\?src=(.+?)&amp;.+?" alt=" ".+?<a class="link" href="(.+?)" title="(.+?)">',re.DOTALL).findall(html)
    if not match:
        addon.end_of_directory()
        return
    for img, link, name in match:
        if movies and not IsMovieUrl(link):
            continue
        elif not movies and IsMovieUrl(link):
            continue
        name = UrlDequote(name)
        print '**************************************'
        print 'Img:'  + img
        print 'Link:' + link
        print 'Name:' + name
        print '**************************************'
        link = UrlQuote(link)
        if movies:
            addon.add_directory({'mode': 'GetLinks', 'url': link, 'title': UrlQuote(name)}, 
                                {'title': name}, None, False, img)
        else:
            addon.add_directory({'mode': 'GetTVShowEpisodes', 'url': link, 'title': UrlQuote(name)}, 
                                {'title': name}, None, False, img)
    #if len(nextUrl) > 0:
        #if nextUrl[len(nextUrl)-1][1] == "&raquo;":
            #nextUrl = nextUrl[len(nextUrl)-1][0] 
            #print 'nextUrl: ' + str(nextUrl)
            #if movies:
                #addon.add_directory({'mode': 'GetMovieTitles', 'url': nextUrl}, {'title':  'Next Page >>'})
            #else:
                #addon.add_directory({'mode': 'GetTVShowTitles', 'url': nextUrl}, {'title':  'Next Page >>'})

    # temporary solution for next url
    tmp = re.compile('(.+?)/date/([0-9]+)').findall(url)
    if len(tmp)>0:
        nextUrl = '%s/date/%d' % (tmp[0][0], (int(tmp[0][1])+1))
        if movies:
            addon.add_directory({'mode': 'GetMovieTitles', 'url': nextUrl}, {'title':  'Next Page >>'})
        else:
            addon.add_directory({'mode': 'GetTVShowTitles', 'url': nextUrl}, {'title':  'Next Page >>'})

    addon.end_of_directory()

def GetTVShowEpisodes(url): # Get Movie Titles
    print 'oneclickmoviez get Movie Titles Menu'
    print 'url: ' + str(url)
    html = net.http_GET(url).content
    try:
        html = html[re.search('<ul class="span-24" id="portfolio">', html).end():]
    except:
        pass
    match = re.compile('<img class="img-preview spec-border"  src="http://www.oneclickmoviez.ag/templates/svarog/timthumb.php\?src=(.+?)&amp;.+?" alt=" ".+?<a class="link" href="(.+?)" title="(.+?)">',re.DOTALL).findall(html)
    if not match:
        match = re.compile('<img class="img-preview spec-border show-thumbnail"  src="http://www.oneclickmoviez.ag/templates/svarog/timthumb.php\?src=(.+?)&amp;.+?" alt=" ".+?<a class="link" href="(.+?)" title="(.+?)">',re.DOTALL).findall(html)

    for img, link, name in match:
        name = UrlDequote(name)
        print '**************************************'
        print 'Img:'  + img
        print 'Link:' + link
        print 'Name:' + name
        print '**************************************'
        link = UrlQuote(link)
        addon.add_directory({'mode': 'GetLinks', 'url': link, 'title': UrlQuote(name)}, 
                            {'title': name}, None, False, img)
    addon.end_of_directory()

def IsMovieUrl(url):
    print 'IsMovieUrl: ' + url
    ret = True
    tmp = re.compile('//(.+?)/(.+?)/').findall(url)
    if len(tmp) > 0 :
        if len(tmp[0]) > 1 :
            ret = tmp[0][1] == "movie"
    return ret

def GetGenres(url,movies): # Get Genres
    print 'oneclickmoviez get Genres'
    print 'url: ' + str(url)
    html = net.http_GET(url).content
    #html = html[re.search('<li class="dropdown boot-active"><a href="%s" class="dropdown-toggle"><b class="caret"></b>' % url,html).end():]
    #html = html[:re.search('</ul>',html).start()]
    #match = re.compile('<li><a href="(.+?)">(.+?)</a></li>',re.DOTALL).findall(html)
    if movies:
        match = re.compile('<li><a href="(%smovie-tags/.+?)">(.+?)</a></li>'% Base_Url,re.DOTALL).findall(html)
    else:
        match = re.compile('<li><a href="(%stv-tags/.+?)">(.+?)</a></li>'% Base_Url,re.DOTALL).findall(html)
    for link, name in match:
        link = UrlQuote('%s/%s' % (link,'/date/1'))
        if movies:
            addon.add_directory({'mode': 'GetMovieTitles', 'url': link}, {'title': name})
        else:
            addon.add_directory({'mode': 'GetTVShowTitles', 'url': link}, {'title': name})
    addon.end_of_directory()

def GetSearch(url, movies): # Get Genres
    print 'oneclickmoviez get Search'
    print 'url: ' + str(url)
    kb = xbmc.Keyboard('', 'Search OneClickMoviez Videos', False)
    # call the keyboard
    kb.doModal()
    # if user presses enter
    if (kb.isConfirmed()):
        # get text from keyboard
        search = kb.getText()
        # if the search text is not nothing
        if search is not '':
            # encode the search phrase to put in url 
            # (ie replace ' ' with '+' etc)
            # normally you would use: search = urllib.quoteplus(search)
            search = re.sub('  ', '+', search) # this one is just in case the
                                               # user accidently enters two
                                               # spaces
            search = re.sub(' ', '+', search)
            # create the search url
            search_url = url + search
            # call get titles
            GetTitles(search_url,movies)

def GetLinks(url,title,download=False): # Get Movie Links
    url = url.replace('amp;', '')
    print 'In GetLinks %s' % url
    html = net.http_GET(url).content
    match = re.compile('<a\s+href="(.+?)" target="_blank">Open video</a>').findall(html)
    if not match:
        addon.end_of_directory()
        return
    # import url resolver
    import urlresolver
    for link in match:
        link = UrlDequote(link)
        linkTitle = title
        name = GetDomain(link) + ' - ' + linkTitle 
        print 'Video Url: %s ' % link
        print 'Video Title: %s' % name
        print 'Link Title: %s' % linkTitle
        hosted_media = urlresolver.HostedMediaFile(url=link)
        print 'HostedMedia: %s' % str(hosted_media)
        if not hosted_media:
            continue
        link = UrlQuote(link)
        playAction = 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'PlayVideo', 'url': link, 'title': UrlQuote(linkTitle)})
        downloadAction = 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'DownloadVideo', 'url': link, 'title': UrlQuote(linkTitle)})
        contextMenuItems = [('Play Video', playAction),('Download Video', downloadAction)]
        addon.add_item({'mode': 'PlayVideo', 'url': link, 'title': UrlQuote(linkTitle), 'baseUrl': Base_Url}, 
                       {'title': name}, contextMenuItems, False)
    addon.end_of_directory()
            
def PlayVideo(url,title,download=False):
    print 'In PlayVideo' 
    print 'URL: %s' % url
    print 'Title: %s' % title
    # import url resolver
    import urlresolver
    source = urlresolver.HostedMediaFile(url=url, title=title)
    if source:
        streamUrl = source.resolve()
        if streamUrl:
            print 'StreamUrl: %s' % streamUrl
            if not download:
                addon.resolve_url(streamUrl)
            else:
                DownloadVideo(streamUrl, title)

def GetDomain(url):
    tmp = re.compile('//(.+?)/').findall(url)
    domain = 'Unknown'
    if len(tmp) > 0 :
        domain = tmp[0].replace('www.', '')
        return domain

def UrlQuote(value): 
    if isinstance(value, unicode): 
        return urllib.quote(value.encode("utf-8"))
    else: 
        return urllib.quote(value)

def UrlDequote(value):
    if isinstance(value, unicode): 
        value = value.encode("utf-8","ignore")
    urlDecode = html_parser.unescape(urllib.unquote(value))
    if isinstance(urlDecode, unicode): 
        urlDecode = urlDecode.encode("utf-8","ignore")
    return urlDecode.rstrip().lstrip()

def DownloadVideo(url, title):
    fileName = url.split('?')[0].strip()
    extension = os.path.splitext(fileName)[1][1:].strip() 
    #remove  invalid file characters
    title = title.replace("/","")
    title = title + "." + extension
    if settings.getSetting('download_path') == '':
        try:
            downloadPath = xbmcgui.Dialog().browse(3, language(30002),'files', '', False, False, '')
            if downloadPath == '':
                return None
            settings.setSetting(id='download_path', value=downloadPath)
            if not os.path.exists(downloadPath):
                os.mkdir(downloadPath)
        except:
            pass
    filePath = xbmc.makeLegalFilename(os.path.join(settings.getSetting('download_path'), title))
    if os.path.isfile(filePath):
        return None
    global pDialog
    global pFileName
    pFileName = title
    pDialog = xbmcgui.DialogProgress()
    pDialog.create('OneClickMoviez', language(30003), language(30004))
    try:
        print 'DownloadVideoURL:',url
        print 'DownloadVideoFilePath:',filePath
        urllib.urlretrieve(url, filePath, VideoReportHook)
        #urllib.urlretrieve(url, filePath)
        print 'DownloadedVideo'
        pDialog.close()
        return filePath
    except Exception, e:
        print "URLRetrieve Error:",e
        pass
    pDialog.close()
    xbmc.sleep(500)
    if os.path.isfile(filePath):
        try:
            os.remove(filePath)
        except:
            pass
    return None

def VideoReportHook(count, blocksize, totalsize):
    percent = int(float(count * blocksize * 100) / totalsize)
    global pDialog
    global pFileName
    pDialog.update(percent, language(30003), pFileName, language(30004))
    if pDialog.iscanceled():
        raise Exception

# dequote url here
if url:
    url = UrlDequote(url)

if title:
    title = UrlDequote(title)

if mode == 'main': 
    MainMenu()
elif mode == 'SubMenu': 
    SubMenu(url)
elif mode == 'GetMovieTitles': 
    GetTitles(url,True)
elif mode == 'GetTVShowTitles': 
    GetTitles(url,False)
elif mode == 'GetTVShowEpisodes': 
    GetTVShowEpisodes(url)
elif mode == 'GetLinks':
    GetLinks(url,title)
elif mode == 'PlayVideo': 
    PlayVideo(url,title)
elif mode == 'DownloadVideo': 
    PlayVideo(url,title,True)
elif mode == 'GetMovieGenres': 
    GetGenres(url,True)
elif mode == 'GetTVShowGenres': 
    GetGenres(url,False)
elif mode == 'GetMovieSearch': 
    GetSearch(url,True)
elif mode == 'GetTVShowSearch': 
    GetSearch(url,False)
elif mode == 'ResolverSettings':
    import urlresolver
    urlresolver.display_settings()
elif mode == 'AddonSettings':
    addon.show_settings()
elif mode == 'Help':
    import helpbox
    helpbox.HelpBox()

