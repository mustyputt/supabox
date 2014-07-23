import urllib, os,re,urllib2,time,datetime
import xbmc,xbmcgui
from t0mm0.common.net import Net

USER_AGENT = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7"


#CONSTANTS
url = sys.argv[1]
downloadpath = sys.argv[2]
name = sys.argv[3]

if 'putlocker' in url:
    filename = name + '.flv'
else:
    filename = name + '.mp4'

print filename
downloadfile = downloadpath+filename


cookiejar = os.path.join(downloadpath,'losmovies.lwp')
net = Net(cookie_file=cookiejar)

print url
print downloadpath
print name

def removeDisallowedFilenameChars(filename):
    cleanedFilename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore')
    return ''.join(c for c in cleanedFilename if c in validFilenameChars)
 
def DownloaderClass(url,dest):
    net.set_cookies(cookiejar)
    req = urllib2.Request(url)
    req.add_header('User-Agent',USER_AGENT)
    response = urllib2.urlopen(req)
    f = open(downloadfile, 'wb')
    meta = response.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (downloadpath, file_size)

    dp = xbmcgui.DialogProgress()
    dp.create("Downloading File",filename+' ['+str(file_size/1024/1024)+'MB]')
    start = time.time()

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = response.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        
        #Writes to log
        #status = r"%10d [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        #print status
        
        elapsed = (time.time() - start) # gives time since started
        #file_size_dl gives bytes dl
        bytespersecond = file_size_dl / 1024 / elapsed
        file_size_left = file_size - file_size_dl
        time_left_seconds = (file_size_left /1024) / bytespersecond

        time_left_string = str(datetime.timedelta(seconds=time_left_seconds))[:-7]


        dp.update(file_size_dl * 100. / file_size,line2=format(bytespersecond, '.2f')+'kb/s',line3='ETA: '+time_left_string)
        if dp.iscanceled(): 
                print "DOWNLOAD CANCELLED" # need to get this part working
                dp.close() #close dialog
                response.close() #close connection
                f.close() # close file
                os.remove(downloadfile)
                break
    f.close()


 
DownloaderClass(url,downloadpath)
