'''
    Cartoon World (cartoon-world.tv) XBMC Plugin

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.		
'''

import os
import string
import sys
import re
import xbmc, xbmcaddon, xbmcplugin, xbmcgui

from t0mm0.common.addon import Addon
from t0mm0.common.net import Net

BASEURL = 'http://www.cartoon-world.tv/'

addon_id = 'plugin.video.cartoonworld'
addon = Addon(addon_id, sys.argv)

net = Net()

mode = addon.queries['mode']
url = addon.queries.get('url', None)
title = addon.queries.get('title', None)
img = addon.queries.get('img', None)
section = addon.queries.get('section', None)
page = addon.queries.get('page', None)


def escape(text):
        try:            
            rep = {" ": "%20"                  
                   }
            for s, r in rep.items():
                text = text.replace(s, r)

        except TypeError:
            pass

        return text
    
def unescape(text):
        try:            
            rep = {"&nbsp;": " ",
                   "\n": "",
                   "\t": "",                   
                   }
            for s, r in rep.items():
                text = text.replace(s, r)
				
            # remove html comments
            text = re.sub(r"<!--.+?-->", "", text)    
				
        except TypeError:
            pass

        return text
		

def MainMenu():  #home-page
    addon.add_directory({'mode' : 'latest'}, {'title':  'Latest Episodes'})
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
def GetLatest():
    url_content = net.http_GET(BASEURL).content
    
    les = re.search(r"(?s)<h4>Latest Episodes</h4>(.+?)<h4", url_content).group(1)
    les = addon.unescape(les)
    les = unescape(les)
    from universal import _common
    les = _common.str_conv(les)
    
    for le in re.finditer(r"<li.+?class=\"(.+?)\".+?<a.+?href=\"(.+?)\".+?<img.+? src=\"(.+?)\".+?title\">(.+?)</div>", les):
        le_typ = le.group(1)
        le_url = le.group(2)
        le_img = le.group(3)
        le_ttl = le.group(4)
        
        addon.add_directory({'mode' : 'links', 'title' : le_ttl, 'img' : le_img, 'url' : le_url}, {'title':  le_ttl}, img= le_img)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks(url, title, img):
    url_content = net.http_GET(url).content
    url_content = addon.unescape(url_content)
    url_content = unescape(url_content)
    
    if re.search(r"<div id=\"vid", url_content):
        for vid in re.finditer(r"<div id=\"vid([0-9]{1,2})\"(.+?)</div>", url_content):
            vid_part = str(int(vid.group(1)) + 1)
            vid_lnks = vid.group(2)
            
            for vid_lnk in re.finditer(r"<h5.+?>(.+?)</h5><iframe.+?src=\"(.+?)\"", vid_lnks):
                vid_lnk_ttl = title + ' - video-' + vid_part + ' - ' + vid_lnk.group(1)
                vid_lnk_url = vid_lnk.group(2)
                
                addon.add_directory({'mode' : 'play', 'title' : vid_lnk_ttl, 'img' : img, 'url' : vid_lnk_url}, {'title':  vid_lnk_ttl}, img= img)
    else:
        for vid_lnk in re.finditer(r"<h5.+?>(.+?)</h5><iframe.+?src=\"(.+?)\"", url_content):
            vid_lnk_ttl = title + ' - ' + vid_lnk.group(1)
            vid_lnk_url = vid_lnk.group(2)
            
            addon.add_directory({'mode' : 'play', 'title' : vid_lnk_ttl, 'img' : img, 'url' : vid_lnk_url}, {'title':  vid_lnk_ttl}, img= img)
            
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
def Play(url, title, img):
    url_content = net.http_GET(url).content
    url_content = addon.unescape(url_content)
    url_content = unescape(url_content)
    
    pi = re.search(r"jwplayer\(.+?'file'.+?'(.+?)'", url_content)
    if pi:
        pi = pi.group(1)
    
        listitem = xbmcgui.ListItem()
        listitem.setInfo('video', {'Title': title} )
        listitem.setIconImage(img)
        listitem.setThumbnailImage(img)
        xbmc.Player().play(pi, listitem)
    
if mode == 'main': 
    MainMenu()
elif mode == 'latest':
    GetLatest()
elif mode == 'links':
    GetLinks(url, title, img)
elif mode == 'play':
    Play(url, title, img)