'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveTVIndexer
from entertainment.plugnplay import Plugin
from entertainment import common

class ntv(LiveTVIndexer):
    implements = [LiveTVIndexer]
    
    display_name = "NTV"
    
    name = "ntv"
    
    other_names = "ntv,NTV"
    
    import xbmcaddon
    import os
    addon_id = 'script.icechannel.extn.extra.uk'
    addon = xbmcaddon.Addon(addon_id)
    img = os.path.join( addon.getAddonInfo('path'), 'resources', 'images', name + '.png' )
    
    regions = [ 
            {
                'name':'United Kingdom', 
                'img':addon.getAddonInfo('icon'), 
                'fanart':addon.getAddonInfo('fanart')
                }, 
        ]
        
    languages = [ 
        {'name':'English', 'img':'', 'fanart':''}, 
        ]
        
    genres = [ 
        {'name':'International', 'img':'', 'fanart':''} 
        ]
    
    addon = None
    
