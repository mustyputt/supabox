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

# Entry point
def run():
    plugintools.log("freshstart.run")
    
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
    plugintools.log("freshstart.main_list "+repr(params))

    yes_pressed = plugintools.message_yes_no("XBMC Fresh Start", "Do you wish to restore your", "XBMC configuration to default settings?")

    if yes_pressed:
        addonPath = xbmcaddon.Addon(id = 'plugin.video.freshstart').getAddonInfo('path')
        addonPath = xbmc.translatePath( addonPath )
        xbmcPath = os.path.join(addonPath,"..","..")
        xbmcPath = os.path.abspath(xbmcPath)
        plugintools.log("freshstart.main_list xbmcPath="+xbmcPath)
        failed=False

        try:
            for root, dirs, files in os.walk(xbmcPath, topdown=False):
                for name in files:
                    try:
                        os.remove(os.path.join(root, name))
                    except:
                        if name not in ["Addons15.db","MyVideos75.db","Textures13.db","xbmc.log"]:
                            failed=True
                        plugintools.log("Error removing "+root+" "+name)

                for name in dirs:
                    try:
                        os.rmdir(os.path.join(root, name))
                    except:
                        if name not in ["Database","userdata"]:
                            failed=True
                        plugintools.log("Error removing "+root+" "+name)

            if not failed:
                plugintools.log("freshstart.main_list All user files removed, you now have a clean install")
                plugintools.message("XBMC Fresh Start", "The process is complete, you're now back to a fresh XBMC configuration!","Please reboot your system or restart XBMC in order for the changes to be applied.")
            else:
                plugintools.log("freshstart.main_list User files partially removed")
                plugintools.message("XBMC Fresh Start", "The process is finished, you're now back to a fresh XBMC configuration!","Please reboot your system or restart XBMC in order for the changes to be applied.")
        except:
            plugintools.message("XBMC Fresh Start", "Problem found","Your settings has not been changed")
            import traceback
            plugintools.log(traceback.format_exc())
            plugintools.log("freshstart.main_list NOT removed")

        plugintools.add_item( action="" , title="Done" , folder=False )
    else:
        plugintools.message("XBMC Fresh Start", "Your settings", "has not been changed")
        plugintools.add_item( action="" , title="Done" , folder=False )

run()