
# Download Thread Module by: Blazetamer and o9r1sh1


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon
from metahandler import metahandlers
from resources.modules import main

from addon.common.addon import Addon

from addon.common.net import Net


net = Net()


import threading

try:
     import StorageServer
except:
     import storageserverdummy as StorageServer
import time

# Cache  
cache = StorageServer.StorageServer("familyfunflix", 0)
#=====================NEW DL======================================
settings = xbmcaddon.Addon(id='plugin.video.familyfunflix')     
addon_id = 'plugin.video.familyfunflix'
addon = Addon(addon_id, sys.argv)
mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
thumb = addon.queries.get('thumb', '')
ext = addon.queries.get('ext', '')
console = addon.queries.get('console', '')
dlfoldername = addon.queries.get('dlfoldername', '')
favtype = addon.queries.get('favtype', '')
mainimg = addon.queries.get('mainimg', '')

print 'Mode is: ' + mode
print 'Url is: ' + url
print 'Name is: ' + name
print 'Thumb is: ' + thumb
print 'Extension is: ' + ext
print 'File Type is: ' + console
print 'DL Folder is: ' + dlfoldername
print 'Favtype is: ' + favtype
print 'Main Image is: ' + mainimg

artPath = xbmc.translatePath(os.path.join('http://addonrepo.com/xbmchub/familyfunflix/images/', ''))
download_path = settings.getSetting('download_folder')

#================Threading===========================================


class downloadThread (threading.Thread):
    def __init__(self, name, url, thumb, console, ext):
        threading.Thread.__init__(self)
        self.thumb = thumb
          
    def run(self):
     queue = cache.get('queue')
  
     if queue:
          queue_items = sorted(eval(queue), key=lambda item: item[1])
          for item in queue_items:
               self.name = item[0]
               self.url = item[1]
               self.ext = item[3]
               self.console = item[4]
               self.thumb = item[2]
                                
               self.path = download_path + self.console
               if not os.path.exists(self.path):
                    os.makedirs(self.path)
  
               self.file_name = self.name + self.ext
  
               addon.show_small_popup(title='Downloads Started', msg=self.name + ' Is Downloading', delay=int(7000), image=thumb)
               u = urllib.urlopen(self.url)
               f = open(os.path.join(self.path,self.file_name), 'wb')
               meta = u.info()
               file_size = int(meta.getheaders("Content-Length")[0])
  
               file_size_dl = 0
               block_sz = 8192
  
               
                 
               while True:
                   buffer = u.read(block_sz)
                   if not buffer:
                       break
  
                   file_size_dl += len(buffer)
                   f.write(buffer)
                   status = int( file_size_dl * 1000. / file_size)
                  
                   if status > 99 and status < 101:
                         addon.show_small_popup(title=self.name, msg='10% Complete',delay=int(10), image=thumb)

                   elif status > 199 and status < 201:
                         addon.show_small_popup(title=self.name, msg='20% Complete',delay=int(10), image=thumb)
                         
                   elif status > 299 and status < 301:
                         addon.show_small_popup(title=self.name, msg='30% Complete',delay=int(10), image=thumb)

                   elif status > 399 and status < 401:
                         addon.show_small_popup(title=self.name, msg='40% Complete',delay=int(10), image=thumb)

                   elif status > 499 and status < 501:
                         addon.show_small_popup(title=self.name, msg='50% Complete',delay=int(10), image=thumb)

                   elif status > 599 and status < 601:
                         addon.show_small_popup(title=self.name, msg='60% Complete',delay=int(10), image=thumb)      
                   
                   elif status > 699 and status < 701:
                         addon.show_small_popup(title=self.name, msg='70% Complete',delay=int(10), image=thumb)

                   elif status > 799 and status < 801:
                         addon.show_small_popup(title=self.name, msg='80% Complete',delay=int(10), image=thumb)

                   elif status > 899 and status < 901:
                         addon.show_small_popup(title=self.name, msg='90% Complete',delay=int(10), image=thumb)

                   elif status > 994 and status < 996:
                         addon.show_small_popup(title=self.name, msg='95% Complete',delay=int(10), image=thumb)       
                   
                   
               f.close()
  
               removeFromQueue(self.name,self.url,self.thumb,self.ext,self.console)
  
  
               try:
                    addon.show_small_popup(title='Download Complete', msg=self.name + ' Completed', delay=int(5000), image=thumb)
               except:
                    addon.show_small_popup(title='Error', msg=self.name + ' Failed To Download File', delay=int(5000), image=thumb)
                    print 'ERROR - File Failed To Download'
  
                 
               addon.show_small_popup(title='[COLOR gold]Process Complete[/COLOR]', msg=self.name + ' is in your downloads folder', delay=int(5000), image=thumb) 

               


############## End DownloadThread Class ################

def addQDir(name,url,mode,thumb,console):
     contextMenuItems = []

     params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb,'console':console, 'ext':ext}

     contextMenuItems.append(('Remove From Queue', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'removeFromQueue', 'name': name,'url': url,'thumb': thumb,'ext': ext,'console': console})))

     addon.add_directory(params, {'title':name}, contextmenu_items=contextMenuItems, img= thumb)
     
def addToQueue(name,url,thumb,ext,console):
     queue = cache.get('queue')
     queue_items = []
     if queue:
          queue_items = eval(queue)
          if queue_items:
               if (name,url,thumb,ext,console) in queue_items:
                    addon.show_small_popup(title='Item Already In Your Queue', msg=name + ' Is Already In Your Download Queue', delay=int(5000), image=thumb)
                    return
     queue_items.append((name,url,thumb,ext,console))         
     cache.set('queue', str(queue_items))
     addon.show_small_popup(title='Item Added To Your Queue', msg=name + ' Was Added To Your Download Queue', delay=int(5000), image=thumb)

def viewQueue():
     main.addDir('[COLOR blue]Start Downloads[/COLOR]','none','download',artPath +'startdownloads.png','','')
     queue = cache.get('queue')
     if queue:
          queue_items = sorted(eval(queue), key=lambda item: item[1])
          print queue_items
          for item in queue_items:
               addQDir(item[0],item[1],'viewQueue',item[2],item[4])

def KILLSLEEP(self):
     queue = cache.get('queue')
     if queue:
          queue_items = sorted(eval(queue), key=lambda item: item[1])
          for item in queue_items:
               self.name = item[0]
               self.url = item[1]
               self.ext = item[3]
               self.console = item[4]
               self.thumb = item[2]

               time.sleep(3)
     removeFromQueue(self.name,self.url,self.thumb,self.ext,self.console)
     
     
          
def removeFromQueue(name,url,thumb,ext,console):
     queue = cache.get('queue')
     if queue:
          queue_items = sorted(eval(queue), key=lambda item: item[1])
          print queue_items
          try:
               queue_items.remove((name,url,thumb,'.mp4',console))
          except:
               try:
                    queue_items.remove((name,url,thumb,'.flv',console))
               except:
                    queue_items.remove((name,url,thumb,'.avi',console))
          cache.set('queue', str(queue_items))
          xbmc.executebuiltin("XBMC.Container.Refresh")


def download():
     download_path = settings.getSetting('download_folder')
     if download_path == '':
          addon.show_small_popup(title='File Not Downloadable', msg='You need to set your download folder in addon settings first', delay=int(5000), image='')
     else:
          viewQueue()
          dlThread = downloadThread(name, url, thumb, console, ext)
          dlThread.start() 

 #Resolve Movie DL Links******************************************
def RESOLVEDL(name,url,thumb):  
     data=0
     try:
          data = GRABMETA(movie_name,year)
     except:
           data=0
     hmf = urlresolver.HostedMediaFile(url)
     host = ''
     if hmf:
          url = urlresolver.resolve(url)
          host = hmf.get_host()
          if '.mp4' in url:
                    ext = '.mp4'
          elif '.flv' in url:
                    ext = '.flv'
          elif '.avi' in url:
                    ext = '.avi'
          if not ext == '':
          
          
               console = 'Downloads/Movies/'+ dlfoldername
               params = {'url':url, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername} 
             

               xbmc.sleep(1000)
        
               addToQueue(name,url,thumb,ext,console)

#********Resolve TV DL Links*****************************************

def RESOLVETVDL(name,url,thumb):
         
     data=0
     try:
          data = GRABMETA(movie_name,year)
     except:
           data=0
     hmf = urlresolver.HostedMediaFile(url)
     host = ''
     if hmf:
          url = urlresolver.resolve(url)
          host = hmf.get_host()
          if '.mp4' in url:
                    ext = '.mp4'
          elif '.flv' in url:
                    ext = '.flv'
          elif '.avi' in url:
                    ext = '.avi'
          if not ext == '':
          
               console = 'Downloads/TV Shows/'+ dlfoldername
               params = {'url':url, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername} 
     
               xbmc.sleep(1000)
        
               addToQueue(name,url,thumb,ext,console)


def DIRECTRESOLVEDL(name,url,thumb,favtype):
               
               if '.mp4' in url:
                    ext = '.mp4'
               elif '.flv' in url:
                    ext = '.flv'
               elif '.avi' in url:
                    ext = '.avi'
               else:
                    ext = '.flv'
          
          
                    
                    params = {'url':url, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername, 'favtype':favtype}
                    name = dlfoldername
                    if favtype == 'movies':
                         console = 'Downloads/Movies/'
                         
                    elif favtype == 'tv':
                         console = 'Downloads/TV Shows/'

                    elif favtype == 'other':
                         console = 'Downloads/Other/'

                    else:
                         console = 'Downloads/Misc/'
                    
                    
               

                    xbmc.sleep(1000)
        
                    addToQueue(name,url,thumb,ext,console)#.play(url, liz, False)

               

#=============END DLFUNCTION======================================================================================================================


     



# Global Stuff
settings = xbmcaddon.Addon(id=addon_id)
net = Net()


#********************* DEFcalls********************
       
        

