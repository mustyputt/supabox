### ############################################################################################################
###	#	
### # Site: 				#		iLiVE - http://www.ilive.to/
### # Author: 			#		The Highway
### # Description: 	#		
### # Credits: 			#		Originally ported from the addon project known as Mash Up - by Mash2k3 2012.
###	#	
### ############################################################################################################
### ############################################################################################################
### Imports ###
import urllib,urllib2,re,cookielib,os,sys,time
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
#from resources.libs import main
from common import *
from common import (_addon,addon,_plugin,net,_artIcon,_artFanart,PlayItCustom)
selfAddon=_plugin
#from universal import watchhistory
#wh=watchhistory.WatchHistory(ps('_addon_id'))
### ############################################################################################################
### ############################################################################################################
SiteName='[COLOR lime]i[COLOR white]LiVE[/COLOR][/COLOR]  [v0.1.1]  [Streams] * (2014-05-01)'
SiteTag='ilive.to'
mainSite='http://www.ilive.to/'
iconSite='http://www.ilive.to/images/logo.png' #_artIcon #http://website.informer.com/thumbnails/280x202/i/ilive.to.png
#	#https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash1/373452_141569702620837_539306243_n.jpg
#	#http://www.ilive.to/images/logo.png
#	#http://www.google.com/url?sa=i&source=images&cd=&cad=rja&docid=bjuYU3p5ns4T3M&tbnid=QscctgKwdsQrBM:&ved=0CAUQjBwwAA&url=http%3A%2F%2Fwww.lifepr.de%2Fattachment%2F262095%2FiLive_Digital_Logo_on_black.jpg&ei=wolHUoaZLdTUyQHUvIF4&psig=AFQjCNHHEGJ8lHifkX1TFQyRd7Vgqd8qKg&ust=1380506434767500
#	#http://www.pwrnewmedia.com/2009/ilive91218/assets/iLive_Logo2FINAL.jpg
#	#http://www.alliance-mktg.com/assets/1/12/GalleryMainDimensionId/iLive_Site_Logo.JPG
#	#http://www.brandsoftheworld.com/sites/default/files/styles/logo-thumbnail/public/112011/logoilive.ai_.png
#	#http://media.marketwire.com/attachments/200712/387150_logo.jpg
#	#https://si0.twimg.com/profile_images/1376125989/logo-1.jpg
#	#
#	#
fanartSite='http://www.iliveconference.com/wp-content/gallery/home-slider/thumbs/thumbs_ilive.png' #_artFanart
colors={'0':'white','1':'red','2':'blue','3':'green','4':'yellow','5':'','6':'lime','7':'','8':'cornflowerblue','9':'blueviolet'}

CR='[CR]'
MyAlphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
MyBrowser=['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3']
### ############################################################################################################
site=addpr('site','')
section=addpr('section','')
url=addpr('url','')
sections={'series':'series','movies':'movies'}
thumbnail=addpr('img','')
fanart=addpr('fanart','')
page=addpr('page','')
### ############################################################################################################
### ############################################################################################################
def About(head=''+cFL(SiteName,'blueviolet')+'',m=''):
	m=''
	if len(m)==0:
		m+='IRC Chat:  '+cFL('#XBMCHUB','blueviolet')+' @ '+cFL('irc.Freenode.net','blueviolet')
		m+=CR+'Site Name:  '+SiteName+CR+'Site Tag:  '+SiteTag+CR+'Site Domain:  '+mainSite+CR+'Site Icon:  '+iconSite+CR+'Site Fanart:  '+fanartSite
		m+=CR+'Age:  Please make sure you are of a valid age to watch the material shown.'
		m+=CR+CR+'Known Hosts for Videos:  '
		m+=CR+'RTMP Live Streams'
		m+=CR+CR+'Features:  '
		m+=CR+'* Includes my Increased List of Categories.  '
		m+='Those which often have no items are marked as such.  '
		m+='Some of My English Shortcuts are included as well.'
		m+=CR+'* Browse Live Channels.'
		m+=CR+'* Play Live Channels.'
		m+=CR+CR+'Notes:  '
		m+=CR+'* Originally ported from mash2k3\'s Mash UP.'
		m+=CR+'* This Project has been given a major overhaul and been reworked to work with my own project\'s functions and methods.'
		#m+=CR+'* Checkout:  Try the iLiVE, CAST ALBA TV, and the rest of Mash Up @ Mash2k3\'s Repo.'
		m+=CR+'* If you really enjoy these addons, please check out the originals'
		m+=CR+'* Some -ORIGINALS- may or may not have stuff like GA-Tracking, Advertisements....'
		m+=CR+'* Some Sub-Addons may be outdated.  Please check their repos for the latest version of their Full-Fledge Addon(s).'
		m+=CR+CR+'Changes:  '
		#m+=CR+'* '
		#m+=CR+'* '
		#m+=CR+'** '
		#m+=CR+'** '
		m+=CR+'* v0.0.9'
		m+=CR+'** Fix for playable link.'
		m+=CR+'* v0.0.8'
		m+=CR+'** '
		m+=CR+'* v0.0.7'
		m+=CR+'** FlashPlayer captcha fixed.'
		m+=CR+'* v0.0.6'
		m+=CR+'** Fixing Streams not listed.'
		m+=CR+'** Fixed Number of Pages.'
		m+=CR+'** Added Movies Category.'
		m+=CR+'* v0.0.5'
		m+=CR+'** Re-did Token Method.  Thanks to BlazeTamer.'
		m+=CR+'* v0.0.4'
		m+=CR+'** Re-did Browsing menus.'
		m+=CR+'** Added Language and Sort setting menus.'
		m+=CR+'** Re-did Pagination Method.'
		m+=CR+"** Added BlazeTamer's method to fix token."
		#m+=CR+'* '
		m+=CR+''
		m+=CR+ps('ReferalMsg')
		m+=CR+''
		m+=CR+''
		m+=CR+''
	String2TextBox(message=cFL(m,'cornflowerblue'),HeaderMessage=head)
	#RefreshList()

### ############################################################################################################
### ############################################################################################################
def DoE(e): xbmc.executebuiltin(E)
def DoA(a): xbmc.executebuiltin("Action(%s)" % a)
# DoA("Back"); 

try: from sqlite3 import dbapi2 as orm
except: from pysqlite2 import dbapi2 as orm
DB='sqlite'; DB_DIR=os.path.join(xbmc.translatePath("special://database"),'Textures13.db'); 
if os.path.isfile(DB_DIR)==True: print "Texture Database Found: "+DB_DIR; 
else: print "Unable to locate Texture Database"

def unCacheAnImage(url):
	if os.path.isfile(DB_DIR)==True: 
		db=orm.connect(DB_DIR); 
		#g='Select cachedurl FROM texture WHERE url = "'+url+'";'; print g; 
		#a=db.execute(g); print str(a); 
		s='DELETE FROM texture WHERE url = "'+url+'";'; print s; 
		db.execute(s); 
		db.commit(); db.close(); 

### ############################################################################################################
### ############################################################################################################

def getToken(url):
	#return 'I8772LDKksadhGHGagf'
	html=net.http_GET(url).content
	token_url=re.compile('\$.getJSON\("(.+?)",').findall(html)[0]
	import datetime,time
	time_now=datetime.datetime.now()
	epoch=time.mktime(time_now.timetuple())+(time_now.microsecond/1000000.)
	epoch_str=str('%f' % epoch); epoch_str=epoch_str.replace('.',''); epoch_str=epoch_str[:-3]
	token_url=token_url + '&_=' + epoch_str
	#
	tokhtml=net.http_GET(token_url+'&_='+str(epoch), headers={'Referer':url}).content
	debob('tokhtml: ')
	debob(tokhtml)
	token=re.compile('":"(.+?)"').findall(tokhtml)[0]
	token=re.compile('":"(.+?)"').findall(net.http_GET(token_url+'&_='+str(epoch), headers={'Referer':url}).content)[0]
	#if '#' in token: token=token.split('#')[0]
	#if '#' in token: token=token.split('#')[1]
	#if '#' in token: token=token.split('#')[0]+token.split('#')[1]
	debob(token)
	return token

def iLivePlay(mname,murl,thumb):
	menuurl=""+murl; name=mname; 
	# #artwork='http://addonrepo.com/xbmchub/moviedb/images/'
	# ###
	#linkA=nURL('http://www.ilive.to/server.php?',headers={'Referer': 'http://www.ilive.to/'}); 
	#match=re.compile('{"token":"(.+?)"}').findall(linkA); 
	#for token in match:
	link=nURL(menuurl) #OPEN_URL(menuurl)
	ok=True
	if link:
			playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
			playlist.clear()
			link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
			#matchserv=re.compile('''.*getJSON\("([^'"]+)".*''').findall(link)
			#for server in matchserv:
			#	print 'Server IS '+server; headers={'Referer':'http://www.ilive.to/'}; url=server; html=net.http_GET(url,headers=headers).content; match=re.compile('{"token":"(.+?)"}').findall(html)
			#	for token in match: print 'SERVERTOKEN IS  '+token; token=token
			server=re.compile('''.*getJSON\("([^'"]+)".*''').findall(link)[0]
			print 'Server IS '+server; headers={'Referer':'http://www.ilive.to/'}; url=server; html=net.http_GET(url,headers=headers).content; 
			token=re.compile('{"token":"(.+?)"}').findall(html)[0]
			###
			#match=re.compile('http://www.ilive.to/embed/(.+?)&width=.+?&height=.+?&autoplay=true').findall(link)
			vid=re.compile('http://www.ilive.to/embed/(.+?)&width=.+?&height=.+?&autoplay=true').findall(link)[0]
			###
			pageUrl='http://www.ilive.to/m/channel.php?n='+vid
			playpath=re.compile('''.*file[:,]\s*['"]([^'"]+).flv['"]''').findall(link)
			playpath=playpath[0]
			newplaypath=str(playpath)        
			rtmp=re.compile('streamer: "(.+?)"').findall(link)
			rtmp=rtmp[0]
			newrtmp=str(rtmp)
			newrtmp=newrtmp.replace('\/','/').replace('\\','')
			try:		app=newrtmp.replace('rtmp://watch.ilive.to:1935/','')
			except:	app=newrtmp.replace('rtmp://watch1.ilive.to:1935/','')
			try:		app=newrtmp.replace('rtmp://watch2.ilive.to:1935/','')
			except:	app=newrtmp.replace('rtmp://watch.ilive.to:1935/','')
			newapp=str(app)
			link=nURL(pageUrl)
			swff=re.compile("type: \'flash\', src: \'(.+?)'").findall(link)
			for swf in swff: swf=swf; print 'SWF IS '+swf
			playable=newrtmp+' app='+newapp+' playpath='+newplaypath+' swfUrl='+swf+' live=1 timeout=15 token='+token+' swfVfy=1 pageUrl=http://www.ilive.to'
			#
			print 'RTMP IS '+playable
			#LIVERESOLVE(name,playable,thumb)
			
			#try: 
			#PlayItCustomMT(url=murl,stream_url=playable,img=thumb,title=name)
			#except: 
			PlayItCustom(url=murl,stream_url=playable,img=thumb,title=name)
			
			###
			#for vid in match:
			#	pageUrl='http://www.ilive.to/m/channel.php?n='+vid
			#	playpath=re.compile('''.*file[:,]\s*['"]([^'"]+).flv['"]''').findall(link)
			#	playpath=playpath[0]
			#	newplaypath=str(playpath)        
			#	rtmp=re.compile('streamer: "(.+?)"').findall(link)
			#	rtmp=rtmp[0]
			#	newrtmp = str(rtmp)
			#	newrtmp = newrtmp.replace('\/','/').replace('\\','')
			#	#try:		app = newrtmp.replace('rtmp://watch.ilive.to:1935/','')
			#	#except:	app = newrtmp.replace('rtmp://watch1.ilive.to:1935/','')
			#	#try:		app = newrtmp.replace('rtmp://watch2.ilive.to:1935/','')
			#	#except:	app = newrtmp.replace('rtmp://watch.ilive.to:1935/','')
			#	#newapp = str(app)
			#	#link=OPEN_URL(pageUrl)
			#	#swff=re.compile("type: \'flash\', src: \'(.+?)'").findall(link)
			#	#for swf in swff:
			#	#	swf= swf
			#	#	#swf= swf[0]
			#	#	#Manual SWF Added
			#	#	#swf = 'http://www.ilive.to/player/player.swf'
			#	#	print 'SWF IS ' + swf
			#	#playable =newrtmp + ' app=' + newapp + ' playpath=' + newplaypath + ' swfUrl=' + swf + ' live=1 timeout=15 token=' + token + ' swfVfy=1 pageUrl=http://www.ilive.to'
			#	##
			#	#print 'RTMP IS ' +  playable
			#	#LIVERESOLVE(name,playable,thumb)
			#
			#
			#match=re.compile('http://www.ilive.to/embed/(.+?)&width=.+?&height=.+?&autoplay=true').findall(link)
			#for fid in match:
			#	vid=fid; 
			#	pageUrl='http://www.ilive.to/m/channel.php?n='+fid; 
			#	server=re.compile('''.*getJSON\("([^'"]+)"''').findall(link); 
			#	playpath=re.compile('''.*file[:,]\s*['"]([^'"]+).flv['"]''').findall(link)[0]; newplaypath=str(playpath); 
			#	swf=re.compile('flashplayer: "http://.+?.ilive.to/(.+?)"').findall(link)[0]; 
			#	rtmp=re.compile('streamer: "(.+?)"').findall(link)[0]; newrtmp=str(rtmp); newrtmp=newrtmp.replace('\/','/').replace('\\',''); 
			#	try: app=newrtmp.replace('rtmp://watch.ilive.to:1935/',''); 
			#	except: app=newrtmp.replace('rtmp://watch1.ilive.to:1935/',''); 
			#	try: app=newrtmp.replace('rtmp://watch2.ilive.to:1935/',''); 
			#	except: app=newrtmp.replace('rtmp://watch.ilive.to:1935/',''); 
			#	newapp=str(app); 
			#	#playable=newrtmp+' app='+newapp+' playpath='+newplaypath+' swfUrl='+newswf+' live=1 timeout=15 token=' + token + ' swfVfy=1 pageUrl=http://www.ilive.to'
			#	playable=newrtmp+' app='+newapp+' playpath='+newplaypath+' swfUrl=http://www.ilive.to/'+swf+' live=1 timeout=15 token=' + token + ' swfVfy=1 pageUrl=http://www.ilive.to'
			#	print 'RTMP IS ' +  playable
			#	#LIVERESOLVE(name,playable,thumb)
			#	PlayItCustom(url=murl,stream_url=playable,img=thumb,title=name)

def iLivePlay_v8(mname,murl,thumb):
	menuurl=murl; name=mname; 
	#artwork='http://addonrepo.com/xbmchub/moviedb/images/'
	###
	linkA=nURL('http://www.ilive.to/server.php?',headers={'Referer': 'http://www.ilive.to/'}); 
	match=re.compile('{"token":"(.+?)"}').findall(linkA); 
	for token in match:
		link=nURL(menuurl) #OPEN_URL(menuurl)
		ok=True
		if link:
			playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
			playlist.clear()
			link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
			match=re.compile('http://www.ilive.to/embed/(.+?)&width=.+?&height=.+?&autoplay=true').findall(link)
			for fid in match:
				vid=fid; 
				pageUrl='http://www.ilive.to/m/channel.php?n='+fid; 
				server=re.compile('''.*getJSON\("([^'"]+)"''').findall(link); 
				playpath=re.compile('''.*file[:,]\s*['"]([^'"]+).flv['"]''').findall(link)[0]; newplaypath=str(playpath); 
				swf=re.compile('flashplayer: "http://.+?.ilive.to/(.+?)"').findall(link)[0]; 
				rtmp=re.compile('streamer: "(.+?)"').findall(link)[0]; newrtmp=str(rtmp); newrtmp=newrtmp.replace('\/','/').replace('\\',''); 
				try: app=newrtmp.replace('rtmp://watch.ilive.to:1935/',''); 
				except: app=newrtmp.replace('rtmp://watch1.ilive.to:1935/',''); 
				try: app=newrtmp.replace('rtmp://watch2.ilive.to:1935/',''); 
				except: app=newrtmp.replace('rtmp://watch.ilive.to:1935/',''); 
				newapp=str(app); 
				#playable=newrtmp+' app='+newapp+' playpath='+newplaypath+' swfUrl='+newswf+' live=1 timeout=15 token=' + token + ' swfVfy=1 pageUrl=http://www.ilive.to'
				playable=newrtmp+' app='+newapp+' playpath='+newplaypath+' swfUrl=http://www.ilive.to/'+swf+' live=1 timeout=15 token=' + token + ' swfVfy=1 pageUrl=http://www.ilive.to'
				print 'RTMP IS ' +  playable
				#LIVERESOLVE(name,playable,thumb)
				PlayItCustom(url=murl,stream_url=playable,img=thumb,title=name)

def iLivePlay_v4(mname,murl,thumb):
	menuurl=murl; name=mname; 
	###
	artwork='http://addonrepo.com/xbmchub/moviedb/images/'
	#LogNotify('Attempting to play Stream', 'Please Wait...', '5000', artwork+'/ilive.png')
	link=nURL('http://goo.gl/bLOqUg').replace('\n','').replace('\r',''); ## BlazeTamer's Method ##
	#link='iLive Token Page<item><token>motngaynew1</token><swf>http://www.ilive.to/player/player_ilive_2.swf</swf></item>'; 
	match=re.compile('<token>(.+?)</token><swf>(.+?)</swf>').findall(link); 
	for token,newswf in match:
		link=nURL(menuurl) #OPEN_URL(menuurl)
		ok=True
		if link:
			playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
			playlist.clear()
			link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
			match=re.compile('http://www.ilive.to/embed/(.+?)&width=.+?&height=.+?&autoplay=true').findall(link)
			for fid in match:
				pageUrl='http://www.ilive.to/m/channel.php?n='+fid
				server=re.compile('''.*getJSON\("([^'"]+)"''').findall(link)
				playpath=re.compile('''.*file[:,]\s*['"]([^'"]+).flv['"]''').findall(link)
				playpath = playpath[0]
				newplaypath =str(playpath)
				rtmp=re.compile('streamer: "(.+?)"').findall(link)
				rtmp= rtmp[0]
				newrtmp = str(rtmp)
				newrtmp = newrtmp.replace('\/','/').replace('\\','')
				try: app = newrtmp.replace('rtmp://watch.ilive.to:1935/','')
				except: app = newrtmp.replace('rtmp://watch1.ilive.to:1935/','')
				try: app = newrtmp.replace('rtmp://watch2.ilive.to:1935/','')
				except: app = newrtmp.replace('rtmp://watch.ilive.to:1935/','')        
				newapp = str(app)
				playable =newrtmp + ' app=' + newapp + ' playpath=' + newplaypath + ' swfUrl=' + newswf + ' live=1 timeout=15 token=' + token + ' swfVfy=1 pageUrl=http://www.ilive.to'
				print 'RTMP IS ' +  playable
				#LIVERESOLVE(name,playable,thumb)
				PlayItCustom(url=murl,stream_url=playable,img=thumb,title=name)

def iLivePlay_v2(mname,murl,thumb):
	myNote('Please Wait!','Opening Stream',3000); stream_url=False; link=nURL(murl); deb('murl',murl)
	if link:
		link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
		match=re.compile('http://www.ilive.to/embed/(.+?)&width=(.+?)&height=(.+?)&autoplay=true').findall(link)
		#debob(match)
		_fid=''
		for fid,wid,hei in match: pageUrl='http://www.ilive.to/embedplayer.php?width='+wid+'&height='+hei+'&channel='+fid+'&autoplay=true'; debob(pageUrl); _fid=fid
		#debob(pageUrl)
		#link=nURL(pageUrl); playpath=re.compile('file: "(.+?).flv"').findall(link); token=getToken(pageUrl)
		link=nURL(pageUrl); playpath=re.compile('file\s*:\s*"(.+?)\.flv"').findall(link); token=getToken(pageUrl)
		#debob(playpath)
		if len(playpath)==0: playpath=re.compile('http://snapshots.ilive.to/snapshots/(.+?)_snapshot.jpg').findall(thumb)
		#debob(playpath)
		#for playPath in playpath: debob(playPath); stream_url='rtmp://live.ilive.to/edge playpath='+playPath+" live=1 timeout=15 swfUrl=http://player.ilive.to/player_ilive_2.swf pageUrl="+pageUrl+" token="+token
		#for playPath in playpath: debob(playPath); stream_url='rtmp://live.ilive.to/edge playpath='+playPath+" live=1 timeout=15 swfUrl=http://player.ilive.to/player_ilive_2.swf pageUrl="+pageUrl+" token="+token
		#for playPath in playpath: debob(playPath); stream_url='rtmp://live.ilive.to/edge playpath='+playPath+" live=1 timeout=15 swfUrl=http://player.ilive.to/secure_player_ilive_z.swf pageUrl="+pageUrl+" token="+token
		
		#for playPath in playpath: debob(playPath); stream_url='rtmp://live.ilive.to/edge playpath='+playPath+" live=1 timeout=15 swfUrl=http://player.ilive.to/player_ilive_2.swf pageUrl="+pageUrl+" token="+token
		for playPath in playpath: debob(playPath); stream_url='rtmp://da.iguide.to/edge playpath='+playPath+" swfUrl=http://player.ilive.to/secure_player_ilive_z.swf live=1 timeout=15 token="+'I8772LDKksadhGHGagf#'+" pageUrl="+'http://www.ilive.to'+""
		#item_info_from=rtmp + ' playpath=' + file + ' swfUrl=' + swf + ' live=1 timeout=15 token=I8772LDKksadhGHGagf# swfVfy=1 pageUrl=http://www.ilive.to
		
		
		#for playPath in playpath: debob(playPath); stream_url='rtmp://176.31.231.124/edge playpath='+playPath+" live=1 timeout=15 swfUrl=http://player.ilive.to/player_ilive_2.swf pageUrl="+pageUrl+" token="+token
		##rtmp://176.31.231.124/edge playpath=1fcjkxa4ar5b4gd swfUrl=http://static.ilive.to/jwplayer/player_embed.swf pageUrl=http://www.ilive.to/embedplayer.php?width=600&amp;height=400&amp;channel=37398&amp;autoplay=true
		
		
		
		#for playPath in playpath: debob(playPath); stream_url='rtmp://stream.ilive.to/edge playpath='+playPath+" live=1 timeout=15 swfUrl=http://player.ilive.to/player_ilive_2.swf pageUrl="+pageUrl+" token="+token
		#for playPath in playpath: debob(playPath); stream_url='rtmp://stream.ilive.to/edge playpath='+playPath+" live=1 timeout=15 swfUrl=http://player.ilive.to/secure_player_ilive_z.swf pageUrl="+pageUrl+" token="+token
		#for playPath in playpath: debob(playPath); stream_url='rtmp://live.ilive.to:1935/edge playpath='+playPath+" live=1 timeout=15 swfUrl=http://player.ilive.to/secure_player_ilive_z.swf pageUrl="+pageUrl+" token="+token
		
		#for playPath in playpath: debob(playPath); stream_url='rtmp://stream.ilive.to:1935/edge playpath='+playPath+" live=1 timeout=15 swfUrl=http://player.ilive.to/player_ilive_2.swf pageUrl="+pageUrl+" token="+token
		#for playPath in playpath: debob(playPath); stream_url='rtmp://live.ilive.to:1935/edge playpath='+playPath+" live=1 timeout=15 swfUrl=http://player.ilive.to/player_ilive_2.swf pageUrl="+pageUrl+" token="+token
		
		#for playPath in playpath: debob(playPath); stream_url='rtmp://stream.ilive.to:1935/edge playpath='+playPath+" live=1 timeout=15 swfUrl=http://player.ilive.to/player.swf pageUrl="+pageUrl+" token="+token
		
		
		#for playPath in playpath: debob(playPath); stream_url='rtmp://live.ilive.to/edge playpath='+playPath+" live=1 timeout=20 swfUrl=http://player.ilive.to/player_ilive_2.swf pageUrl=http://www.ilive.to/view/"+_fid+" token="+token; debob(stream_url)
		#for playPath in playpath: debob(playPath); stream_url='rtmp://stream.ilive.to/edge playpath='+playPath+" live=1 timeout=20 swfUrl=http://player.ilive.to/player_ilive_2.swf pageUrl=http://www.ilive.to/view/"+_fid+" token="+token; debob(stream_url)
		
		#for playPath in playpath: debob(playPath); stream_url='rtmp://da.iguide.to/iguide playpath='+playPath+" live=1 timeout=15 swfUrl=http://player.ilive.to/player_ilive_2.swf pageUrl="+pageUrl+" token="+token
		
		
		#####for playPath in playpath: debob(playPath); stream_url='rtmp://live.ilive.to/edge playpath='+playPath+".flv live=1 timeout=15 swfUrl=http://player.ilive.to/player_ilive_2.swf pageUrl="+pageUrl+" token="+token
		#PlayItCustom(url=murl,stream_url=stream_url,img=thumb,title=mname)
		PlayItCustom(url=murl,stream_url=stream_url,img='http://snapshots.ilive.to/snapshots/'+playPath+'_snapshot.jpg',title=mname)
		#

def iLiveList(mmurl):
	murl=mmurl.lower()
	if murl=='general':
		try: urllist=['http://www.ilive.to/channels/General','http://www.ilive.to/channels/General?p=2']
		except: urllist=['http://www.ilive.to/channels/General']
	if murl=='entertainment':
		try: urllist=['http://www.ilive.to/channels/Entertainment','http://www.ilive.to/channels/Entertainment?p=2','http://www.ilive.to/channels/Entertainment?p=3','http://www.ilive.to/channels/Entertainment?p=4','http://www.ilive.to/channels/Entertainment?p=5','http://www.ilive.to/channels/Entertainment?p=6']
		except: urllist=['http://www.ilive.to/channels/Entertainment','http://www.ilive.to/channels/Entertainment?p=2','http://www.ilive.to/channels/Entertainment?p=3','http://www.ilive.to/channels/Entertainment?p=4','http://www.ilive.to/channels/Entertainment?p=5']
	if murl=='sports':
		try: urllist=['http://www.ilive.to/channels/Sport','http://www.ilive.to/channels/Sport?p=2','http://www.ilive.to/channels/Sport?p=3','http://www.ilive.to/channels/Sport?p=4']
		except: urllist=['http://www.ilive.to/channels/Sport','http://www.ilive.to/channels/Sport?p=2','http://www.ilive.to/channels/Sport?p=3']
	if murl=='news':
		try: urllist=['http://www.ilive.to/channels/News']
		except: urllist=['http://www.ilive.to/channels/News']
	if murl=='music':
		try: urllist=['http://www.ilive.to/channels/Music']
		except: urllist=['http://www.ilive.to/channels/Music']
	if murl=='animation':
		try: urllist=['http://www.ilive.to/channels/Animation','http://www.ilive.to/channels/Animation?p=2']
		except: urllist=['http://www.ilive.to/channels/Animation']
	if murl=='family':
		try: urllist=['http://www.ilive.to/channels/Family']
		except: urllist=['http://www.ilive.to/channels/Family']
	if murl=='lifecaster':
		try: urllist=['http://www.ilive.to/channels/Lifecaster']
		except: urllist=['http://www.ilive.to/channels/Lifecaster']
	if murl=='gaming':
		try: urllist=['http://www.ilive.to/channels/Gaming']
		except: urllist=['http://www.ilive.to/channels/Gaming']
	if murl=='mobile':
		try: urllist=['http://www.ilive.to/channels/Mobile']
		except: urllist=['http://www.ilive.to/channels/Mobile']
	if murl=='religion':
		try: urllist=['http://www.ilive.to/channels/Religion']
		except: urllist=['http://www.ilive.to/channels/Religion']
	if murl=='radio':
		try: urllist=['http://www.ilive.to/channels/Radio']
		except: urllist=['http://www.ilive.to/channels/Radio']
	if murl=='all':
		try: urllist=['http://www.ilive.to/channels','http://www.ilive.to/channels?p=2','http://www.ilive.to/channels?p=3','http://www.ilive.to/channels?p=4','http://www.ilive.to/channels?p=5','http://www.ilive.to/channels?p=6','http://www.ilive.to/channels?p=7','http://www.ilive.to/channels?p=8','http://www.ilive.to/channels?p=9','http://www.ilive.to/channels?p=10','http://www.ilive.to/channels?p=11','http://www.ilive.to/channels?p=12','http://www.ilive.to/channels?p=13','http://www.ilive.to/channels?p=14','http://www.ilive.to/channels?p=15','http://www.ilive.to/channels?p=16']
		except: urllist=['http://www.ilive.to/channels','http://www.ilive.to/channels?p=2','http://www.ilive.to/channels?p=3','http://www.ilive.to/channels?p=4','http://www.ilive.to/channels?p=5','http://www.ilive.to/channels?p=6','http://www.ilive.to/channels?p=7','http://www.ilive.to/channels?p=8','http://www.ilive.to/channels?p=9','http://www.ilive.to/channels?p=10']
	if murl=='allenglish':
		try: urllist=['http://www.ilive.to/channels?lang=1','http://www.ilive.to/channels?lang=1&p=2','http://www.ilive.to/channels?lang=1&p=3','http://www.ilive.to/channels?lang=1&p=4','http://www.ilive.to/channels?lang=1&p=5','http://www.ilive.to/channels?lang=1&p=6','http://www.ilive.to/channels?lang=1&p=7','http://www.ilive.to/channels?lang=1&p=8','http://www.ilive.to/channels?lang=1&p=9','http://www.ilive.to/channels?lang=1&p=10']
		except: urllist=['http://www.ilive.to/channels?lang=1','http://www.ilive.to/channels?lang=1&p=2','http://www.ilive.to/channels?lang=1&p=3','http://www.ilive.to/channels?lang=1&p=4','http://www.ilive.to/channels?lang=1&p=5','http://www.ilive.to/channels?lang=1&p=6','http://www.ilive.to/channels?lang=1&p=7','http://www.ilive.to/channels?lang=1&p=8','http://www.ilive.to/channels?lang=1&p=9']
	if murl=='entertainmentenglish':
		try: urllist=['http://www.ilive.to/channels/Entertainment?lang=1','http://www.ilive.to/channels/Entertainment?lang=1&p=2','http://www.ilive.to/channels/Entertainment?lang=1&p=3','http://www.ilive.to/channels/Entertainment?lang=1&p=4','http://www.ilive.to/channels/Entertainment?lang=1&p=5','http://www.ilive.to/channels/Entertainment?lang=1&p=6']
		except: urllist=['http://www.ilive.to/channels/Entertainment?lang=1','http://www.ilive.to/channels/Entertainment?lang=1&p=2','http://www.ilive.to/channels/Entertainment?lang=1&p=3','http://www.ilive.to/channels/Entertainment?lang=1&p=4','http://www.ilive.to/channels/Entertainment?lang=1&p=5']
	if murl=='sportsenglish':
		try: urllist=['http://www.ilive.to/channels/Sport?lang=1','http://www.ilive.to/channels/Sport?lang=1&p=2']
		except: urllist=['http://www.ilive.to/channels/Sport?lang=1']
	pLd='Pages loaded :: [B]'; loadedLinks=0; totalLinks=len(urllist); dialogWait=xbmcgui.DialogProgress()
	remaining_display=pLd+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'; ret=dialogWait.create('Please wait until channel list is loaded.')
	dialogWait.update(0,'[B]Loading.....[/B]',remaining_display)
	for durl in urllist:
		link=html=messupText(nURL(durl),True,True)
		link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
		match=re.compile('src=".+?" alt=".+?<img width=".+?" height=".+?" src="([^<]+)" alt=".+?"/></noscript></a><a href="(.+?)"><strong>(.+?)</strong></a><br/>.+?<a href="http://[A-Za-z0-9\.]*/channels\?lang=\d*">([A-Za-z]*)</a>').findall(link) ## From TheHighway
		#match=re.compile('src=".+?" alt=".+?<img width=".+?" height=".+?" src="([^<]+)" alt=".+?"/></noscript></a><a href="(.+?)"><strong>(.+?)</strong></a><br/>').findall(link) ## From MashUP
		match=sorted(match, key=lambda item: item[2], reverse=False)
		match=sorted(match, key=lambda item: item[3], reverse=False)
		#debob(match)
		for thumb,url,name,lang in match: #for thumb,url,name in match:
			try: _addon.add_directory({'mode':'iLivePlay','site':site,'section':section,'title':name,'url':url,'fanart':thumb,'img':thumb},{'title':cFL_(name,colors['6'])+'  ['+cFL(lang,colors['6'])+']'},is_folder=False,fanart=thumb,img=thumb)
			except: pass
			##match=re.compile('Hongkong').findall(name)
			##match2=re.compile('sex').findall(name)
			##if len(match)==0 and len(match2)==0:
			#	#if name != 'Playboy TV':
			#	#_addon.add_directory({'mode':iLL,'site':site,sC1:sC2,'title':name,'url':url},{'title':cFL_(name,colors['6'])},is_folder=True,fanart=thumb,img=thumb)
			#	#main.addPlayL(name+'  ['+lang+']',url,121,thumb,'','','','','') #main.addPlayL(name,url,121,thumb,'','','','','')
		loadedLinks=loadedLinks + 1; percent=(loadedLinks * 100)/totalLinks; remaining_display=pLd+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'; dialogWait.update(percent,'[B]Loading.....[/B]',remaining_display)
		if (dialogWait.iscanceled()): return False
	dialogWait.close(); del dialogWait
	set_view('list',view_mode=addst('default-view')); eod(); 

def iLiveBrowse(channel,iLive_Sort,iLive_Language):
	if len(iLive_Sort)==0: iLive_Sort="0"
	#channel=channel.replace(" ","%20"); 
	### \/ Catching the first page.
	tUrl="http://www.ilive.to/channels/"+channel.replace(" ","%20")+"?sort="+iLive_Sort+"&lang="+iLive_Language; deb("url",tUrl); 
	html=nURL(tUrl); deb("length of first page",str(len(html))); 
	### \/ Catching the rest of the pages.
	if '<p align="center" class="pages"><strong>Page: </strong>' in html:
		phtml=html.split('<p align="center" class="pages"><strong>Page: </strong>')[1].split('</span></p>')[0]; deb("length of phtml",str(len(phtml))); 
		try: ppages=re.compile('<a href="(http://www.ilive.to/channels/.+?)">\s*(\d+)\s*</a>').findall(phtml)
		except: ppages=[]
		deb("number of pages",str(len(ppages)+1)); debob(ppages); 
		dialogWait=xbmcgui.DialogProgress(); loaded=1; ptotal=len(ppages)+1; ret=dialogWait.create('Please wait...'); 
		percent=(loaded * 100)/ptotal; remaining_display='[B]Page '+str(loaded)+' of '+str(ptotal)+'[/B].'; dialogWait.update(percent,'[B]Loading Pages...[/B]',remaining_display); 
		for (ppage,pname) in ppages: 
			time.sleep(1); html+=nURL(ppage.replace(" ","%20")); 
			loaded=loaded+1; percent=(loaded * 100)/ptotal; remaining_display='[B]Page '+str(loaded)+' of '+str(ptotal)+'[/B].'; dialogWait.update(percent,'[B]Loading Pages...[/B]',remaining_display); 
		dialogWait.close(); del dialogWait
	### \/ Catching Items.
	html=nolines(messupText(html.replace("&nbsp;",""),True,True)); 
	deb("length of all pages",str(len(html))); 
	###s='src=".+?" alt=".+?<img width=".+?" height=".+?" src="([^<]+)" alt=".+?"/></noscript></a><a href="(.+?)"><strong>(.+?)</strong></a><br/>.+?<a href="http://[A-Za-z0-9\.]*/channels\?lang=\d*">([A-Za-z]*)</a>\s*</li>'; 
	###s='src=".+?" alt=".+?
	##s='<img width=".+?" height=".+?" src="(http://snapshots.ilive.to/snapshots/[0-9a-zA-Z]+_snapshot.[jpg|png]+)" alt=".+?"/></noscript></a><a href="(.+?)"><strong>(.+?)</strong></a><br/>.+?'; 
	##s+='<span class="viewers">(.*?)</span>\s*'; s+='<span class="totalviews">(.*?)</span><br/>\s*'; 
	##s+='<a href="http://[A-Za-z0-9\.]*/channels/[A-Za-z\s]*">([A-Za-z0-9\s]*)</a>\s*'; 
	##s+='<a href="http://[A-Za-z0-9\.]*/channels\?lang=\d*">([A-Za-z0-9\s]*)</a>\s*</li>'; 
	#'src=".+?" alt=".+?<img width=".+?" height=".+?" src="([^<]+)" alt=".+?"/></noscript></a><a href="(.+?)"><strong>(.*?)</strong></a><br/>'
	s='<noscript><img width="\d+" height="\d+" src="(http://snapshots.ilive.to/snapshots/[0-9a-zA-Z]+_snapshot.jpg)" alt=".+?"\s*/></noscript>\s*</a>\s*\n*\s*'; 
	s+='<a href="(http://www.ilive.to/view/\d+/.+?)"><strong>\s*(.+?)\s*</strong></a><br/>\s*'; 
	s+='<span class="viewers">([0-9\,]+)</span>\s*'; 
	s+='<span class="totalviews">([0-9\,]+)</span><br/>\s*'; 
	s+='<a href="http://www.ilive.to/channels/.+?">([A-Za-z0-9\s]*)</a>\s*'; 
	s+='<a href="http://www.ilive.to/channels\?lang=\d*">([A-Za-z0-9\s]*)</a>\s*</li>'; 
	#debob(html); 
	match=re.compile(s).findall(html); ItemCount=len(match); 
	debob(match); 
	#match=sorted(match, key=lambda item: item[2], reverse=False)
	#match=sorted(match, key=lambda item: item[3], reverse=False)
	### \/ Links
	for thumb,url,name,iViewers,iTotalViews,Category,lang in match:
		unCacheAnImage(thumb); 
		pars={'mode':'iLivePlay','site':site,'section':section,'title':name,'url':url,'fanart':thumb,'img':thumb}; 
		PlotD=cFL("[CR]Language: "+lang+"[CR]Category: "+Category+"[CR]Viewers: "+iViewers+"[CR]TotalViews: "+iTotalViews,"tan"); 
		try: _addon.add_directory(pars,{'title':name+'  ['+cFL(lang,colors['6'])+']','plot':PlotD},is_folder=False,fanart=thumb,img=thumb,total_items=ItemCount)
		except: pass
	
	###
	set_view('movies',view_mode=addst('movies-view')); 
	#set_view('tvshows',view_mode=addst('tvshows-view')); 
	#set_view('list',view_mode=addst('default-view')); 
	eod(); 

##<label>Category:&nbsp;</label><select name="category" style="width:120px" onchange="document.location='http://www.ilive.to/channels/'+this.options[this.selectedIndex].value+'?sort=1&lang=1'">
#<option value="">All</option><option value="Live Sport">Live Sport</option>
#<option value="Entertainment">Entertainment</option><option value="Animation">Animation</option><option value="Lifecaster">Lifecaster</option>
#<option value="Gaming">Gaming</option><option value="General">General</option><option value="News">News</option>
#<option value="Music">Music</option><option value="Mobile">Mobile</option><option value="Family">Family</option>
#<option value="Religion">Religion</option><option value="Radio">Radio</option><option value="Movies">Movies</option> </select>
##<label style="margin-left:10px">Language:&nbsp;</label><select name="language" style="width:120px" onchange="document.location=addParameter('http://www.ilive.to/channels/?sort=1&lang=1', 'lang', this.options[this.selectedIndex].value)">
#<option value="">All</option><option value="1" selected="selected">English</option><option value="2">Spanish</option><option value="3">Portuguese</option><option value="4">French</option><option value="5">German</option><option value="6">Russian</option><option value="7">Vietnamese</option><option value="8">Italian</option><option value="9">Filipino</option><option value="10">Thai</option><option value="11">Chinese</option><option value="12">Indian</option><option value="13">Japanese</option><option value="14">Greek</option><option value="15">Dutch</option><option value="16">Swedish</option><option value="17">Unidentified</option><option value="18">Korean</option><option value="19">Brazilian</option><option value="20">Indian</option><option value="21">Romanian</option> </select>
##<label style="margin-left:10px">Sort by:&nbsp;</label><select name="sort" style="width:120px" onchange="document.location=addParameter('http://www.ilive.to/channels/?sort=1&lang=1', 'sort', this.options[this.selectedIndex].value)">
#<option value="0">Default</option><option value="1" selected="selected">Current Viewers</option><option value="2">Total Views</option>
#	#BB.append(("","")); 

def SSortSet(SSort): addstv("iLive_Sort",SSort); eod(); DoA("Back"); 
def SSortMenu():
	sC1='section'; sC2='live'; iLL='SSortSet'; fS=fanartSite; iS=iconSite; BB=[]; 
	BB.append(("0","Default")); BB.append(("1","Current Viewers")); BB.append(("2","Total Views")); 
	for (ssort,name) in BB:
		_addon.add_directory({'sort':ssort,'mode':iLL,'site':site,sC1:sC2,'title':name},{'title':cFL_(name,colors['6'])},is_folder=True,fanart=fS,img=iS); 
	set_view('list',view_mode=addst('default-view')); eod(); 

def LanguageSet(Language): addstv("iLive_Language",Language); eod(); DoA("Back"); 
def LanguageMenu():
	sC1='section'; sC2='live'; iLL='LanguageSet'; fS=fanartSite; iS=iconSite; BB=[]; 
	BB.append(("","All")); BB.append(("1","English")); BB.append(("2","Spanish")); BB.append(("3","Portuguese")); BB.append(("4","French")); BB.append(("5","German")); BB.append(("6","Russian")); BB.append(("7","Vietnamese")); BB.append(("8","Italian")); BB.append(("9","Filipino")); BB.append(("10","Thai")); BB.append(("11","Chinese")); BB.append(("12","Indian")); BB.append(("13","Japanese")); BB.append(("14","Greek")); BB.append(("15","Dutch")); BB.append(("16","Swedish")); BB.append(("17","Unidentified")); BB.append(("18","Korean")); BB.append(("19","Brazilian")); BB.append(("20","Indian")); BB.append(("21","Romanian")); 
	for (language,name) in BB:
		_addon.add_directory({'language':language,'mode':iLL,'site':site,sC1:sC2,'title':name},{'title':cFL_(name,colors['6'])},is_folder=True,fanart=fS,img=iS); 
	set_view('list',view_mode=addst('default-view')); eod(); 

def SectionMenu(): #(site):
	sC1='section'; sC2='live'; iLL='iLiveList'; fS=fanartSite; iS=iconSite; 
	_addon.add_directory({'mode':'LanguageMenu','site':site,sC1:sC2},{'title':'* '+cFL_("Language",colors['6'])},is_folder=True,fanart=fS,img=iS); 
	_addon.add_directory({'mode':'SSortMenu','site':site,sC1:sC2},{'title':'* '+cFL_("Sort By",colors['6'])},is_folder=True,fanart=fS,img=iS); 
	###
	BB=[]; 
	BB.append(("","All")); BB.append(("Movies","Movies")); BB.append(("Entertainment","Entertainment")); BB.append(("Live Sport","Live Sport")); 
	BB.append(("Animation","Animation")); BB.append(("Lifecaster","Lifecaster")); BB.append(("Gaming","Gaming")); 
	BB.append(("General","General")); BB.append(("News","News")); BB.append(("Music","Music")); 
	BB.append(("Mobile","Mobile")); BB.append(("Family","Family")); BB.append(("Religion","Religion")); 
	BB.append(("Radio","Radio")); 
	for (channel,name) in BB:
		_addon.add_directory({'channel':channel,'mode':'iLiveBrowse','site':site,sC1:sC2,'title':name},{'title':cFL_(name,colors['6'])},is_folder=True,fanart=fS,img=iS); 
	
	###
	#_addon.add_directory({'mode':iLL,'site':site,sC1:sC2,'title':'allenglish'},{'title':cFL_('All [English]',colors['6'])},is_folder=True,fanart=fS,img=iS)
	#_addon.add_directory({'mode':iLL,'site':site,sC1:sC2,'title':'entertainmentenglish'},{'title':cFL_('Entertainment [English]',colors['6'])},is_folder=True,fanart=fS,img=iS)
	#_addon.add_directory({'mode':iLL,'site':site,sC1:sC2,'title':'sportsenglish'},{'title':cFL_('Sports [English]',colors['6'])},is_folder=True,fanart=fS,img=iS)
	#_addon.add_directory({'mode':iLL,'site':site,sC1:sC2,'title':'all'},{'title':cFL_('All',colors['6'])},is_folder=True,fanart=fS,img=iS)
	#_addon.add_directory({'mode':iLL,'site':site,sC1:sC2,'title':'General'},{'title':cFL_('General',colors['6'])},is_folder=True,fanart=fS,img=iS)
	#_addon.add_directory({'mode':iLL,'site':site,sC1:sC2,'title':'Entertainment'},{'title':cFL_('Entertainment',colors['6'])},is_folder=True,fanart=fS,img=iS)
	#_addon.add_directory({'mode':iLL,'site':site,sC1:sC2,'title':'Sports'},{'title':cFL_('Sports',colors['6'])},is_folder=True,fanart=fS,img=iS)
	#_addon.add_directory({'mode':iLL,'site':site,sC1:sC2,'title':'News'},{'title':cFL_('News',colors['6'])},is_folder=True,fanart=fS,img=iS)
	#_addon.add_directory({'mode':iLL,'site':site,sC1:sC2,'title':'Music'},{'title':cFL_('Music',colors['6'])},is_folder=True,fanart=fS,img=iS)
	#_addon.add_directory({'mode':iLL,'site':site,sC1:sC2,'title':'Animation'},{'title':cFL_('Animation',colors['6'])},is_folder=True,fanart=fS,img=iS)
	#_addon.add_directory({'mode':iLL,'site':site,sC1:sC2,'title':'Family'},{'title':cFL_('Family',colors['6'])},is_folder=True,fanart=fS,img=iS)
	#_addon.add_directory({'mode':iLL,'site':site,sC1:sC2,'title':'lifecaster'},{'title':cFL_('Lifecaster (Often Empty)',colors['6'])},is_folder=True,fanart=fS,img=iS)
	#_addon.add_directory({'mode':iLL,'site':site,sC1:sC2,'title':'gaming'},{'title':cFL_('Gaming (Often Empty)',colors['6'])},is_folder=True,fanart=fS,img=iS)
	#_addon.add_directory({'mode':iLL,'site':site,sC1:sC2,'title':'mobile'},{'title':cFL_('Mobile (Often Empty)',colors['6'])},is_folder=True,fanart=fS,img=iS)
	#_addon.add_directory({'mode':iLL,'site':site,sC1:sC2,'title':'religion'},{'title':cFL_('Religion (Often Empty)',colors['6'])},is_folder=True,fanart=fS,img=iS)
	#_addon.add_directory({'mode':iLL,'site':site,sC1:sC2,'title':'radio'},{'title':cFL_('Radio (Often Empty)',colors['6'])},is_folder=True,fanart=fS,img=iS)
	###
	
	#_addon.add_directory({'mode':iLL,'site':site,sC1:sC2,'title':''},{'title':cFL_('',colors['6'])},is_folder=True,fanart=fS,img=iS)
	#_addon.add_directory({'mode':iLL,'site':site,sC1:sC2,'title':''},{'title':cFL_('',colors['6'])},is_folder=True,fanart=fS,img=iS)
	
	#_addon.add_directory({'mode':'SubMenu','site':site,'section':'movies'},{'title':cFL_('Anime Movies',colors['1'])},is_folder=True,fanart=fanartSite,img=iconSite)
	#_addon.add_directory({'mode':'SubMenu','site':site,'section':'series'},{'title':cFL_('Anime Series',colors['2'])},is_folder=True,fanart=fanartSite,img=iconSite)
	#_addon.add_directory({'mode':'Page','site':site,'section':'series','url':mainSite+'ongoing-anime'},{'title':cFL_('Ongoing Series',colors['2'])},is_folder=True,fanart=fanartSite,img=iconSite)
	#_addon.add_directory({'mode':'Page','site':site,'section':'series','url':mainSite+'new-anime'},{'title':cFL_('New Series',colors['2'])},is_folder=True,fanart=fanartSite,img=iconSite)
	#_addon.add_directory({'mode':'Episodes','site':site,'section':'series','url':mainSite+'surprise'},{'title':cFL_('Suprise Me',colors['0'])},is_folder=True,fanart=fanartSite,img=iconSite)
	#_addon.add_directory({'mode':'Search','site':site},{'title':cFL_('Search',colors['0'])},is_folder=True,fanart=fanartSite,img=iconSite)
	#if (len(addst('LastSearchTitle'+SiteTag)) > 0): _addon.add_directory({'mode':'SearchLast','site':site},{'title':cFL_('Repeat Last Search',colors['0'])},is_folder=True,fanart=fanartSite,img=iconSite)
	###if (len(addst('LastSearchTitle'+SiteTag)) > 0): _addon.add_directory({'mode':'SearchLast','site':site,'endit':'false'},{'title':cFL_('Repeat Last Search',colors['0'])},is_folder=True,fanart=fanartSite,img=iconSite)
	_addon.add_directory({'mode':'About','site':site},{'title':cFL_('About',colors['9'])},is_folder=False,fanart=fanartSite,img='http://i.imgur.com/0h78x5V.png') # iconSite
	#
	set_view('list',view_mode=addst('default-view')); eod()


### ############################################################################################################
### ############################################################################################################
def mode_subcheck(mode='',site='',section='',url=''):
	deb('mode',mode); 
	if (mode=='SectionMenu'): 		SectionMenu()
	elif (mode=='') or (mode=='main') or (mode=='MainMenu'): SectionMenu()
	elif (mode=='SubMenu'): 			SubMenu()
	elif (mode=='Page'): 					Browse_Page(url=url,page=page,metamethod=addpr('metamethod','')) #(site,section)
	elif (mode=='Episodes'): 			Browse_Episodes(url,page)
	elif (mode=='Hosts'): 				Browse_Hosts(url)
	elif (mode=='AZ'): 						Browse_AZ()
	elif (mode=='Genres'): 				Browse_Genres()
	elif (mode=='PlayFromHost'): 	PlayFromHost(url)
	elif (mode=='Search'): 				Search_Site(title=addpr('title',''),url=url,page=page,metamethod=addpr('metamethod','')) #(site,section)
	elif (mode=='iLiveList'): 		iLiveList(addpr('title',''))
	elif (mode=='iLivePlay'): 		iLivePlay(addpr('title',''),url,thumbnail)
	### \/ Testing \/
	#elif (mode=='SearchLast'): 		
	#	Search_Site(title=addst('LastSearchTitle'+SiteTag),url=url,page=page,metamethod=addpr('metamethod',''),endit=tfalse(addpr('endit','true'))) #(site,section)
	#	Search_Site(title=addst('LastSearchTitle'+SiteTag),url=url,page=page,metamethod=addpr('metamethod',''),endit=True) #(site,section)
	elif (mode=='SearchLast'): 		Search_Site(title=addst('LastSearchTitle'+SiteTag),url=url,page=page,metamethod=addpr('metamethod',''),endit=tfalse(addpr('endit','true'))) #(site,section)
	elif (mode=='About'): 				About()
	#
	elif (mode=='LanguageSet'): 	LanguageSet(addpr('language',''))
	elif (mode=='LanguageMenu'): 	LanguageMenu()
	elif (mode=='SSortSet'): 			SSortSet(addpr('sort',''))
	elif (mode=='SSortMenu'): 		SSortMenu()
	elif (mode=='iLiveBrowse'): 	iLiveBrowse(addpr('channel',''),addst('iLive_Sort',''),addst('iLive_Language',''))
	#
	#
	#elif (mode=='FavList'): 			Fav_List(site,section)
	##
	elif (mode=='PlayURL'): 						PlayURL(url)
	elif (mode=='PlayURLs'): 						PlayURLs(url)
	elif (mode=='PlayURLstrm'): 				PlayURLstrm(url)
	elif (mode=='PlayFromHost'): 				PlayFromHost(url)
	elif (mode=='PlayVideo'): 					PlayVideo(url)
	elif (mode=='PlayItCustom'): 				PlayItCustom(url,addpr('streamurl',''),addpr('img',''),addpr('title',''))
	elif (mode=='PlayItCustomL2A'): 		PlayItCustomL2A(url,addpr('streamurl',''),addpr('img',''),addpr('title',''))
	elif (mode=='Settings'): 						_addon.addon.openSettings() # Another method: _plugin.openSettings() ## Settings for this addon.
	elif (mode=='ResolverSettings'): 		import urlresolver; urlresolver.display_settings()  ## Settings for UrlResolver script.module.
	elif (mode=='ResolverUpdateHostFiles'):	import urlresolver; urlresolver.display_settings()  ## Settings for UrlResolver script.module.
	elif (mode=='TextBoxFile'): 				TextBox2().load_file(url,addpr('title','')); #eod()
	elif (mode=='TextBoxUrl'):  				TextBox2().load_url(url,addpr('title','')); #eod()
	elif (mode=='Download'): 						
		try: _addon.resolve_url(url)
		except: pass
		debob([url,addpr('destfile',''),addpr('destpath',''),str(tfalse(addpr('useResolver','true')))])
		DownloadThis(url,addpr('destfile',''),addpr('destpath',''),tfalse(addpr('useResolver','true')))
	elif (mode=='toJDownloader'): 			SendTo_JDownloader(url,tfalse(addpr('useResolver','true')))
	elif (mode=='cFavoritesEmpty'):  	fav__COMMON__empty( site=site,section=section,subfav=addpr('subfav','') ); xbmc.executebuiltin("XBMC.Container.Refresh"); 
	elif (mode=='cFavoritesRemove'):  fav__COMMON__remove( site=site,section=section,subfav=addpr('subfav',''),name=addpr('title',''),year=addpr('year','') )
	elif (mode=='cFavoritesAdd'):  		fav__COMMON__add( site=site,section=section,subfav=addpr('subfav',''),name=addpr('title',''),year=addpr('year',''),img=addpr('img',''),fanart=addpr('fanart',''),plot=addpr('plot',''),commonID=addpr('commonID',''),commonID2=addpr('commonID2',''),ToDoParams=addpr('todoparams',''),Country=addpr('country',''),Genres=addpr('genres',''),Url=url ) #,=addpr('',''),=addpr('','')
	elif (mode=='AddVisit'):							
		try: visited_add(addpr('title')); RefreshList(); 
		except: pass
	elif (mode=='RemoveVisit'):							
		try: visited_remove(addpr('title')); RefreshList(); 
		except: pass
	elif (mode=='EmptyVisit'):						
		try: visited_empty(); RefreshList(); 
		except: pass
	elif (mode=='refresh_meta'):			refresh_meta(addpr('video_type',''),TagAnimeName(addpr('title','')),addpr('imdb_id',''),addpr('alt_id',''),addpr('year',''))
	else: myNote(header='Site:  "'+site+'"',msg=mode+' (mode) not found.'); import mMain
	#

mode_subcheck(addpr('mode',''),addpr('site',''),addpr('section',''),addpr('url',''))
### ############################################################################################################
### ############################################################################################################
