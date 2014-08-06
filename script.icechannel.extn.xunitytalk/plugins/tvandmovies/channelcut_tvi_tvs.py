'''
    Istream
    channelcut.me
    Copyright (C) 2013 Coolwave, Mikey1234, the-one, voinage

    version 0.1

'''


from entertainment.plugnplay import Plugin
from entertainment import common

from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import TVShowIndexer


class channelcut(TVShowIndexer,TVShowSource):
    implements = [TVShowIndexer,TVShowSource]
	
    #unique name of the source
    name = "channelcut"
    source_enabled_by_default = 'false'
    default_indexer_enabled = 'false'
    #display name of the source
    display_name = "Channel Cut"
    
    #base url of the source website
    base_url = 'http://www.channelcut.tv/last-150'

    def ExtractContentAndAddtoList(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 
        
        if section == 'latest':
            
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = 'http://www.channelcut.tv/page/'+page
                
            from entertainment.net import Net
            net = Net()
            import urllib
            import re
            url = urllib.unquote_plus(url)
            html = net.http_GET(new_url).content
            total_pages = '3011'
            
            self.AddInfo(list, indexer, 'latest', '', type, str(page), total_pages)
        
            match=re.compile('<h1 class="entry-title"><a href="(.+?)" title=".+?" rel="bookmark">(.+?) Season (.+?) Episode (.+?) .+?</a></h1>').findall(html)
            for url, name, Sea_num, eps_num in match:
                name = self.CleanTextForSearch(name)
                season_pull = "0%s"%Sea_num if len(Sea_num)<2 else Sea_num
                episode_pull = "0%s"%eps_num if len(eps_num)<2 else eps_num
                sea_eps = 'S'+season_pull+'E'+episode_pull
                year= '0'

                item_id = common.CreateIdFromString(name + '_' + year + '_season_' + Sea_num + '_episode_' + eps_num)

                self.AddContent(list, indexer, common.mode_File_Hosts, name +'[COLOR royalblue] ('+sea_eps+')[/COLOR]', item_id, 'tv_episodes', url=url, name=name, year=year, season=Sea_num, episode=eps_num)

        elif section == 'last':
            
            new_url = url
                
            from entertainment.net import Net
            net = Net()
            import urllib
            import re
            url = urllib.unquote_plus(url)
            html = net.http_GET(new_url).content

            match=re.compile('<li>(.+?) \: <a href="(.+?)">(.+?) Season (.+?) Episode (.+?) .+?</a> </li>').findall(html)
            
            ''' Pagination Code Start '''
            num_items_on_a_page = 25
            if page == '':                
                page = '1'
                total_items = len(match)
                total_pages = str ( ( total_items / num_items_on_a_page ) + ( 1 if total_items % num_items_on_a_page >= 1 else 0) )
                
            self.AddInfo(list, indexer, section, url, type, page, total_pages, sort_by, sort_order)
            
            start_index = ( int(page) - 1 ) * num_items_on_a_page
            match = match[ start_index : start_index + num_items_on_a_page  ]
            ''' Pagination Code End '''

            for date, url, name, Sea_num, eps_num in match:
                name = self.CleanTextForSearch(name)
                season_pull = "0%s"%Sea_num if len(Sea_num)<2 else Sea_num
                episode_pull = "0%s"%eps_num if len(eps_num)<2 else eps_num
                sea_eps = 'S'+season_pull+'E'+episode_pull
                year= '0'

                item_id = common.CreateIdFromString(name + '_' + year + '_season_' + Sea_num + '_episode_' + eps_num)

                self.AddContent(list, indexer, common.mode_File_Hosts, name +'[COLOR royalblue] ('+sea_eps+')[/COLOR]', item_id, 'tv_episodes', url=url, name=name, year=year, season=Sea_num, episode=eps_num)
 
        elif section == 'az':
            
            new_url = url
                
            from entertainment.net import Net
            net = Net()
            import urllib
            import re
            url = urllib.unquote_plus(url)
            html = net.http_GET(new_url).content

            match=re.compile('<option class="level-0" value=".+?">(.+?)</option>').findall(html)
            
            ''' Pagination Code Start '''
            num_items_on_a_page = 25
            if page == '':                
                page = '1'
                total_items = len(match)
                total_pages = str ( ( total_items / num_items_on_a_page ) + ( 1 if total_items % num_items_on_a_page >= 1 else 0) )
                
            self.AddInfo(list, indexer, section, url, type, page, total_pages, sort_by, sort_order)
            
            start_index = ( int(page) - 1 ) * num_items_on_a_page
            match = match[ start_index : start_index + num_items_on_a_page  ]
            ''' Pagination Code End '''

            for name in match:
                name = self.CleanTextForSearch(name)
                url = 'http://services.tvrage.com/myfeeds/search.php?key=ag6txjP0RH4m0c8sZk2j&show='+name
                self.AddContent(list, indexer, common.mode_Content, name, '', 'tv_seasons', url=url, name=name)


    def GetContent(self, indexer, url, title, name, year, season, episode, type, list):
        import urllib
        url = urllib.unquote_plus(url)
        title = urllib.unquote_plus(title)
        name = urllib.unquote_plus(name)
        
        from entertainment.net import Net
        net = Net()
        import re
        
        show_url = self.GoogleSearchByTitleReturnFirstResultOnlyIfValid('tvrage.com', name, 'shows', item_count=2, title_extrctr=['(.+?) tv show', '(.+?) \- tvrage'], exact_match=True)
        if show_url == '' :
            tv_url= 'http://www.tvrage.com/search.php?search=%s&searchin=2&button=Go' %(name.lower().replace(' ','+'))
            html = net.http_GET(tv_url).content
            r = re.search(r'<h2><a href="(.+?)">(.+?)</a> <img src=\'.+?\' /> </h2>\s*</dt>\s*<dd class="img"> <a href="/(.+?)">', html)
            show_url = 'http://www.tvrage.com' + r.group(1)
        
        item_url = show_url + '/episode_list'
                    
        import datetime
        todays_date = datetime.date.today()
        content = net.http_GET(item_url).content
        
        if type == 'tv_seasons':
            match=re.compile('>S-(.+?)<').findall(content)
            for seasonnumber in match:                
                item_url = item_url
                item_title = 'Season ' + seasonnumber
                item_id = common.CreateIdFromString(title + ' ' + item_title)               
                self.AddContent(list, indexer, common.mode_Content, item_title, item_id, 'tv_episodes', url=item_url, name=name, season=seasonnumber)

        elif type == 'tv_episodes':
            new_url = url+'/'+season
            content2 = net.http_GET(new_url).content
            match=re.compile("<td width='40' align='center'><a href='(.+?)' title='.+?'>.+?x(.+?)</i></a></td>\s*<td width='80' align='center'>(.+?)</td>\s*<td style='padding-left: 6px;'> <a href='.+?/([0-9]*)'>(.+?)</a> </td>",re.DOTALL).findall(content2)
            for item_url, item_v_id_2, item_date, fixscrape, item_title in match:
                item_v_id_2 = str(int(item_v_id_2))
                
                item_fmtd_air_date = self.get_formated_date( item_date )
                if item_fmtd_air_date.date() > todays_date: break
                
                item_id = common.CreateIdFromString(name + '_season_' + season + '_episode_' + item_v_id_2)
                self.AddContent(list, indexer, common.mode_File_Hosts, item_title, item_id, type, url=item_url, name=name, season=season, episode=item_v_id_2)


    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''):
        
        from entertainment.net import Net
        
        net = Net()
        url_type = ''
        content_type = ''

        
        if section == 'main':
            self.AddSection(list, indexer,'latest','Date Added','http://www.channelcut.tv/',indexer)
            self.AddSection(list, indexer,'last','Last 300','http://www.channelcut.tv/last-150',indexer)
            self.AddSection(list, indexer,'az','A-Z','http://www.channelcut.tv/index',indexer)
            
        else:
            self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)

            
    
    def GetFileHosts(self, url, list, lock, message_queue):
        import re

        from entertainment.net import Net
        net = Net()

        
        content = net.http_GET(url).content
        r = 'rel="nofollow">(.+?)</a>'
        match  = re.compile(r).findall(content)
        
        for url in match:
                        
            self.AddFileHost(list,'DVD', url)



    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):
        import urllib2
        import re
        from entertainment.net import Net
        net = Net()
        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)
        
        new_url='http://www.channelcut.tv//?s=%s+%s'%(name.replace(' ','+'),title.replace(' ','+'))

        req = urllib2.Request(new_url, headers={'User-Agent' : "Magic Browser"}) 
        con = urllib2.urlopen( req )
        html= con.read()
                                                            
        link= html.split('Start: Post')
                                                                     
        for p in link:
                                                    
            if 'Season '+season in p:
                                                                 
                if 'Episode '+episode in p:
                                                            
                    Found_Url=re.compile('<a href="(.+?)" rel="bookmark"').findall(p)[0]


                                                                     
                    self.GetFileHosts(Found_Url, list, lock, message_queue)
