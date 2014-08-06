'''
    Ice Channel
    Copyright (C) 2013 Coolwave
'''
from entertainment.plugnplay.interfaces import MovieIndexer
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common
import os

do_no_cache_keywords_list = ['Sorry for this interruption but we have detected an elevated amount of request from your IP']

class popcornered(MovieIndexer,MovieSource):
    implements = [MovieIndexer,MovieSource]
    
    name = "popcornered"
    display_name = "Popcornered"
    img='https://raw.githubusercontent.com/Coolwavexunitytalk/images/master/popcornered.png'
    cookie_file = os.path.join(common.cookies_path, 'popcornered')
    source_enabled_by_default = 'false'
    default_indexer_enabled = 'false'

    def ExtractContentAndAddtoList(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 
        if section == 'latest':
            
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                headers={'Referer':'http://popcornered.com/search_results?new','Host':'popcornered.com','Origin':'http://popcornered.com','Content-Type':'application/x-www-form-urlencoded','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Encoding':'gzip,deflate,sdch','Accept-Language':'en-US,en;q=0.8','Cache-Control':'max-age=0','Connection':'keep-alive','User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'}

                form_data={ 'page':page }
                #html = net.http_POST('http://popcornered.com/search_results?new', form_data, headers).content
            
            from entertainment.net import Net
            import re
            net = Net(cached=False)
            import urllib

            headers={'Referer':'http://popcornered.com/search_results?new','Host':'popcornered.com','Origin':'http://popcornered.com','Content-Type':'application/x-www-form-urlencoded','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Encoding':'gzip,deflate,sdch','Accept-Language':'en-US,en;q=0.8','Cache-Control':'max-age=0','Connection':'keep-alive','User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'}

            form_data={ 'page':page }
            html = net.http_POST('http://popcornered.com/search_results?new', form_data, headers).content
                
            #html = net.http_GET(new_url).content
            #total_pages = '56'
            
            if total_pages == '':
                r= '<li class="disabled"><span>...</span></li><li><a href=".+?">.+?</a></li><li><a href=".+?">(.+?)</a>'
                total_pages = re.compile(r).findall(html)[0]   
                
            self.AddInfo(list, indexer, 'latest', url, type, str(page), total_pages)

            for item in re.finditer(r'<td class="rates__obj"><a href="(.+?)" class="rates__obj-name">(.+?)</a></td>\s*<td class="rates__vote">(.+?)</td>',html,re.I):
                url=item.group(1)
                name=item.group(2)
                item_year=item.group(3)
                name = self.CleanTextForSearch(name)
                self.AddContent(list,indexer,common.mode_File_Hosts,name+' ('+item_year+')','',type, url=url, name=name, year=item_year)

        elif section == 'azlist':
            
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                headers={'Referer':'http://popcornered.com/search_results?a-z','Host':'popcornered.com','Origin':'http://popcornered.com','Content-Type':'application/x-www-form-urlencoded','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Encoding':'gzip,deflate,sdch','Accept-Language':'en-US,en;q=0.8','Cache-Control':'max-age=0','Connection':'keep-alive','User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'}

                form_data={ 'page':page }
                #html = net.http_POST('http://popcornered.com/search_results?new', form_data, headers).content
            
            from entertainment.net import Net
            import re
            net = Net(cached=False)
            import urllib

            headers={'Referer':'http://popcornered.com/search_results?a-z','Host':'popcornered.com','Origin':'http://popcornered.com','Content-Type':'application/x-www-form-urlencoded','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Encoding':'gzip,deflate,sdch','Accept-Language':'en-US,en;q=0.8','Cache-Control':'max-age=0','Connection':'keep-alive','User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'}

            form_data={ 'page':page }
            html = net.http_POST('http://popcornered.com/search_results?a-z', form_data, headers).content
                
            #html = net.http_GET(new_url).content
            #total_pages = '56'
            
            if total_pages == '':
                r= '<li class="disabled"><span>...</span></li><li><a href=".+?">.+?</a></li><li><a href=".+?">(.+?)</a>'
                total_pages = re.compile(r).findall(html)[0]   
                
            self.AddInfo(list, indexer, 'azlist', url, type, str(page), total_pages)

            for item in re.finditer(r'<td class="rates__obj"><a href="(.+?)" class="rates__obj-name">(.+?)</a></td>\s*<td class="rates__vote">(.+?)</td>',html,re.I):
                url=item.group(1)
                name=item.group(2)
                item_year=item.group(3)
                name = self.CleanTextForSearch(name)
                self.AddContent(list,indexer,common.mode_File_Hosts,name+' ('+item_year+')','',type, url=url, name=name, year=item_year)

        elif section == 'rating':
            
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                headers={'Referer':'http://popcornered.com/search_results?rating','Host':'popcornered.com','Origin':'http://popcornered.com','Content-Type':'application/x-www-form-urlencoded','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Encoding':'gzip,deflate,sdch','Accept-Language':'en-US,en;q=0.8','Cache-Control':'max-age=0','Connection':'keep-alive','User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'}

                form_data={ 'page':page }
                #html = net.http_POST('http://popcornered.com/search_results?new', form_data, headers).content
            
            from entertainment.net import Net
            import re
            net = Net(cached=False)
            import urllib

            headers={'Referer':'http://popcornered.com/search_results?rating','Host':'popcornered.com','Origin':'http://popcornered.com','Content-Type':'application/x-www-form-urlencoded','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Encoding':'gzip,deflate,sdch','Accept-Language':'en-US,en;q=0.8','Cache-Control':'max-age=0','Connection':'keep-alive','User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'}

            form_data={ 'page':page }
            html = net.http_POST('http://popcornered.com/search_results?rating', form_data, headers).content
                
            #html = net.http_GET(new_url).content
            #total_pages = '56'
            
            if total_pages == '':
                r= '<li class="disabled"><span>...</span></li><li><a href=".+?">.+?</a></li><li><a href=".+?">(.+?)</a>'
                total_pages = re.compile(r).findall(html)[0]   
                
            self.AddInfo(list, indexer, 'rating', url, type, str(page), total_pages)

            for item in re.finditer(r'<td class="rates__obj"><a href="(.+?)" class="rates__obj-name">(.+?)</a></td>\s*<td class="rates__vote">(.+?)</td>',html,re.I):
                url=item.group(1)
                name=item.group(2)
                item_year=item.group(3)
                name = self.CleanTextForSearch(name)
                self.AddContent(list,indexer,common.mode_File_Hosts,name+' ('+item_year+')','',type, url=url, name=name, year=item_year)

                
    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''):
        
        from entertainment.net import Net
        
        net = Net()

        url_type = ''
        content_type = ''
        
        if indexer == common.indxr_Movies:#'[COLOR orange]'+year+'[/COLOR]'

            if section == 'main':
                self.AddSection(list, indexer,'latest','[COLOR yellow]Credits go to[/COLOR] [COLOR red]popcorn[/COLOR][COLOR white]ered.com[/COLOR][COLOR yellow] Please visit!!![/COLOR]','http://popcornered.com/search_results?new',indexer)
                self.AddSection(list, indexer,'latest','[COLOR red]Ordered[/COLOR] [COLOR white]by Latest[/COLOR]','http://popcornered.com/search_results?new',indexer)
                self.AddSection(list, indexer,'azlist','[COLOR red]Ordered[/COLOR] [COLOR white]by A-Z[/COLOR]','http://popcornered.com/search_results?a-z',indexer)
                self.AddSection(list, indexer,'rating','[COLOR red]Ordered[/COLOR] [COLOR white]by Highest Rated[/COLOR]','http://popcornered.com/search_results?rating',indexer)
                
            else:
                self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)
                         


    
    def GetFileHosts(self, url, list, lock, message_queue):
        import re
        from entertainment.net import Net
        
        net = Net()
        html = net.http_GET(url).content
        mp4file = re.compile('data-video="(.+?)"').findall(html)[0]
        url = 'http://popcornered.com/'+mp4file
        self.AddFileHost(list, 'HD', url)
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        new_url = 'http://popcornered.com/search_results'
        import re
        from entertainment.net import Net
        
        net = Net(do_not_cache_if_any=do_no_cache_keywords_list)
        
        if os.path.exists(self.cookie_file):
                try: os.remove(self.cookie_file)
                except: pass
        html = net.http_GET(new_url).content
        token = re.compile('<input name="_token" type="hidden" value="(.+?)">').findall(html)[0]
                
        headers={'Referer':'http://popcornered.com/search_results','Host':'popcornered.com','Origin':'http://popcornered.com','Content-Type':'application/x-www-form-urlencoded','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Encoding':'gzip,deflate,sdch','Accept-Language':'en-US,en;q=0.8','Cache-Control':'max-age=0','Connection':'keep-alive','User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'}

        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)

        form_data={ '_token':token, 'search_field':name, 'search_filter':'1' }
        content = net.http_POST('http://popcornered.com/search_results', form_data, headers).content
        
        helper = '%s (%s)' %(name,year) 
        
        match=re.compile('<td class="rates__obj"><a href="(.+?)" class="rates__obj-name">(.+?)</a></td>\s*<td class="rates__vote">(.+?)</td>').findall(content)
        
        for url, item_name, item_year in match:
            print url
            name_lower = common.CreateIdFromString(name)
            if item_year == year:
                print item_name

                self.GetFileHosts(url, list, lock, message_queue)
                    
