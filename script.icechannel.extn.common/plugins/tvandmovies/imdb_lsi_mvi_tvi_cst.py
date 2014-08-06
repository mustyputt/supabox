'''
    IMDb
'''

from entertainment.plugnplay.interfaces import ListIndexer
from entertainment.plugnplay.interfaces import MovieIndexer
from entertainment.plugnplay.interfaces import TVShowIndexer
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common

class IMDb(MovieIndexer, TVShowIndexer, CustomSettings, ListIndexer):
    implements = [MovieIndexer, TVShowIndexer, CustomSettings, ListIndexer]
    
    name = "IMDb"
    display_name = "IMDb"
    base_url = 'http://akas.imdb.com/'
    
    img='https://istream-xbmc-repo.googlecode.com/svn/images/imdb.png'
    
    default_indexer_enabled = 'true'
    
    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="IMDb SETTINGS">\n'
        xml += '<setting id="imdb_user_number" label="User Number" type="text" default="" />\n'
        xml += '<setting id="future" type="bool" label="Show Future Episodes" default="false" />\n'
        xml += '</category>\n' 
        xml += '</settings>\n'
        
        self.CreateSettings(self.name, self.display_name, xml)
    
    def ExtractContentAndAddtoList(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 
        
        import urllib
        
        if section != 'search':
            url = urllib.unquote_plus(url)
        
        import re
        
        new_url = url
                
        if not new_url.startswith(self.base_url):
            new_url = re.sub("http\://.*?/", self.base_url, url)
        
        if page == '':
            page = '1'
            
        page_item_count = (100 if section == 'watchlist' else 25)
            
        start = str( ( (int(page) - 1) * page_item_count ) + 1 )
        count = str(page_item_count)
        new_url = new_url + '&start=' + start + '&count=' + count
            
        if sort_by == '' and 'sort' not in new_url:
            sort_by = 'moviemeter'            
        if sort_order == '' and 'sort' not in new_url:
            sort_order = 'asc'
            
        if 'sort' not in new_url:
            new_url = new_url + '&sort=' + ('title' if section == 'watchlist' and sort_by == 'alpha' else sort_by) + (':' if section == 'watchlist' else ',') + sort_order
            
        
        from entertainment.net import Net
        cached = False if section == 'watchlist' else True
        net = Net(cached=cached)

        content = net.http_GET(new_url).content
        
        if total_pages == '' :
            re_page =  '<span>\(.+? of ([0-9,]+)' if section == 'watchlist' else '(?s)<div id="left">.+? of ([0-9,]+)'
            total_pages = re.search(re_page, content)
            if total_pages:
                total_count = total_pages.group(1)
                total_count = int ( total_count.replace(',', '') )
                total_pages = str( total_count / page_item_count + ( 1 if total_count % page_item_count > 0 else 0 ) )
            else:
                if re.search('0 items found', content):
                    page = '0'
                    total_pages = '0'
                else:
                    page = '1'
                    total_pages = '1'

        self.AddInfo(list, indexer, section, url, type, page, total_pages, sort_by, sort_order)
        
        mode = common.mode_File_Hosts
        if type == 'tv_shows':
            mode = common.mode_Content
            type = 'tv_seasons'
        
        item_re = r'<a href="/title/(.+?)/" title="(.+?)"><img'
        if section == 'theaters':
            item_re = r'<h4 itemprop="name"><a href="/title/(.+?)/.+?title="(.+?)"'
            
        if section == 'watchlist':
            item_re = r'(?s)<b><a.+?href="/title/(.+?)/".+?>(.+?)</a>.+?<span class="year_type">(.+?)<.+?<div class="(.+?)"'

        for item in re.finditer(item_re, content):
            
            if section == 'watchlist':
                if item.group(4) == 'episode': continue
            
            item_v_id = item.group(1)            
            item_title = common.addon.unescape(item.group(2))
            item_type = item.group(3) if section == 'watchlist' else item_title
            item_year = re.search("\(([0-9]+)", item_type)
            if item_year:
                item_year = item_year.group(1)
            else:
                item_year = ''
            item_name = item_title if section == 'watchlist' else re.sub(" \([0-9]+.+?\)", "", item_title )
            
            item_title = item_name
            if item_year != '':
                item_title = item_title + ' (' + item_year + ')'
            
            item_url = self.base_url+'title/'+item_v_id+'/'
            
            if total_pages == '':
                total_pages = '1'
            
            if section == 'watchlist':                
                if 'movie' in item_type.lower() or re.sub("[0-9]+", "", item_type) == "()":
                    type = common.indxr_Movies 
                    mode = common.mode_File_Hosts
                    indexer = common.indxr_Movies                     
                elif 'series' in item_type.lower():
                    type = 'tv_seasons'
                    mode = common.mode_Content
                    indexer = common.indxr_TV_Shows 
                else:
                    type = common.indxr_Movies 
                    mode = common.mode_File_Hosts
                    indexer = common.indxr_Movies

            self.AddContent(list, indexer, mode, item_title, '', type, url=item_url, name=item_name, year=item_year, imdb_id=item_v_id)
            
    def get_formated_date(self, date_str):
        
        import re
        import datetime
        
        item_air_date = common.unescape(date_str).replace('      ', '')
        item_fmtd_air_date = ""
        if 'Jan' in item_air_date: item_fmtd_air_date = '01-'
        elif 'Feb' in item_air_date: item_fmtd_air_date = '02-'
        elif 'Mar' in item_air_date: item_fmtd_air_date = '03-'
        elif 'Apr' in item_air_date: item_fmtd_air_date = '04-'
        elif 'May' in item_air_date: item_fmtd_air_date = '05-'
        elif 'Jun' in item_air_date: item_fmtd_air_date = '06-'
        elif 'Jul' in item_air_date: item_fmtd_air_date = '07-'
        elif 'Aug' in item_air_date: item_fmtd_air_date = '08-'
        elif 'Sep' in item_air_date: item_fmtd_air_date = '09-'
        elif 'Oct' in item_air_date: item_fmtd_air_date = '10-'
        elif 'Nov' in item_air_date: item_fmtd_air_date = '11-'
        elif 'Dec' in item_air_date: item_fmtd_air_date = '12-'
        else: item_fmtd_air_date = '12-'
        date = re.search('([0-9]{1,2})', item_air_date)
        if date: 
            date = date.group(1)
            item_fmtd_air_date += "%02d-" % int(date)
        else:
            item_fmtd_air_date += "01-"
        year = re.search('([0-9]{4})', item_air_date)
        if year: 
            year = year.group(1)
            item_fmtd_air_date += year
        else:
            item_fmtd_air_date += "0001"
            
        try:
            item_fmtd_air_date = datetime.datetime.strptime(item_fmtd_air_date, "%m-%d-%Y")
        except TypeError:
            import time
            item_fmtd_air_date = datetime.datetime(*(time.strptime(item_fmtd_air_date, "%m-%d-%Y")[0:6]))
            
        return item_fmtd_air_date

    def GetContent(self, indexer, url, title, name, year, season, episode, type, list):      
        import urllib
        url = urllib.unquote_plus(url)
        title = urllib.unquote_plus(title)
        name = urllib.unquote_plus(name)
        
        import re
        
        new_url = url
        if not new_url.startswith(self.base_url):
            new_url = re.sub("http\://.*?/", self.base_url, url)
        
        from entertainment.net import Net
        net = Net(cached=False)
        content = net.http_GET(new_url).content
        
        import datetime
        todays_date = datetime.date.today()
        
        if type == 'tv_seasons':
            check_season = 0
            last_season = 0
            season_url = None
            seasons = re.search('<a href="/(title/.+?/episodes\?season=)([0-9]+)', content)
            if seasons:
                last_season = int(seasons.group(2))
                season_url = seasons.group(1)
            
            for season_num in xrange(last_season, 0, -1):
                item_v_id = str(season_num)
                item_url = self.base_url + season_url + item_v_id
                
                if check_season < 2:
                    check_season += 1
                    item_content = net.http_GET(item_url).content
                    season_item = re.search('<div>S' + item_v_id +', Ep([0-9]+)</div>', item_content)
                    if not season_item: 
                        check_season -= 1
                        continue          
                    item_item = re.search('(?s)<div class="list_item.+?href="(.+?)".+?title="(.+?)".+?<div>S' + item_v_id +', Ep([0-9]+)</div>.+?<div class="airdate">(.+?)</div>', item_content)
                    if 'unknown' in item_item.group(4).lower(): continue 
                    item_fmtd_air_date = self.get_formated_date( item_item.group(4) )

                    if item_fmtd_air_date.date() > todays_date or item_fmtd_air_date.date() == '0001-12-01': continue
                
                
                item_title = 'Season ' + item_v_id
                
                item_id = common.CreateIdFromString(title + ' ' + item_title)
                
                self.AddContent(list, indexer, common.mode_Content, item_title, item_id, 'tv_episodes', url=item_url, name=name, year=year, season=item_v_id)
            
            
        elif type == 'tv_episodes':
            season_item = re.search('<div>S' + season +', Ep([0-9]+)</div>', content)
            if not season_item: 
                return

            for item in re.finditer('(?s)<div class="list_item.+?href="(.+?)".+?title="(.+?)".+?<div>S' + season +', Ep([0-9]+)</div>.+?<div class="airdate">(.+?)</div>', content):
                item_fmtd_air_date = self.get_formated_date( item.group(4) )

                if self.Settings().get_setting('future')=='false':
                    if item_fmtd_air_date.date() > todays_date: break
                
                item_url = self.base_url + item.group(1)
                item_v_id = item.group(3)
                item_title = item.group(2)
                if item_title == None:
                    item_title = ''
                
                item_id = common.CreateIdFromString(name + '_' + year + '_season_' + season + '_episode_' + item_v_id)
                
                self.AddContent(list, indexer, common.mode_File_Hosts, item_title, item_id, type, url=item_url, name=name, year=year, season=season, episode=item_v_id)
        
    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 
        url_type = ''
        content_type = ''

        if indexer == common.indxr_Movies:
            url_type = 'title_type=feature,tv_movie&'
        elif indexer == common.indxr_TV_Shows:
            url_type = 'title_type=tv_series,mini_series&'
        elif indexer == common.indxr_Lists:
            url_type = ''#title_type=feature,tv_movie,tv_series,mini_series&'
            
        if section == 'main':
            
            if indexer != common.indxr_Lists:
                #self.AddSection(list, indexer, 'a_z', 'A-Z')
                self.AddSection(list, indexer, 'genres', 'Genres')
                self.AddSection(list, indexer, 'moviemeter', 'Most Popular', self.base_url+'search/title?' + url_type + 'sort=moviemeter,asc', indexer)
                self.AddSection(list, indexer, 'year', 'Most Popular By Year')
                self.AddSection(list, indexer, 'user_rating', 'Highly Rated', self.base_url+'search/title?' + url_type + 'sort=user_rating,desc', indexer)
                self.AddSection(list, indexer, 'num_votes', 'Most Voted', self.base_url+'search/title?' + url_type + 'sort=num_votes,desc', indexer)
                self.AddSection(list, indexer, 'boxoffice_gross_us', 'Box Office', self.base_url+'search/title?' + url_type + 'sort=boxoffice_gross_us,desc', indexer)
                if indexer == common.indxr_Movies:
                    self.AddSection(list, indexer, 'oscar_best_picture_winners', 'Oscar Winners', self.base_url+'search/title?' + url_type + 'groups=oscar_best_picture_winners&sort=year,desc', indexer)
                    self.AddSection(list, indexer, 'theaters', 'In Cinemas Now', self.base_url+'movies-in-theaters/?'+ url_type , indexer)
                    self.AddSection(list, indexer, 'kids', 'Kids Zone', self.base_url+'search/title?genres=animation,family&title_type=feature,video', indexer)
            
            user_number = self.Settings().get_setting('imdb_user_number')
            if user_number:
                list_url_type = ''#title_type=feature,tv_movie,tv_series,mini_series&'
                self.AddSection(list, indexer, 'watchlist', 'Watchlist', self.base_url+'user/' + user_number + '/watchlist?' + list_url_type + 'view=detail', indexer)
                
                from entertainment.net import Net
                net = Net(cached=False)
                import re

                named_lists_url = self.base_url+'user/' + user_number + '/lists?tab=public'
                named_lists = net.http_GET(named_lists_url).content
                
                match = re.compile('<div class="list_name"><b><a.+?href="(.+?)".+?>(.+?)</a>').findall(named_lists)
                for url, name in match:
                    custom_name='%s List' % name   
                    custom_url=self.base_url + str(url) + '?' + list_url_type + 'view=detail'
                    self.AddSection(list, indexer, 'watchlist', '%s' % custom_name, custom_url, indexer, hlevel=1) 
                
        elif section == 'genres':
            
            import re
            
            from entertainment.net import Net
            net = Net()
            
            genre_url = self.base_url         
            genre_re = ''
            
            genre_url = genre_url + 'genre/'
            genre_re = '(?s)<h2>Television.+?<table(.+?)</table>'

            content = net.http_GET(genre_url).content
            
            genres = re.search(genre_re, content)
            if genres:
                genres = genres.group(1)
                for genre in re.finditer('<a href=".+?">(.+?)</a>', genres):                    
                    genre_title = genre.group(1)
                    genre_section = genre_title.lower()
                    genre_url = self.base_url +'search/title?' + url_type + 'genres=' + genre_section
                    
                    self.AddSection(list, indexer, genre_section, genre_title, genre_url, indexer)
                        
        elif section == 'a_z':
            self.AddSection(list, indexer, '123', '#123', self.base_url+'?' + url_type + 'letter=123', indexer)
            A2Z=[chr(i) for i in xrange(ord('A'), ord('Z')+1)]
            for letter in A2Z:
                self.AddSection(list, indexer, letter.lower(), letter, self.base_url+'?' + url_type + 'letter=' + letter.lower(), indexer)                
        elif section == 'year':
            start = 1900
            import datetime
            end   = datetime.datetime.today().year
            year = []
            for yr in range(end, start-1, -1):
                str_year = str(yr)
                self.AddSection(list, indexer, str_year, str_year, 
                    self.base_url+'search/title?year=' + str_year+','+str_year + '&' + url_type + 'sort=moviemeter,asc', indexer)
        else:
            self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)
            
    def GetSortByOptions(self): 
        
        from entertainment import odict
        sort_by_dict = odict.odict()
        
        sort_by_dict['alpha'] = 'Alphabet'
        sort_by_dict['user_rating'] = 'Ratings'
        sort_by_dict['moviemeter'] = 'Views'
        sort_by_dict['num_votes'] = 'Votes'
        
        
        return sort_by_dict
    
    def GetSortOrderOptions(self): 
        
        from entertainment import odict
        sort_order_dict = odict.odict()
        
        sort_order_dict['asc'] = 'Ascending'
        sort_order_dict['desc'] = 'Descending'
        
        return sort_order_dict
        
    def Search(self, indexer, keywords, type, list, lock, message_queue, page='', total_pages=''): 

        from entertainment.net import Net
        net = Net() 
        
        keywords = self.CleanTextForSearch(keywords) 
        
        keywords_lower = keywords.lower().split(' ')
        match_total = float( len(keywords_lower) )
        
        from entertainment import odict
        search_dict = odict.odict({ 's' : 'tt', 'q' : keywords})
        
        if indexer == common.indxr_Movies:
            search_dict.update({'ttype':'ft'})
        elif indexer == common.indxr_TV_Shows:
            search_dict.update({'ttype':'tv'})
        
        search_dict.sort(key=lambda x: x[0].lower())
                
        import urllib
        search_for_url = self.base_url + 'find?' + urllib.urlencode(search_dict)
        
        content = net.http_GET(search_for_url).content        
        
        if '<h1 class="findHeader">No results found' in content:            
            return
            
        self.AddInfo(list, indexer, 'search', self.base_url, type, '1', '1')
        
        mode = common.mode_File_Hosts
        if type == 'tv_shows':
            mode = common.mode_Content
            type = 'tv_seasons'
        
        import re
        
        search_results = re.search('(?s)<table class="findList">(.+?)</table>', content)
        
        if search_results:            
            search_results = search_results.group(1)
            
            search_term_not_found_count = 0
            for search_item in re.finditer('<td class="result_text"> <a href="/title/(.+?)/.+?" >(.+?)</a> (.+?) <(.+?)</td>', content):
            
                item_id = search_item.group(1)
                item_url = self.base_url + 'title/' + item_id
                
                item_name = search_item.group(2)
                item_name_lower = item_name.lower()
                
                match_count = 0
                for kw in keywords_lower:
                    if kw in item_name_lower:
                        match_count = match_count + 1

                match_fraction = ( match_count / match_total )

                if not ( match_fraction >= 0.8  ):

                    aka_item = search_item.group(4)

                    aka_name = re.search('aka <i>"(.+?)"</i>', aka_item)
                    if aka_name:
                        item_name = aka_name.group(1)
                        item_name_lower = item_name.lower()
                        match_count = 0
                        for kw in keywords_lower:
                            if kw in item_name_lower:
                                match_count = match_count + 1
                        match_fraction = ( match_count / match_total )
                        if not ( match_fraction >= 0.8  ):
                            search_term_not_found_count += 1
                            if search_term_not_found_count >= 2:
                                break
                            else:
                                continue
                    else:
                        search_term_not_found_count += 1
                        if search_term_not_found_count >= 2:
                            break
                        else:
                            continue
                
                item_title = item_name
                item_other_info = search_item.group(3)
                item_year = re.search('\(([0-9]+)\)', item_other_info)
                if item_year:
                    item_year = item_year.group(1)
                    item_title += ' (' + item_year + ')'
                else:
                    item_year = ''
        
        
                if 'movie' in item_other_info.lower():
                    type = common.indxr_Movies 
                    mode = common.mode_File_Hosts
                    indexer = common.indxr_Movies                     
                elif 'series' in item_other_info.lower():
                    type = 'tv_seasons'
                    mode = common.mode_Content
                    indexer = common.indxr_TV_Shows 
                    
                self.AddContent(list, indexer, mode, item_title, '', type, url=item_url, name=item_name, year=item_year, imdb_id=item_id)
