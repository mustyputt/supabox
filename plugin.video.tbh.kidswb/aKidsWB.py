### ############################################################################################################
###	#	
### # Site: 				#		Kids WB - http://www.kidswb.com/
### # Author: 			#		The Highway
### # Description: 	#		
###	#	
### ############################################################################################################
### ############################################################################################################
### Imports ###
import xbmc
import os,sys,string,StringIO,logging,random,array,time,datetime,re
import urllib,urllib2,xbmcaddon,xbmcplugin,xbmcgui
from common import *
from common import (_addon,_artIcon,_artFanart,_addonPath)
### ############################################################################################################
### ############################################################################################################
SiteName='[COLOR blue]Kids[/COLOR] [COLOR red][B]WB[/B][/COLOR]  [v0.0.1]  [Cartoons]'
SiteTag='kidswb.com'
mainSite='http://staticswf.kidswb.com/'
mainSite2='http://www.kidswb.com'
iconSite='http://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/KidsWB.svg/593px-KidsWB.svg.png' #'http://images2.wikia.nocookie.net/__cb20110630033115/logopedia/images/1/12/KidsWBLogo.gif' #_artIcon
fanartSite='http://static.kidswb.com/franchise/backgroundTakeovers/KWB_1.jpg' #_artFanart
colors={'0':'white','1':'red','2':'blue','3':'green','4':'yellow','5':'orange','6':'lime','7':'','8':'cornflowerblue','9':'blueviolet','10':'hotpink','11':'pink','12':'tan'}

CR='[CR]'
MyAlphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
MyBrowser=['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3']

workingUrl=mainSite+'ram.pls'
### ############################################################################################################
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
		m+=CR+'Live Streams (RTMPE)'
		m+=CR+CR+'Features:  '
		m+=CR+'* Browse Shows'
		m+=CR+'* Browse Episodes'
		m+=CR+'* Browse Bit-rates'
		m+=CR+'* Play Videos'
		m+=CR+CR+'Notes:  '
		#m+=CR+'* '
		#m+=CR+'* '
		m+=CR+''
		m+=CR+ps('ReferalMsg')
		m+=CR+''
		m+=CR+''
		m+=CR+''
	String2TextBox(message=cFL(m,'cornflowerblue'),HeaderMessage=head)
	#RefreshList()
def spAfterSplit(t,ss):
	if ss in t: t=t.split(ss)[1]
	return t
def spBeforeSplit(t,ss):
	if ss in t: t=t.split(ss)[0]
	return t
### ############################################################################################################
### ############################################################################################################
def GetMedia(VideoID,title='',url='',img=iconSite):
	html=messupText(nURL('http://metaframe.digitalsmiths.tv/v2/WBtv/assets/'+VideoID+'/partner/11?format=json'),True)
	s='"length": (\d+), "bitrate": "(.+?)", "uri": "(.+?://.+?)"'; matches=re.compile(s).findall(nolines(html)); deb('# of matches found',str(len(matches))); #debob(matches)
	for (_length,_name,_url) in matches:
		labs={'title':title+' - ['+_name+']'}
		try: _addon.add_directory({'mode':'PlayVideo','img':img,'studio':'['+_name+']','url':_url,'title':title,'site':site},labs,is_folder=False,fanart=fanartSite,img=img)
		except: pass
	set_view('list',view_mode=addst('default-view')); eod()

def ListEpisodes(url,title):
	html=messupText(nURL(url),True); deb('length of html',str(len(html))); #debob(html)
	html=spAfterSplit(html,'<ul id="videoList_ul">'); html=spBeforeSplit(html,'</ul>'); 
	if len(html)==0: return
	s='<li class="vidItem \D+" id="video_(.+?)">\s*\n*\s*<div class="vidThumbContain">\s*\n*\s*<a id="vidlink_.+?" class="vidThumbLink" href="(/video/.+?/.+?/.+?)"></a>\s*\n*\s*<div class="vidThumbOverlay \D+"></div>\s*\n*\s*'
	s+='<img id="vidthumb_.+?" src="(http://cdn.wwtv.warnerbros.com/wbtv/channels/thumbs/\d\d\d\d/\d\d/\d\d/.+?.jpg)" height="\d+" width="\d+"/>\s*\n*\s*'
	s+='</div>\s*\n*\s*<div class="vidInfo">\s*\n*\s*<p class="vidtitle"><span id=".+?">(.*?)</span> - (.*?)</p>\s*\n*\s*\n*\s*\n*\s*<p id=".+?">\s*(.*?)\s*...</p>\s*\n*\s*<p id=".+?" style="display:none;">\s*(.*?)\s*...</p>\s*\n*\s*\n*\s*\n*\s*<div class="vidMoreLess"><a id=".+?" href="#">more</a></div>\s*\n*\s*\n*\s*\n*\s*</div>\s*\n*\s*</li>'
	s='<li class="vidItem \D+" id="video_.+?">(.+?)</li>'
	matches=re.compile(s).findall(nolines(html)); deb('# of matches found',str(len(matches))); #debob(matches)
	if len(matches)==0: return
	#for (idtag,_url,img,episodetitle,showtitle,plotoutline,plot) in matches:
	for match in matches:
		labs={}; labs['plot']=''; labs['plotoutline']=''; labs['showtitle']=''; labs['episodetitle']=''; labs['videoid']=''; 
		try: labs['videoid']+=re.compile('<a id="vidlink_(.+?-.+?-.+?-.+?-.+?)"').findall(match)[0]
		except: pass
		try: img=re.compile('<img id="vidthumb_.+?" src="(http://.+?.jpg)"').findall(match)[0]
		except: img=iconSite
		_url=mainSite2+re.compile('<a id="vidlink_.+?" class="vidThumbLink" href="(/video/.+?/.+?/.+?)">').findall(match)[0]
		try: labs['showtitle']+=re.compile('<div class="vidInfo">\s*\n*\s*<p class="vidtitle"><span id="vidtitle_.+?">\s*.*?\s*</span>\s*-\s*(.*?)</p>').findall(match)[0]
		except: pass
		try: labs['episodetitle']+=re.compile('<div class="vidInfo">\s*\n*\s*<p class="vidtitle"><span id="vidtitle_.+?">\s*(.*?)\s*</span>\s*-\s*.*?</p>').findall(match)[0]
		except: pass
		try: labs['plotoutline']+=re.compile('<p id="viddesctrunc_.+?">(.*?)</p>').findall(match)[0]
		except: pass
		try: labs['plot']+=re.compile('<p id="viddesc_.+?" style="display:none;">(.*?)</p>').findall(match)[0]
		except:
			try: labs['plot']+=re.compile('<p id="viddesc_.+?">(.*?)</p>').findall(match)[0]
			except: pass
		#debob([_url,img,labs])
		if (len(labs['showtitle'])==0) or (len(labs['episodetitle'])==0) or (len(img)==0) or (len(_url)==0): pass
		else:
			labs['title']=cFL(labs['episodetitle'],colors['0'])+CR+cFL(labs['showtitle'],colors['5'])
			try: _addon.add_directory({'mode':'GetMedia','img':img,'videoid':labs['videoid'],'url':_url,'title':labs['showtitle']+' - '+labs['episodetitle'],'site':site},labs,is_folder=True,fanart=fanartSite,img=img)
			except: pass
	set_view('episodes',view_mode=addst('episode-view')); eod()

def ListShows():
	html=messupText(nURL(mainSite2+'/video'),True); deb('length of html',str(len(html))); #debob(html)
	html=spAfterSplit(html,'<ul id="channelCarousel_ul">'); html=spBeforeSplit(html,'</ul>'); 
	if len(html)==0: return
	s='<li class="channelCarousel_li channelCarousel_li_\d+ rollover">\s*\n*\s*'
	s+='<a href="(/video/.+?)" title=".*?">\s*\n*\s*'
	#s+='<img height="80" width="95" border="0" alt="(.*?)" src="(/images/touts/video_channel_thumbs/.+?.jpg)"/>\s*\n*\s*</a>\s*\n*\s*</li>'
	s+='<img height="\d+" width="\d+" border="0" alt="(.*?)" src="(/images/touts/video_channel_thumbs/.+?.jpg)"/>\s*\n*\s*</a>\s*\n*\s*</li>'
	matches=re.compile(s).findall(html); deb('# of matches found',str(len(matches))); #debob(matches)
	if len(matches)==0: return
	for (_url,_name,img) in matches:
		img=mainSite2+img; _url=mainSite2+_url; #debob([_name,_url,img]); 
		_title=cFL_(_name,colors['5'])
		try: _addon.add_directory({'mode':'ListEpisodes','url':_url,'title':_name,'site':site},{'title':_title},is_folder=True,fanart=fanartSite,img=img)
		except: pass
	set_view('tvshows',view_mode=addst('tvshows-view')); eod()

### ############################################################################################################
### ############################################################################################################
def SectionMenu():
	_addon.add_directory({'mode':'About','site':site},{'title':cFL_('About',colors['9'])},is_folder=False,fanart=fanartSite,img='http://i.imgur.com/0h78x5V.png') # iconSite
	_addon.add_directory({'mode':'ListShows','site':site},{'title':cFL_('Cartoon List',colors['5'])},is_folder=True,fanart=fanartSite,img=iconSite)
	###
	set_view('list',view_mode=addst('default-view')); eod()
### ############################################################################################################
### ############################################################################################################
def mode_subcheck(mode='',site='',section='',url=''):
	deb('mode',mode); 
	if (mode=='SectionMenu'): 		SectionMenu()
	elif (mode=='') or (mode=='main') or (mode=='MainMenu'): SectionMenu()
	elif (mode=='SubMenu'): 			SubMenu()
	elif (mode=='NowPlaying'): 		NowPlaying()
	elif (mode=='ListAZ'): 				ListAZ()
	elif (mode=='List'): 					Browse_List(addpr('title',''))
	elif (mode=='DoRequest'): 		DoRequest(url,addpr('title',''))
	elif (mode=='ListShows'): 		ListShows()
	elif (mode=='ListEpisodes'): 	ListEpisodes(url,addpr('title',''))
	elif (mode=='GetMedia'): 			GetMedia(addpr('videoid',''),addpr('title',''),url,addpr('img',''))
	#elif (mode=='Hosts'): 				Browse_Hosts(url)
	#elif (mode=='Search'): 				Search_Site(title=addpr('title',''),url=url,page=page,metamethod=addpr('metamethod','')) #(site,section)
	#elif (mode=='SearchLast'): 		Search_Site(title=addst('LastSearchTitle'+SiteTag),url=url,page=page,metamethod=addpr('metamethod',''),endit=tfalse(addpr('endit','true'))) #(site,section)
	elif (mode=='About'): 				About()
	#elif (mode=='FavoritesList'): Fav_List(site=site,section=section,subfav=addpr('subfav',''))
	elif (mode=='SlideShowStart'): path = os.path.join(_addonPath, 'c_SlideShow.py'); xbmc.executebuiltin('XBMC.RunScript(%s)' % path)
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
