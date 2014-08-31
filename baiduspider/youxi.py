# -*- coding: utf-8 -*-
import urllib.request as request
from http.client import IncompleteRead
from urllib.error import HTTPError , URLError
import socket  
import time  
import chardet
import re
import os

class YouXiNews(object):
	"""docstring for YouXiNews"""
	def __init__(self,url):
		super(YouXiNews, self).__init__()
		self.url = url
		self.codedetect = ''
		self.articlelink = []

	def getPage(self, url):
		timeout = 10 
		socket.setdefaulttimeout(timeout)
		sleep_download_time = 1
		time.sleep(sleep_download_time)
		user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
		headers = { 'User-Agent' : user_agent }
		req = request.Request(url, headers = headers)
		myResponse = request.urlopen(req)
		myPage = myResponse.read()
		self.codedetect = chardet.detect(myPage)['encoding']
		if self.codedetect:
			myPage =myPage.decode(self.codedetect,'ignore')
		myResponse.close()
		return myPage

	def saveData(self,url,title,article):
		symbol = 'baidunews'
		if os.path.exists(str(symbol)):
			pass
		else:
			os.mkdir(str(symbol))
		symbol = 'baidunews/youxi'
		if os.path.exists(str(symbol)):
			pass
		else:
			os.mkdir(str(symbol))
		pattern = re.compile(r'[0-9]+?',re.S)
		result= ''.join(pattern.findall(url))
		filename ='./baidunews/youxi/' + result + '.txt'
		file_object = open(filename, 'w')
		file_object.write(title)
		file_object.write('\n')
		file_object.write(article)
		file_object.close()		

	def getArticleLink(self):
		myPage = self.getPage(self.url)
		if self.codedetect != 'utf-8' and self.codedetect != 'gbk' and self.codedetect !='GB2312':
			pass
		else:
			myPage = myPage.replace(u'\u30fb', u'')
			pattern = re.compile(r'<a href="http:.+?<span class="s">',re.M)	
			result = pattern.findall(myPage)
			print('list:',len(result))
			for x in result:
				pattern = re.compile(r'<a href=".+?"')
				result = ''.join(pattern.findall(x))
				line = result[9:-1]
				self.articlelink.append(line)

	def getArticleFile(self):
		for link in self.articlelink:
			try:
				myPage = self.getPage(link)
			except HTTPError :
				pos = self.articlelink.index(link)
				del(self.articlelink[pos])
				continue
			except URLError :
				pos = self.articlelink.index(link)
				del(self.articlelink[pos])
				continue
			except socket.timeout :
				pos = self.articlelink.index(link)
				del(self.articlelink[pos])
				continue
			except IncompleteRead :
				pos = self.articlelink.index(link)
				del(self.articlelink[pos])
				continue
			if self.codedetect != 'utf-8' and self.codedetect != 'gbk' and self.codedetect !='GB2312':
				continue
			else:
				myPage = myPage.replace(u'\ue844', u'')
				myPage = myPage.replace(u'\u30fb', u'')
				myPage = myPage.replace(u'\u3000', u'')
				myPage = myPage.replace(u'\u2022', u'')	
				myPage = myPage.replace(u'\u200b', u'')
				pattern = re.compile(r'<title>.*?</title>',re.M)
				match = pattern.search(myPage)
				if match:
					title = match.group()
					title = title[7:-8]
					print('title: ', title)
					article = []
					pattern = re.compile(r'(<p>.*?</p>|<p style.*?</p>)', re.S|re.I)
					result = pattern.findall(myPage)
					for x in result:
						pattern = re.compile(r'.*?href="http:.*?',re.S)
						match = pattern.match(x)
						if match:
							pass
						else:		
							pattern = re.compile(u'([\u2E80-\u9FFF]+)', re.M)
							line = ''.join(pattern.findall(x))
							article.append(line)
					articlepaper = ''.join(article)
					if len(articlepaper) != 0 :
						self.saveData(link,title,articlepaper)
		print('get YouXiNewsFile success')

	def getYouXiNews(self):
		self.getArticleLink()
		self.getArticleFile()
