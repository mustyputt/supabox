# -*- coding: utf-8 -*-
#------------------------------------------------------------
# XBMC Add-on for restoring XBMC to its default settings
# Version 1.0.1
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------

import os
import sys
import plugintools
import xbmcaddon
from texturecache import *

# Entry point
def run():
    plugintools.log("clean.run")
    
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
    plugintools.log("clean.main_list "+repr(params))

    yes_pressed = plugintools.message_yes_no("Supabox Fresh clean", "Do you wish to restore your", "Supabox configuration to default settings?")

    if yes_pressed:
        addonPath = xbmcaddon.Addon(id = 'plugin.video.supaboxclean').getAddonInfo('path')
        addonPath = xbmc.translatePath( addonPath )
        xbmcPath = os.path.join(addonPath,"..","..","userdata","Thumbnails")
        xbmcPath = os.path.abspath(xbmcPath)
        
        addonPath1 = xbmcaddon.Addon(id = 'plugin.video.supaboxclean').getAddonInfo('path')
        addonPath1 = xbmc.translatePath( addonPath1 )
        xbmcPath1 = os.path.join(addonPath1,"..","..","addons","packages")
        xbmcPath1 = os.path.abspath(xbmcPath1)

        plugintools.log("clean.main_list xbmcPath="+xbmcPath)
        failed=False
        
        try:
            row=main("P")
            row=main("Xd")
        finally:
            pass
        
        try:
            for root, dirs, files in os.walk(xbmcPath1, topdown=False):
                for name in files:
                    try:
                        os.remove(os.path.join(root, name))
                    except:
                        failed=True
                        plugintools.log("Error removing "+root+" "+name)

                for name in dirs:
                    try:
                        os.rmdir(os.path.join(root, name))
                    except:
                        plugintools.log("Error removing "+root+" "+name)

            if not failed:
                plugintools.log("clean.main_list All cache files removed, you now have more space.")
                plugintools.message("Supabox Fresh Clean", "Cleaned System!")
            else:
                plugintools.log("clean.main_list addon packages partially removed")
                plugintools.message("Supabox Fresh Clean", "Failed to clean system!")
        except:
            plugintools.log("clean.main_list NOT removed")

        plugintools.add_item( action="" , title="Done" , folder=False )
    else:
        plugintools.message("Supabox Fresh Clean", "Your settings", "has not been changed")
        plugintools.add_item( action="" , title="Done" , folder=False )

run()