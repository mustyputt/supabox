##  Credit to Stacked for the original plugin.
##  Thanks to toastcutter for save passwords patch

import urllib
import urllib2
import os
from urlparse import urlparse, parse_qs

import StorageServer
import json

import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs

addon = xbmcaddon.Addon()
addon_id = addon.getAddonInfo('id')
addon_version = addon.getAddonInfo('version')
addon_profile = xbmc.translatePath(addon.getAddonInfo('profile')).encode('utf-8')
addon_path = xbmc.translatePath(addon.getAddonInfo('path')).encode('utf-8')
addon_icon = addon.getAddonInfo('icon')
addon_fanart = addon.getAddonInfo('fanart')
j_nick = addon.getSetting('nickname')
j_pass = addon.getSetting('password')
cache = StorageServer.StorageServer("Jtv_Archives", 24)
search_queries = os.path.join(addon_profile, 'search_queries')
passwords_file = os.path.join(addon_profile, 'passwords')
blacklist_file = os.path.join(addon_profile, 'blacklist')
favorites_file = os.path.join(addon_profile, 'favorites')
api_url = 'http://api.justin.tv/api'

languages = {
    'Swedish': 'sv',
    'Icelandic': 'is',
    'Estonian': 'et',
    'Vietnamese': 'vi',
    'Romanian': 'ro',
    'Slovenian': 'sl',
    'Hindi': 'hi',
    'Dutch': 'nl',
    'Korean': 'ko',
    'Danish': 'da',
    'Indonesian': 'id',
    'Hungarian': 'hu',
    'Ukrainian': 'uk',
    'Lithuanian': 'lt',
    'French': 'fr',
    'Catalan': 'ca',
    'Russian': 'ru',
    'Thai': 'th',
    'Croatian': 'hr',
    'ç®€ä½“ä¸­æ–‡': 'zh-cn',
    'Finnish': 'fi',
    'Hebrew': 'he',
    'Bulgarian': 'bg',
    'Turkish': 'tr',
    'Greek': 'el',
    'Latvian': 'lv',
    'English': 'en',
    'PortugueseBrazil': 'pt-br',
    'Italian': 'it',
    'Portuguese': 'pt',
    'ChineseTW': 'zh-tw',
    'German': 'de',
    'Japanese': 'ja',
    'Norsk (BokmÃ¥l)': 'nb',
    'Czech': 'cs',
    'Slovak': 'sk',
    'Spanish': 'es',
    'Polish': 'pl',
    'Arabic': 'ar',
    'Tagalog': 'tl'
    }

def addon_log(string):
    try:
        log_message = string.encode('utf-8', 'ignore')
    except:
        log_message = 'addonException: addon_log: %s' %format_exc()
    xbmc.log("[%s-%s]: %s" %(addon_id, addon_version, log_message), level=xbmc.LOGNOTICE)


def make_request(url, headers=None, get_url=False):
    addon_log('Request: '+url)
    if headers is None:
        headers = {
            'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0',
            'Referer' : 'http://www.justin.tv/'
            }
    try:
        req = urllib2.Request(url,None,headers)
        response = urllib2.urlopen(req)
        if get_url:
            data = response.geturl()
        else:
            data = response.read()
        # addon_log(str(response.info()))
        response.close()
        return data
    except urllib2.URLError, e:
        data = None
        errorStr = str(e.read())
        addon_log('We failed to open "%s".' %url)
        if hasattr(e, 'reason'):
            addon_log('We failed to reach a server.')
            addon_log('Reason: %s' %e.reason)
        if hasattr(e, 'code'):
            addon_log('We failed with error code - %s.' %e.code)


def get_lang_code(language):
    for i in LANGUAGES.items():
        if i[1] == language:
            lang_code = i[0]
            return lang_code


def get_category_list():
    return make_request(api_url + '/category/list.json')


def display_main_dir():
    all_icon = os.path.join(addon_path, 'resources', 'icons','all.png')
    fav_icon = os.path.join(addon_path, 'resources', 'icons','fav.png')
    jfav_icon = os.path.join(addon_path, 'resources', 'icons','jfav.png')
    search_icon = os.path.join(addon_path, 'resources', 'icons', 'search.png')
    if xbmcvfs.exists(favorites_file):
        favorites_list = open(favorites_file).read()
        if favorites_list:
            add_dir('Favorites', 'get_favorites', fav_icon, 'get_favorites')
    justin_user_name = addon.getSetting('j_user')
    if justin_user_name:
        add_dir('%s Favorites / Follows' %justin_user_name, justin_user_name, jfav_icon, 'get_justin_favorites')
    add_dir('All', '', all_icon, 'get_all')
    data = json.loads(cache.cacheFunction(get_category_list))
    for i in data.keys():
        if data[i]['name'] in ['Creativity', 'Poker']:
            item_icon = all_icon
        else:
            item_icon = os.path.join(addon_path, 'resources', 'icons', data[i]['icon'].split('/')[-1])
        add_dir(data[i]['name'], 'subcategory', item_icon, 'get_subcategories', {'category_id': i})
    add_dir('Enter Channel Name', 'get_channel', all_icon,'get_channel')
    add_dir('Search', 'get_search', search_icon, 'get_search')
    return end_of_dir()


def display_subcategories(category_id, iconimage):
    data = json.loads(cache.cacheFunction(get_category_list))
    if len(data[category_id]['subcategories'].keys()) == 1:
        sub_category = data[category_id]['subcategories'].keys()[0]
        return get_channels(sub_category, category_id)
    if len(data[category_id]['subcategories'].keys()) > 1:
        add_dir('All', '', iconimage, 'get_channels', {'category_id': category_id})
        items = data[category_id]['subcategories']
        for i in items.keys():
            info = {'category_id': category_id, 'sub_category': i}
            add_dir(items[i]['name'], 'display_channels', iconimage, 'get_channels', info)
        return end_of_dir()
    return get_channels(None, category_id)


def get_channels(sub_category, category_id, page=None):
    url = api_url + '/stream/list.json?'
    if category_id:
        url += 'category=%s' %category_id
    if sub_category:
        url +='&subcategory=%s' %sub_category
    if not addon.getSetting('lang') == "None":
        url += '&language=%s' %languages[addon.getSetting('lang')]
        if not addon.getSetting('lang1') == "None":
            url += ',%s' %languages[addon.getSetting('lang1')]
    if page is None:
        page = 1
    else:
        page = int(page)
    url += '&limit=20&offset=%s' %((page -1) * 20)
    addon_log('LiveData URL: %s' %url)
    data = make_request(url)
    if data:
        return display_channels(data, sub_category, category_id, page)


def display_channels(data, sub_category, category_id, page):
    data = json.loads(data)
    if not isinstance(data, list):
        addon_log('data type: %s' %type(data))
        data = [data]
    addon_log('json data: %s' %data)
    addon_log('Len Data: %s' %str(len(data)))
    addon_log('page: %s' %str(page))
    try:
        blacklist = json.loads(open(blacklist_file).read())
    except:
        blacklist = None
    desc_keys = [
        'video_bitrate',
        'video_codec',
        'audio_codec',
        'video_height',
        'video_width',
        'category',
        'subcategory',
        'up_time',
        'geo',
        'meta_game',
        'language',
        'stream_count',
        'channel_view_count',
        'featured',
        'broadcast_part',
        'name',
        'stream_type'
        ]
    for i in data:
        if not i.has_key('channel'):
            addon_log('No channel data: %s' %i)
        info = {}

        desc = ' | '.join(['%s: %s' %(k.replace('_', ' ').title(), i[k]) for
                           k in desc_keys if i.has_key(k) and i[k]])
        if desc:
            info['plot'] = desc
        if i.has_key('channel'):
            if i['channel'].has_key('login') and i['channel']['login']:
                name = i['channel']['login']
        elif i.has_key('login') and i['login']:
            name = i['login']
        elif i.has_key('name') and i['name']:
            name = i['name'].split('user_')[-1]
        else:
            try:
                name = str(i['image_url_medium']).split('/')[-1].split('-')[0]
            except:
                addon_log('Name not found: %s' %i)
                continue
        if blacklist and name in blacklist:
            addon_log('Channel: %s - Blacklisted' %name)
            continue
        if i.has_key('channel'):
            if (i['channel'].has_key('status') and i['channel']['status'] and
                    i['channel']['status'] != 'Broadcasting LIVE on Justin.tv'):
                info['title'] = i['channel']['status']
            elif i['channel'].has_key('title') and i['channel']['title']:
                info['title'] = i['channel']['title']
        elif i.has_key('title') and i['title']:
            info['title'] = i['title']
        else:
            info['title'] = name

        thumb = None
        fanart = None
        if addon.getSetting('fanart') == "true":
            if i.has_key('channel'):
                if i['channel'].has_key('image_url_huge') and i['channel']['image_url_huge']:
                    fanart = i['channel']['image_url_huge']
            elif i.has_key('image_url_huge') and i['image_url_huge']:
                fanart = i['image_url_huge']
            info['fanart'] = fanart
        if addon.getSetting('use_channel_icon') == "0" and fanart:
            thumb = fanart
        if not thumb:
            if i.has_key('channel'):
                if i['channel'].has_key('screen_cap_url_large') and i['channel']['screen_cap_url_large']:
                    thumb = i['channel']['screen_cap_url_large']
                elif i['channel'].has_key('image_url_large') and i['channel']['image_url_large']:
                    thumb = i['channel']['image_url_large']
            elif i.has_key('image_url_large') and i['image_url_large']:
                thumb = i['image_url_large']
        if not thumb:
            addon_log('No Thumb')
            thumb = addon_icon
        if not fanart:
            addon_log('No Fanart')
            fanart = addon_fanart
        add_dir(name, 'play_stream', thumb, 'set_resolved_url', info, get_stream_info(i))

    if not category_id == 'search':
        page_num = None
        if len(data) == 20:
            if page:
                page_num = page + 1
            else:
                page_num = 1
        if page_num:
            info = {'category_id': category_id, 'sub_category': sub_category, 'page': page_num}
            next_png = os.path.join(addon_path, 'resources', 'icons','next.png')
            add_dir('Next Page', 'load_more_channels', next_png, 'get_channels', info)
    return end_of_dir(True)


def get_stream_info(item_dict):
    stream_info = {'video_info': {}, 'audio_info': {}}
    if item_dict.has_key('video_codec') and item_dict['video_codec']:
        stream_info['video_info']['codec'] = item_dict['video_codec']
    if item_dict.has_key('video_height') and item_dict['video_height']:
        stream_info['video_info']['height'] = item_dict['video_height']
    if item_dict.has_key('video_width') and item_dict['video_width']:
        stream_info['video_info']['width'] = item_dict['video_width']
    if (item_dict.has_key('audio_codec') and
        item_dict['audio_codec'] and item_dict['audio_codec'] != '???'):
            stream_info['audio_info']['codec'] = item_dict['audio_codec']
    return stream_info


def get_user_data(user_name):
    url = api_url + '/user/show/%s.json' %user_name
    data = make_request(url)
    if data and not data == '[]':
        addon_log('User Data: %s' %data)
        return data


def get_user_favorites(justin_user_name):
    url = api_url + '/user/favorites/%s.json?limit=100' %justin_user_name
    if addon.getSetting('live_only') == "true":
        url += '&live=true'
    data = make_request(url)
    if data:
        return display_channels(data, '', '', None)


def display_channel_archives(name, url=None):
    if url is None:
        url = api_url + '/channel/archives/%s.json' %name
    responce = make_request(url)
    next_png = os.path.join(addon_path, 'resources', 'icons','next.png')
    if responce and responce != '[]':
        data = json.loads(responce)
        for i in data:
            info = {}
            info['plot'] = ' | '.join(['%s: %s' %(k.replace('_', ' ').title(), i[k]) for
                                       k in i.keys() if i[k]])
            stream_url = i['video_file_url']
            thumb = i['image_url_medium']
            info['title'] = i['title'].encode('utf-8')
            if i.has_key('broadcast_part') and i['broadcast_part']:
                info['title'] += ' - Part: %s' %i['broadcast_part'].encode('utf-8')
            if i.has_key('length') and i['length']:
                info['duration'] = int(i['length']) / 60
            add_dir(info['title'], stream_url, thumb, 'set_archive_url', info, get_stream_info(i))

        if len(data) == 20:
            if not 'offset=' in url:
                url = url + '?offset=20'
            else:
                offset = int(url.split('offset=')[1])
                url = url.split('?')[0]+'?offset=%s' %(offset + 20)
            add_dir('Next Page', url, next_png, 'get_channel_archives')
        return end_of_dir(True)
    else:
        notify('No archives found for channel: %s' %name)


def notify(message):
    xbmc.executebuiltin("XBMC.Notification(Addon Notification,%s,5000,%s)"
                        %(message, addon_icon))


def resolve_url(channel_name, password=None):
    url = 'https://api.twitch.tv/api/channels/%s/access_token?as3=t' %channel_name
    data = json.loads(make_request(url))
    if not data:
        addon_log('No Data: api.twitch.tv')
        notify('Channel data not found')
        return
    token_data = json.loads(data['token'])
    for i in token_data:
        addon_log('%s: %s' %(i, token_data[i]))

    private_code = 'null'
    if not token_data['private']['allowed_to_view']:
        if token_data['needed_info']:
            addon_log('needed_info: %s' %token_data['needed_info'])
            if 'private' in token_data['needed_info']:
                if not password:
                    password = get_password(channel_name)
                private_code = urllib2.quote(password)
    params = [
        'nauthsig=%s' %data['sig'],
        'player=jtvweb',
        'private_code=%s' %private_code,
        'type=any',
        'nauth=%s' %urllib2.quote(data['token']),
        'allow_source=true',
            ]
    stream_url = 'http://usher.twitch.tv/select/%s.json?' %channel_name + '&'.join(params)
    return stream_url


def set_resolved_url(resolved_url):
    success = False
    if resolved_url:
        success = True
    else:
        resolved_url = ''
    item = xbmcgui.ListItem(path=resolved_url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), success, item)


def loadPasswords():
    passwords = {}
    if addon.getSetting('save_passwords') == 'true':
        if xbmcvfs.exists(passwords_file):
            passwords = json.loads(open(passwords_file).read())
    return passwords


def savePasswords(passwords):
    if addon.getSetting('save_passwords') == 'true':
        f = open(passwords_file, "w")
        f.write(json.dumps(passwords))
        f.close()


def get_password(name):
    passwords = loadPasswords()
    password = ''
    if name in passwords:
        password = passwords[name]
    keyboard = xbmc.Keyboard(password,'Enter Password')
    keyboard.doModal()
    if (keyboard.isConfirmed() == False):
        return
    password = keyboard.getText()
    passwords[name] = password
    savePasswords(passwords)
    if len(password) == 0:
        return None
    else:
        return password


def add_dir(name, url, iconimage, mode, info={}, stream_info={}):
    isfolder = True
    fanart = addon_fanart
    params = {'name': name, 'url': url, 'mode': mode, 'iconimage': iconimage}
    if info.has_key('category_id') and info['category_id']:
        params['category_id'] = info['category_id']
    if info.has_key('sub_category') and info['sub_category']:
        params['sub_category'] = info['sub_category']
    if info.has_key('page'):
        params['page'] = info['page']
    url = '%s?%s' %(sys.argv[0], urllib.urlencode(params))
    if info.has_key('title'):
        title = info['title']
    else:
        title = name
    listitem = xbmcgui.ListItem(title, iconImage=iconimage, thumbnailImage=iconimage)
    if stream_info:
        if stream_info['video_info'].keys():
            listitem.addStreamInfo('video', stream_info['video_info'])
        if stream_info['audio_info'].keys():
            listitem.addStreamInfo('audio', stream_info['audio_info'])
    if info.has_key('fanart') and info['fanart']:
        fanart = info['fanart']
    listitem.setProperty("Fanart_Image", fanart)
    context_menu = []
    if info.has_key('fav'):
        context_menu.append(
            ('Remove from Jtv Favorites',
             'XBMC.RunPlugin(%s?mode=remove_fav&name=%s)'
              %(sys.argv[0], urllib.quote(name))))
    else:
        context_menu.append(
            ('Add to Jtv Favorites',
             'XBMC.RunPlugin(%s?mode=add_favorite&params=%s&info=%s)'
             %(sys.argv[0], urllib.quote(json.dumps(params)),
               urllib.quote(json.dumps(info)))))
    if mode in ['resolve_url', 'set_resolved_url', 'set_archive_url']:
        isfolder = False
        listitem.setProperty('IsPlayable', 'true')
        listitem.setInfo('video', infoLabels=info)
        context_menu.append(
            ('Get Channel Archives',
             'XBMC.Container.Update(%s?mode=get_channel_archives&name=%s)'
             %(sys.argv[0], urllib.quote(name))))
        context_menu.append(
            ('Run IrcChat',
             "RunScript(script.ircchat,"
             "run_irc=True&nickname=%s&username=%s&password=%s&host=%s&channel=%s)"
             %(j_nick, j_nick, j_pass, 'irc.twitch.tv', name)))
        context_menu.append(
            ('Blacklist Channel','XBMC.RunPlugin(%s?mode=blacklist_channel&name=%s)'
             %(sys.argv[0], urllib.quote(name))))
    if mode == 'search' and name == 'Previous Search Queries':
        context_menu.append(
            ('Remove',
             'XBMC.Container.Update(%s?mode=remove_query&name=%s)'
             %(sys.argv[0], urllib.quote(name))))
    listitem.addContextMenuItems(context_menu)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, listitem, isfolder)


def search(search_q, url=None):
    if search_q == 'Previous Search Queries':
        search_icon = os.path.join(addon_path, 'resources', 'icons', 'search.png')
        search_list = json.loads(open(search_queries).read())
        for i in search_list:
            addon_log('search type: %s' %type(i))
            if isinstance(i, list):
                # prior to 4.0 will return a list
                title = i[0]
            else:
                title = i
            add_dir(title, 'saved_search_query', search_icon, 'search')
        return end_of_dir()

    elif search_q == 'New Search':
        keyboard = xbmc.Keyboard('','Search')
        keyboard.doModal()
        if (keyboard.isConfirmed() == False):
            return
        search_q = keyboard.getText()
        if len(search_q) == 0:
            return
        if addon.getSetting('save_search') == 'true':
            search_file = xbmcvfs.exists(search_queries)
            if not search_file:
                search_list = []
            else:
                search_list = json.loads(open(search_queries).read())
            search_list.append(search_q)
            a = open(search_queries, "w")
            a.write(json.dumps(search_list))
            a.close()

    url = 'http://api.justin.tv/api/stream/search/%s.json' %urllib.quote(search_q)
    addon_log('Search URL: '+url)
    data = make_request(url)
    if data:
        return display_channels(data, sub_category, category_id, None)
    else:
        return notify('No Results for: %s' %search_q)


def remove_search(name):
    search_list = json.loads(open(search_queries).read())
    for i in range(len(search_list)):
        if name in search_list[i]:
            del search_list[i]
            a = open(search_queries, "w")
            a.write(json.dumps(search_list))
            a.close()
            return xbmc.executebuiltin('Container.Refresh')


def get_search():
    if addon.getSetting('save_search') == 'true':
        search_file = xbmcvfs.exists(search_queries)
        if search_file:
            search_icon = os.path.join(addon_path, 'resources', 'icons', 'search.png')
            add_dir('New Search', 'new_search', search_icon, 'search')
            add_dir('Previous Search Queries', 'previous_search', search_icon, 'search')
            return end_of_dir()
    else:
        return search('New Search')


def get_channel(channel_name, play=False, password=None):
    if channel_name == 'Enter Channel Name':
        keyboard = xbmc.Keyboard('','Channel Name')
        keyboard.doModal()
        if (keyboard.isConfirmed() == False):
            return
        channel_name = keyboard.getText()
        if len(channel_name) == 0:
            return

    user_data = get_user_data(channel_name)
    if not user_data:
        return notify('Did not find channel: %s' %channel_name)

    url = api_url + '/stream/list.json?channel=%s' %channel_name
    data = make_request(url)
    if not data or data == '[]':
        display_channels(user_data, None, 'channel', None)
        dialog = xbmcgui.Dialog()
        ret = dialog.yesno('%s is a valid channel' %channel_name,
                           'The channel does not seem to be live\n',
                           'Do you want to check for archives?')
        if ret:
            return display_channel_archives(channel_name, password)
    else:
        if play == 'player':
            return xbmc.Player().play(resolve_url(channel_name, password))
        elif play:
            return set_resolved_url(resolve_url(channel_name, password))
        return display_channels(data, None, 'channel', None)


def display_favorites():
    favorites_list = open(favorites_file).read()
    for i in json.loads(favorites_list):
        if isinstance(i[0], dict):
            i[1]['fav'] = True
            add_dir(i[0]['name'], i[0]['url'], i[0]['iconimage'], i[0]['mode'], i[1])
        else:
            # pre version 0.4 favorite
            info = {'title': i[2].encode('utf-8'), 'fav': True}
            add_dir(i[0], 'get_channel', i[1], 'get_channel', info)
    return end_of_dir(True)


def add_favorite(params, info):
    info = json.loads(info)
    params = json.loads(params)
    if info.has_key('title'):
        title = info['title']
    else:
        title = params['name']
    keyboard = xbmc.Keyboard(title, 'Rename?')
    keyboard.doModal()
    if (keyboard.isConfirmed() == False):
        return
    title = keyboard.getText()
    if len(title) == 0:
        return
    info['title'] = title
    if xbmcvfs.exists(favorites_file):
        favorites_list = open(favorites_file).read()
        if favorites_list:
            fav_list = json.loads(favorites_list)
        else:
            fav_list = []
    else:
        fav_list = []
    fav_list.append((params, info))
    a = open(favorites_file, "w")
    a.write(json.dumps(fav_list))
    a.close()


def remove_favorite(name):
    data = json.loads(favorites_list)
    for i in range(len(data)):
        if isinstance(data[i][0], dict):
            if name in data[i][0]['name']:
                del data[i]
                break
        elif name in data[i]:
            del data[i]
            break
    a = open(favorites_file, "w")
    a.write(json.dumps(data))
    a.close()
    return xbmc.executebuiltin('Container.Refresh')


def blacklist_channel(name):
    blacklist_ = xbmcvfs.exists(blacklist_file)
    if not blacklist_:
        black_list = []
    else:
        black_list = json.loads(open(blacklist_file, "r").read())
    black_list.append(name)
    f = open(blacklist_file, "w")
    f.write(json.dumps(black_list))
    f.close
    return xbmc.executebuiltin('Container.Refresh')


def get_params():
    p = parse_qs(sys.argv[2][1:])
    for i in p.keys():
        p[i] = p[i][0]
    return p


def set_view_mode():
    view_modes = {
        '0': '502', # List
        '1': '51', # Big List
        '2': '500', # Thumbnails
        '3': '501', # Poster Wrap
        '4': '508', # Fanart
        '5': '504',  # Media info
        '6': '503',  # Media info 2
        '7': '515'  # Media info 3
        }
    view_mode = addon.getSetting('view_mode')
    if view_mode == '8':
        return
    xbmc.executebuiltin('Container.SetViewMode(%s)' %view_modes[view_mode])


def end_of_dir(set_content=False):
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
    if set_content:
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        set_view_mode()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


params = get_params()
addon_log("params: %s" %params)
try:
    mode = params['mode']
except:
    mode = None

if mode == None:
    display_main_dir()

elif mode == 'get_all':
    get_channels(None, None)

elif mode == 'get_subcategories':
    display_subcategories(params['category_id'], params['iconimage'])

elif mode == 'get_channels':
    page = None
    sub_category = None
    if params.has_key('page'):
        page = params['page']
    if params.has_key('sub_category'):
        sub_category = params['sub_category']
    get_channels(sub_category, params['category_id'], page)

elif mode == 'set_resolved_url':
    set_resolved_url(resolve_url(params['name']))
    xbmc.sleep(3000)
    if addon.getSetting('run_chat') == 'true':
        xbmc.executebuiltin(
            "RunScript(script.ircchat,"
            "run_irc=True&nickname=%s&username=%s&password=%s&host=%s&channel=%s)"
            %(j_nick, j_nick, j_pass, 'irc.twitch.tv', params['name']))

elif mode == 'get_search':
    get_search()

elif mode == 'get_channel':
    play = False
    if params.has_key('play') and params['play']:
        play = params['play']
    password = False
    if params.has_key('password') and params['password']:
        password = params['password']
    get_channel(params['name'], play, password)

elif mode == 'get_favorites':
    display_favorites()

elif mode == 'get_channel_archives':
    url = None
    if params.has_key('url'):
        url = params['url']
    display_channel_archives(params['name'], url)

elif mode == 'add_favorite':
    add_favorite(params['params'], params['info'])

elif mode == 'remove_fav':
    remove_favorite(params['name'])

elif mode == 'set_archive_url':
    set_resolved_url(params['url'])

elif mode == 'get_justin_favorites':
    get_user_favorites(params['url'])

elif mode == 'search':
    search(params['name'], params['url'])

elif mode == 'remove_query':
    remove_search(params['name'])

elif mode == 'blacklist_channel':
    blacklist_channel(params['name'])
