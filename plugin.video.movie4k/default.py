# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Movie4k
# Version 1.0.2
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------

import os
import sys
import plugintools
import xbmcaddon
import datetime
import urlparse
import urllib2

THUMBNAIL_PATH = os.path.join( plugintools.get_runtime_path() , "resources" , "img" )
FANART = os.path.join( plugintools.get_runtime_path() , "fanart.jpg" )
plugintools.module_log_enabled = (plugintools.get_setting("debug")=="true")
plugintools.http_debug_log_enabled = (plugintools.get_setting("debug")=="true")

HOSTERS_ALLOWED = ["flashx","promptfi","filenuk","nosvide","divxsta","shares","mighty","putlock","nowvid","uploadc","zala","vidho","novamo","streamclo","videowee","socksha","primesha","played","vidbux","vidxden","clicktov","stagevu","vidstream","movreel","hugefiles","180upload","megarelease","lemuploads","epicshare","2shared","youtube","vimeo","movpod","gorillavid","daclips"]

if plugintools.get_setting("use_proxy")=="true":
    MAIN_URL = "http://movie4kproxy.com/"
    SITE_DOMAIN = "movie4kproxy.com"
else:
    MAIN_URL = "http://www.movie4k.to/"
    SITE_DOMAIN = "www.movie4k.to"

# Entry point
def run():
    plugintools.log("movie4k.run")
    
    # Get params
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    
    plugintools.close_item_list()

# Main menu
def main_list(params):
    plugintools.log("movie4k.main_list "+repr(params))

    plugintools.set_view(plugintools.THUMBNAIL)

    plugintools.add_item( action="movies",    title="Movies" , thumbnail = os.path.join(THUMBNAIL_PATH,"movies.png") , fanart=FANART , folder=True )
    plugintools.add_item( action="tvshows",   title="TV Shows" , thumbnail = os.path.join(THUMBNAIL_PATH,"tvshows.png") , fanart=FANART , folder=True )
    if plugintools.get_setting("show_adult")=="true":
        plugintools.add_item( action="xxxmovies", title="XXX Movies" , thumbnail = os.path.join(THUMBNAIL_PATH,"xxx.png") , fanart=FANART , folder=True )
    plugintools.add_item( action="search",    title="Search" , thumbnail = os.path.join(THUMBNAIL_PATH,"search.png") , fanart=FANART , folder=True )
    plugintools.add_item( action="settings",  title="Preferences" , thumbnail = os.path.join(THUMBNAIL_PATH,"settings.png") , fanart=FANART , folder=False )

# Settings dialog
def settings(params):
    plugintools.log("movie4k.settings "+repr(params))

    plugintools.open_settings_dialog()

    if plugintools.get_setting("force_advancedsettings")=="true":
        # advancedsettings.xml path
        import xbmc,xbmcgui,os
        advancedsettings = xbmc.translatePath("special://userdata/advancedsettings.xml")

        if not os.path.exists(advancedsettings):
            # copy advancedsettings.xml from resources to userdata
            fichero = open( os.path.join(plugintools.get_runtime_path(),"resources","advancedsettings.xml") )
            text = fichero.read()
            fichero.close()
            
            fichero = open(advancedsettings,"w")
            fichero.write(text)
            fichero.close()

            plugintools.message("movie4k", "A new file userdata/advancedsettings.xml","has been created for optimal streaming")

# Search
def search(params):
    plugintools.log("movie4k.search "+repr(params))
    text = plugintools.keyboard_input(title="Input search terms")

    url = MAIN_URL+"movies.php?list=search"
    post = "search="+text.replace(" ","+")

    body,response_headers = read_body_and_headers(url, post=post)
    pattern  = '<TR id="coverPreview[^<]+'
    pattern += '<TD width="550" id="tdmovies"[^<]+'
    pattern += '<a href="([^"]+)">([^<]+)</a>'
    matches = plugintools.find_multiple_matches(body,pattern)

    for scrapedurl, scrapedtitle in matches:
        
        url = urlparse.urljoin(url,scrapedurl)
        title = scrapedtitle.strip()
        thumbnail = ""
        plot = ""
        plugintools.log("movie4k.search title="+title+", url="+url+", thumbnail="+thumbnail)

        if "watch-tvshow" in url:
            url = MAIN_URL+"tvshows-season-"+plugintools.find_single_match(url,MAIN_URL+"([A-Za-z0-9\-]+)-watch-tvshow-\d+.html")+".html"
            plugintools.add_item( action="tvshow_seasons", title=title, url=url, thumbnail=thumbnail , plot=plot, fanart=thumbnail , folder=True )
        else:
            plugintools.add_item( action="single_movie", title=title, url=url, thumbnail=thumbnail , plot=plot, fanart=thumbnail , folder=True )

# Movies
def movies(params):
    plugintools.log("movie4k.movies "+repr(params))

    plugintools.set_view(plugintools.THUMBNAIL)

    plugintools.add_item( action="movies_cinema",    title="Cinema movies" , thumbnail = os.path.join(THUMBNAIL_PATH,"movies.png") , fanart=FANART, url=MAIN_URL+"index.php", folder=True )
    plugintools.add_item( action="movies_updates",   title="Latest updates" , thumbnail = os.path.join(THUMBNAIL_PATH,"movies.png") , fanart=FANART, url=MAIN_URL+"movies-updates.html", folder=True )
    plugintools.add_item( action="letters",          title="All movies" , thumbnail = os.path.join(THUMBNAIL_PATH,"movies.png") , fanart=FANART, extra="movies-all", url=MAIN_URL+"movies-all.html", folder=True )
    plugintools.add_item( action="genres",           title="Genres" , thumbnail = os.path.join(THUMBNAIL_PATH,"movies.png") , fanart=FANART, extra="movies-genre", url=MAIN_URL+"genres-movies.html", folder=True )

# TV Shows
def tvshows(params):
    plugintools.log("movie4k.tvshows "+repr(params))

    plugintools.set_view(plugintools.THUMBNAIL)

    plugintools.add_item( action="tvshows_featured",  title="Featured" , thumbnail = os.path.join(THUMBNAIL_PATH,"tvshows.png") , fanart=FANART , folder=True , url=MAIN_URL+'tvshows_featured.php' )
    plugintools.add_item( action="tvshow_episodes",   title="Latest updates" , thumbnail = os.path.join(THUMBNAIL_PATH,"tvshows.png") , fanart=FANART , folder=True , url=MAIN_URL+'tvshows-updates.html' )
    plugintools.add_item( action="letters",           title="All TV shows" , thumbnail = os.path.join(THUMBNAIL_PATH,"tvshows.png") , fanart=FANART , folder=True , extra="tvshows-all", url = MAIN_URL+'tvshows-all.html' )
    plugintools.add_item( action="genres",            title="Genres" , thumbnail = os.path.join(THUMBNAIL_PATH,"tvshows.png") , fanart=FANART , folder=True , extra="tvshows-genre", url = MAIN_URL+'genres-tvshows.html' )

# XXX Movies
def xxxmovies(params):
    plugintools.log("movie4k.xxxmovies "+repr(params))

    plugintools.set_view(plugintools.THUMBNAIL)

    plugintools.add_item( action="xxx_movies_updates", title="Latest updates" , thumbnail = os.path.join(THUMBNAIL_PATH,"xxx.png") , fanart=FANART , folder=True , url=MAIN_URL+'xxx-updates.html' )
    plugintools.add_item( action="letters",            title="All movies" , thumbnail = os.path.join(THUMBNAIL_PATH,"xxx.png") , fanart=FANART , folder=True , extra="xxx-all", url=MAIN_URL+'xxx-all.html' )
    plugintools.add_item( action="genres",             title="Genres" , thumbnail = os.path.join(THUMBNAIL_PATH,"xxx.png") , fanart=FANART , folder=True , extra="xxx-genre", url=MAIN_URL+'genres-xxx.html' )

# Cinema movies
def movies_cinema(params):
    plugintools.log("movie4k.movies_cinema "+repr(params))

    #plugintools.set_view(plugintools.MOVIES)

    body,response_headers = read_body_and_headers(params.get("url"))
    pattern  = '<div style="float.left"[^<]+'
    pattern += '<a href="([^"]+)"><img src="([^"]+)".*?'
    pattern += '<h2[^<]+<a[^<]+<font[^<]+</a[^<]+<img src="([^"]+)".*?'
    pattern += '<div id="info\d+"[^<]+<STRONG>([^<]+)</STRONG><BR>([^<]+)</div>'
    matches = plugintools.find_multiple_matches(body,pattern)

    for scrapedurl, scrapedthumbnail, flag, scrapedtitle, scrapedplot in matches:
        
        url = urlparse.urljoin(params.get("url"),scrapedurl)
        title = scrapedtitle
        if title.strip().endswith(":"):
            title = title.strip()[:-1]
        title=title + get_language_from_flag_img(flag)
        thumbnail = urlparse.urljoin(params.get("url"),scrapedthumbnail)
        plot = scrapedplot
        plugintools.log("movie4k.movies_cinema title="+title+", url="+url+", thumbnail="+thumbnail)

        plugintools.add_item( action="single_movie", title=title, url=url, thumbnail=thumbnail , plot=plot, fanart=thumbnail , folder=True )

    pattern = '<div id="maincontent2"[^<]+<div style="float: left;"><a href="([^"]+)"><img src="([^"]+)" alt="([^"]+)"'
    matches = plugintools.find_multiple_matches(body,pattern)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        
        url = urlparse.urljoin(params.get("url"),scrapedurl)
        title = scrapedtitle
        thumbnail = urlparse.urljoin(params.get("url"),scrapedthumbnail)
        plugintools.log("movie4k.movies_cinema title="+title+", url="+url+", thumbnail="+thumbnail)

        plugintools.add_item( action="single_movie", title=title, url=url, thumbnail=thumbnail , fanart=thumbnail , folder=True )

# Latest updates
def movies_updates(params):
    plugintools.log("movie4k.movies_updates "+repr(params))

    #plugintools.set_view(plugintools.LIST)

    body,response_headers = read_body_and_headers(params.get("url"))

    pattern  = '<TR id="coverPreview[^<]+'
    pattern += '<TD width="550" id="tdmovies"[^<]+'
    pattern += '<a href="([^"]+)">([^<]+)</a[^<]+.*?<img border=0 src="([^"]+)"'
    matches = plugintools.find_multiple_matches(body,pattern)

    for scrapedurl, scrapedtitle, flag in matches:
        
        url = urlparse.urljoin(params.get("url"),scrapedurl)
        title = scrapedtitle.strip()
        if title.strip().endswith(":"):
            title = title.strip()[:-1]
        title=title + get_language_from_flag_img(flag)
        thumbnail = ""
        plot = ""
        plugintools.log("movie4k.movies_updates title="+title+", url="+url+", thumbnail="+thumbnail)

        plugintools.add_item( action="single_movie", title=title, url=url, thumbnail=thumbnail , plot=plot, fanart=thumbnail , folder=True )

# Latest updates
def xxx_movies_updates(params):
    plugintools.log("movie4k.xxx_movies_updates "+repr(params))

    #plugintools.set_view(plugintools.LIST)

    body,response_headers = read_body_and_headers(params.get("url"))

    pattern  = '<div style="float. left.">'
    pattern += '<a href="([^"]+)"><img src="([^"]+)" alt="([^"]+)"'
    matches = plugintools.find_multiple_matches(body,pattern)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        
        url = urlparse.urljoin(params.get("url"),scrapedurl)
        title = scrapedtitle.strip()
        thumbnail = urlparse.urljoin(params.get("url"),scrapedthumbnail)
        plot = ""
        plugintools.log("movie4k.xxx_movies_updates title="+title+", url="+url+", thumbnail="+thumbnail)

        plugintools.add_item( action="single_movie", title=title, url=url, thumbnail=thumbnail , plot=plot, fanart=thumbnail , folder=True )

# All movies by letter
def letters(params):
    plugintools.log("movie4k.letters "+repr(params))

    #plugintools.set_view(plugintools.LIST)

    body,response_headers = read_body_and_headers(params.get("url"))

    #<div id="boxgrey"><a href=MAIN_URL+"/tvshows-all-G.html">
    #<div id="boxgrey"><a href="./xxx-all-N.html">N</a> 
    #<div id="boxgrey"><a href="./movies-all-O.html">O</a>
    pattern  = '<div id="boxgrey"><a href="(./'+params.get("extra")+'[^"]+)">([^<]+)</a>'
    matches = plugintools.find_multiple_matches(body,pattern)

    plugintools.add_item( action="movies_all", title="#", thumbnail="" , plot="", fanart="", url=MAIN_URL+""+params.get("extra")+"-1.html", folder=True )

    for scrapedurl, scrapedtitle in matches:
        url = urlparse.urljoin(params.get("url"),scrapedurl)
        title = scrapedtitle.strip()
        thumbnail = ""
        plot = ""
        plugintools.log("movie4k.letters title="+title+", url="+url+", thumbnail="+thumbnail)

        if params.get("extra")=="tvshows-all":
            plugintools.add_item( action="tvshows_all", title=title, url=url, thumbnail=thumbnail , plot=plot, fanart=thumbnail , folder=True )
        else:
            plugintools.add_item( action="movies_all", title=title, url=url, thumbnail=thumbnail , plot=plot, fanart=thumbnail , folder=True )

    #<div id="boxgrey"><a href=MAIN_URL+"/tvshows-all-G.html">
    pattern  = '<div id="boxgrey"><a href="(http\://'+SITE_DOMAIN+'//'+params.get("extra")+'-[^"]+)">([^<]+)</a>'
    matches = plugintools.find_multiple_matches(body,pattern)

    for scrapedurl, scrapedtitle in matches:
        
        url = urlparse.urljoin(params.get("url"),scrapedurl)
        title = scrapedtitle.strip()
        thumbnail = ""
        plot = ""
        plugintools.log("movie4k.letters title="+title+", url="+url+", thumbnail="+thumbnail)

        if params.get("extra")=="tvshows-all":
            plugintools.add_item( action="tvshows_all", title=title, url=url, thumbnail=thumbnail , plot=plot, fanart=thumbnail , folder=True )
        else:
            plugintools.add_item( action="movies_all", title=title, url=url, thumbnail=thumbnail , plot=plot, fanart=thumbnail , folder=True )

# All movies by letter
def movies_all(params):
    plugintools.log("movie4k.movies_all "+repr(params))

    #plugintools.set_view(plugintools.THUMBNAIL)

    body,response_headers = read_body_and_headers(params.get("url"))
    pattern  = '<TR id="(coverPreview\d+)[^<]+'
    pattern += '<TD width="550" id="tdmovies"[^<]+'
    pattern += '<a href="([^"]+)">([^<]+)</a[^<]+.*?<TD align="right" id="tdmovies"[^<]+<img border=0 src="([^\"]+)"'
    matches = plugintools.find_multiple_matches(body,pattern)

    for cover_id, scrapedurl, scrapedtitle, flag in matches:
        
        url = urlparse.urljoin(params.get("url"),scrapedurl)
        title = scrapedtitle.strip()
        if title.strip().endswith(":"):
            title = title.strip()[:-1]
        title=title + get_language_from_flag_img(flag)
        thumbnail = plugintools.find_single_match(body,"\$\(\"\#"+cover_id+"\"\).hover\(function\(e\)[^<]+<p id='coverPreview'><img src='([^']+)'")
        plot = ""
        plugintools.log("movie4k.movies_all title="+title+", url="+url+", thumbnail="+thumbnail)

        plugintools.add_item( action="single_movie", title=title, url=url, thumbnail=thumbnail , plot=plot, fanart=thumbnail , folder=True )

    next_page_url = plugintools.find_single_match(body,'<div id="boxwhite">\d+ </div><div id="boxgrey"><a href="([^"]+)">\d+')
    next_page_number = plugintools.find_single_match(body,'<div id="boxwhite">\d+ </div><div id="boxgrey"><a href="[^"]+">(\d+)')
    if next_page_url!="":
        plugintools.add_item( action="movies_all", title=">> Go to page "+next_page_number, url=urlparse.urljoin(params.get("url"),next_page_url), folder=True )

# Movie genres
def genres(params):
    plugintools.log("movie4k.genres "+repr(params))

    #plugintools.set_view(plugintools.LIST)

    body,response_headers = read_body_and_headers(params.get("url"))

    '''
    <TR>
    <TD id="tdmovies" width="155"><a href="movies-genre-59-Reality-TV.html">Reality-TV</a></TD>
    <TD id="tdmovies" width="50">30</TD>
    </TR>
    '''
    pattern  = '<TR[^<]+'
    pattern += '<TD id="tdmovies" width="\d+"><a href="('+params.get("extra")+'-[^"]+)">([^<]+)</a></TD[^<]+'
    pattern += '<TD id="tdmovies" width="\d+">(\d+)</TD[^<]+'
    pattern += '</TR>'
    matches = plugintools.find_multiple_matches(body,pattern)

    for scrapedurl, scrapedtitle, counter in matches:
        
        url = urlparse.urljoin(params.get("url"),scrapedurl)
        title = scrapedtitle.strip()+" ("+counter+" movies)"
        thumbnail = ""
        plot = ""
        plugintools.log("movie4k.genres title="+title+", url="+url+", thumbnail="+thumbnail)

        if params.get("extra") == "tvshows-genre":
            plugintools.add_item( action="tvshows_all", title=title, url=url, thumbnail=thumbnail , plot=plot, fanart=thumbnail , folder=True )
        else:
            plugintools.add_item( action="movies_all", title=title, url=url, thumbnail=thumbnail , plot=plot, fanart=thumbnail , folder=True )

# Featured tv shows
def tvshows_featured(params):
    plugintools.log("movie4k.tvshows_featured "+repr(params))

    #plugintools.set_view(plugintools.MOVIES)

    body,response_headers = read_body_and_headers(params.get("url"))
    pattern  = '<div style="float.left"[^<]+'
    pattern += '<a href="([^"]+)"><img src="([^"]+)".*?'
    pattern += '<h2[^<]+<a[^<]+<font[^>]+>([^<]+)</a[^<]+<img src="([^"]+)".*?'
    matches = plugintools.find_multiple_matches(body,pattern)

    for scrapedurl, scrapedthumbnail, scrapedtitle, flag in matches:
        
        url = urlparse.urljoin(params.get("url"),scrapedurl)
        url = MAIN_URL+"tvshows-season-"+plugintools.find_single_match(url,MAIN_URL+"([A-Za-z0-9\-]+)-watch-tvshow-\d+.html")+".html"

        title = scrapedtitle
        if title.strip().endswith(":"):
            title = title.strip()[:-1]
        title=title + get_language_from_flag_img(flag)
        thumbnail = urlparse.urljoin(params.get("url"),scrapedthumbnail)
        plot = ""
        plugintools.log("movie4k.tvshows_featured title="+title+", url="+url+", thumbnail="+thumbnail)

        plugintools.add_item( action="tvshow_seasons", title=title, url=url, thumbnail=thumbnail , plot=plot, fanart=thumbnail , folder=True )

# All tv shows by letter
def tvshows_all(params):
    plugintools.log("movie4k.tvshows_all "+repr(params))

    #plugintools.set_view(plugintools.THUMBNAIL)

    '''
    <TR>
    <TD id="tdmovies" width="538"><a href="tvshows-season-Jane-by-Design.html">Jane By Design                                   </a></TD>
    <TD id="tdmovies"><img border=0 src="http://img.movie4k.to/img/us_flag_small.png" width=24 height=14></TD>
    </TR>
    '''

    body,response_headers = read_body_and_headers(params.get("url"))
    pattern  = '<TR[^<]+'
    pattern += '<TD id="tdmovies" width="538"[^<]+'
    pattern += '<a href="([^"]+)">([^<]+)</a.*?<img border=0 src="([^\"]+)"'
    matches = plugintools.find_multiple_matches(body,pattern)

    for scrapedurl, scrapedtitle, flag in matches:
        
        url = urlparse.urljoin(params.get("url"),scrapedurl)
        title = scrapedtitle.strip()
        if title.strip().endswith(":"):
            title = title.strip()[:-1]
        title=title + get_language_from_flag_img(flag)
        thumbnail = ""
        plot = ""
        plugintools.log("movie4k.tvshows_all title="+title+", url="+url+", thumbnail="+thumbnail)

        plugintools.add_item( action="tvshow_seasons", title=title, url=url, thumbnail=thumbnail , plot=plot, fanart=thumbnail , folder=True )

    next_page_url = plugintools.find_single_match(body,'<div id="boxwhite">\d+ </div><div id="boxgrey"><a href="([^"]+)">\d+')
    next_page_number = plugintools.find_single_match(body,'<div id="boxwhite">\d+ </div><div id="boxgrey"><a href="[^"]+">(\d+)')
    if next_page_url!="":
        plugintools.add_item( action="tvshows_all", title=">> Go to page "+next_page_number, url=urlparse.urljoin(params.get("url"),next_page_url), folder=True )

# TV Show seasons
def tvshow_seasons(params):
    plugintools.log("movie4k.tvshow_seasons "+repr(params))

    #plugintools.set_view(plugintools.LIST)

    body,response_headers = read_body_and_headers(params.get("url"))

    '''
    <TR>
    <TD id="tdmovies" width="538"><a href="tvshows-episode-1-Arrow.html">Arrow          , Season: 1                     </a></TD>
    <TD id="tdmovies"><img border=0 src="http://img.movie4k.to/img/us_ger_small.png" width=24 height=14></TD>
    </TR>
    '''
    pattern  = '<TR[^<]+'
    pattern += '<TD id="tdmovies" width="\d+"><a href="([^"]+)">([^<]+)</a></TD[^<]+'
    pattern += '<TD id="tdmovies"><img border=0 src="([^\"]+)"'
    matches = plugintools.find_multiple_matches(body,pattern)

    for scrapedurl, scrapedtitle, flag in matches:
        
        url = urlparse.urljoin(params.get("url"),scrapedurl)
        title = scrapedtitle.strip()
        title=title + get_language_from_flag_img(flag)
        thumbnail = ""
        plot = ""
        plugintools.log("movie4k.tvshow_seasons title="+title+", url="+url+", thumbnail="+thumbnail)

        plugintools.add_item( action="tvshow_episodes", title=title, url=url, thumbnail=thumbnail , plot=plot, fanart=thumbnail , folder=True )

# Latest updates
def tvshow_episodes(params):
    plugintools.log("movie4k.tvshow_episodes "+repr(params))

    #plugintools.set_view(plugintools.LIST)
    '''
    <TR>
    <TD id="tdmovies" width="538"><a href="Arrow-watch-tvshow-3334157.html">Arrow           , Season: 1         , Episode: 22           </a></TD>
    <TD id="tdmovies" width="182">
    <img src="http://img.movie4k.to/img/question.png" width=16> watch on N/A            </TD>
    <TD id="tdmovies" width="25">&nbsp;</TD>
    <TD id="tdmovies" width="175">06/08/2013 09:03 am</TD>
    <TD id="tdmovies"><img border=0 src="http://img.movie4k.to/img/us_flag_small.png" width=24 height=14></TD>
    </TR>
    '''
    body,response_headers = read_body_and_headers(params.get("url"))

    pattern  = '<TR[^<]+'
    pattern += '<TD id="tdmovies" width="\d+"[^<]+'
    pattern += '<a href="([^"]+)">([^<]+)</a></TD[^<]+'
    pattern += '<TD id="tdmovies" width="\d+"[^<]+'
    pattern += '<img[^>]+>([^<]+)</TD[^<]+'
    pattern += '.*?<img border=0 src="([^"]+)"'
    matches = plugintools.find_multiple_matches(body,pattern)

    for scrapedurl, scrapedtitle, mirrorname, flag in matches:
        
        url = urlparse.urljoin(params.get("url"),scrapedurl)
        title = scrapedtitle.strip()
        if title.strip().endswith(":"):
            title = title.strip()[:-1]
        title = title + " ("+mirrorname.strip().replace("watch on ","")+")"
        title=title + get_language_from_flag_img(flag)
        thumbnail = ""
        plot = ""
        plugintools.log("movie4k.tvshow_episodes title="+title+", url="+url+", thumbnail="+thumbnail)

        for hoster in HOSTERS_ALLOWED:
            #plugintools.log("<<<<<"+hoster+">>>>> IN <<<<<<"+title.lower()+">>>>>>")
            if hoster in title.lower():
                plugintools.add_item( action="play", title=title, url=url, thumbnail=thumbnail , plot=plot, fanart=thumbnail , folder=True )

# Show movie links
def single_movie(params):
    plugintools.log("movie4k.single_movie "+repr(params))

    #plugintools.set_view(plugintools.LIST)
    found = False

    body,response_headers = read_body_and_headers(params.get("url"))
    body = body.replace("\\\"","\"")

    '''
    <tr id="tablemoviesindex2">
    <td height="20" width="150">
    <a href="Thor-The-Dark-World-watch-movie-4650640.html">11/16/2013 
    <img border=0 style="vertical-align:top;" src="http://img.movie4k.to/img/divx.gif" alt="Divxstage Thor The Dark World" title="Divxstage Thor The Dark World" width="16"> &nbsp;Divxstage</a>
    </td><td align="right" width="58"><a href="Thor-The-Dark-World-watch-movie-4650640.html">Quality:</a> 
    <img style="vertical-align: top;" src="http://img.movie4k.to/img/smileys/1.gif" alt="Movie quality CAM Mic dubbed" title="Movie quality CAM Mic dubbed"></td></tr>
    '''

    '''
    links[4658139]="<tr id=\"tablemoviesindex2\"><td height=\"20\" width=\"150\"><a href=\"Thor-The-Dark-World-watch-movie-4658139.html\">11/17/2013 <img border=0 style=\"vertical-align:top;\" src=\"http://img.movie4k.to/img/flashPlayer2.gif\" alt=\"Sharesix Thor The Dark World\" title=\"Sharesix Thor The Dark World\" width=\"16\"> &nbsp;Sharesix</a></td><td align=\"right\" width=\"58\"><a href=\"Thor-The-Dark-World-watch-movie-4658139.html\">Quality:</a> <img style=\"vertical-align: top;\" src=\"http://img.movie4k.to/img/smileys/1.gif\" alt=\"Movie quality CAM Mic dubbed\" title=\"Movie quality CAM Mic dubbed\"></td></tr>";
    '''

    pattern  = '<tr id="tablemoviesindex2"[^<]+'
    pattern += '<td height="\d+" width="\d+"[^<]+'
    pattern += '<a href="([^"]+)">([^<]+)'
    pattern += '<img border=0 style="[^"]+" src="([^"]+)"[^>]+>([^<]+)</a[^<]+'
    pattern += '</td><td align="right" width="58"><a[^>]+>Quality.</a[^<]+'
    pattern += '<img style="[^"]+" src="[^"]+" alt="([^"]+)"'
    matches = plugintools.find_multiple_matches(body,pattern)

    for scrapedurl, date_added, server_thumbnail, server_name, quality in matches:
        
        url = urlparse.urljoin(params.get("url"),scrapedurl)
        title = server_name.strip().replace("&nbsp;","")+" ("+quality.replace("Movie quality","").strip()+") (Added "+date_added+")"
        thumbnail = ""
        plot = ""
        plugintools.log("movie4k.single_movie title="+title+", url="+url+", thumbnail="+thumbnail)

        for hoster in HOSTERS_ALLOWED:
            #plugintools.log("<<<<<"+hoster+">>>>> IN <<<<<<"+title.lower()+">>>>>>")
            if hoster in title.lower():
                plugintools.add_item( action="play", title="Video published at "+title, url=url, thumbnail=thumbnail , plot=plot, fanart=thumbnail , folder=True )
                found = True

    '''
    <tr id="tablemoviesindex2" onClick="window.location.href = 'tvshows-3415901-Arrow.html';return false;" style="cursor:hand;cursor:pointer;"><td style="padding-left:5px;height:20px;width:80px;"><a href="tvshows-3415901-Arrow.html">Episode 1</a>&nbsp;</td><td align="left" width="150"><a href="tvshows-3415901-Arrow.html" style="margin-left:18px;"><img border=0 style="vertical-align:top;" src="http://img.movie4k.to/img/divx.gif" alt="Filebox Arrow" title="Filebox Arrow" width="16"> &nbsp;Filebox</a></td></tr>
    '''
    '''
    links[1522783]="
    <tr id=\"tablemoviesindex2\" onClick=\"window.location.href = 'tvshows-1522783-Arrow.html';return false;\" style=\"cursor:hand;cursor:pointer;\">
    <td style=\"padding-left:5px;height:20px;width:80px;\">
    <a href=\"tvshows-1522783-Arrow.html\">Episode 1</a>&nbsp;
    </td>
    <td align=\"left\" width=\"150\">
    <a href=\"tvshows-1522783-Arrow.html\" style=\"margin-left:18px;\">
    <img border=0 style=\"vertical-align:top;\" src=\"http://img.movie4k.to/img/hoster/113.png\" alt=\"Sockshare Arrow\" title=\"Sockshare Arrow\" width=\"16\"> &nbsp;Sockshare</a></td></tr>";
    '''
    pattern  = '<tr id="tablemoviesindex2"[^<]+'
    pattern += '<td[^<]+'
    pattern += '<a href="([^"]+)"[^<]+</a[^<]+'
    pattern += '</td[^<]+'
    pattern += '<td[^<]+'
    pattern += '<a[^<]+<img border=0 style="[^"]+" src="([^"]+)"[^>]+>([^<]+)</a>'
    matches = plugintools.find_multiple_matches(body,pattern)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        
        url = urlparse.urljoin(params.get("url"),scrapedurl)
        title = scrapedtitle.strip().replace("&nbsp;","")
        thumbnail = urlparse.urljoin(params.get("url"),scrapedthumbnail)
        plot = ""
        plugintools.log("movie4k.single_movie title="+title+", url="+url+", thumbnail="+thumbnail)

        for hoster in HOSTERS_ALLOWED:
            #plugintools.log("<<<<<"+hoster+">>>>> IN <<<<<<"+title.lower()+">>>>>>")
            if hoster in title.lower():
                plugintools.add_item( action="play", title="Video published at "+title, url=url, thumbnail=thumbnail , plot=plot, fanart=FANART , folder=True )
                found = True

    if not found:
        play(params)

# Resolve hoster links
def play(params):
    plugintools.log("movie4k.play "+repr(params))

    #plugintools.set_view(plugintools.LIST)

    try:
        body,response_headers = read_body_and_headers(params.get("url"))
        plugintools.log("movie4k.play body="+repr(body))

        url = plugintools.find_single_match(body,'<a target="_blank" href="([^"]+)">')
        plugintools.log("movie4k.play url="+repr(url))

        if url=="":
            url = plugintools.find_single_match(body,'<iframe.*?src="([^"]+)"')

        if url!="":
            if url.startswith("http://www.nowvideo.sx/video/"):
                url = url.replace("http://www.nowvideo.sx/video/","http://embed.nowvideo.eu/embed.php?v=")+"&width=600&height=480"

            from urlresolver.types import HostedMediaFile
            hosted_media_file = HostedMediaFile(url=url)
            plugintools.log("movie4k.play hosted_media_file="+repr(hosted_media_file))

            try:
                media_url = hosted_media_file.resolve()
                plugintools.log("movie4k.play media_url="+repr(media_url))

                if media_url:
                    plugintools.add_item( action="playable", title="Play this video from [B]"+hosted_media_file.get_host()+"[/B] ["+get_filename_from_url(media_url)[-4:]+"]", url=media_url, isPlayable=True, folder=False )
                else:
                    plugintools.add_item( action="play", title="This video is not playable", isPlayable=True, folder=False )
            except:
                plugintools.add_item( action="play", title="This hoster is not working at this moment", isPlayable=True, folder=False )
                plugintools.add_item( action="play", title="Please select other option", isPlayable=True, folder=False )

        else:
            plugintools.add_item( action="play", title="No valid links found", isPlayable=True, folder=False )

    except urllib2.URLError,e:
        plugintools.add_item( action="play", title="Error reading data from movie4k.to, please try again", isPlayable=True, folder=False )
        body = ""

    if params.get("extra")=="noalternatives":
        plugintools.log("movie4k.play noalternatives")
    else:
        #<OPTION value="Arrow-watch-tvshow-1522775.html" style="Background: URL('http://img.movie4k.to/img/hoster/186.png') no-repeat 3px center transparent; Text-Indent: 25px">Nowvideo (2/7)</OPTION>
        bloque = plugintools.find_single_match(body,'<SELECT name="hosterlist(.*?)</SELECT')
        pattern  = '<OPTION value="([^"]+)"[^>]+>([^<]+)</OPTION>'
        matches = plugintools.find_multiple_matches(bloque,pattern)

        for scrapedurl, scrapedtitle in matches:
            
            url = urlparse.urljoin(params.get("url"),scrapedurl)
            title = scrapedtitle.strip()
            thumbnail = ""
            plot = ""
            plugintools.log("movie4k.play title="+title+", url="+url+", thumbnail="+thumbnail)

            for hoster in HOSTERS_ALLOWED:
                #plugintools.log("<<<<<"+hoster+">>>>> IN <<<<<<"+title.lower()+">>>>>>")
                if hoster in title.lower():
                    plugintools.add_item( action="play", title="Alternative link found at "+title, url=url, thumbnail=thumbnail , plot=plot, fanart=FANART , folder=True, extra="noalternatives" )

# Play hoster link
def playable(params):
    plugintools.play_resolved_url( params.get("url") )    

def get_filename_from_url(url):
    
    parsed_url = urlparse.urlparse(url)
    try:
        filename = parsed_url.path
    except:
        if len(parsed_url)>=4:
            filename = parsed_url[2]
        else:
            filename = ""

    return filename

def get_language_from_flag_img(url):
    if "us_flag" in url:
        return " (English)"
    elif "us_ger" in url:
        return " (German)"
    elif "flag_spain" in url:
        return " (Spanish)"
    elif "flag_greece" in url:
        return " (Greek)"
    elif "flag_turkey" in url:
        return " (Turk)"
    elif "flag_russia" in url:
        return " (Russian)"
    elif "flag_japan" in url:
        return " (Japanese)"
    elif "flag_france" in url:
        return " (French)"

    return ""

def read_body_and_headers(url, post=None, headers=[], follow_redirects=False, timeout=None):
    plugintools.log("movie4k.read_body_and_headers url="+url)

    expiration = datetime.datetime.now() + datetime.timedelta(days=365)
    expiration_gmt = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")

    if plugintools.get_setting("only_english")=="true":
        plugintools.log("movie4k.read_body_and_headers only english")
        headers.append(["Cookie","onlylanguage=en; expires="+expiration_gmt+"; xxx2=ok; expires="+expiration_gmt+";"])
    else:
        headers.append(["Cookie","xxx2=ok; expires="+expiration_gmt+";"])

    try:
        body,response_headers = plugintools.read_body_and_headers(url,post,headers,follow_redirects,timeout)
    except:
        xbmc.sleep(3)
        body,response_headers = plugintools.read_body_and_headers(url,post,headers,follow_redirects,timeout)

    return body,response_headers

run()