#!/usr/bin/python
# -*- coding: utf-8 -*-
##┌──────────────────────────────────────
##│  YouTube 3D v0.0.1 (2014/07/19)
##│  Copyright (c) Inpane
##│  plugin.video.youtube.3d
##│  http://xbmc.inpane.com/
##│  info@inpane.com
##└──────────────────────────────────────
##
## [ 更新履歴 ]
## 2014/07/19 -> v0.0.1
##  テスト版公開
##
##==============================================================================
## 設定値をここに記載する。
import sys, os, string

__script_path__    = os.path.abspath( os.path.dirname(__file__) )
__resources_path__ = __script_path__ + '/resources'
__module_path__    = __resources_path__ + '/module'
#-------------------------------------------------------------------------------
sys.path.append (__module_path__)
import re
import threading, time
import httplib, urllib, urllib2, cookielib
import struct, zlib, xml.dom.minidom
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
try:    import json
except: import simplejson as json

import glob, sqlite3
import datetime, calendar
#-------------------------------------------------------------------------------
__addon_id__ = 'plugin.video.youtube.3d'
__settings__ = xbmcaddon.Addon(__addon_id__)

__youtube_url__  = 'plugin://plugin.video.youtube/?action=play_video&videoid='
__youtube_rss__  = 'http://gdata.youtube.com/feeds/api/videos?vq=3D+SBS+-oculus&orderby=relevance&v=2'

__max_results__  = "50"

try:    __xbmc_version__ = xbmc.getInfoLabel('System.BuildVersion')
except: __xbmc_version__ = 'Unknown'
class AppURLopener(urllib.FancyURLopener):
	version = 'XBMC/' + __xbmc_version__ + ' - Download and play (' + os.name + ')'
urllib._urlopener = AppURLopener()

IN  = {}
OUT = {}
#-------------------------------------------------------------------------------
def getParams():
	ParamDict = {}
	try:
		#print "getParams() argv=", sys.argv
		if sys.argv[2] : ParamPairs = sys.argv[2][1:].split( "&" )
		for ParamsPair in ParamPairs : 
			ParamSplits = ParamsPair.split('=')
			if (len(ParamSplits)) == 2 : ParamDict[ParamSplits[0]] = ParamSplits[1]
	except : pass
	return ParamDict

#-------------------------------------------------------------------------------
def main():
	global IN
	global OUT
	IN = getParams()

	IN[ 'handle' ] = int(sys.argv[1])
	OUT[ 'handle' ] = IN[ 'handle' ]

	if IN.has_key('ope') and IN['ope'] == "play" :

		# 3D再生形式のダイアログを自動表示しない
		query = '{"jsonrpc":"2.0","method":"Settings.SetSettingValue","params":{"setting":"videoplayer.stereoscopicplaybackmode","value":1},"id":1}'
		result = xbmc.executeJSONRPC(query)

		# 3D再生形式の選択を自動的になしに戻さない
		query = '{"jsonrpc":"2.0","method":"Settings.SetSettingValue","params":{"setting":"videoplayer.quitstereomodeonstop","value":false},"id":1}'
		result = xbmc.executeJSONRPC(query)

		# 3D再生形式が設定されていなければ、自動的にアナグラフ形式にする。
		query = '{"jsonrpc":"2.0","method":"Settings.GetSettingValue","params":{"setting":"videoscreen.stereoscopicmode"},"id":1}'
		result = xbmc.executeJSONRPC(query)
		rjson = json.loads(result)
		if not rjson['result'].has_key('value') or rjson['result']['value'] == 0:
			query = '{"jsonrpc":"2.0","method":"Settings.SetSettingValue","params":{"setting":"videoscreen.stereoscopicmode","value":3},"id":1}'
			result = xbmc.executeJSONRPC(query)

		youtube_url = __youtube_url__ + IN['id']
		addon = youtube_url
		addon = addon.replace('%', '$%$')
		addon = addon.replace('_', '$_$')

		# 一回目の再生：youtubeアドオンから再生用URLを得る
		xbmc.Player().play(youtube_url) # sao
		url = xbmc.Player().getPlayingFile() + '&_3D_SBS_'
		path, file = os.path.split( url )
		if path: path += ( "/", "\\" )[ not path.count( "/" ) ]
		file = file.replace('%', '$%$')
		file = file.replace('_', '$_$')

		while True:
			tit  = xbmc.getInfoLabel("Player.Title")
			thum = xbmc.getInfoLabel("Player.Art(thumb)")
			if xbmc.Player().isPlayingVideo() and tit:
				#xbmc.sleep(200)
				#xbmc.Player().pause()
				break
			xbmc.sleep(1)
		#xbmc.sleep(500)

		# レリゴー
		li = xbmcgui.ListItem(tit, "", thum, thum, url)
		xbmc.Player().play(url, li)

		xbmcplugin.endOfDirectory(handle = OUT[ 'handle' ], succeeded = False)

	else : 

		if not IN.has_key('idx'): IN['idx'] = "1"
		OUT['idx'] = IN['idx']

		rss = __youtube_rss__ + "&start-index=" + OUT['idx'] + "&max-results=" + __max_results__
		res = urllib2.urlopen(rss)
		dom = xml.dom.minidom.parseString(res.read())

		entrys = dom.getElementsByTagName('entry')
		for e in entrys:
			title = e.getElementsByTagName('title')[0].firstChild.data.strip().encode('utf-8')

			thum = e.getElementsByTagName('media:thumbnail')[0].getAttribute('url')
			p = re.compile(r'\/vi\/(.+)\/')
			m = p.search(thum)
			id = m.group(1)

			url = 'plugin://' + __addon_id__ + '?ope=play&id=%(id)s' % locals()
			li = xbmcgui.ListItem( title, "", thum, thum )

			commands = []
			commands.append(( 'runme', 'XBMC.RunPlugin(plugin://video/' + __addon_id__ + ')', 'ope=play&id=%(id)s' % locals()))
			li.addContextMenuItems( commands )
			#li.setInfo(type="Video", infoLabels={"Title":title})
			ok = xbmcplugin.addDirectoryItem(OUT[ 'handle' ], url, listitem = li, isFolder=True)

		IN['total'] = dom.getElementsByTagName('openSearch:totalResults')[0].firstChild.data.strip()
		IN['next'] = str(int(IN['idx']) + int(__max_results__))
		if int(IN['total']) >= int(IN['next']): OUT['next'] = IN['next']
		if OUT.has_key('next'): 
			url = 'plugin://' + __addon_id__ + '?ope=list&idx=%s' % OUT['next']
			li = xbmcgui.ListItem('Next Page', "", "DefaultFolder.png", "DefaultFolder.png", url)
			li.setInfo(type="Video", infoLabels={"Title":'Next Page'})
			xbmcplugin.addDirectoryItem(OUT[ 'handle' ], url, li, isFolder=True)

		xbmcplugin.endOfDirectory(handle = OUT[ 'handle' ], succeeded = True)

#-------------------------------------------------------------------------------
if __name__  == '__main__': main()
