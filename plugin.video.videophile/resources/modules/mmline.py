#MegaMovieLine Module by o9r1sh October 2013
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,sys,main,xbmc,os

net = main.net
artwork = main.artwork
settings = main.settings
base_url = 'http://www.megamovieline.com'

def CATEGORIES():
        main.addDir('A-Z',base_url + '/movies/sort/alphabet/page/1','mmlineIndex',artwork + '/main/a-z.png')
        main.addDir('Recently Added',base_url + '/movies/sort/recently/page/1','mmlineIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '/movies/sort/popular/page/1','mmlineIndex',artwork + '/main/popular.png')
        main.addDir('Highly Rated',base_url + '/movies/sort/ratings/page/1','mmlineIndex',artwork + '/main/toprated.png')
        main.addDir('Genres','None','mmlineGenres',artwork + '/main/genres.png')
        main.addDir('Search','None','mmlineSearch',artwork + '/main/search.png')

def GENRES():
        main.addDir('Action',base_url + '/movies/gen/Action/page/1','mmlineAction',artwork + '/genres/action.png')
        main.addDir('Adventure',base_url + '/movies/gen/Adventure/page/1','mmlineAdventure',artwork + '/genres/adventure.png')
        main.addDir('Animation',base_url + '/movies/gen/Animation/page/1','mmlineAnimation',artwork + '/genres/animation.png')
        main.addDir('Biography',base_url + '/movies/gen/Biography/page/1','mmlineBiography',artwork + '/genres/biography.png')
        main.addDir('Comedy',base_url + '/movies/gen/Comedy/page/1','mmlineComedy',artwork + '/genres/comedy.png')
        main.addDir('Crime',base_url + '/movies/gen/Crime/page/1','mmlineCrime',artwork + '/genres/crime.png')
        main.addDir('Documentary',base_url + '/movies/gen/Documentary/page/1','mmlineDocumentary',artwork + '/genres/docs.png')
        main.addDir('Drama',base_url + '/movies/gen/Drama/page/1','mmlineDrama',artwork + '/genres/drama.png')
        main.addDir('Family',base_url + '/movies/gen/Family/page/1','mmlineFamily',artwork + '/genres/family.png')
        main.addDir('Fantasy',base_url + '/movies/gen/Fantasy/page/1','mmlineFantasy',artwork + '/genres/fantasy.png')
        main.addDir('History',base_url + '/movies/gen/History/page/1','mmlineHistory',artwork + '/genres/history.png')
        main.addDir('Horror',base_url + '/movies/gen/Horror/page/1','mmlineHorror',artwork + '/genres/horror.png')
        main.addDir('Music',base_url + '/movies/gen/Music/page/1','mmlineMusic',artwork + '/genres/music.png')
        main.addDir('Musical',base_url + '/movies/gen/Musical/page/1','mmlineMusical',artwork + '/genres/musical.png')
        main.addDir('Mystery',base_url + '/movies/gen/Mystery/page/1','mmlineMystery',artwork + '/genres/mystery.png')
        main.addDir('Romance',base_url + '/movies/gen/Romance/page/1','mmlineRomance',artwork + '/genres/romance.png')
        main.addDir('Sci-Fi',base_url + '/movies/gen/Sci-Fi/page/1','mmlineScifi',artwork + '/genres/sci-fi.png')
        main.addDir('Sport',base_url + '/movies/gen/Sport/page/1','mmlineSport',artwork + '/genres/sport.png')
        main.addDir('Thriller',base_url + '/movies/gen/Thriller/page/1','mmlineThriller',artwork + '/genres/thriller.png')
        main.addDir('War',base_url + '/movies/gen/War/page/1','mmlineWar',artwork + '/genres/war.png')
        main.addDir('Western',base_url + '/movies/gen/Western/page/1','mmlineWestern',artwork + '/genres/western.png')
        main.addDir('Indian',base_url + '/movies/gen/Indian/page/1','mmlineIndian',artwork + '/genres/indian.png')
        main.addDir('Short',base_url + '/movies/gen/Short/page/1','mmlineShort',artwork + '/genres/short.png')
        main.addDir('Classic',base_url + '/movies/gen/Classic/page/1','mmlineClassic',artwork + '/genres/classic.png')

def ACTION():
        main.addDir('A-Z',base_url + '/movies/gen/Action/sort/alphabet/page/1','mmlineIndex',artwork + '/main/a-z.png')
        main.addDir('Recently Added',base_url + '/movies/gen/Action/sort/recently/page/1','mmlineIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '/movies/gen/Action/sort/popular/page/1','mmlineIndex',artwork + '/main/popular.png')
        main.addDir('Highly Rated',base_url + '/movies/gen/Action/sort/ratings/page/1','mmlineIndex',artwork + '/main/toprated.png')

        
def ADVENTURE():
        main.addDir('A-Z',base_url + '/movies/gen/Adventure/sort/alphabet/page/1','mmlineIndex',artwork + '/main/a-z.png')
        main.addDir('Recently Added',base_url + '/movies/gen/Adventure/sort/recently/page/1','mmlineIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '/movies/gen/Adventure/sort/popular/page/1','mmlineIndex',artwork + '/main/popular.png')
        main.addDir('Highly Rated',base_url + '/movies/gen/Adventure/sort/ratings/page/1','mmlineIndex',artwork + '/main/toprated.png')

        
def ANIMATION():
        main.addDir('A-Z',base_url + '/movies/gen/Animation/sort/alphabet/page/1','mmlineIndex',artwork + '/main/a-z.png')
        main.addDir('Recently Added',base_url + '/movies/gen/Animation/sort/recently/page/1','mmlineIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '/movies/gen/Animation/sort/popular/page/1','mmlineIndex',artwork + '/main/popular.png')
        main.addDir('Highly Rated',base_url + '/movies/gen/Animation/sort/ratings/page/1','mmlineIndex',artwork + '/main/toprated.png')

        
def BIOGRAPHY():
        main.addDir('A-Z',base_url + '/movies/gen/Biography/sort/alphabet/page/1','mmlineIndex',artwork + '/main/a-z.png')
        main.addDir('Recently Added',base_url + '/movies/gen/Biography/sort/recently/page/1','mmlineIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '/movies/gen/Biography/sort/popular/page/1','mmlineIndex',artwork + '/main/popular.png')
        main.addDir('Highly Rated',base_url + '/movies/gen/Biography/sort/ratings/page/1','mmlineIndex',artwork + '/main/toprated.png')

        
def COMEDY():
        main.addDir('A-Z',base_url + '/movies/gen/Comedy/sort/alphabet/page/1','mmlineIndex',artwork + '/main/a-z.png')
        main.addDir('Recently Added',base_url + '/movies/gen/Comedy/sort/recently/page/1','mmlineIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '/movies/gen/Comedy/sort/popular/page/1','mmlineIndex',artwork + '/main/popular.png')
        main.addDir('Highly Rated',base_url + '/movies/gen/Comedy/sort/ratings/page/1','mmlineIndex',artwork + '/main/toprated.png')

        
def CRIME():
        main.addDir('A-Z',base_url + '/movies/gen/Crime/sort/alphabet/page/1','mmlineIndex',artwork + '/main/a-z.png')
        main.addDir('Recently Added',base_url + '/movies/gen/Crime/sort/recently/page/1','mmlineIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '/movies/gen/Crime/sort/popular/page/1','mmlineIndex',artwork + '/main/popular.png')
        main.addDir('Highly Rated',base_url + '/movies/gen/Crime/sort/ratings/page/1','mmlineIndex',artwork + '/main/toprated.png')

        
def DOCUMENTARY():
        main.addDir('A-Z',base_url + '/movies/gen/Documentary/sort/alphabet/page/1','mmlineIndex',artwork + '/main/a-z.png')
        main.addDir('Recently Added',base_url + '/movies/gen/Documentary/sort/recently/page/1','mmlineIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '/movies/gen/Documentary/sort/popular/page/1','mmlineIndex',artwork + '/main/popular.png')
        main.addDir('Highly Rated',base_url + '/movies/gen/Documentary/sort/ratings/page/1','mmlineIndex',artwork + '/main/toprated.png')

        
def DRAMA():
        main.addDir('A-Z',base_url + '/movies/gen/Drama/sort/alphabet/page/1','mmlineIndex',artwork + '/main/a-z.png')
        main.addDir('Recently Added',base_url + '/movies/gen/Drama/sort/recently/page/1','mmlineIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '/movies/gen/Drama/sort/popular/page/1','mmlineIndex',artwork + '/main/popular.png')
        main.addDir('Highly Rated',base_url + '/movies/gen/Drama/sort/ratings/page/1','mmlineIndex',artwork + '/main/toprated.png')

        
def FAMILY():
        main.addDir('A-Z',base_url + '/movies/gen/Family/sort/alphabet/page/1','mmlineIndex',artwork + '/main/a-z.png')
        main.addDir('Recently Added',base_url + '/movies/gen/Family/sort/recently/page/1','mmlineIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '/movies/gen/Family/sort/popular/page/1','mmlineIndex',artwork + '/main/popular.png')
        main.addDir('Highly Rated',base_url + '/movies/gen/Family/sort/ratings/page/1','mmlineIndex',artwork + '/main/toprated.png')

        
def FANTASY():
        main.addDir('A-Z',base_url + '/movies/gen/Fantasy/sort/alphabet/page/1','mmlineIndex',artwork + '/main/a-z.png')
        main.addDir('Recently Added',base_url + '/movies/gen/Fantasy/sort/recently/page/1','mmlineIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '/movies/gen/Fantasy/sort/popular/page/1','mmlineIndex',artwork + '/main/popular.png')
        main.addDir('Highly Rated',base_url + '/movies/gen/Fantasy/sort/ratings/page/1','mmlineIndex',artwork + '/main/toprated.png')

        
def HISTORY():
        main.addDir('A-Z',base_url + '/movies/gen/History/sort/alphabet/page/1','mmlineIndex',artwork + '/main/a-z.png')
        main.addDir('Recently Added',base_url + '/movies/gen/History/sort/recently/page/1','mmlineIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '/movies/gen/History/sort/popular/page/1','mmlineIndex',artwork + '/main/popular.png')
        main.addDir('Highly Rated',base_url + '/movies/gen/History/sort/ratings/page/1','mmlineIndex',artwork + '/main/toprated.png')

        
def HORROR():
        main.addDir('A-Z',base_url + '/movies/gen/Horror/sort/alphabet/page/1','mmlineIndex',artwork + '/main/a-z.png')
        main.addDir('Recently Added',base_url + '/movies/gen/Horror/sort/recently/page/1','mmlineIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '/movies/gen/Horror/sort/popular/page/1','mmlineIndex',artwork + '/main/popular.png')
        main.addDir('Highly Rated',base_url + '/movies/gen/Horror/sort/ratings/page/1','mmlineIndex',artwork + '/main/toprated.png')

        
def MUSIC():
        main.addDir('A-Z',base_url + '/movies/gen/Music/sort/alphabet/page/1','mmlineIndex',artwork + '/main/a-z.png')
        main.addDir('Recently Added',base_url + '/movies/gen/Music/sort/recently/page/1','mmlineIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '/movies/gen/Music/sort/popular/page/1','mmlineIndex',artwork + '/main/popular.png')
        main.addDir('Highly Rated',base_url + '/movies/gen/Music/sort/ratings/page/1','mmlineIndex',artwork + '/main/toprated.png')

        
def MUSICAL():
        main.addDir('A-Z',base_url + '/movies/gen/Musical/sort/alphabet/page/1','mmlineIndex',artwork + '/main/a-z.png')
        main.addDir('Recently Added',base_url + '/movies/gen/Musical/sort/recently/page/1','mmlineIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '/movies/gen/Musical/sort/popular/page/1','mmlineIndex',artwork + '/main/popular.png')
        main.addDir('Highly Rated',base_url + '/movies/gen/Musical/sort/ratings/page/1','mmlineIndex',artwork + '/main/toprated.png')

        
def MYSTERY():
        main.addDir('A-Z',base_url + '/movies/gen/Mystery/sort/alphabet/page/1','mmlineIndex',artwork + '/main/a-z.png')
        main.addDir('Recently Added',base_url + '/movies/gen/Mystery/sort/recently/page/1','mmlineIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '/movies/gen/Mystery/sort/popular/page/1','mmlineIndex',artwork + '/main/popular.png')
        main.addDir('Highly Rated',base_url + '/movies/gen/Mystery/sort/ratings/page/1','mmlineIndex',artwork + '/main/toprated.png')

        
def ROMANCE():
        main.addDir('A-Z',base_url + '/movies/gen/Romance/sort/alphabet/page/1','mmlineIndex',artwork + '/main/a-z.png')
        main.addDir('Recently Added',base_url + '/movies/gen/Romance/sort/recently/page/1','mmlineIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '/movies/gen/Romance/sort/popular/page/1','mmlineIndex',artwork + '/main/popular.png')
        main.addDir('Highly Rated',base_url + '/movies/gen/Romance/sort/ratings/page/1','mmlineIndex',artwork + '/main/toprated.png')

        
def SCIFI():
        main.addDir('A-Z',base_url + '/movies/gen/Sci-Fi/sort/alphabet/page/1','mmlineIndex',artwork + '/main/a-z.png')
        main.addDir('Recently Added',base_url + '/movies/gen/Sci-Fi/sort/recently/page/1','mmlineIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '/movies/gen/Sci-Fi/sort/popular/page/1','mmlineIndex',artwork + '/main/popular.png')
        main.addDir('Highly Rated',base_url + '/movies/gen/Sci-Fi/sort/ratings/page/1','mmlineIndex',artwork + '/main/toprated.png')

        
def SPORT():
        main.addDir('A-Z',base_url + '/movies/gen/Sport/sort/alphabet/page/1','mmlineIndex',artwork + '/main/a-z.png')
        main.addDir('Recently Added',base_url + '/movies/gen/Sport/sort/recently/page/1','mmlineIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '/movies/gen/Sport/sort/popular/page/1','mmlineIndex',artwork + '/main/popular.png')
        main.addDir('Highly Rated',base_url + '/movies/gen/Sport/sort/ratings/page/1','mmlineIndex',artwork + '/main/toprated.png')

        
def THRILLER():
        main.addDir('A-Z',base_url + '/movies/gen/Thriller/sort/alphabet/page/1','mmlineIndex',artwork + '/main/a-z.png')
        main.addDir('Recently Added',base_url + '/movies/gen/Thriller/sort/recently/page/1','mmlineIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '/movies/gen/Thriller/sort/popular/page/1','mmlineIndex',artwork + '/main/popular.png')
        main.addDir('Highly Rated',base_url + '/movies/gen/Thriller/sort/ratings/page/1','mmlineIndex',artwork + '/main/toprated.png')

        
def WAR():
        main.addDir('A-Z',base_url + '/movies/gen/War/sort/alphabet/page/1','mmlineIndex',artwork + '/main/a-z.png')
        main.addDir('Recently Added',base_url + '/movies/gen/War/sort/recently/page/1','mmlineIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '/movies/gen/War/sort/popular/page/1','mmlineIndex',artwork + '/main/popular.png')
        main.addDir('Highly Rated',base_url + '/movies/gen/War/sort/ratings/page/1','mmlineIndex',artwork + '/main/toprated.png')

        
def WESTERN():
        main.addDir('A-Z',base_url + '/movies/gen/Western/sort/alphabet/page/1','mmlineIndex',artwork + '/main/a-z.png')
        main.addDir('Recently Added',base_url + '/movies/gen/Western/sort/recently/page/1','mmlineIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '/movies/gen/Western/sort/popular/page/1','mmlineIndex',artwork + '/main/popular.png')
        main.addDir('Highly Rated',base_url + '/movies/gen/Western/sort/ratings/page/1','mmlineIndex',artwork + '/main/toprated.png')

        
def INDIAN():
        main.addDir('A-Z',base_url + '/movies/gen/Indian/sort/alphabet/page/1','mmlineIndex',artwork + '/main/a-z.png')
        main.addDir('Recently Added',base_url + '/movies/gen/Indian/sort/recently/page/1','mmlineIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '/movies/gen/Indian/sort/popular/page/1','mmlineIndex',artwork + '/main/popular.png')
        main.addDir('Highly Rated',base_url + '/movies/gen/Indian/sort/ratings/page/1','mmlineIndex',artwork + '/main/toprated.png')

        
def SHORT():
        main.addDir('A-Z',base_url + '/movies/gen/Short/sort/alphabet/page/1','mmlineIndex',artwork + '/main/a-z.png')
        main.addDir('Recently Added',base_url + '/movies/gen/Short/sort/recently/page/1','mmlineIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '/movies/gen/Short/sort/popular/page/1','mmlineIndex',artwork + '/main/popular.png')
        main.addDir('Highly Rated',base_url + '/movies/gen/Short/sort/ratings/page/1','mmlineIndex',artwork + '/main/toprated.png')

        
def CLASSIC():
        main.addDir('A-Z',base_url + '/movies/gen/Classic/sort/alphabet/page/1','mmlineIndex',artwork + '/main/a-z.png')
        main.addDir('Recently Added',base_url + '/movies/gen/Classic/sort/recently/page/1','mmlineIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '/movies/gen/Classic/sort/popular/page/1','mmlineIndex',artwork + '/main/popular.png')
        main.addDir('Highly Rated',base_url + '/movies/gen/Classic/sort/ratings/page/1','mmlineIndex',artwork + '/main/toprated.png')

        
        

def INDEX(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)"><img src="(.+?)" width=".+?" title=".+?" alt="(.+?)"></a>').findall(link)
        np=re.compile('<a href="/(.+?) " >').findall(link)
        if len(np) > 0:
                np_url = base_url + '/' + str(np[0])
                if settings.getSetting('nextpagetop') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',np_url,'mmlineIndex',artwork + '/main/next.png')
        inc = 0
        if len(match) > 0:
                for url,thumbnail,name in match:
                        inc += 1
                        if inc > 8:
                                movie_name = name[:-6]
                                year = name[-6:]
                                
                                try:
                                        main.addMDir(movie_name,base_url + url,'mmlineVideoLinks',base_url+thumbnail,year,False)
                                except:
                                        pass
        if len(np) > 0:
                if settings.getSetting('nextpagebottom') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',np_url,'mmlineIndex',artwork + '/main/next.png')

                
        main.AUTOVIEW('movies')

def VIDEOLINKS(name,url,thumb):
        link = net.http_GET(url).content
        match=re.compile('<a target="_blank" href="(.+?)">.+?</a>').findall(link)
        for url in match:
                if main.resolvable(url):
                        try:
                                main.addHDir(name,url,'resolve','')
                        except:
                                continue
                        
        
def SEARCH():
        search = ''
        keyboard = xbmc.Keyboard(search,'Search')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search = keyboard.getText()
                search = search.replace(' ','+')
                
                url = base_url + '?search_key=' + search
                
                INDEX(url)

def MASTERSEARCH(search):
        url = base_url + '?search_key=' + search
        INDEX(url)
