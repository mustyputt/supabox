# -*- coding: utf-8 -*-

'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import re,urllib,urlparse,base64
import requests
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from BeautifulSoup import BeautifulSoup
from resources.lib.modules.common import  random_agent, quality_tag
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full

class source:
	def __init__(self):
		self.base_link = 'http://www.solarmovies.ag'
		self.movie_link = '/%s.html'
		self.ep_link = '/%s.html'

	def movie(self, imdb, title, year):
		self.genesisreborn_url = []
		try:
			headers = {'User-Agent': random_agent()}
			
			title = cleantitle.getsearch(title)
			title = title.replace(' ','-')
			title = title + "-" + year
			query = self.movie_link % title
			u = urlparse.urljoin(self.base_link, query)
			self.genesisreborn_url.append(u)
			return self.genesisreborn_url
		except:
			return
			
	
	def tvshow(self, imdb, tvdb, tvshowtitle, year):
		try:
			url = {'tvshowtitle': tvshowtitle, 'year': year}
			url = urllib.urlencode(url)
			return url
		except:
			return			

	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		self.genesisreborn_url = []
		try:
			headers = {'User-Agent': random_agent()}
			data = urlparse.parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			data['season'], data['episode'] = season, episode
			self.genesisreborn_url = []
			title = cleantitle.getsearch(title)
			title = title.replace(' ','-')
			query = title + "-season-" + season + "-episode-" + episode
			query= self.ep_link % query
			# print("SOLAR query", query)
			u = urlparse.urljoin(self.base_link, query)
			self.genesisreborn_url.append(u)
			return self.genesisreborn_url
		except:
			return

			
	def sources(self, url, hostDict, hostprDict):
		sources = []
		try:
			headers = {'User-Agent': random_agent()}
			for url in self.genesisreborn_url:
				if url == None: return
				
				html = requests.get(url, headers=headers, timeout=10).text
				
				match = re.compile('<a href="[^"]+go.php\?url=([^"]+)" target="_blank">').findall(html)
				for url in match:
					try:
						# print("SOLAR SOURCE", url)
						host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
						host = host.encode('utf-8')			
						if not host in hostDict: raise Exception()
						quality = "SD"
							# print("OpenMovies SOURCE", stream_url, label)
						sources.append({'source': host, 'quality':quality, 'provider': 'Solar', 'url': url, 'direct': False, 'debridonly': False})
					except:
						pass


			return sources
		except:
			return sources


	def resolve(self, url):
			return url


