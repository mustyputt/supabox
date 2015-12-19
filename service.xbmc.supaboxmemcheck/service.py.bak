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

import platform,urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc, xbmcaddon, os, sys
import xbmc
import plugintools
import datetime
import texturecache,sqlite3
import lib.common
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
TribecaUrl='http://tribeca.tvaddons.ag/'; #TribecaUrl='http://tribeca.xbmchub.com/'
mainurl=TribecaUrl+'tools/maintenance'
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
        xbmc.sleep(int(clear_check)*60000)
 
    def _update(self, type):
        xbmc.sleep(1000)

class Widgets_Monitor(xbmc.Monitor):
    def __init__(self, *args, **kwargs):
        xbmc.Monitor.__init__(self)
        self.update_listitems = kwargs['update_listitems']

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
        dp = xbmcgui.DialogProgress()
        dp.create(AddonTitle,"Clearing Cache",'')
   
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
        dialog = xbmcgui.Dialog()
        dialog.ok(AddonTitle, "Error Deleting Packages.")

################################
###    End Purge Packages    ###
################################
        
if (__name__ == "__main__"):
    log('Version %s started' % ADDONVERSION)
    Main()
