import xbmc,xbmcgui,xbmcaddon,os,sys,main,re,time,calendar
from datetime import datetime
addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)


def tosec(m):
    if m.group(1) == '-': pos = 1
    else: pos = -1
    sec = 0
    sec += int(m.group(2)) * 3600
    sec += int(m.group(3))
    sec = sec * pos
    return str(sec)

def html_escape(text):
    return text.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&apos;',"'").replace('&quot;','"')

def showChangeLog(env):
    if env.lower() == 'dev':
        url = 'https://github.com/mash2k3/MashUp/commits/master'
        env = 'Dev'
        html = main.OPENURL(url,cookie='github')
    else:
        url = 'https://github.com/mash2k3/AutoUpdate/commits/master'
        env = ''
        html = main.OPENURL(url)
    
    text = ''
    for changes,date in re.findall('(?sim)class="message" data-pjax="true" title="([^"]+?)".+?datetime="([^"]+?)"',html):
        shift = int(re.sub('.*([+-])(\d+):(\d+)$',tosec,date))
        try:
            date = re.sub('([+-])(\d+):(\d+)$','',date)
            ts = int(calendar.timegm(time.strptime(date, "%Y-%m-%dT%H:%M:%S")) + shift);
            date = pretty_date(ts)
        except: pass
        if env == 'Dev':
            changes = [line.strip() for line in changes.split('\n') if line.strip()] # and line.startswith('#')
        else: 
            changes = [line.strip() for line in changes.split('\n') if line.strip() and line.startswith('#')]
        if changes and date:
            for change in changes:
                text += html_escape(change.strip('#')) + "\n"
            text += "[COLOR blue]" + date + "[/COLOR]\n\n"
    main.TextBoxes('[B]Auto Update ChangeLog '+env+'[/B]', text)
    
def pretty_date(time=False):
    now = datetime.utcnow()
    if type(time) is int: diff = now - datetime.utcfromtimestamp(time)
    elif isinstance(time,datetime): diff = now - time 
    elif not time: diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0: return 'just now'
    if day_diff == 0:
        if second_diff < 10: return "just now"
        if second_diff < 60: return str(second_diff) + " seconds ago"
        if second_diff < 120: return  "a minute ago"
        if second_diff < 3600: return str( second_diff / 60 ) + " minutes ago"
        if second_diff < 7200: return "an hour ago"
        if second_diff < 86400: return str( (second_diff+1800) / 3600 ) + " hours ago"
    if day_diff == 1: return "Yesterday"
    if day_diff < 7: return str(day_diff) + " days ago"
    if day_diff < 31: return str(day_diff/7) + " weeks ago"
    if day_diff < 365: return str(day_diff/30) + " months ago"
    return str(day_diff/365) + " years ago"

if  __name__ == "__main__": showChangeLog(sys.argv[1])
