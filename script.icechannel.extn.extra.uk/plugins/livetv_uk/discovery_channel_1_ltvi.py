'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveTVIndexer
from entertainment.plugnplay import Plugin
from entertainment import common

class discovery_channel_1(LiveTVIndexer):
    implements = [LiveTVIndexer]
    
    display_name = "Discovery Channel +1"
    
    name = "discovery_channel_1"
    
    other_names = "discovery_channel_1,Discovery Channel +1"
    
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
        {'name':'+1 Channels', 'img':'', 'fanart':''} 
        ]
    
    addon = None
    
