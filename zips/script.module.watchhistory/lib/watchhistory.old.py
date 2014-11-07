'''

    These classes are to be used by others to add to The Watch History
    
'''

import os    
import datetime
import sys
import xbmc
import xbmcvfs
import re

from t0mm0.common.addon import Addon

addon_identifier = 'script.module.watchhistory'
addon = None
if len(sys.argv) < 2:
    addon = Addon(addon_identifier)
else:
    addon = Addon(addon_identifier, sys.argv)
addon_path = addon.get_path()

try:
    if  addon.get_setting('use_remote_db')=='true' and   \
        addon.get_setting('db_address') is not None and  \
        addon.get_setting('db_user') is not None and     \
        addon.get_setting('db_pass') is not None and     \
        addon.get_setting('db_name') is not None:
        import mysql.connector as database
        addon.log('Loading MySQLdb as DB engine', 2)
        DB = 'mysql'
    else:
        raise ValueError('MySQL not enabled or not setup correctly')
except:
    try: 
        import sqlite3
        from sqlite3 import dbapi2 as database
        addon.log('Loading sqlite3 as DB engine version: %s' % database.sqlite_version, 2)
    except Exception, e:
        print e
        from pysqlite2 import dbapi2 as database
        addon.log('pysqlite2 as DB engine', 2)
    DB = 'sqlite'

def make_dir(mypath, dirname):
    ''' Creates sub-directories if they are not found. '''
    subpath = os.path.join(mypath, dirname)
    if not xbmcvfs.exists(subpath): xbmcvfs.mkdir(subpath)
    return subpath
    
def bool2string(myinput):
    ''' Neatens up usage of preparezip flag. '''
    if myinput is False: return 'false'
    elif myinput is True: return 'true'
    
def string2bool(myinput):
    ''' Neatens up usage of preparezip flag. '''
    if myinput == 'false': return False
    elif myinput == 'true': return True
    
def str_conv(data):
    if isinstance(data, unicode):
        data = data.encode('utf8')
    elif isinstance(data, str):
        data.decode('utf8')        
    data = data.decode('string-escape')
    return data
    
def encode_dict(dict):
    out_dict = {}
    for k, v in dict.iteritems():
        v = str_conv(v)
        if v.find(',') >= 0:
            v = v.replace(',', '<comma>')
        if v.find("'") >= 0:
            v = v.replace("'", '<squot>')
        if v.find('"') >= 0:
            v = v.replace('"', '<dquot>')
        if v.find('{') >= 0:
            v = v.replace('{', '<ltbrc>')
        if v.find('}') >= 0:
            v = v.replace('}', '<rtbrc>')
        if v.find(':') >= 0:
            v = v.replace(':', '<colon>')
        out_dict[k] = v
    return out_dict
    
def decode_dict(dict):
    out_dict = {}
    for k, v in dict.iteritems():
        v = str_conv(v)
        if v.find('<comma>') >= 0:
            v = v.replace('<comma>', ',')
        if v.find("<squot>") >= 0:
            v = v.replace("<squot>", "'")
        if v.find('<dquot>') >= 0:
            v = v.replace("<dquot>", "'")
        if v.find('<ltbrc>') >= 0:
            v = v.replace('<ltbrc>', '{')
        if v.find('<rtbrc>') >= 0:
            v = v.replace('<rtbrc>', '}')
        if v.find('<colon>') >= 0:
            v = v.replace('<colon>', ':')        
        out_dict[k] = v
    return out_dict    


class WatchHistory:
    '''
    This class provides all the handling of watch history.    
    '''
    path = 'special://profile/addon_data/script.module.watchhistory/'
    
    def __init__(self, addon_id):       
        
        #Check if a path has been set in the addon settings
        settings_path = addon.get_setting('local_save_location')
        if settings_path:
            self.path = xbmc.translatePath(settings_path)
        else:
            self.path = xbmc.translatePath(self.path)
        
        self.addon_id = addon_id
        self.cache_path = make_dir(self.path, '')
        
        self.watchhistory = os.path.join(self.cache_path, 'watch_history.db')
        
        # connect to db at class init and use it globally
        if DB == 'mysql':
            class MySQLCursorDict(database.cursor.MySQLCursor):
                def _row_to_python(self, rowdata, desc=None):
                    row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
                    if row:
                        return dict(zip(self.column_names, row))
                    return None
            db_address = addon.get_setting('db_address')
            db_port = addon.get_setting('db_port')
            if db_port: db_address = '%s:%s' %(db_address,db_port)
            db_user = addon.get_setting('db_user')
            db_pass = addon.get_setting('db_pass')
            db_name = addon.get_setting('db_name')
            self.dbcon = database.connect(db_name, db_user, db_pass, db_address, buffered=True, charset='utf8')
            self.dbcur = self.dbcon.cursor(cursor_class=MySQLCursorDict, buffered=True)
        else:
            self.dbcon = database.connect(self.watchhistory)
            self.dbcon.row_factory = database.Row # return results indexed by field names and not numbers so we can convert to dict
            self.dbcon.text_factory = str
            self.dbcur = self.dbcon.cursor()
                
        self._create_watch_history_db()
    
    def __del__(self):
        ''' Cleanup db when object destroyed '''
        try:
            self.dbcur.close()
            self.dbcon.close()
        except: pass

    def _create_watch_history_db(self):
        
        sql_create = "CREATE TABLE IF NOT EXISTS watch_history ("\
                            "addon_id TEXT,"\
                            "title TEXT,"\
                            "url TEXT,"\
                            "infolabels TEXT,"\
                            "image_url TEXT,"\
                            "fanart_url TEXT,"\
                            "isfolder TEXT,"\
                            "isplayable TEXT,"\
                            "hasmultiplelinks TEXT,"\
                            "lastwatched TIMESTAMP,"\
                            "UNIQUE(addon_id, title, hasmultiplelinks)"\
                            ");"
        if DB == 'mysql':
            sql_create = sql_create.replace("addon_id TEXT", "addon_id VARCHAR(100)")
            sql_create = sql_create.replace("title TEXT"  ,"title VARCHAR(200)")
            sql_create = sql_create.replace("isfolder TEXT"  ,"isfolder VARCHAR(5)")
            sql_create = sql_create.replace("isplayable TEXT"  ,"isplayable VARCHAR(5)")
            sql_create = sql_create.replace("hasmultiplelinks TEXT"  ,"hasmultiplelinks VARCHAR(5)")
            self.dbcur.execute(sql_create)
            try: self.dbcur.execute('CREATE INDEX whindex on on watch_history (addon_id, title, hasmultiplelinks);')
            except: pass
        else:
            self.dbcur.execute(sql_create)
            self.dbcur.execute('CREATE INDEX IF NOT EXISTS whindex on watch_history (addon_id, title, hasmultiplelinks);')            
        addon.log('Table watch_history initialized', 0)    
        
    def _add_as_dir(self):
        return addon.get_setting('add_dir')
        
    def _cleanup_history(self):
        
        _ch = addon.get_setting('cleanup-history')
        
        ch = ''
        
        if _ch == '0':
            ch = 'days'            
        elif _ch == '1':
            ch = 'count'
            
        return ch
        
    def _cleanup_history_max(self, ch):
        
        chm = ''
    
        if ch == 'days':
            chm = addon.get_setting('cleanup-history-days')
        elif ch == 'count':
            chm = addon.get_setting('cleanup-history-count')
            
        return chm
        
    def add_item(self, title, url, infolabels='', img='', fanart='', is_playable=False, is_folder=False, has_multiple_links=False):

        if url.find('&watchhistory=true'):
            url = url.replace('&watchhistory=true', '')
        elif url.find('?watchhistory=true&'):
            url = url.replace('?watchhistory=true&', '?')
            
        #title = str_conv(title)
                       
        row_exists = True
        try:
            if DB == 'mysql':
                sql_select = "SELECT * FROM watch_history WHERE addon_id = %s AND title = %s AND hasmultiplelinks = %s"
            else:
                sql_select = "SELECT * FROM watch_history WHERE addon_id = ? AND title = ? AND hasmultiplelinks = ?"
            print sql_select 
            print self.addon_id 
            print title
            self.dbcur.execute(sql_select, (self.addon_id, title, bool2string(has_multiple_links)))
            print str(self.dbcur.fetchall()[0])
        except:
            row_exists = False
                
        sql_update_or_insert = ''
        if row_exists == True:
            if DB == 'mysql':
                sql_update_or_insert = "UPDATE watch_history SET lastwatched = %s WHERE addon_id = %s AND title = %s AND hasmultiplelinks = %s" 
            else:
                sql_update_or_insert = "UPDATE watch_history SET lastwatched = ? WHERE addon_id = ? AND title = ? AND hasmultiplelinks = ?" 
                
            print sql_update_or_insert 
            print self.addon_id 
            print title
                
            self.dbcur.execute(sql_update_or_insert, (datetime.datetime.now(), self.addon_id, title, bool2string(has_multiple_links)))
        else:
            if DB == 'mysql':
                sql_update_or_insert = "INSERT INTO watch_history(addon_id, title, url, infolabels, image_url, fanart_url, isplayable, isfolder, lastwatched, hasmultiplelinks) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            else:
                sql_update_or_insert = "INSERT INTO watch_history(addon_id, title, url, infolabels, image_url, fanart_url, isplayable, isfolder, lastwatched, hasmultiplelinks) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"            
                
            if infolabels:
                infolabels = encode_dict(infolabels)
                
            print sql_update_or_insert
            print self.addon_id 
            print title
                
            self.dbcur.execute(sql_update_or_insert, (self.addon_id, title, url, str(infolabels), img, fanart, bool2string(is_playable), bool2string(is_folder), datetime.datetime.now(), bool2string(has_multiple_links)))
        self.dbcon.commit()
    
    
    def add_video_item(self, title, url, infolabels='', img='', fanart='', is_playable=False):
        self.add_item(title, url, infolabels=infolabels, img=img, fanart=fanart, is_playable=is_playable)
        
    def add_directory(self, title, url, infolabels='', img='', fanart='', has_multiple_links=False):
        self.add_item(title, url, infolabels=infolabels, img=img, fanart=fanart, is_folder=True, has_multiple_links=has_multiple_links)
        
    def get_watch_history(self, addon_id):
    
        history_items = []
        
        try:
            import json
        except:
            import simplejson as json

        sql_select = "SELECT * FROM watch_history"
        
        whereadded = False
        if addon_id != 'all':
            sql_select = sql_select + ' WHERE addon_id = \'' + addon_id + '\''
            whereadded = True
        
        if self._add_as_dir() == 'true':
            sql_select = sql_select + " ORDER BY lastwatched DESC, title ASC, hasmultiplelinks DESC"
        else:
            if whereadded == False:
                sql_select = sql_select + ' WHERE '
                whereadded = True
            else:
                sql_select = sql_select + ' AND '
                
            sql_select = sql_select + " hasmultiplelinks = 'false' ORDER BY lastwatched DESC, title ASC"
            
        print sql_select

        self.dbcur.execute(sql_select)
        
        last_title = 'DUMMY_TITLE'
        curr_title = ''
        for matchedrow in self.dbcur.fetchall():
        
            match = dict(matchedrow)
            
            curr_title = match['title'].lower()
                    
            if self._add_as_dir() == 'true' and last_title in curr_title:
                continue
            
            infolabels = {}
            if match['infolabels']:
                infolabels = json.loads(re.sub(r",\s*(\w+)", r", '\1'", re.sub(r"\{(\w+)", r"{'\1'", match['infolabels'].replace('\\','\\\\'))).replace("'", '"'))
            infolabels['title'] = match['title']

            item = {'title':match['title'], 'url' : match['url'], 'infolabels': decode_dict(infolabels), 'image_url':match['image_url'], 'fanart_url':match['fanart_url'], 'isplayable':match['isplayable'], 'isfolder':match['isfolder']}
            
            history_items.append(item)
            
            last_title = curr_title
            
        return history_items
        
    def get_my_watch_history(self):
        
        return self.get_watch_history(self.addon_id)
        
    def get_watch_history_for_all(self):
        
        return self.get_watch_history('all')
        
    def has_watch_history(self):
    
        has_wh = True
        
        try:
            sql_select = "SELECT * FROM watch_history WHERE addon_id = '%s'" % self.addon_id
            self.dbcur.execute(sql_select)    
            matchedrow = self.dbcur.fetchall()[0]
        except:
            has_wh = False
            
        return has_wh
        
    def get_addons_that_have_watch_history(self):
    
        addons = []
    
        sql_select = "SELECT DISTINCT addon_id FROM watch_history ORDER BY addon_id"
    
        self.dbcur.execute(sql_select)
    
        for matchedrow in self.dbcur.fetchall():
        
            match = dict(matchedrow)
            
            try:
                tmp_addon_id = match['addon_id']
                tmp_addon = Addon(tmp_addon_id)
                tmp_addon_name = tmp_addon.get_name()
            except:
                tmp_addon_name = tmp_addon_id
                pass
            
            tmp_addon_dtl = {'title' : tmp_addon_name, 'id' : tmp_addon_id}
            
            addons.append(tmp_addon_dtl)
            
        return addons
        
    def cleanup_history(self):
        
        ch = self._cleanup_history()
                
        chm = self._cleanup_history_max(ch)
        sql_delete = ''
        if ch == 'days':
            cutoff_date = str(datetime.date.today() - datetime.timedelta(int(chm)))
            sql_delete = "DELETE FROM watch_history WHERE lastwatched < '%s'" % cutoff_date            
        elif ch == 'count':
            if DB == 'mysql':
                sql_delete = "DELETE FROM watch_history WHERE (addon_id, title, hasmultiplelinks) NOT IN (SELECT * FROM (SELECT wh1.addon_id, wh1.title, wh1.hasmultiplelinks FROM watch_history wh1 JOIN (SELECT addon_id, title, hasmultiplelinks FROM watch_history ORDER BY lastwatched DESC LIMIT %s) as wh2 on wh1.addon_id = wh2.addon_id AND wh1.title = wh2.title AND wh1. hasmultiplelinks = wh2.hasmultiplelinks) as wh3)" % chm
            else:
                sql_delete = "DELETE FROM watch_history WHERE addon_id || '-' || title || '-' || hasmultiplelinks NOT IN (SELECT addon_id || '-' || title || '-' || hasmultiplelinks FROM watch_history ORDER BY lastwatched DESC LIMIT %s)" % chm
            
        print sql_delete
        self.dbcur.execute(sql_delete)
        self.dbcon.commit()

def settings():
    addon.show_settings()