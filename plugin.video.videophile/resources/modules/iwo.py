#IWO Module by o9r1sh October 2013
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,sys,main,xbmc,os

artwork = main.artwork
base_url = 'http://www.iwatchonline.to'
settings = main.settings

net = main.net


def MOVIE_CATEGORIES():
        main.addDir('Recently Added',base_url +'/movies?sort=latest','iwoIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '/movies?sort=popular','iwoIndex',artwork + '/main/popular.png')
        main.addDir('A-Z','none','iwoLetters',artwork + '/main/a-z.png')
        main.addDir('HD Movies','none','iwoHDMovies',artwork + '/main/hd.png')
        main.addDir('Genres','none','iwoGenres',artwork + '/main/genres.png')

def SERIES_CATEGORIES():
        main.addDir('Recently Added',base_url +'/tv-show?sort=latest','iwoSeriesIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '/tv-show?sort=popular','iwoSeriesIndex',artwork + '/main/popular.png')
        main.addDir('A-Z','none','iwoSeriesLetters',artwork + '/main/a-z.png')
        main.addDir('Genres','none','iwoSeriesGenres',artwork + '/main/genres.png')

def SERIES_LETTERS():
        main.addDir('#',base_url + '/tv-show?startwith=09','iwoSeriesIndex',artwork + '/letters/num.png')
        main.addDir('A',base_url + '/tv-show?startwith=a','iwoSeriesIndex',artwork + '/letters/a.png')
        main.addDir('B',base_url + '/tv-show?startwith=b','iwoSeriesIndex',artwork + '/letters/b.png')
        main.addDir('C',base_url + '/tv-show?startwith=c','iwoSeriesIndex',artwork + '/letters/c.png')
        main.addDir('D',base_url + '/tv-show?startwith=d','iwoSeriesIndex',artwork + '/letters/d.png')
        main.addDir('E',base_url + '/tv-show?startwith=e','iwoSeriesIndex',artwork + '/letters/e.png')
        main.addDir('F',base_url + '/tv-show?startwith=f','iwoSeriesIndex',artwork + '/letters/f.png')
        main.addDir('G',base_url + '/tv-show?startwith=g','iwoSeriesIndex',artwork + '/letters/g.png')
        main.addDir('H',base_url + '/tv-show?startwith=h','iwoSeriesIndex',artwork + '/letters/h.png')
        main.addDir('I',base_url + '/tv-show?startwith=i','iwoSeriesIndex',artwork + '/letters/i.png')
        main.addDir('J',base_url + '/tv-show?startwith=j','iwoSeriesIndex',artwork + '/letters/j.png')
        main.addDir('K',base_url + '/tv-show?startwith=k','iwoSeriesIndex',artwork + '/letters/k.png')
        main.addDir('L',base_url + '/tv-show?startwith=l','iwoSeriesIndex',artwork + '/letters/l.png')
        main.addDir('M',base_url + '/tv-show?startwith=m','iwoSeriesIndex',artwork + '/letters/m.png')
        main.addDir('N',base_url + '/tv-show?startwith=n','iwoSeriesIndex',artwork + '/letters/n.png')
        main.addDir('O',base_url + '/tv-show?startwith=o','iwoSeriesIndex',artwork + '/letters/o.png')
        main.addDir('P',base_url + '/tv-show?startwith=p','iwoSeriesIndex',artwork + '/letters/p.png')
        main.addDir('Q',base_url + '/tv-show?startwith=q','iwoSeriesIndex',artwork + '/letters/q.png')
        main.addDir('R',base_url + '/tv-show?startwith=r','iwoSeriesIndex',artwork + '/letters/r.png')
        main.addDir('S',base_url + '/tv-show?startwith=s','iwoSeriesIndex',artwork + '/letters/s.png')
        main.addDir('T',base_url + '/tv-show?startwith=t','iwoSeriesIndex',artwork + '/letters/t.png')
        main.addDir('U',base_url + '/tv-show?startwith=u','iwoSeriesIndex',artwork + '/letters/u.png')
        main.addDir('V',base_url + '/tv-show?startwith=v','iwoSeriesIndex',artwork + '/letters/v.png')
        main.addDir('W',base_url + '/tv-show?startwith=w','iwoSeriesIndex',artwork + '/letters/w.png')
        main.addDir('X',base_url + '/tv-show?startwith=x','iwoSeriesIndex',artwork + '/letters/x.png')
        main.addDir('Y',base_url + '/tv-show?startwith=y','iwoSeriesIndex',artwork + '/letters/y.png')
        main.addDir('Z',base_url + '/tv-show?startwith=z','iwoSeriesIndex',artwork + '/letters/z.png')

def SERIES_GENRES():
        main.addDir('Action',base_url + '/tv-show?gener=action','iwoSeriesIndex',artwork + '/genres/action.png')
        main.addDir('Adventure',base_url + '/tv-show?gener=adventure','iwoSeriesIndex',artwork + '/genres/adventure.png')
        main.addDir('Adult Cartoons',base_url + '/tv-show?gener=adult-cartoons','iwoSeriesIndex',artwork + '/genres/adultcartoons.png')
        main.addDir('Animals',base_url + '/tv-show?gener=pets-animals-general','iwoSeriesIndex',artwork + '/genres/animals.png')
        main.addDir('Animation',base_url + '/tv-show?gener=animation-general','iwoSeriesIndex',artwork + '/genres/animation.png')
        main.addDir('Anime',base_url + '/tv-show?gener=anime','iwoSeriesIndex',artwork + '/genres/anime.png')
        main.addDir('Anthology',base_url + '/tv-show?gener=anthology','iwoSeriesIndex',artwork + '/genres/anthology.png')
        main.addDir('Arts & Crafts',base_url + '/tv-show?gener=arts-crafts','iwoSeriesIndex',artwork + '/genres/artscrafts.png')
        main.addDir('Automobiles',base_url + '/tv-show?gener=automobiles','iwoSeriesIndex',artwork + '/genres/automobiles.png')
        main.addDir('Barter',base_url + '/tv-show?gener=buy-sell-trade','iwoSeriesIndex',artwork + '/genres/barter.png')
        main.addDir('Building',base_url + '/tv-show?gener=housing-building','iwoSeriesIndex',artwork + '/genres/building.png')
        main.addDir('Business',base_url + '/tv-show?gener=financial-business','iwoSeriesIndex',artwork + '/genres/business.png')
        main.addDir('Cartoons',base_url + '/tv-show?gener=children-cartoons','iwoSeriesIndex',artwork + '/genres/cartoons.png')
        main.addDir('Celebrities',base_url + '/tv-show?gener=celebrities','iwoSeriesIndex',artwork + '/genres/celebrities.png')
        main.addDir('Children',base_url + '/tv-show?gener=children','iwoSeriesIndex',artwork + '/genres/children.png')
        main.addDir('Comedy',base_url + '/tv-show?gener=comedy','iwoSeriesIndex',artwork + '/genres/comedy.png')
        main.addDir('Cooking',base_url + '/tv-show?gener=cooking-food','iwoSeriesIndex',artwork + '/genres/cooking.png')
        main.addDir('Crime',base_url + '/tv-show?gener=crime','iwoSeriesIndex',artwork + '/genres/crime.png')
        main.addDir('Current Events',base_url + '/tv-show?gener=current-events','iwoSeriesIndex',artwork + '/genres/currentevents.png')
        main.addDir('Dance',base_url + '/tv-show?gener=dance','iwoSeriesIndex',artwork + '/genres/dance.png')
        main.addDir('Debate',base_url + '/tv-show?gener=debate','iwoSeriesIndex',artwork + '/genres/debate.png')
        main.addDir('Design',base_url + '/tv-show?gener=design-decorating','iwoSeriesIndex',artwork + '/genres/design.png')
        main.addDir('Discovery',base_url + '/tv-show?gener=discovery-science','iwoSeriesIndex',artwork + '/genres/discovery.png')
        main.addDir('DIY',base_url + '/tv-show?gener=how-to-do-it-yourself','iwoSeriesIndex',artwork + '/genres/diy.png')
        main.addDir('Drama',base_url + '/tv-show?gener=drama','iwoSeriesIndex',artwork + '/genres/drama.png')
        main.addDir('Educational',base_url + '/tv-show?gener=educational','iwoSeriesIndex',artwork + '/genres/educational.png')
        main.addDir('Family',base_url + '/tv-show?gener=family','iwoSeriesIndex',artwork + '/genres/family.png')
        main.addDir('Fantasy',base_url + '/tv-show?gener=fantasy','iwoSeriesIndex',artwork + '/genres/fantasy.png')
        main.addDir('Fashion',base_url + '/tv-show?gener=fashion-make-up','iwoSeriesIndex',artwork + '/genres/fashion.png')
        main.addDir('Finance',base_url + '/tv-show?gener=finance','iwoSeriesIndex',artwork + '/genres/finance.png')
        main.addDir('Fitness',base_url + '/tv-show?gener=fitness','iwoSeriesIndex',artwork + '/genres/fitness.png')
        main.addDir('Garden',base_url + '/tv-show?gener=garden-landscape','iwoSeriesIndex',artwork + '/genres/garden.png')
        main.addDir('History',base_url + '/tv-show?gener=history','iwoSeriesIndex',artwork + '/genres/history.png')
        main.addDir('Horror',base_url + '/tv-show?gener=horror-supernatural','iwoSeriesIndex',artwork + '/genres/horror.png')
        main.addDir('Interview',base_url + '/tv-show?gener=interview','iwoSeriesIndex',artwork + '/genres/interview.png')
        main.addDir('Lifestyle',base_url + '/tv-show?gener=lifestyle','iwoSeriesIndex',artwork + '/genres/lifestyle.png')
        main.addDir('Literature',base_url + '/tv-show?gener=literature','iwoSeriesIndex',artwork + '/genres/literature.png')
        main.addDir('Medical',base_url + '/tv-show?gener=medical','iwoSeriesIndex',artwork + '/genres/medical.png')
        main.addDir('Military',base_url + '/tv-show?gener=military-war','iwoSeriesIndex',artwork + '/genres/military.png')
        main.addDir('Music',base_url + '/tv-show?gener=music','iwoSeriesIndex',artwork + '/genres/music.png')
        main.addDir('Mystery',base_url + '/tv-show?gener=mystery','iwoSeriesIndex',artwork + '/genres/mystery.png')
        main.addDir('Pets',base_url + '/tv-show?gener=pets','iwoSeriesIndex',artwork + '/genres/pets.png')
        main.addDir('Politics',base_url + '/tv-show?gener=politics','iwoSeriesIndex',artwork + '/genres/politics.png')
        main.addDir('Reality',base_url + '/tv-show?gener=reality-tv','iwoSeriesIndex',artwork + '/genres/reality.png')
        main.addDir('Religion',base_url + '/tv-show?gener=religion','iwoSeriesIndex',artwork + '/genres/religion.png')
        main.addDir('Romance',base_url + '/tv-show?gener=romance-dating','iwoSeriesIndex',artwork + '/genres/romance.png')
        main.addDir('Sci-Fi',base_url + '/tv-show?gener=sci-fi','iwoSeriesIndex',artwork + '/genres/sci-fi.png')
        main.addDir('Sketch',base_url + '/tv-show?gener=sketch-improv','iwoSeriesIndex',artwork + '/genres/sketch.png')
        main.addDir('Soap Opera',base_url + '/tv-show?gener=soaps-improv','iwoSeriesIndex',artwork + '/genres/soapopera.png')
        main.addDir('Sport',base_url + '/tv-show?gener=sports','iwoSeriesIndex',artwork + '/genres/sport.png')
        main.addDir('Super Heroes',base_url + '/tv-show?gener=super-heroes','iwoSeriesIndex',artwork + '/genres/superhero.png')
        main.addDir('Talent',base_url + '/tv-show?gener=talent','iwoSeriesIndex',artwork + '/genres/talent.png')
        main.addDir('Teens',base_url + '/tv-show?gener=teens','iwoSeriesIndex',artwork + '/genres/teens.png')
        main.addDir('Theatre',base_url + '/tv-show?gener=cinema-theatre','iwoSeriesIndex',artwork + '/genres/theatre.png')
        main.addDir('Thriller',base_url + '/tv-show?gener=thriller','iwoSeriesIndex',artwork + '/genres/thriller.png')
        main.addDir('Travel',base_url + '/tv-show?gener=travel','iwoSeriesIndex',artwork + '/genres/travel.png')
        main.addDir('Vehicles',base_url + '/tv-show?gener=automobiles-vehicles','iwoSeriesIndex',artwork + '/genres/vehicles.png')
        main.addDir('Western',base_url + '/tv-show?gener=western','iwoSeriesIndex',artwork + '/genres/western.png')
        main.addDir('Wildlife',base_url + '/tv-show?gener=wildlife','iwoSeriesIndex',artwork + '/genres/wildlife.png')
     
def HD_MOVIES():
        main.addDir('Recently Added',base_url +'//movies?sort=latest&quality=hd','iwoIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Popular',base_url + '//movies?sort=popular&quality=hd','iwoIndex',artwork + '/main/popular.png')
        main.addDir('A-Z','none','iwoHDLetters',artwork + '/main/a-z.png')
        main.addDir('Genres','none','iwoHDGenres',artwork + '/main/genres.png')
        
def LETTERS():
        main.addDir('#',base_url + '/movies?startwith=09','iwoIndex',artwork + '/letters/num.png')
        main.addDir('A',base_url + '/movies?startwith=a','iwoIndex',artwork + '/letters/a.png')
        main.addDir('B',base_url + '/movies?startwith=b','iwoIndex',artwork + '/letters/b.png')
        main.addDir('C',base_url + '/movies?startwith=c','iwoIndex',artwork + '/letters/c.png')
        main.addDir('D',base_url + '/movies?startwith=d','iwoIndex',artwork + '/letters/d.png')
        main.addDir('E',base_url + '/movies?startwith=e','iwoIndex',artwork + '/letters/e.png')
        main.addDir('F',base_url + '/movies?startwith=f','iwoIndex',artwork + '/letters/f.png')
        main.addDir('G',base_url + '/movies?startwith=g','iwoIndex',artwork + '/letters/g.png')
        main.addDir('H',base_url + '/movies?startwith=h','iwoIndex',artwork + '/letters/h.png')
        main.addDir('I',base_url + '/movies?startwith=i','iwoIndex',artwork + '/letters/i.png')
        main.addDir('J',base_url + '/movies?startwith=j','iwoIndex',artwork + '/letters/j.png')
        main.addDir('K',base_url + '/movies?startwith=k','iwoIndex',artwork + '/letters/k.png')
        main.addDir('L',base_url + '/movies?startwith=l','iwoIndex',artwork + '/letters/l.png')
        main.addDir('M',base_url + '/movies?startwith=m','iwoIndex',artwork + '/letters/m.png')
        main.addDir('N',base_url + '/movies?startwith=n','iwoIndex',artwork + '/letters/n.png')
        main.addDir('O',base_url + '/movies?startwith=o','iwoIndex',artwork + '/letters/o.png')
        main.addDir('P',base_url + '/movies?startwith=p','iwoIndex',artwork + '/letters/p.png')
        main.addDir('Q',base_url + '/movies?startwith=q','iwoIndex',artwork + '/letters/q.png')
        main.addDir('R',base_url + '/movies?startwith=r','iwoIndex',artwork + '/letters/r.png')
        main.addDir('S',base_url + '/movies?startwith=s','iwoIndex',artwork + '/letters/s.png')
        main.addDir('T',base_url + '/movies?startwith=t','iwoIndex',artwork + '/letters/t.png')
        main.addDir('U',base_url + '/movies?startwith=u','iwoIndex',artwork + '/letters/u.png')
        main.addDir('V',base_url + '/movies?startwith=v','iwoIndex',artwork + '/letters/v.png')
        main.addDir('W',base_url + '/movies?startwith=w','iwoIndex',artwork + '/letters/w.png')
        main.addDir('X',base_url + '/movies?startwith=x','iwoIndex',artwork + '/letters/x.png')
        main.addDir('Y',base_url + '/movies?startwith=y','iwoIndex',artwork + '/letters/y.png')
        main.addDir('Z',base_url + '/movies?startwith=z','iwoIndex',artwork + '/letters/z.png')

def HD_LETTERS():
        main.addDir('#',base_url + '/movies?quality=hd&startwith=09','iwoIndex',artwork + '/letters/num.png')
        main.addDir('A',base_url + '/movies?quality=hd&startwith=a','iwoIndex',artwork + '/letters/a.png')
        main.addDir('B',base_url + '/movies?quality=hd&startwith=b','iwoIndex',artwork + '/letters/b.png')
        main.addDir('C',base_url + '/movies?quality=hd&startwith=c','iwoIndex',artwork + '/letters/c.png')
        main.addDir('D',base_url + '/movies?quality=hd&startwith=d','iwoIndex',artwork + '/letters/d.png')
        main.addDir('E',base_url + '/movies?quality=hd&startwith=e','iwoIndex',artwork + '/letters/e.png')
        main.addDir('F',base_url + '/movies?quality=hd&startwith=f','iwoIndex',artwork + '/letters/f.png')
        main.addDir('G',base_url + '/movies?quality=hd&startwith=g','iwoIndex',artwork + '/letters/g.png')
        main.addDir('H',base_url + '/movies?quality=hd&startwith=h','iwoIndex',artwork + '/letters/h.png')
        main.addDir('I',base_url + '/movies?quality=hd&startwith=i','iwoIndex',artwork + '/letters/i.png')
        main.addDir('J',base_url + '/movies?quality=hd&startwith=j','iwoIndex',artwork + '/letters/j.png')
        main.addDir('K',base_url + '/movies?quality=hd&startwith=k','iwoIndex',artwork + '/letters/k.png')
        main.addDir('L',base_url + '/movies?quality=hd&startwith=l','iwoIndex',artwork + '/letters/l.png')
        main.addDir('M',base_url + '/movies?quality=hd&startwith=m','iwoIndex',artwork + '/letters/m.png')
        main.addDir('N',base_url + '/movies?quality=hd&startwith=n','iwoIndex',artwork + '/letters/n.png')
        main.addDir('O',base_url + '/movies?quality=hd&startwith=o','iwoIndex',artwork + '/letters/o.png')
        main.addDir('P',base_url + '/movies?quality=hd&startwith=p','iwoIndex',artwork + '/letters/p.png')
        main.addDir('Q',base_url + '/movies?quality=hd&startwith=q','iwoIndex',artwork + '/letters/q.png')
        main.addDir('R',base_url + '/movies?quality=hd&startwith=r','iwoIndex',artwork + '/letters/r.png')
        main.addDir('S',base_url + '/movies?quality=hd&startwith=s','iwoIndex',artwork + '/letters/s.png')
        main.addDir('T',base_url + '/movies?quality=hd&startwith=t','iwoIndex',artwork + '/letters/t.png')
        main.addDir('U',base_url + '/movies?quality=hd&startwith=u','iwoIndex',artwork + '/letters/u.png')
        main.addDir('V',base_url + '/movies?quality=hd&startwith=v','iwoIndex',artwork + '/letters/v.png')
        main.addDir('W',base_url + '/movies?quality=hd&startwith=w','iwoIndex',artwork + '/letters/w.png')
        main.addDir('X',base_url + '/movies?quality=hd&startwith=x','iwoIndex',artwork + '/letters/x.png')
        main.addDir('Y',base_url + '/movies?quality=hd&startwith=y','iwoIndex',artwork + '/letters/y.png')
        main.addDir('Z',base_url + '/movies?quality=hd&startwith=z','iwoIndex',artwork + '/letters/z.png')

def GENRES():
        main.addDir('Action','none','iwoAction',artwork + '/genres/action.png')
        main.addDir('Adventure','none','iwoAdventure',artwork + '/genres/adventure.png')
        main.addDir('Animation','none','iwoAnimation',artwork + '/genres/animation.png')
        main.addDir('Biography','none','iwoBiography',artwork + '/genres/biography.png')
        main.addDir('Comedy','none','iwoComedy',artwork + '/genres/comedy.png')
        main.addDir('Crime','none','iwoCrime',artwork + '/genres/crime.png')
        main.addDir('Documentary','none','iwoDocumentary',artwork + '/genres/docs.png')
        main.addDir('Drama','none','iwoDrama',artwork + '/genres/drama.png')
        main.addDir('Family','none','iwoFamily',artwork + '/genres/family.png')
        main.addDir('Fantasy','none','iwoFantasy',artwork + '/genres/fantasy.png')
        main.addDir('Film-Noir','none','iwoFilmNoir',artwork + '/genres/film-noir.png')
        main.addDir('History','none','iwoHistory',artwork + '/genres/history.png')
        main.addDir('Horror','none','iwoHorror',artwork + '/genres/horror.png')
        main.addDir('Music','none','iwoMusic',artwork + '/genres/music.png')
        main.addDir('Musical','none','iwoMusical',artwork + '/genres/musical.png')
        main.addDir('Mystery','none','iwoMystery',artwork + '/genres/mystery.png')
        main.addDir('News','none','iwoNews',artwork + '/genres/news.png')
        main.addDir('Romance','none','iwoRomance',artwork + '/genres/romance.png')
        main.addDir('Sci-Fi','none','iwoSciFi',artwork + '/genres/sci-fi.png')
        main.addDir('Short','none','iwoShort',artwork + '/genres/short.png')
        main.addDir('Sport','none','iwoSport',artwork + '/genres/sport.png')
        main.addDir('Thriller','none','iwoThriller',artwork + '/genres/thriller.png')
        main.addDir('War','none','iwoWar',artwork + '/genres/war.png')
        main.addDir('Western','none','iwoWestern',artwork + '/genres/western.png')

def ACTION():
        main.addDir('Popular',base_url + '/movies?gener=action&sort=popular','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=action&sort=latest','iwoIndex',artwork + '/main/recentlyadded.png')

def ADVENTURE():
        main.addDir('Popular',base_url + '/movies?gener=adventure&sort=popular','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=adventure&sort=latest','iwoIndex',artwork + '/main/recentlyadded.png')

def ANIMATION():
        main.addDir('Popular',base_url + '/movies?gener=animation&sort=popular','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=animation&sort=latest','iwoIndex',artwork + '/main/recentlyadded.png')

def BIOGRAPHY():
        main.addDir('Popular',base_url + '/movies?gener=biography&sort=popular','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=biography&sort=latest','iwoIndex',artwork + '/main/recentlyadded.png')

def COMEDY():
        main.addDir('Popular',base_url + '/movies?gener=comedy&sort=popular','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=comedy&sort=latest','iwoIndex',artwork + '/main/recentlyadded.png')

def CRIME():
        main.addDir('Popular',base_url + '/movies?gener=crime&sort=popular','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=crime&sort=latest','iwoIndex',artwork + '/main/recentlyadded.png')

def DOCUMENTARY():
        main.addDir('Popular',base_url + '/movies?gener=documentary&sort=popular','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=documentary&sort=latest','iwoIndex',artwork + '/main/recentlyadded.png')

def DRAMA():
        main.addDir('Popular',base_url + '/movies?gener=drama&sort=popular','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=drama&sort=latest','iwoIndex',artwork + '/main/recentlyadded.png')

def FAMILY():
        main.addDir('Popular',base_url + '/movies?gener=family&sort=popular','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=family&sort=latest','iwoIndex',artwork + '/main/recentlyadded.png')

def FANTASY():
        main.addDir('Popular',base_url + '/movies?gener=fantasy&sort=popular','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=fantasy&sort=latest','iwoIndex',artwork + '/main/recentlyadded.png')

def FILMNOIR():
        main.addDir('Popular',base_url + '/movies?gener=film-noir&sort=popular','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=film-noir&sort=latest','iwoIndex',artwork + '/main/recentlyadded.png')

def HISTORY():
        main.addDir('Popular',base_url + '/movies?gener=history&sort=popular','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=history&sort=latest','iwoIndex',artwork + '/main/recentlyadded.png')

def HORROR():
        main.addDir('Popular',base_url + '/movies?gener=horror&sort=popular','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=horror&sort=latest','iwoIndex',artwork + '/main/recentlyadded.png')

def MUSIC():
        main.addDir('Popular',base_url + '/movies?gener=music&sort=popular','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=music&sort=latest','iwoIndex',artwork + '/main/recentlyadded.png')

def MUSICAL():
        main.addDir('Popular',base_url + '/movies?gener=musical&sort=popular','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=musical&sort=latest','iwoIndex',artwork + '/main/recentlyadded.png')

def MYSTERY():
        main.addDir('Popular',base_url + '/movies?gener=mystery&sort=popular','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=mystery&sort=latest','iwoIndex',artwork + '/main/recentlyadded.png')

def NEWS():
        main.addDir('Popular',base_url + '/movies?gener=news&sort=popular','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=news&sort=latest','iwoIndex',artwork + '/main/recentlyadded.png')

def ROMANCE():
        main.addDir('Popular',base_url + '/movies?gener=romance&sort=popular','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=romance&sort=latest','iwoIndex',artwork + '/main/recentlyadded.png')

def SCIFI():
        main.addDir('Popular',base_url + '/movies?gener=sci-fi&sort=popular','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=sci-fi&sort=latest','iwoIndex',artwork + '/main/recentlyadded.png')

def SHORT():
        main.addDir('Popular',base_url + '/movies?gener=short&sort=popular','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=short&sort=latest','iwoIndex',artwork + '/main/recentlyadded.png')

def SPORT():
        main.addDir('Popular',base_url + '/movies?gener=sport&sort=popular','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=sport&sort=latest','iwoIndex',artwork + '/main/recentlyadded.png')

def THRILLER():
        main.addDir('Popular',base_url + '/movies?gener=thriller&sort=popular','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=thriller&sort=latest','iwoIndex',artwork + '/main/recentlyadded.png')

def WAR():
        main.addDir('Popular',base_url + '/movies?gener=war&sort=popular','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=war&sort=latest','iwoIndex',artwork + '/main/recentlyadded.png')

def WESTERN():
        main.addDir('Popular',base_url + '/movies?gener=western&sort=popular','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=western&sort=latest','iwoIndex',artwork + '/main/recentlyadded.png')

def HD_GENRES():
        main.addDir('Action','none','iwoHDAction',artwork + '/genres/action.png')
        main.addDir('Adventure','none','iwoHDAdventure',artwork + '/genres/adventure.png')
        main.addDir('Animation','none','iwoHDAnimation',artwork + '/genres/animation.png')
        main.addDir('Biography','none','iwoHDBiography',artwork + '/genres/biography.png')
        main.addDir('Comedy','none','iwoHDComedy',artwork + '/genres/comedy.png')
        main.addDir('Crime','none','iwoHDCrime',artwork + '/genres/crime.png')
        main.addDir('Documentary','none','iwoHDDocumentary',artwork + '/genres/docs.png')
        main.addDir('Drama','none','iwoHDDrama',artwork + '/genres/drama.png')
        main.addDir('Family','none','iwoHDFamily',artwork + '/genres/family.png')
        main.addDir('Fantasy','none','iwoHDFantasy',artwork + '/genres/fantasy.png')
        main.addDir('Film-Noir','none','iwoHDFilmNoir',artwork + '/genres/film-noir.png')
        main.addDir('History','none','iwoHDHistory',artwork + '/genres/history.png')
        main.addDir('Horror','none','iwoHDHorror',artwork + '/genres/horror.png')
        main.addDir('Music','none','iwoHDMusic',artwork + '/genres/music.png')
        main.addDir('Musical','none','iwoHDMusical',artwork + '/genres/musical.png')
        main.addDir('Mystery','none','iwoHDMystery',artwork + '/genres/mystery.png')
        main.addDir('News','none','iwoHDNews',artwork + '/genres/news.png')
        main.addDir('Romance','none','IwoHDRomance',artwork + '/genres/romance.png')
        main.addDir('Sci-Fi','none','iwoHDSciFi',artwork + '/genres/sci-fi.png')
        main.addDir('Short','none','iwoHDShort',artwork + '/genres/short.png')
        main.addDir('Sport','none','iwoHDSport',artwork + '/genres/sport.png')
        main.addDir('Thriller','none','iwoHDThriller',artwork + '/genres/thriller.png')
        main.addDir('War','none','iwoHDWar',artwork + '/genres/war.png')
        main.addDir('Western','none','iwoHDWestern',artwork + '/genres/western.png')

def HD_ACTION():
        main.addDir('Popular',base_url + '/movies?gener=action&sort=popular&quality=hd','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=action&sort=latest&quality=hd','iwoIndex',artwork + '/main/recentlyadded.png')

def HD_ADVENTURE():
        main.addDir('Popular',base_url + '/movies?gener=adventure&sort=popular&quality=hd','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=adventure&sort=latest&quality=hd','iwoIndex',artwork + '/main/recentlyadded.png')

def HD_ANIMATION():
        main.addDir('Popular',base_url + '/movies?gener=animation&sort=popular&quality=hd','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=animation&sort=latest&quality=hd','iwoIndex',artwork + '/main/recentlyadded.png')

def HD_BIOGRAPHY():
        main.addDir('Popular',base_url + '/movies?gener=biography&sort=popular&quality=hd','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=biography&sort=latest&quality=hd','iwoIndex',artwork + '/main/recentlyadded.png')

def HD_COMEDY():
        main.addDir('Popular',base_url + '/movies?gener=comedy&sort=popular&quality=hd','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=comedy&sort=latest&quality=hd','iwoIndex',artwork + '/main/recentlyadded.png')

def HD_CRIME():
        main.addDir('Popular',base_url + '/movies?gener=crime&sort=popular&quality=hd','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=crime&sort=latest&quality=hd','iwoIndex',artwork + '/main/recentlyadded.png')

def HD_DOCUMENTARY():
        main.addDir('Popular',base_url + '/movies?gener=documentary&sort=popular&quality=hd','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=documentary&sort=latest&quality=hd','iwoIndex',artwork + '/main/recentlyadded.png')

def HD_DRAMA():
        main.addDir('Popular',base_url + '/movies?gener=drama&sort=popular&quality=hd','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=drama&sort=latest&quality=hd','iwoIndex',artwork + '/main/recentlyadded.png')

def HD_FAMILY():
        main.addDir('Popular',base_url + '/movies?gener=family&sort=popular&quality=hd','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=family&sort=latest&quality=hd','iwoIndex',artwork + '/main/recentlyadded.png')

def HD_FANTASY():
        main.addDir('Popular',base_url + '/movies?gener=fantasy&sort=popular&quality=hd','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=fantasy&sort=latest&quality=hd','iwoIndex',artwork + '/main/recentlyadded.png')

def HD_FILMNOIR():
        main.addDir('Popular',base_url + '/movies?gener=film-noir&sort=popular&quality=hd','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=film-noir&sort=latest&quality=hd','iwoIndex',artwork + '/main/recentlyadded.png')

def HD_HISTORY():
        main.addDir('Popular',base_url + '/movies?gener=history&sort=popular&quality=hd','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=history&sort=latest&quality=hd','iwoIndex',artwork + '/main/recentlyadded.png')

def HD_HORROR():
        main.addDir('Popular',base_url + '/movies?gener=horror&sort=popular&quality=hd','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=horror&sort=latest&quality=hd','iwoIndex',artwork + '/main/recentlyadded.png')

def HD_MUSIC():
        main.addDir('Popular',base_url + '/movies?gener=music&sort=popular&quality=hd','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=music&sort=latest&quality=hd','iwoIndex',artwork + '/main/recentlyadded.png')

def HD_MUSICAL():
        main.addDir('Popular',base_url + '/movies?gener=musical&sort=popular&quality=hd','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=musical&sort=latest&quality=hd','iwoIndex',artwork + '/main/recentlyadded.png')

def HD_MYSTERY():
        main.addDir('Popular',base_url + '/movies?gener=mystery&sort=popular&quality=hd','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=mystery&sort=latest&quality=hd','iwoIndex',artwork + '/main/recentlyadded.png')

def HD_NEWS():
        main.addDir('Popular',base_url + '/movies?gener=news&sort=popular&quality=hd','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=news&sort=latest&quality=hd','iwoIndex',artwork + '/main/recentlyadded.png')

def HD_ROMANCE():
        main.addDir('Popular',base_url + '/movies?gener=romance&sort=popular&quality=hd','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=romance&sort=latest&quality=hd','iwoIndex',artwork + '/main/recentlyadded.png')

def HD_SCIFI():
        main.addDir('Popular',base_url + '/movies?gener=sci-fi&sort=popular&quality=hd','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=sci-fi&sort=latest&quality=hd','iwoIndex',artwork + '/main/recentlyadded.png')

def HD_SHORT():
        main.addDir('Popular',base_url + '/movies?gener=short&sort=popular&quality=hd','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=short&sort=latest&quality=hd','iwoIndex',artwork + '/main/recentlyadded.png')

def HD_SPORT():
        main.addDir('Popular',base_url + '/movies?gener=sport&sort=popular&quality=hd','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=sport&sort=latest&quality=hd','iwoIndex',artwork + '/main/recentlyadded.png')

def HD_THRILLER():
        main.addDir('Popular',base_url + '/movies?gener=thriller&sort=popular&quality=hd','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=thriller&sort=latest&quality=hd','iwoIndex',artwork + '/main/recentlyadded.png')

def HD_WAR():
        main.addDir('Popular',base_url + '/movies?gener=war&sort=popular&quality=hd','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=war&sort=latest&quality=hd','iwoIndex',artwork + 'recentlyadded.png')

def HD_WESTERN():
        main.addDir('Popular',base_url + '/movies?gener=western&sort=popular&quality=hd','iwoIndex',artwork + '/main/popular.png')
        main.addDir('Recently Added',base_url + '/movies?gener=western&sort=latest&quality=hd','iwoIndex',artwork + '/main/recentlyadded.png')
        
def MOVIE_INDEX(url):
        next_page = ''
        link = net.http_GET(url).content
        np=re.compile('<li class="next pagea"><a href="(.+?)">Next &rarr;</a>').findall(link)
        match=re.compile('<a href="(.+?)" class=".+?" rel=".+?">\r\n\t\t\t\t\t\t\t<img class=".+?" src="(.+?)" alt="">\r\n\t\t\t\t\t\t\t <div class=".+?">.+?</div>\t  \r\n\t\t\t\t\t\t</a>\r\n\t\t\t\t\t\t<div class=".+?">.+?').findall(link)
        if len(np) > 0:
                next_page = np[0]
                next_page = next_page.replace('&amp;','&')
                if settings.getSetting('nextpagetop') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'iwoIndex',artwork + '/main/next.png')
        
        for url,thumbnail in match:
                head,sep,tail = url.partition('/movie/')
                head,sep,tail = url.partition('-')
                year = tail[-4:]
                year = '(' + year + ')'
                name = tail[:-4]
                name = re.sub('-s','s',name)
                name = re.sub('-',' ',name)
                name = re.sub("'",'',name)
                name = name.title()
        
                try:
                        main.addMDir(name,url,'iwoVideoLinks',thumbnail,year,False)
                except:
                        continue
        if len(np) > 0:
                if settings.getSetting('nextpagebottom') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'iwoIndex',artwork + '/main/next.png')

        main.AUTOVIEW('movies')

def SERIES_INDEX(url):
        link = net.http_GET(url).content
        np=re.compile('<li class="next pagea"><a href="(.+?)">Next &rarr;</a>').findall(link)
        match=re.compile('<a href="(.+?)" class=".+?" rel=".+?">\r\n\t\t\t\t\t\t\t<img class=".+?" src="(.+?)" alt="">\r\n\t\t\t\t\t\t\t <div class=".+?">.+?</div>\t  \r\n\t\t\t\t\t\t</a>\r\n\t\t\t\t\t\t<div class=".+?">.+?').findall(link)
        if len(np) > 0:
                next_page = np[0]
                next_page = next_page.replace('&amp;','&')
                next_page = next_page.replace('movies','tv-show')
                if settings.getSetting('nextpagetop') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'iwoSeriesIndex',artwork + '/main/next.png')
        
        for url,thumbnail in match:
                head,sep,tail = url.partition('/tv-shows/')
                head,sep,tail = url.partition('-')
                split = re.split('\d\d\d\d\d-',tail)
                try:
                        name = str(split[1])
                except:
                        continue
                name = name.replace('-',' ')
                name = name.title()

                if name == 'Battlestar Galactica':
                        name = 'Battlestar Galactica (2003)'
        
                try:
                        main.addSDir(name,url,'iwoEpisodesIndex',thumbnail,False)
                except:
                        continue
        if settings.getSetting('nextpagebottom') == 'true':
                main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'iwoSeriesIndex',artwork + '/main/next.png')

        main.AUTOVIEW('tvshows')

def EPISODES_INDEX(url,name):
        show = name
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)"><i class="icon-play-circle"></i>.+?</a></td>\r\n\t\t\t\t\t\t\t  <td>(.+?)</td>\r\n\t\t\t\t\t\t\t  <td><div class="pull-right"><div class="star" data-rating=".+?">').findall(link)
        for url,name in match:
                s,e = main.GET_EPISODE_NUMBERS(url)
                s = 'S' + s
                e = 'E' + e
                se = s+e
                name = name + ' ' + se
                try:
                        main.addEDir(name,url,'iwoVideoLinks','',show)
                except:
                        continue
        main.AUTOVIEW('episodes')

def VIDEOLINKS(name,url,thumb):
        inc = 0
        link = net.http_GET(url).content
        match=re.compile('<td class="sideleft"><a href="(.+?)"').findall(link)
        for url in match:
                if inc < 50:
                        link = net.http_GET(url).content
                        urls=re.compile('<iframe name="frame" class="frame" src="(.+?)"').findall(link)
                        if main.resolvable(urls[0]):
                                try:
                                        main.addHDir(name,str(urls[0]),'resolve','')
                                        inc +=1
                                except:
                                        continue
                



