"""The MIT License (MIT)

Copyright (c) 2015 João Paulo

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""


import requests
from bs4 import BeautifulSoup as bs


def search_query_yt(query):
	URL_BASE = "https://www.youtube.com/results?search_query=%s"%(query)
	url_yt= "https://www.youtube.com"
	r = requests.get(URL_BASE)
	page = r.text
	soup = bs(page,"html.parser")
	id_url = None
	list_videos = []
	max = 0
	for link in soup.find_all('a'):
		url = link.get('href')
		title = link.get('title')
		if url.startswith("/watch") and (id_url!=url) and (title!=None):
			id_url = url
			dic = {'title':title,'url':url_yt+url}
			list_videos.append(dic)
			max +=1
			if max == 10:
				dic = {'bot_api_yt':list_videos}
				return dic
