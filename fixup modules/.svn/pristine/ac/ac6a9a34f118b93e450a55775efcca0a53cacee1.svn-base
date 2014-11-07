import os
import platform
import re
import sys
import xbmc
import xbmcgui
import xbmcaddon
from mlb_common import addon_log
from traceback import format_exc, print_exc
from subprocess import Popen, PIPE, STDOUT

filename = sys.argv[1]
dir = sys.argv[2]
event = sys.argv[3]
target = sys.argv[4]
mlbhls = 0
addon = xbmcaddon.Addon(id='plugin.video.mlbmc.hls')
profile = xbmc.translatePath(addon.getAddonInfo('profile'))
home = xbmc.translatePath(addon.getAddonInfo('path'))
language = addon.getLocalizedString
icon = os.path.join(home, 'icon.png')
system_os = platform.system()

class MlbPlayer(xbmc.Player):
    def __init__(self):
        xbmc.Player.__init__(self)
        addon_log('Player created')
        self.state = False

    def onPlayBackStarted(self):
        addon_log('- Playback Started -')
        self.state = 'Started'

    def get_time(self):
        player_time = None
        try:
            player_time = self.getTime()
        except:
            pass
        return player_time

    def onPlayBackEnded(self):
        addon_log('-Playback Ended-')
        self.state = 'Ended'

    def onPlayBackStopped(self):
        addon_log('- Playback Stopped -')
        self.state = 'Stopped'

    def player_state(self):
        return self.state


def check_subprocess():
    global mlbhls
    addon_log('Platform: %s' %system_os)
    if system_os == 'Windows':
        list_cmd = 'tasklist /fi "IMAGENAME eq mlbhls*"'
    else:
        list_cmd = 'ps -A|grep mlbhls'
    s = Popen(list_cmd, shell=True, stdout=PIPE)
    mlbhls_shell = None
    for i in s.stdout:
        # addon_log(i)
        if system_os == 'Windows':
            if 'mlbhls' in i:
                mlbhls = i.split()[1]
                addon_log('MLB-HLS is Running: %s' %mlbhls)
                return True
        
        else:
            # seems some os's will return the grep and shell process with ps -A
            if not 'grep' in i:
                if 'bin/sh' in i:
                    mlbhls_shell = i.split()[0]
                else:
                    mlbhls = i.split()[0]
                    addon_log('MLB-HLS is Running: %s' %mlbhls)
                    return True
    if mlbhls == 0:
        if mlbhls_shell:
            mlbhls = mlbhls_shell
            addon_log('MLB-HLS shell is Running: %s' %mlbhls)
            return True
    addon_log('MLB-HLS is not running.')
    return False


def stop_subprocess():
    global mlbhls
    addon_log('- killing mlbhls -')
    success = False
    for i in range(0,5):
        if system_os == 'Windows':
            stop_cmd = 'taskkill /F /im mlbhls*'
        else:
            stop_cmd = 'kill -9 %s' %mlbhls
        s = Popen(stop_cmd, shell=True, stdout=PIPE)
        for i in s.stdout:
            addon_log(i)
            if 'SUCCESS' in i:
                success = True
                break
        if success:
            break
        mlbhls = 0
        xbmc.sleep(200)
        if not check_subprocess():
            break
        else:
            addon_log('attempt to kill mlbhls %s' %(i+1))
            if i == 4:
                addon_log('Unable to kill mlbhls???????')
                xbmc.executebuiltin("XBMC.Notification(MLBMC, Warning: Unabel to stop MLB-HLS subprocesss ,8000, '')")
                
def clean_up():
    try:
        os.remove(filename)
    except:
        print_exc
        addon_log('Exception: remove')
    try:
        os.rmdir(dir)
    except:
        print_exc
        addon_log('Exception: rmdir')

def start_player(seektime=None):
    player = MlbPlayer()
    state = False
    player.play(filename)
    if seektime:
        player.seekTime(seektime)
    addon_log('Player Returned')
    addon_log('starting player_monitor')
    player_time = None
    while not xbmc.abortRequested:
        state = player.player_state()
        if not state:
            if player.isPlaying():
                state = 'Started'
        if state == 'Started':
            t = player.get_time()
            if not t is None:
                player_time = t
            xbmc.sleep(2000)
        else:
            break

    addon_log('Player is not playing anymore.')
    state = player.player_state()
    addon_log('PlayerState: %s' %state)
    addon_log('PlayerTime: %s' %player_time)
    dialog = xbmcgui.Dialog()
    if check_subprocess():
        if state == 'Stopped':
            del player
            stop_subprocess()
        else:
            ret = dialog.yesno('MLBMC', 'MLB-HLS is running. Restart the player?')
            addon_log('Returned: %s' %ret)
            if ret:
                del player
                player = MlbPlayer()
                return start_player(player_time)
            else:
                del player
                stop_subprocess()
    else:
        if state == 'Stopped':
            del player
            stop_subprocess()
        else:
            ret = dialog.yesno('MLBMC', 'MLB-HLS is not running. Restart the player?')
            addon_log('Returned: %s' %ret)
            if ret:
                del player
                stop_subprocess()
                return xbmc.executebuiltin("XBMC.RunPlugin(plugin://plugin.video.mlbmc.hls/?mode=7&event=%s)" %event)


addon_log('Starting Player Script')

hls_log = open(os.path.join(profile, 'hls.log'), 'wb')
size_values = {
    '0': -1,
    '1': 0,
    '2': 4096,
    '3': 8192,
    '4': 12288,
    '5': 16384,
    '6': 20480,
    '7': 24576
    }
if addon.getSetting('fifo') == 'true':
    buf_size = size_values[addon.getSetting('buf_size')]
    addon_log('Bufer Size: %s' %buf_size)
else:
    buf_size = -1
process = Popen(target, shell=True, stdout=hls_log, bufsize=buf_size)

if addon.getSetting('fifo') == 'false':
    hls_wait = int(addon.getSetting('hls_wait')+'000')
    if hls_wait >= 5000:
        xbmc.executebuiltin("XBMC.Notification("+language(30035)+
                            ",Caching for "+addon.getSetting('hls_wait')+
                            " Seconds,"+str(hls_wait - 1000)+","+icon+")")
    else: hls_wait = 4000
    xbmc.sleep(hls_wait)
                
if check_subprocess():
    start_player()
    clean_up()
addon_log('Script Finished')