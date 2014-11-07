class WatchHistory:
    '''
    This class provides all the handling of watch history.    
    '''
    def __init__(self, addon_id):
        return None
    
    def add_item(self, title, url, infolabels='', img='', fanart='', is_folder=False, has_multiple_links=False):
        return ""
        
    def add_video_item(self, title, url, infolabels='', img='', fanart=''):
        self.add_item(title, url, infolabels=infolabels, img=img, fanart=fanart)
        
    def add_directory(self, title, url, infolabels='', img='', fanart='', is_folder=True, has_multiple_links=False):
        self.add_item(title, url, infolabels=infolabels, img=img, fanart=fanart, is_folder=is_folder)
        
    def get_watch_history(self, addon_id): 
        return []
        
    def get_my_watch_history(self):
        return []
        
    def get_watch_history_for_all(self):
        return []
        
    def get_addons_that_have_watch_history(self):
        return []
        
    def has_watch_history(self):
        return False

def settings():
        return False