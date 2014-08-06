from universal import watchhistory 

class WatchHistory:
    '''
    This class provides all the handling of watch history.    
    '''
    def __init__(self, addon_id):       
        self.addon_id = addon_id
        self.wh_obj = watchhistory.WatchHistory(addon_id)
    
    def __del__(self):
        ''' Cleanup db when object destroyed '''
        try:
            self.wh_obj = None
        except: pass

    def add_item(self, title, url, infolabels='', img='', fanart='', is_playable=False, is_folder=False, has_multiple_links=False):
        level = '0'
        if has_multiple_links == True:
            level = '1'            
        self.wh_obj.add_item(title, url, infolabels=infolabels, img=img, fanart=fanart, is_playable=is_playable, is_folder=is_folder, level=level)
    
    
    def add_video_item(self, title, url, infolabels='', img='', fanart='', is_playable=False):
        self.add_item(title, url, infolabels=infolabels, img=img, fanart=fanart, is_playable=is_playable)
        
    def add_directory(self, title, url, infolabels='', img='', fanart='', has_multiple_links=False):
        self.add_item(title, url, infolabels=infolabels, img=img, fanart=fanart, is_folder=True, has_multiple_links=has_multiple_links)
        
    def get_watch_history(self, addon_id):
        return self.wh_obj.get_watch_history(addon_id)    
        
    def get_my_watch_history(self):        
        return self.get_watch_history(self.addon_id)
        
    def get_watch_history_for_all(self):        
        return self.get_watch_history('all')
        
    def has_watch_history(self):
        return self.wh_obj.has_watch_history()
        
    def get_addons_that_have_watch_history(self):    
        return self.wh_obj.get_addons_that_have_watch_history()
        
    def cleanup_history(self):    
        return self.wh_obj.cleanup_history()

def settings():
    from universal import _common
    _common.addon.show_settings()