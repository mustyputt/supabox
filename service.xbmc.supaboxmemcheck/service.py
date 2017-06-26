#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2013 Team-XBMC
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#



import platform,urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,shutil,time,extract,xbmcaddon, os, sys
import xbmc
import plugintools
import datetime
import texturecache,sqlite3
import lib.common

import xbmcvfs, glob
from datetime import datetime
try:    from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database

from lib.common import log, dialog_yesno
from lib.common import upgrade_message as _upgrademessage
from lib.common import upgrade_message2 as _upgrademessage2
from addon.common.addon import Addon
from addon.common.net import Net
ADDON        = lib.common.ADDON
ADDONVERSION = lib.common.ADDONVERSION
ADDONNAME    = lib.common.ADDONNAME
ADDONPATH    = lib.common.ADDONPATH
ICON         = lib.common.ICON
oldversion = False

AddonTitle="Maintenance Tool"
addon_id='service.xbmc.supaboxmemcheck'
local=xbmcaddon.Addon(id=addon_id); maintenancepath=xbmc.translatePath(local.getAddonInfo('path'))
clear_hour=local.getSetting('clear_hour')
free_mem=local.getSetting('free_mem')
clear_check=local.getSetting('clear_check')
art=maintenancepath+'/art'
supaboxUrl='http://172.13.129.150/'
mainurl=supaboxUrl+'tools/'
databaseFolder    = xbmc.translatePath( "special://database" )
thumbnailsFolder  = xbmc.translatePath( "special://thumbnails" )
addonsFolder = xbmc.translatePath( "special://addons" )
class RawXBMC():
     @staticmethod
     def Query( Query ):
	  RawXBMCConnect = ConnectToXbmcDb()
	  Cursor = RawXBMCConnect.cursor()
	  Cursor.execute( Query )
	  Matches = []
	  for Row in Cursor: Matches.append( Row )
	  RawXBMCConnect.commit()
	  Cursor.close()
	  return Matches

     @staticmethod
     def Execute( Query ):
        return RawXBMC.Query( Query )

def ConnectToXbmcDb():
     dbHost = os.path.join( databaseFolder, "Textures13.db" )
     return sqlite3.connect( dbHost )

class Main:
    def __init__(self):
        self.WINDOW = xbmcgui.Window(10000)
        self._init_vars()
        self.WINDOW.clearProperty('LibraryDataProvider_Running')
        self.WINDOW.setProperty('LibraryDataProvider_Running', 'true')
        self._daemon()

    def _init_vars(self):
        self.WINDOW = xbmcgui.Window(10000)
        
        self.Monitor = Widgets_Monitor(update_listitems=self._update)

    def _daemon(self):
        # deamon is meant to keep script running at all time
        while not self.Monitor.abortRequested() and self.WINDOW.getProperty('LibraryDataProvider_Running') == 'true':
            if self.Monitor.waitForAbort(1):
                    # Abort was requested while waiting. We should exit
                    break
            if not xbmc.Player().isPlayingVideo():
                self._fetch_random()
                    
    def _fetch_random(self):  
        free_mem=local.getSetting('free_mem')
        clear_check=local.getSetting('clear_check')    
        freespace = xbmc.getInfoLabel('system.memory(free)').split('MB')
        if ((int(freespace[0])) < (int(free_mem))): 
            #dialog = xbmcgui.Dialog()
            #dialog.ok(AddonTitle, "int freespace is:" + (freespace[0])+"<" + free_mem)
            xbmc.executebuiltin("Notification(Time to clear memory,Working....,10000)")
            CLEARCACHE2()
        check_stats()
        SETICONS()
        xbmc.sleep(int(clear_check)*60000)
        
    def _update(self, type):
        xbmc.sleep(1000)

class Widgets_Monitor(xbmc.Monitor):
    def __init__(self, *args, **kwargs):
        xbmc.Monitor.__init__(self)
        self.update_listitems = kwargs['update_listitems']


def OPEN_URL(url): req=urllib2.Request(url); req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'); response=urllib2.urlopen(req); link=response.read(); response.close(); return link

def _versioncheck():
    # initial vars
    from lib.jsoninterface import get_installedversion, get_versionfilelist
    from lib.versions import compare_version
    # retrieve versionlists from supplied version file
    versionlist = get_versionfilelist()
    # retrieve version installed
    version_installed = get_installedversion()
    # copmpare installed and available
    oldversion, version_installed, version_available, version_stable = compare_version(version_installed, versionlist)
    return oldversion, version_installed, version_available, version_stable


def CLEARCACHE():
    print '###CLEARING CACHE FILES###'
    xbmc_cache_path = os.path.join(xbmc.translatePath('special://home'),'userdata','Thumbnails')
    if os.path.exists(xbmc_cache_path)==True:    
        for root, dirs, files in os.walk(xbmc_cache_path):
            file_count = 0
            file_count += len(files)
            #print '###'+AddonTitle+'past file count'+root+dirs+files
            if file_count > 0:
                    #print '###'+AddonTitle+'past file count'+root+dirs+files
               # dialog = xbmcgui.Dialog()
                #if dialog.yesno("Delete XBMC Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        try:
                            os.unlink(os.path.join(root, f))
                            plugintools.log("deleting file: "+f)
                        except:
                            pass
                    for d in dirs:
                        try:
                            plugintools.log("deleting folder: "+d)
                            shutil.rmtree(os.path.join(root, d))
                            plugintools.log("deleting folder: "+d)
                        except:
                            pass
                            
                        
            else:
                pass                          


    try:
        RawXBMC.Execute( "DELETE FROM texture" )
    finally:
        plugintools.log("texturecache failed ")
        pass
    dialog = xbmcgui.Dialog()
    dialog.ok(AddonTitle, "       Done Clearing Cache files")
    PURGEPACKAGES();
    
################################
###     End Clear Cache      ###
################################
    
    ################################
###       Clear Cache   2     ###
################################
  
def CLEARCACHE2():
    print '###CLEARING CACHE FILES###'
    xbmc_cache_path = os.path.join(xbmc.translatePath('special://home'),'userdata','Thumbnails')
    freespace = xbmc.getInfoLabel('system.memory(free)').split('M')
    #dialog = xbmcgui.Dialog()
    #dialog.ok(AddonTitle, "home folder is: "+freespace[0])
    #xbmc.executebuiltin("Notification(Free memory before:,\'+freespace[0]+\',10000)")
    if os.path.exists(xbmc_cache_path)==True: 
        #dp = xbmcgui.DialogProgress()
        #dp.create(AddonTitle,"Clearing Cache",'')
   
        for root, dirs, files in os.walk(xbmc_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    try:
                        os.unlink(os.path.join(root, f))
                        plugintools.log("deleting file: "+f)
                    except:
                        pass                      
            else:
                pass                          
            
    xbmc_cache_path = os.path.join(xbmc.translatePath('special://home'))
    #dialog = xbmcgui.Dialog()
    #dialog.ok(AddonTitle, "home folder is: "+xbmc_cache_path)
    if os.path.exists(xbmc_cache_path)==True:    
        for the_file in os.listdir(xbmc_cache_path):
            file_path = os.path.join(xbmc_cache_path, the_file)
            try:
                if os.path.isfile(file_path):
                    #dialog = xbmcgui.Dialog()
                    #dialog.ok(AddonTitle, "deleting file is: "+file_path)
                    os.unlink(file_path)
                
            except Exception, e:
                print e                
    try:
        RawXBMC.Execute( "DELETE FROM texture" )
    finally:
        plugintools.log("texturecache failed ")
        #pass
        #dialog = xbmcgui.Dialog()
        #dialog.ok(AddonTitle, "       Done Clearing Cache files")
    PURGEPACKAGES();
    xbmc.executebuiltin("Notification(Memory Cleared,All Set!!,10000)")
    #dialog = xbmcgui.Dialog()
    #dialog.ok("Supabox Message","Free memory after: " + xbmc.getInfoLabel('system.memory(free)'))
    xbmc.executebuiltin("XBC.ActivateWindow(Programs)");
################################
###     End Clear Cache  2    ###
################################

################################
###     Purge Packages       ###
################################
    
def PURGEPACKAGES():
    print '###'+AddonTitle+' - DELETING PACKAGES###'
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
    #dialog = xbmcgui.Dialog()
    #dialog.ok(AddonTitle, packages_cache_path)
    try:    
        for root, dirs, files in os.walk(packages_cache_path):
            file_count = 0
            file_count += len(files)
            
        # Count files and give option to delete
            if file_count > 0:
    
               # dialog = xbmcgui.Dialog()
                #if dialog.yesno("Delete Package Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                            
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                    #dialog = xbmcgui.Dialog()
                    #dialog.ok(AddonTitle, "       Deleting Packages all done")
               # else:
                #        pass
            #else:
                #dialog = xbmcgui.Dialog()
                #dialog.ok(AddonTitle, "       No Packages to Purge")
    except: 
        #dialog = xbmcgui.Dialog()
        print '###'+AddonTitle+' - DELETING PACKAGES###'
        #dialog.ok(AddonTitle, "Error Deleting Packages.")
        
################################
###    End Purge Packages    ###
################################

################################
###      Addon Installer     ###
################################
def ADDONINSTALLER(urln,state):
    if state == 1 :
        path=os.path.join(xbmc.translatePath('special://home'),'..','..','..','..','..','downloads')       
        url=supaboxUrl+'app/'+urln+'.zip'; lib=os.path.join(path, urln+'.zip'); DownloaderClass(url,lib)
        time.sleep(10)
        dp=xbmcgui.DialogProgress(); print '=== INSTALLING ADDON INSTALLER ==='; dp.create(AddonTitle,"Extracting Zip Please Wait")
        extract.all(lib,path,dp)
        os.remove(lib)
        addoninstalled(urln)
    else:
        pluginpath=os.path.exists(xbmc.translatePath(os.path.join('special://home','addons',urln)))
        if (pluginpath and state != 2): return #xbmc.executebuiltin("RunAddon("+urln+")")
        else:
            url=supaboxUrl+'app/'+urln+'.zip'; path=xbmc.translatePath(os.path.join('special://home','addons','packages')); lib=os.path.join(path, urln+'.zip'); DownloaderClass(url,lib)
            #dialog = xbmcgui.Dialog()
            #dialog.ok(AddonTitle, "url:"+url+" lib:"+lib)
            time.sleep(3)
            addonfolder=xbmc.translatePath(os.path.join('special://home','addons','')); dp=xbmcgui.DialogProgress(); print '=== INSTALLING ADDON INSTALLER ==='; dp.create(AddonTitle,"Extracting Zip Please Wait")
            extract.all(lib,addonfolder,dp); xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
            addoninstalled(urln)
################################
###    End Addon Installer   ###
################################

def addoncheck(url):
    path=os.path.join(xbmc.translatePath('special://home'),'userdata',url+'.ok')
    if not os.path.exists(path): 
        return False
    else:
        return True

def addonstatuscheck(url):
    path=os.path.join(xbmc.translatePath('special://home'),'userdata',url+'.ok')
    if os.path.exists(path): 
        os.remove(path)
        addonremoved(url)
     
def addondelcheck(url):
    path=os.path.join(xbmc.translatePath('special://home'),'userdata',url+'.deleted')
    #path=os.path.join(xbmc.translatePath('special://home'),'userdata',url+'.ok')
    if os.path.exists(path): 
        return False
    else:
        return True
       
def addonremoved(url):
    path=os.path.join(xbmc.translatePath('special://home'),'userdata',url+'.ok')
    path2=os.path.join(xbmc.translatePath('special://home'),'userdata',url+'.deleted')
    #dialog = xbmcgui.Dialog()
    #dialog.ok(AddonTitle, "deleted:"+url)
    if not os.path.exists(path): 
        time.sleep(1)
    else:
        os.remove(path)
    f=open(path2,mode='w'); 
    f.write('ADDON INSTLLAER####   '+url+' addon deleted');
    f.close(); 
       

def addoninstalled(url):
    path=os.path.join(xbmc.translatePath('special://home'),'userdata',url+'.ok')
    path2=os.path.join(xbmc.translatePath('special://home'),'userdata',url+'.deleted')
    if not os.path.exists(path): 
        f=open(path,mode='w'); 
        f.write('ADDON INSTLLAER####   '+url+' addon loaded');
        f.close();
    if os.path.exists(path2): 
        os.remove(path2) 
       
################################
###    Check Addon Installer status  ###
################################
debug=0
def check_stats():
    totadd = 0
    totremove = 0
    xbmc.executebuiltin("Notification(Checking Status,........,2000)")
    
    
    try:
        if (debug):
            url="service.xbmc.supaboxmemcheck\update.txt"
            path=os.path.join(xbmc.translatePath('special://home'),'addons',url)
            
            f=open(path).read();
        
            link=f.replace('\n','').replace('\r','')
           
            #f.close();
          
        else:
            link=OPEN_URL('http://172.13.129.150/app/updateaddon.txt').replace('\n','').replace('\r','')
        
        shorts=re.compile('addon="(.+?)".+?tatus="(.+?)".+?ype="(.+?)"').findall(link)
        for addon, status, type in shorts:
            plugintools.log(addon)
            plugintools.log(status)
            if status == "add":
                totadd = totadd + 1
            if status == "remove":
                totremove = totremove + 1
        for addon, status, type in shorts:
            #dialog = xbmcgui.Dialog()
            #dialog.ok(AddonTitle, "addstatus:"+status+" addname:"+addon)
            if status == "apk":
                #xbmc.executebuiltin("Notification(Update Status,updading:"+addon+",2000)")
                ADDONINSTALLER(addon,1)
                enableAddons()
            if status == "update":
                if not addoncheck(addon):
                    #xbmc.executebuiltin("Notification(Update Status,updading:"+addon+",2000)")
                    ADDONINSTALLER(addon,2)
                    enableAddons()
            if status == "add":
                if not addoncheck(addon):
                    #xbmc.executebuiltin("Notification(Update Status,updading:"+addon+",2000)")
                    ADDONINSTALLER(addon,0)
                    enableAddons()
            if status == "remove":
                if addondelcheck(addon):
                    #xbmc.executebuiltin("Notification(Update Status,Removing:"+addon+",2000)")
                    FINDADDON(type,addon)
                    #enableAddons()
            if status == "delete":
                addonstatuscheck(addon)
    except:
        xbmc.executebuiltin("Notification(Update Status,No updates,10000)")
    xbmc.executebuiltin("XBMC.UpdateLocalAddons()")    
    #if (totadd > 0 or totremove > 0):
        #dialog = xbmcgui.Dialog()
        #dialog.ok(AddonTitle, "Adding:"+str(totadd)+" Removing:"+str(totremove))
      

################################
###    Check Addon Installer status  ###
################################



################################
###       Addon Removal      ###
################################
        
def FINDADDON(url,name):  
    print '###'+AddonTitle+' - ADDON REMOVAL###'
    pluginpath = xbmc.translatePath(os.path.join('special://home/addons',''))
    nameComp=str(name).replace(pluginpath,'').replace('plugin.','').replace('service.','').replace('audio.','').replace('video.','').replace('skin.','').replace('repository.','').replace('program.','').replace('image.','').replace('script.','')
    for file in os.listdir(pluginpath):
        if url in file:
                file = pluginpath+file; #print file; 
                if os.path.isfile(os.path.join(file,'addon.xml'))==True:
                    try:
                        html=nolines(File_Open(os.path.join(file,'addon.xml'))); #print str(len(html)); 
                        name2=re.compile('<addon\s*.*?\s+name="(.+?)"\s*.*?>').findall(html)[0]
                    #print name
                    except:
                        try: name2=re.compile("<addon\s*.*?\s+name='(.+?)'\s*.*?>").findall(html)
                        except: name2=str(file).replace(pluginpath,'').replace('plugin.','').replace('service.','').replace('audio.','').replace('video.','').replace('skin.','').replace('repository.','').replace('program.','').replace('image.','').replace('script.','')
                else: name2=str(file).replace(pluginpath,'').replace('plugin.','').replace('service.','').replace('audio.','').replace('video.','').replace('skin.','').replace('repository.','').replace('program.','').replace('image.','').replace('script.','')
                iconimage=(os.path.join(file,'icon.png'))
                fanart=(os.path.join(file,'fanart.jpg'))
                #dialog = xbmcgui.Dialog()
                #dialog.ok(AddonTitle, "nameComp:"+nameComp+" name2:"+name2)
                if nameComp == name2:
                    try: REMOVEADDON2(name,file)
                    except:
                        name2=str(file).replace(pluginpath,'').replace('plugin.','').replace('service.','').replace('audio.','').replace('video.','').replace('skin.','').replace('repository.','').replace('program.','').replace('image.','').replace('script.','')
                        REMOVEADDON2(name,file)

def REMOVEADDON(url):   
    dialog = xbmcgui.Dialog()
    if dialog.yesno(AddonTitle, '', "Do you want to Remove this Addon?"+url):
        for root, dirs, files in os.walk(url):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                dialog = xbmcgui.Dialog()
                if dialog.yesno(AddonTitle, '', "Do you want to Remove this Addon?"+url):
                    shutil.rmtree(os.path.join(root, d),0)
        os.rmdir(url)
        xbmc.executebuiltin('Container.Refresh')

def REMOVEADDON2(name,path):
    # check if folder exists
    if os.path.exists(path):
         # remove if exists
         shutil.rmtree(path)
    #xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
    #dialog = xbmcgui.Dialog()
    #dialog.ok(AddonTitle, "nameComp:"+name+" name2:"+path)
    addonremoved(name)
    #dialog = xbmcgui.Dialog()
    #dialog.ok("ADDONS UPDATE", "Non-Functional Addons have been deleted.  Please restart Supabox Media.  Press the HOME button on your remote")
################################
###     End Addon Removal    ###
################################
        
def addDir(name,url,mode,iconimage,fanart):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart); ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage); liz.setInfo(type="Video",infoLabels={"Title":name,"Plot":name}); liz.setProperty("Fanart_Image",fanart)
    if mode==3 or mode==9 or mode==6 or mode==15 or mode==17 or mode==21 or mode==23 or mode==28 or mode==42 or mode==37 or mode==38 or mode==25 or mode==32 or mode==33 or mode==34 or mode==35 or mode==22 or mode==19 or mode==26 or mode==18 or mode==16 or mode==27 or mode==5 or mode==61 or mode==62 or mode==63:
          ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    else: ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def DownloaderClass(url,dest, useReq = True):
    dp = xbmcgui.DialogProgress()
    dp.create(AddonTitle,"Downloading & Copying File",'')

    if useReq:
        import urllib2
        req = urllib2.Request(url)
        req.add_header('Referer', 'http://172.13.129.150/')
        f       = open(dest, mode='wb')
        resp    = urllib2.urlopen(req)
        content = int(resp.headers['Content-Length'])
        size    = content / 100
        total   = 0
        while True:
            if dp.iscanceled(): 
                raise Exception("Canceled")                
                dp.close()

            chunk = resp.read(size)
            if not chunk:            
                f.close()
                break

            f.write(chunk)
            total += len(chunk)
            percent = min(100 * total / content, 100)
            dp.update(percent)       
    else:
        urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))

def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        dp.update(percent)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled(): 
        raise Exception("Canceled")
        dp.close()

def DownloaderClass2(url,dest):
    #url1=url.split('@')[1]; url=url.split('@')[0]; name=url.replace(url1,''); useReq=False;  path=os.path.join(xbmc.translatePath('special://home'),'..','..','..','..','..','downloads'); dest=os.path.join(path,name)
    dp=xbmcgui.DialogProgress(); dp.create(AddonTitle,"Downloading & Copying File",'')
    print( "url:"+url+" url1:"+url+" path:" +path+" dest: "+dest)    
    if useReq:
        print( "use req is used")
        import urllib2; req=urllib2.Request(url); req.add_header('Referer', 'http://andersonflagg.com/'); f=open(dest, mode='wb'); resp=urllib2.urlopen(req); content=int(resp.headers['Content-Length']); size=content / 100; total=0
        #print( url1+" : "+url+" content:" +content+" size: "+size)  
        while True:
            if dp.iscanceled(): raise Exception("Canceled"); dp.close()
            chunk=resp.read(size)
            if not chunk: f.close(); break
            f.write(chunk); total+=len(chunk); percent=min(100 * total / content,100); dp.update(percent)       
    else: 
        print( "use req is NOT used")
        #test=urllib.urlretrieve(url,dest)

def _pbhook2(numblocks,blocksize,filesize,url=None,dp=None):
    try: percent=min((numblocks*blocksize*100)/filesize,100); dp.update(percent)
    except: percent=100; dp.update(percent)
    if dp.iscanceled():  dp.close(); pass


def SETICONS():
    link=OPEN_URL('http://172.13.129.150/shortcut/shortcuts.txt')
    shorts=re.compile('shortcut="(.+?)"').findall(link)
    for shortname in shorts: xbmc.executebuiltin("Skin.SetString(%s)" % shortname)
    #CLEARCACHE2('url');


def enableAddons():
	class enableAll():
		def __init__(self):
			self.databasepath = xbmc.translatePath('special://database/')
			self.addons       = xbmc.translatePath('special://home/addons/')
			self.dbfilename   = self.latestDB()
			self.dbfilename   = os.path.join(self.databasepath, self.dbfilename)
			if not os.path.exists(os.path.join(self.databasepath, self.dbfilename)):
				xbmc.sleep(2000)
				xbmcgui.Dialog().notification("AutoExec.py", "No Addons27.db file")
				self.log("DB File not found.")
				return False
			
			self.addonlist = glob.glob(os.path.join(self.addons, '*/'))
			self.disabledAddons = []
			for folder in sorted(self.addonlist, key = lambda x: x):
				addonxml = os.path.join(folder, 'addon.xml')
				if os.path.exists(addonxml):
					fold   = folder.replace(self.addons, '')[1:-1]
					f      = open(addonxml)
					a      = f.read()
					aid    = parseDOM(a, 'addon', ret='id')
					f.close()
					try:
						if len(aid) > 0: add = aid[0]
						else: add = fold
						xadd    = xbmcaddon.Addon(id=add)
					except:
						try:
							self.disabledAddons.append(add)
						except:
							self.log("Unabled to enable: %s" % folder, xbmc.LOGERROR)
			if len(self.disabledAddons) > 0:
				self.addonDatabase(self.disabledAddons, 1, True)
			xbmc.executebuiltin('UpdateAddonRepos()')
			xbmc.executebuiltin('UpdateLocalAddons()')
			xbmc.executebuiltin("ReloadSkin()")
			
		def log(self, msg, level=xbmc.LOGNOTICE):
			try:
				if isinstance(msg, unicode):
					msg = '%s' % (msg.encode('utf-8'))
				#xbmc.log('[AutoExec.py]: %s' % msg, level)
			except Exception as e:
				try: xbmc.log('[AutoExec.py] Logging Failure: %s' % (e), xbmc.LOGERROR)
				except: pass
			
		def latestDB(self, DB="Addons"):
			match = glob.glob(os.path.join(self.databasepath,'%s*.db' % DB))
			comp = '%s(.+?).db' % DB[1:]
			highest = 0
			for file in match:
				try: check = int(re.compile(comp).findall(file)[0])
				except Exception, e: check = 0; self.log(str(e))
				if highest < check:
					highest = check
			return '%s%s.db' % (DB, highest)
		
		def addonDatabase(self, addon=None, state=1, array=False):
			installedtime = str(datetime.now())[:-7]
			if os.path.exists(self.dbfilename):
				try:
					textdb = database.connect(self.dbfilename)
					textexe = textdb.cursor()
				except Exception, e:
					self.log("DB Connection Error: %s" % str(e), xbmc.LOGERROR)
					return False
			else: return False
			try:
				if array == False:
					textexe.execute('INSERT or IGNORE into installed (addonID , enabled, installDate) VALUES (?,?,?)', (addon, state, installedtime,))
					textexe.execute('UPDATE installed SET enabled = ? WHERE addonID = ? ', (state, addon,))
				else:
					for item in addon:
						textexe.execute('INSERT or IGNORE into installed (addonID , enabled, installDate) VALUES (?,?,?)', (item, state, installedtime,))
						textexe.execute('UPDATE installed SET enabled = ? WHERE addonID = ? ', (state, item,))
				textdb.commit()
				textexe.close()
			except Exception, e:
				self.log("Erroring enabling addon: %s" % addon, xbmc.LOGERROR)
	
	try:
		#xbmcgui.Dialog().notification("AutoExec.py", "Starting Script...")
		firstRun = enableAll()
		#xbmcgui.Dialog().notification("AutoExec.py", "All Addons Enabled")
		xbmcvfs.delete('special://userdata/autoexec.py')
	except Exception, e:
		#xbmcgui.Dialog().notification("AutoExec.py", "Error Check LogFile")
		#xbmc.log(str(e), xbmc.LOGERROR)
		xbmcvfs.delete('special://userdata/autoexec.py')

def parseDOM(html, name=u"", attrs={}, ret=False):
	# Copyright (C) 2010-2011 Tobias Ussing And Henrik Mosgaard Jensen
	if isinstance(html, str):
		try:
			html = [html.decode("utf-8")]
		except:
			html = [html]
	elif isinstance(html, unicode):
		html = [html]
	elif not isinstance(html, list):
		return u""

	if not name.strip():
		return u""

	ret_lst = []
	for item in html:
		temp_item = re.compile('(<[^>]*?\n[^>]*?>)').findall(item)
		for match in temp_item:
			item = item.replace(match, match.replace("\n", " "))

		lst = []
		for key in attrs:
			lst2 = re.compile('(<' + name + '[^>]*?(?:' + key + '=[\'"]' + attrs[key] + '[\'"].*?>))', re.M | re.S).findall(item)
			if len(lst2) == 0 and attrs[key].find(" ") == -1:
				lst2 = re.compile('(<' + name + '[^>]*?(?:' + key + '=' + attrs[key] + '.*?>))', re.M | re.S).findall(item)

			if len(lst) == 0:
				lst = lst2
				lst2 = []
			else:
				test = range(len(lst))
				test.reverse()
				for i in test:
					if not lst[i] in lst2:
						del(lst[i])

		if len(lst) == 0 and attrs == {}:
			lst = re.compile('(<' + name + '>)', re.M | re.S).findall(item)
			if len(lst) == 0:
				lst = re.compile('(<' + name + ' .*?>)', re.M | re.S).findall(item)

		if isinstance(ret, str):
			lst2 = []
			for match in lst:
				attr_lst = re.compile('<' + name + '.*?' + ret + '=([\'"].[^>]*?[\'"])>', re.M | re.S).findall(match)
				if len(attr_lst) == 0:
					attr_lst = re.compile('<' + name + '.*?' + ret + '=(.[^>]*?)>', re.M | re.S).findall(match)
				for tmp in attr_lst:
					cont_char = tmp[0]
					if cont_char in "'\"":
						if tmp.find('=' + cont_char, tmp.find(cont_char, 1)) > -1:
							tmp = tmp[:tmp.find('=' + cont_char, tmp.find(cont_char, 1))]

						if tmp.rfind(cont_char, 1) > -1:
							tmp = tmp[1:tmp.rfind(cont_char)]
					else:
						if tmp.find(" ") > 0:
							tmp = tmp[:tmp.find(" ")]
						elif tmp.find("/") > 0:
							tmp = tmp[:tmp.find("/")]
						elif tmp.find(">") > 0:
							tmp = tmp[:tmp.find(">")]

					lst2.append(tmp.strip())
			lst = lst2
		else:
			lst2 = []
			for match in lst:
				endstr = u"</" + name

				start = item.find(match)
				end = item.find(endstr, start)
				pos = item.find("<" + name, start + 1 )

				while pos < end and pos != -1:
					tend = item.find(endstr, end + len(endstr))
					if tend != -1:
						end = tend
					pos = item.find("<" + name, pos + 1)

				if start == -1 and end == -1:
					temp = u""
				elif start > -1 and end > -1:
					temp = item[start + len(match):end]
				elif end > -1:
					temp = item[:end]
				elif start > -1:
					temp = item[start + len(match):]

				if ret:
					endstr = item[end:item.find(">", item.find(endstr)) + 1]
					temp = match + temp + endstr

				item = item[item.find(temp, item.find(match)) + len(temp):]
				lst2.append(temp)
			lst = lst2
		ret_lst += lst

	return ret_lst
	




if (__name__ == "__main__"):
    log('Version %s started' % ADDONVERSION)
    Main()
