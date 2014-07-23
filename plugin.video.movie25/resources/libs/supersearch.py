import urllib,re,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin,threading
import main

#Mash Up - by Mash2k3 2012.

addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art
cachedir = xbmc.translatePath('special://temp/')

def SEARCHistory():
    dialog = xbmcgui.Dialog()
    if xbmcgui.Window(10000).getProperty('MASH_SSR_TYPE'):
        ret = int(xbmcgui.Window(10000).getProperty('MASH_SSR_TYPE'))-1
    else:
        ret = dialog.select('[B]Choose A Search Type[/B]',['[B]TV Shows[/B]','[B]Movies[/B]'])
    if ret == -1:
        xbmcplugin.endOfDirectory(int(sys.argv[1]), False, False)
    if ret == 0:
        searchType = 'TV'
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistoryTv')
        if not os.path.exists(SeaFile):
            SEARCH('',searchType)
        else:
            main.addDir('Search',searchType,20,art+'/search.png')
            main.addDir('Clear History',SeaFile,128,art+'/cleahis.png')
            thumb=art+'/link.png'
            searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
            for seahis in reversed(searchis):
                seahis=urllib.unquote(seahis)               
                main.addDir(seahis,searchType,20,thumb)
    if ret == 1:
        searchType = 'Movies'
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistory25')
        if not os.path.exists(SeaFile):
            SEARCH('',searchType)
        else:
            main.addDir('Search',searchType,20,art+'/search.png')
            main.addDir('Clear History',SeaFile,128,art+'/cleahis.png')
            thumb=art+'/link.png'
            searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
            for seahis in reversed(searchis):
                seahis=urllib.unquote(seahis)    
                main.addDir(seahis,searchType,20,thumb)

def sortSearchList(searchList,query):
    import locale
    locale.setlocale(locale.LC_ALL, "")
    searchList.sort(key=lambda tup: tup[0].decode('utf-8').encode('utf-8'),cmp=locale.strcoll)
    temp = []
    itemstoremove = []
    i = 0
    if re.search('(?i)s(\d+)e(\d+)',query) or re.search('(?i)Season(.+?)Episode',query) or re.search('(?i)(\d+)x(\d+)',query):
        for item in searchList:
            if re.search('(?i)\ss(\d+)e(\d+)',item[0]) or re.search('(?i)Season(.+?)Episode',item[0]) or re.search('(?i)(\d+)x(\d+)',item[0]):
                temp.append(item)
                itemstoremove.append(i)
            i += 1
    i = 0
    for remove in itemstoremove:
        searchList.pop(remove - i)
        i += 1
    return temp + searchList

def SEARCH(mname,type):
    main.GA("None","SuperSearch")
    try: import Queue as queue
    except ImportError: import queue
    results = []
    searchList=[]
    #mname=main.unescapes(mname)
    mname=main.removeColoredText(mname)
    if mname=='Search': mname=''
    encode = main.updateSearchFile(mname,type)
    if not encode: return False
    else:
        encode = encode.replace('%21','')
        if type=='Movies':
            q = queue.Queue()
            threading.Thread(target=iwatch,args=(encode,type,q)).start()
            results.append(q)
            q = queue.Queue()
            threading.Thread(target=movie25,args=(encode,type,q)).start()
            results.append(q)
            q = queue.Queue()
            threading.Thread(target=icefilms,args=(encode,type,q)).start()
            results.append(q)
            q = queue.Queue()
            threading.Thread(target=watchingnow,args=(encode,type,q)).start()
            results.append(q)
            q = queue.Queue()
            threading.Thread(target=mbox,args=(encode,type,q)).start()
            results.append(q)
            if selfAddon.getSetting('username') != '' and selfAddon.getSetting('password') != '':
                q = queue.Queue()
                threading.Thread(target=noobroom,args=(encode,type,q)).start()
                results.append(q)
            q = queue.Queue()
            threading.Thread(target=tubeplus,args=(encode,type,q)).start()
            results.append(q)
            q = queue.Queue()
            threading.Thread(target=tvrelease,args=(encode,type,q)).start()
            results.append(q)
            q = queue.Queue()
            threading.Thread(target=mynewvideolinks,args=(encode,type,q)).start()
            results.append(q)
            q = queue.Queue()
            threading.Thread(target=sceper,args=(encode,type,q)).start()
            results.append(q)
            q = queue.Queue()
            threading.Thread(target=fma,args=(encode,type,q)).start()
            results.append(q)
            q = queue.Queue()
            threading.Thread(target=scenesource,args=(encode,type,q)).start()
            results.append(q)
        else:
            encodewithoutepi = urllib.quote(re.sub('(?i)(\ss(\d+)e(\d+))|(Season(.+?)Episode)|(\d+)x(\d+)','',urllib.unquote(encode)).strip())
            q = queue.Queue()
            threading.Thread(target=mbox,args=(encodewithoutepi,type,q)).start()
            results.append(q)
            q = queue.Queue()
            threading.Thread(target=watchseries,args=(encodewithoutepi,type,q)).start()
            results.append(q)
            q = queue.Queue()
            threading.Thread(target=iwatch,args=(encodewithoutepi,type,q)).start()
            results.append(q)
            q = queue.Queue()
            threading.Thread(target=icefilms,args=(encodewithoutepi,type,q)).start()
            results.append(q)
            q = queue.Queue()
            threading.Thread(target=tubeplus,args=(encodewithoutepi,type,q)).start()
            results.append(q)
            q = queue.Queue()
            threading.Thread(target=tvrelease,args=(encode,type,q)).start()
            results.append(q)
            q = queue.Queue()
            threading.Thread(target=mynewvideolinks,args=(encode,type,q)).start()
            results.append(q)
            if selfAddon.getSetting('rlsusername') != '' and selfAddon.getSetting('rlspassword') != '':
                q = queue.Queue()
                threading.Thread(target=rlsmix,args=(encode,type,q)).start()
                results.append(q)
            q = queue.Queue()
            threading.Thread(target=scenelog,args=(encode,type,q)).start()
            results.append(q)
            q = queue.Queue()
            threading.Thread(target=sceper,args=(encode,type,q)).start()
            results.append(q)
            q = queue.Queue()
            threading.Thread(target=scenesource,args=(encode,type,q)).start()
            results.append(q)
        for n in range(len(results)):
            searchList.extend(results[n].get())
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Video list is cached.')
        totalLinks = len(searchList)
        loadedLinks = 0
        remaining_display = 'Videos loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        searchList = sortSearchList(searchList,mname)
        wordsorg = set(encode.lower().split("%20"))
        if type == 'TV':
            wordsalt = set(encodewithoutepi.lower().split("%20"))
        for name,section,url,thumb,mode,dir in searchList:
            name = name.strip()+' [COLOR=FF67cc33]'+section+'[/COLOR]'
            name = name.replace('&rsquo;',"'").replace('&quot;','"')
            if type == 'TV' and (section == 'MBox' or section == 'WatchSeries' or section == 'iWatchOnline' or section == 'IceFilms' or section == 'TubePlus'):
                words = wordsalt
            else: words = wordsorg
            if words.issubset(name.lower().split()):
                if dir:
                    if type=='Movies':
                        main.addDirM(name,url,int(mode),thumb,'','','','','')
                    else:
                        if re.search('(?i)\ss(\d+)e(\d+)',name) or re.search('(?i)Season(.+?)Episode',name) or re.search('(?i)(\d+)x(\d+)',name):
                            main.addDirTE(name,url,int(mode),thumb,'','','','','')
                        else:
                            main.addDirT(name,url,int(mode),thumb,'','','','','')
                else:
                    if type=='Movies':
                        main.addPlayM(name,url,int(mode),thumb,'','','','','')
                    else:
                        if re.search('(?i)\ss(\d+)e(\d+)',name) or re.search('(?i)Season(.+?)Episode',name) or re.search('(?i)(\d+)x(\d+)',name):
                            main.addPlayTE(name,url,int(mode),thumb,'','','','','')
                        else:
                            main.addPlayT(name,url,int(mode),thumb,'','','','','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Videos loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if dialogWait.iscanceled(): return False    
        dialogWait.close()
        del dialogWait
        if type=='Movies':
            xbmcgui.Window(10000).setProperty('MASH_SSR_TYPE', '2')
        else: xbmcgui.Window(10000).setProperty('MASH_SSR_TYPE', '1')
        try:
            filelist = [ f for f in os.listdir(cachedir) if f.endswith(".fi") ]
            for f in filelist: os.remove(os.path.join(cachedir,f))
        except:pass
        if not loadedLinks:
            xbmc.executebuiltin("XBMC.Notification(Super Search - "+encode.replace("%20"," ")+",No Results Found,3000)")
            xbmcplugin.endOfDirectory(int(sys.argv[1]), False, False) 
            return False

def movie25(encode,type,q):
    from resources.libs import movie25
    returnList = movie25.superSearch(encode,type)
    if q: q.put(returnList)
    return returnList

def iwatch(encode,type,q):
    from resources.libs.plugins import iwatchonline
    returnList = iwatchonline.superSearch(encode,type)
    if q: q.put(returnList)
    return returnList
        
def icefilms(encode,type,q):
    from resources.libs.movies_tv import icefilms
    returnList = icefilms.superSearch(encode,type)
    if q: q.put(returnList)
    return returnList

def watchingnow(encode,type,q):
    from resources.libs.plugins import extramina
    returnList = extramina.superSearch(encode,type)
    if q: q.put(returnList)
    return returnList

def fma(encode,type,q):
    from resources.libs.plugins import fma
    returnList = fma.superSearch(encode,type)
    if q: q.put(returnList)
    return returnList

def noobroom(encode,type,q):
    from resources.libs.movies_tv import starplay
    returnList = starplay.superSearch(encode,type)
    if q: q.put(returnList)
    return returnList

def tubeplus(encode,type,q):
    from resources.libs.plugins import tubeplus
    returnList = tubeplus.superSearch(encode,type)
    if q: q.put(returnList)
    return returnList

def tvrelease(encode,type,q):
    from resources.libs.plugins import tvrelease
    returnList = tvrelease.superSearch(encode,type)
    if q: q.put(returnList)
    return returnList

def watchseries(encode,type,q):
    from resources.libs.plugins import watchseries
    returnList = watchseries.superSearch(encode,type)
    if q: q.put(returnList)
    return returnList

def mynewvideolinks(encode,type,q):
    from resources.libs.movies_tv import newmyvideolinks
    returnList = newmyvideolinks.superSearch(encode,type)
    if q: q.put(returnList)
    return returnList

def rlsmix(encode,type,q):
    from resources.libs.movies_tv import rlsmix
    returnList = rlsmix.superSearch(encode,type)
    if q: q.put(returnList)
    return returnList

def scenelog(encode,type,q):
    from resources.libs.movies_tv import scenelog
    returnList = scenelog.superSearch(encode,type)
    if q: q.put(returnList)
    return returnList

def sceper(encode,type,q):
    from resources.libs.plugins import sceper
    returnList = sceper.superSearch(encode,type)
    if q: q.put(returnList)
    return returnList

def mbox(encode,type,q):
    from resources.libs.plugins import mbox
    returnList = mbox.superSearch(encode,type)
    if q: q.put(returnList)
    return returnList

def scenesource(encode,type,q):
    from resources.libs.plugins import scenesource
    returnList = scenesource.superSearch(encode,type)
    if q: q.put(returnList)
    return returnList
