import urllib,urllib2,re,cookielib,os,sys
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from resources.libs import main
from urllib2 import (urlopen, Request)
from BeautifulSoup import BeautifulSoup

#Mash Up - by Mash2k3 2012.

from t0mm0.common.addon import Addon
addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.movie25', sys.argv)
art = main.art
from resources.universal import watchhistory
    
wh = watchhistory.WatchHistory('plugin.video.movie25')

def get(url):
    """Performs a GET request for the given url and returns the response"""
    try:
        conn = urlopen(url)
        resp = conn.read()
        conn.close()
        return resp
    except IOError:
        pass
    return ""

def _html(url):
    """Downloads the resource at the given url and parses via BeautifulSoup"""
    return BeautifulSoup(main.OPENURL(url), convertEntities=BeautifulSoup.HTML_ENTITIES)

def _parse_channels_from_html_dom(html):
    items = []
    items.append({
            'title': '2M',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/2m.jpg',
            'path': '2m'})

    items.append({
            'title': 'ANN TV',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/ann_tv.jpg',
            'path': 'ann_tv'})

    items.append({
            'title': 'Abu Dhabi Drama',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/abu_dhabi_drama.jpg',
            'path': 'abu_dhabi_drama'})

    items.append({
            'title': 'Aghanina',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/aghanina.jpg',
            'path': 'aghanina'})

    items.append({
            'title': 'Ajyal',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/ajyal.jpg',
            'path': 'ajyal'})

    items.append({
            'title': 'Al Aoula Maroc',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/al_aoula_maroc.jpg',
            'path': 'al_aoula_maroc'})

    items.append({
            'title': 'Al Haneen Music',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/al_haneen_music.jpg',
            'path': 'al_haneen_music'})

    items.append({
            'title': 'Al Janoubiya',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/al_janoubiya.jpg',
            'path': 'al_janoubiya'})

    items.append({
            'title': 'Al Maghribia',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/al_maghribia.jpg',
            'path': 'al_maghribia'})

    items.append({
            'title': 'Al Majd',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/al_majd.jpg',
            'path': 'al_majd'})

    items.append({
            'title': 'Al Manar',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/al_manar.jpg',
            'path': 'al_manar'})

    items.append({
            'title': 'Al Masriyah',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/al_masriyah.jpg',
            'path': 'al_masriyah'})

    items.append({
            'title': 'Al Moustakilla',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/al_moustakilla.jpg',
            'path': 'al_moustakilla'})

    items.append({
            'title': 'Al Shareka',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/al_shareka.jpg',
            'path': 'al_shareka'})

    items.append({
            'title': 'Al Sharqiya',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/al_sharqiya.jpg',
            'path': 'al_sharqiya'})

    items.append({
            'title': 'Al Sumaria',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/al_sumaria.jpg',
            'path': 'al_sumaria'})

    items.append({
            'title': 'Al Thaniya',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/al_thaniya.jpg',
            'path': 'al_thaniya'})

    items.append({
            'title': 'Al Tunisia',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/al_tunisia.jpg',
            'path': 'al_tunisia'})

    items.append({
            'title': 'Al mayaden',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/al_mayaden.jpg',
            'path': 'al_mayaden'})

    items.append({
            'title': 'Al-Hurria',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/al_hurria.jpg',
            'path': 'al_hurria'})

    items.append({
            'title': 'Al-Nahar Drama',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/al_nahar_drama.jpg',
            'path': 'al_nahar_drama'})

    items.append({
            'title': 'Al-Resalah',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/al_resalah.jpg',
            'path': 'al_resalah'})

    items.append({
            'title': 'Al-hurra Iraq',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/al_hurra_iraq.jpg',
            'path': 'al_hurra_iraq'})

    items.append({
            'title': 'AlGeria',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/algeria.jpg',
            'path': 'algeria'})

    items.append({
            'title': 'Alan',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/alan.jpg',
            'path': 'alan'})

    items.append({
            'title': 'Alarabiya',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/alarabiya.jpg',
            'path': 'alarabiya'})

    items.append({
            'title': 'Algeria 3',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/algeria_3.jpg',
            'path': 'algeria_3'})

    items.append({
            'title': 'Alhayat 1',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/alhayat_1.jpg',
            'path': 'alhayat_1'})

    items.append({
            'title': 'Alhayat Cinema',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/alhayat_cinema.jpg',
            'path': 'alhayat_cinema'})

    items.append({
            'title': 'Alhayat-Series',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/alhayat_series.jpg',
            'path': 'alhayat_series'})

    items.append({
            'title': 'Aliraqiya',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/aliraqiya.jpg',
            'path': 'aliraqiya'})

    items.append({
            'title': 'Aljadeed',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/aljadeed.jpg',
            'path': 'aljadeed'})

    items.append({
            'title': 'Alqudis',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/alqudis.jpg',
            'path': 'alqudis'})

    items.append({
            'title': 'Alrashid',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/alrashid.jpg',
            'path': 'alrashid'})

    items.append({
            'title': 'Alriadia Sport',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/alriadia_sport.jpg',
            'path': 'alriadia_sport'})

    items.append({
            'title': 'Arabica Music',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/arabica_music.jpg',
            'path': 'arabica_music'})

    items.append({
            'title': 'Arrabia',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/arrabia.jpg',
            'path': 'arrabia'})

    items.append({
            'title': 'Assadissa',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/assadissa.jpg',
            'path': 'assadissa'})

    items.append({
            'title': 'BBC Arabic',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/bbc_arabic.jpg',
            'path': 'bbc_arabic'})

    items.append({
            'title': 'Baghdad',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/baghdad.jpg',
            'path': 'baghdad'})

    items.append({
            'title': 'Baghdadia',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/baghdadia.jpg',
            'path': 'baghdadia'})

    items.append({
            'title': 'Bahrain',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/bahrain.jpg',
            'path': 'bahrain'})

    items.append({
            'title': 'Baraem',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/baraem.jpg',
            'path': 'baraem'})

    items.append({
            'title': 'Blue Nile',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/blue_nile.jpg',
            'path': 'blue_nile'})

    items.append({
            'title': 'CBC Drama',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/cbc_drama.jpg',
            'path': 'cbc_drama'})

    items.append({
            'title': 'CBC Tv',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/cbc_tv.jpg',
            'path': 'cbc_tv'})

    items.append({
            'title': 'CCTV Arabic',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/cctv_arabic.jpg',
            'path': 'cctv_arabic'})

    items.append({
            'title': 'CNBC',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/cnbc.jpg',
            'path': 'cnbc'})

    items.append({
            'title': 'Cairo Cinema',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/cairo_cinema.jpg',
            'path': 'cairo_cinema'})

    items.append({
            'title': 'Cairo Drama',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/cairo_drama.jpg',
            'path': 'cairo_drama'})

    items.append({
            'title': 'Cima',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/cima.jpg',
            'path': 'cima'})

    items.append({
            'title': 'Coran',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/coran.jpg',
            'path': 'coran'})

    items.append({
            'title': 'Dream 1',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/dream_1.jpg',
            'path': 'dream_1'})

    items.append({
            'title': 'Dubai One',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/dubai_one.jpg',
            'path': 'dubai_one'})

    items.append({
            'title': 'Dubai Sport 1',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/dubai_sport_1.jpg',
            'path': 'dubai_sport_1'})

    items.append({
            'title': 'Dubai Sport 2',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/dubai_sport_2.jpg',
            'path': 'dubai_sport_2'})

    items.append({
            'title': 'Dubai',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/dubai.jpg',
            'path': 'dubai'})

    items.append({
            'title': 'Echorouk Tv',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/echorouk_tv.jpg',
            'path': 'echorouk_tv'})

    items.append({
            'title': 'Fatafeat',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/fatafeat.jpg',
            'path': 'fatafeat'})

    items.append({
            'title': 'Fox Movies',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/fox_movies.jpg',
            'path': 'fox_movies'})

    items.append({
            'title': 'Fox',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/fox.jpg',
            'path': 'fox'})

    items.append({
            'title': 'France24 Arabic',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/france24_arabic.jpg',
            'path': 'france24_arabic'})

    items.append({
            'title': 'Funoon',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/funoon.jpg',
            'path': 'funoon'})

    items.append({
            'title': 'Fx Arabia',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/fx_arabia.jpg',
            'path': 'fx_arabia'})

    items.append({
            'title': 'Ghinwa',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/ghinwa.jpg',
            'path': 'ghinwa'})

    items.append({
            'title': 'Hanibal',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/hanibal.jpg',
            'path': 'hanibal'})

    items.append({
            'title': 'Hi music',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/hi_music.jpg',
            'path': 'hi_music'})

    items.append({
            'title': 'Infinity',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/infinity.jpg',
            'path': 'infinity'})

    items.append({
            'title': 'Iqra',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/iqra.jpg',
            'path': 'iqra'})

    items.append({
            'title': 'Jordan',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/jordan.jpg',
            'path': 'jordan'})

    items.append({
            'title': 'KSA 1',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/ksa_1.jpg',
            'path': 'ksa_1'})

    items.append({
            'title': 'Kurdistan',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/kurdistan.jpg',
            'path': 'kurdistan'})

    items.append({
            'title': 'Kuwait',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/kuwait.jpg',
            'path': 'kuwait'})

    items.append({
            'title': 'LLBN',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/llbn.jpg',
            'path': 'llbn'})

    items.append({
            'title': 'Lbc Europe',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/lbc_europe.jpg',
            'path': 'lbc_europe'})

    items.append({
            'title': 'Lbc',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/lbc.jpg',
            'path': 'lbc'})

    items.append({
            'title': 'Libya',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/libya.jpg',
            'path': 'libya'})

    items.append({
            'title': 'MBC 2',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/mbc_2.jpg',
            'path': 'mbc_2'})

    items.append({
            'title': 'MBC 3',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/mbc_3.jpg',
            'path': 'mbc_3'})

    items.append({
            'title': 'MBC 4',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/mbc_4.jpg',
            'path': 'mbc_4'})

    items.append({
            'title': 'MBC Action',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/mbc_action.jpg',
            'path': 'mbc_action'})

    items.append({
            'title': 'MBC Bollywood',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/mbc_bollywood.jpg',
            'path': 'mbc_bollywood'})

    items.append({
            'title': 'MBC Drama',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/mbc_drama.jpg',
            'path': 'mbc_drama'})

    items.append({
            'title': 'MBC Masr',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/mbc_masr.jpg',
            'path': 'mbc_masr'})

    items.append({
            'title': 'MBC Max',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/mbc_max.jpg',
            'path': 'mbc_max'})

    items.append({
            'title': 'MBC Persia',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/mbc_persia.jpg',
            'path': 'mbc_persia'})

    items.append({
            'title': 'Maghreb 1',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/maghreb_1.jpg',
            'path': 'maghreb_1'})

    items.append({
            'title': 'Masrawi Aflam',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/masrawi_aflam.jpg',
            'path': 'masrawi_aflam'})

    items.append({
            'title': 'Mauritanie',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/mauritanie.jpg',
            'path': 'mauritanie'})

    items.append({
            'title': 'Mazeka zoom',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/mazeka_zoom.jpg',
            'path': 'mazeka_zoom'})

    items.append({
            'title': 'Mazzika',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/mazzika.jpg',
            'path': 'mazzika'})

    items.append({
            'title': 'Medi 1 Sat',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/medi_1_sat.jpg',
            'path': 'medi_1_sat'})

    items.append({
            'title': 'Mehwar',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/mehwar.jpg',
            'path': 'mehwar'})

    items.append({
            'title': 'Melody Aflam',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/melody_aflam.jpg',
            'path': 'melody_aflam'})

    items.append({
            'title': 'Melody Tv',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/melody_tv.jpg',
            'path': 'melody_tv'})

    items.append({
            'title': 'Moga Comedy',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/moga_comedy.jpg',
            'path': 'moga_comedy'})

    items.append({
            'title': 'Mtv',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/mtv.jpg',
            'path': 'mtv'})

    items.append({
            'title': 'Music plus',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/music_plus.jpg',
            'path': 'music_plus'})

    items.append({
            'title': 'NBN',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/nbn.jpg',
            'path': 'nbn'})

    items.append({
            'title': 'National Geo Ad',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/national_geo_ad.jpg',
            'path': 'national_geo_ad'})

    items.append({
            'title': 'Nessma khadhra',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/nessma_khadhra.jpg',
            'path': 'nessma_khadhra'})

    items.append({
            'title': 'Nessma',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/nessma.jpg',
            'path': 'nessma'})

    items.append({
            'title': 'Nile Cinema',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/nile_cinema.jpg',
            'path': 'nile_cinema'})

    items.append({
            'title': 'Nile Comedy',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/nile_comedy.jpg',
            'path': 'nile_comedy'})

    items.append({
            'title': 'Nile Drama 2',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/nile_drama_2.jpg',
            'path': 'nile_drama_2'})

    items.append({
            'title': 'Nile Drama',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/nile_drama.jpg',
            'path': 'nile_drama'})

    items.append({
            'title': 'Nile Family',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/nile_family.jpg',
            'path': 'nile_family'})

    items.append({
            'title': 'Nile News',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/nile_news.jpg',
            'path': 'nile_news'})

    items.append({
            'title': 'Nile Sport',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/nile_sport.jpg',
            'path': 'nile_sport'})

    items.append({
            'title': 'Noor Dubai',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/noor_dubai.jpg',
            'path': 'noor_dubai'})

    items.append({
            'title': 'Noursat',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/noursat.jpg',
            'path': 'noursat'})

    items.append({
            'title': 'OTV Lebanon',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/otv_lebanon.jpg',
            'path': 'otv_lebanon'})

    items.append({
            'title': 'On TV',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/on_tv.jpg',
            'path': 'on_tv'})

    items.append({
            'title': 'Palestine',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/palestine.jpg',
            'path': 'palestine'})

    items.append({
            'title': 'Panorama',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/panorama.jpg',
            'path': 'panorama'})

    items.append({
            'title': 'Rotana Aflam',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/rotana_aflam.jpg',
            'path': 'rotana_aflam'})

    items.append({
            'title': 'Rotana Cinema',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/rotana_cinema.jpg',
            'path': 'rotana_cinema'})

    items.append({
            'title': 'Rotana Clip',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/rotana_clip.jpg',
            'path': 'rotana_clip'})

    items.append({
            'title': 'Rotana Khaligi',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/rotana_khaligi.jpg',
            'path': 'rotana_khaligi'})

    items.append({
            'title': 'Rotana Masriya',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/rotana_masriya.jpg',
            'path': 'rotana_masriya'})

    items.append({
            'title': 'Rotana Music',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/rotana_music.jpg',
            'path': 'rotana_music'})

    items.append({
            'title': 'Rotana classic',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/rotana_classic.jpg',
            'path': 'rotana_classic'})

    items.append({
            'title': 'Royali Somali',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/royali_somali.jpg',
            'path': 'royali_somali'})

    items.append({
            'title': 'Russia Alyaum',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/russia_alyaum.jpg',
            'path': 'russia_alyaum'})

    items.append({
            'title': 'Sama Dubai',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/sama_dubai.jpg',
            'path': 'sama_dubai'})

    items.append({
            'title': 'Samira Tv',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/samira_tv.jpg',
            'path': 'samira_tv'})

    items.append({
            'title': 'Sharjah',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/sharjah.jpg',
            'path': 'sharjah'})

    items.append({
            'title': 'Spacetoon',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/spacetoon.jpg',
            'path': 'spacetoon'})

    items.append({
            'title': 'Star Cinema',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/star_cinema.jpg',
            'path': 'star_cinema'})

    items.append({
            'title': 'Sudan TV',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/sudan_tv.jpg',
            'path': 'sudan_tv'})

    items.append({
            'title': 'Syria Drama',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/syria_drama.jpg',
            'path': 'syria_drama'})

    items.append({
            'title': 'Syria',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/syria.jpg',
            'path': 'syria'})

    items.append({
            'title': 'Tamazigh Algeria',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/tamazigh_algeria.jpg',
            'path': 'tamazigh_algeria'})

    items.append({
            'title': 'Time Comedy',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/time_comedy.jpg',
            'path': 'time_comedy'})

    items.append({
            'title': 'Top Movies',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/top_movies.jpg',
            'path': 'top_movies'})

    items.append({
            'title': 'Tounesna',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/tounesna.jpg',
            'path': 'tounesna'})

    items.append({
            'title': 'Toyor Al Janah',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/toyor_al_janah.jpg',
            'path': 'toyor_al_janah'})

    items.append({
            'title': 'Toyor baby',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/toyor_baby.jpg',
            'path': 'toyor_baby'})

    items.append({
            'title': 'Tunisia national 1',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/tunisia_national_1.jpg',
            'path': 'tunisia_national_1'})

    items.append({
            'title': 'Tunisia national 2',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/tunisia_national_2.jpg',
            'path': 'tunisia_national_2'})

    items.append({
            'title': 'Yemen',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/yemen.jpg',
            'path': 'yemen'})

    items.append({
            'title': 'Zagros',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/zagros.jpg',
            'path': 'zagros'})

    items.append({
            'title': 'Zaitouna',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/zaitouna.jpg',
            'path': 'zaitouna'})

    items.append({
            'title': 'Zee Aflam',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/zee_aflam.jpg',
            'path': 'zee_aflam'})

    items.append({
            'title': 'Zee Alwan',
            'thumbnail': 'http://www.teledunet.com/tv_/icones/zee_alwan.jpg',
            'path': 'zee_alwan'})
    items.append({
            'title': 'JSC +1',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_1'})
    items.append({
            'title': 'JSC +2',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_2'})
    items.append({
            'title': 'JSC +3',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_3'})
    items.append({
            'title': 'JSC +4',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_4'})
    items.append({
            'title': 'JSC +5',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_5'})
    items.append({
            'title': 'JSC +6',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_6'})
    items.append({
            'title': 'JSC +7',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_7'})
    items.append({
            'title': 'JSC +8',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_8'})
    items.append({
            'title': 'JSC +9',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_9'})
    items.append({
            'title': 'JSC +10',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_10'})
    items.append({
            'title': 'Abu Dhabi Al Oula',
            'thumbnail': 'https://www.zawya.com/pr/images/2009/ADTV_One_RGB_2009_10_08.jpg',
            'path': 'abu_dhabi'})
    items.append({
            'title': 'Abu Dhabi Sports',
            'thumbnail': 'https://si0.twimg.com/profile_images/2485587448/2121.png',
            'path': 'abu_dhabi_sports_1'})
    items.append({
            'title': 'Al Jazeera',
            'thumbnail': 'http://www.chicagonow.com/chicago-sports-media-watch/files/2013/04/Al-Jazeera.jpg',
            'path': 'aljazeera'})
    items.append({
            'title': 'JAl Jazeera Sport 1',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'aljazeera_sport_1'})
    items.append({
            'title': 'Al Jazeera Sport 2',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'aljazeera_sport_2'})
    items.append({
            'title': 'Al Jazeera Mubasher Masr',
            'thumbnail': 'http://www.chicagonow.com/chicago-sports-media-watch/files/2013/04/Al-Jazeera.jpg',
            'path': 'aljazeera_mubasher_masr'})
    items.append({
            'title': 'Al Jazeera Children',
            'thumbnail': 'http://www.chicagonow.com/chicago-sports-media-watch/files/2013/04/Al-Jazeera.jpg',
            'path': 'aljazeera_children'})
    
    return items

def MAIN():
    main.GA("Live","ArabicStreams")
    items = _parse_channels_from_html_dom('http://www.teledunet.com/')
    for channels in sorted(items):
        main.addPlayL(channels['title'],channels['path'],232,channels['thumbnail'],'','','','','',secName='Arabic Streams',secIcon=art+'/arabicstream.png')

        

def _get_channel_time_player(channel_name):
    #from t0mm0.common.net import Net as net
    url = 'http://www.teledunet.com/tv_/?channel=%s&no_pub' % channel_name
    """source = net().http_GET(url).content
    cookie=net().get_cookies()
    cooks= str(cookie)
    cook = re.findall("value='([^<]+)', port=None", cooks)[0]
    print str(cook)"""
    req = Request(url)
    req.add_header('Referer', 'http://www.teledunet.com/')
    req.add_header('Cookie', 'PHPSESSID=cbebf918442d1f43c0423c182847d14c')
    # Simulate request is coming from website
    html = get(req)
    m = re.search('time_player=(.*);', html, re.M | re.I)
    time_player_str = eval(m.group(1))
    

    m = re.search('curent_media=\'(.*)\';', html, re.M | re.I)
    rtmp_url = m.group(1)
    play_path= rtmp_url[rtmp_url.rfind("/")+1:]
    tpID=repr(time_player_str).rstrip('0').rstrip('.')
    swfUrl='swfUrl=http://www.teledunet.com/tv/player.swf?bufferlength=5&repeat=single&autostart=true&id0=%s&streamer=%s&file=%s&provider=rtmp' %(tpID, rtmp_url, play_path, )
    return rtmp_url+' app=teledunet '+swfUrl+' playpath='+play_path+' live=1 timeout=15 pageUrl='+url


        
def LINK(mname,url,thumb):
        main.GA("ArabicStreams","Watched")
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Opening Stream,3000)")
        stream_url = _get_channel_time_player(url)
        ok=True
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        
        listitem = xbmcgui.ListItem(thumbnailImage=thumb)
        infoL={'Title': mname, 'Genre': 'Live'} 
        from resources.universal import playbackengine
        player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type='movie', title=mname,season='', episode='', year='',img=thumb,infolabels=infoL, watchedCallbackwithParams='',imdb_id='')

        #WatchHistory
        if selfAddon.getSetting("whistory") == "true":
            wh.add_item(mname+' '+'[COLOR green]ArabicStreams[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
        return ok


