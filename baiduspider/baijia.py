# -*- coding: utf-8 -*-
import urllib.request as request
from http.client import IncompleteRead
from urllib.error import HTTPError , URLError
import socket  
import time  
import chardet
import re
import os

class BaijiaNews(object):
	"""docstring for BaijiaNews"""
	def __init__(self,url):
		super(BaijiaNews, self).__init__()
		self.url = url
		self.codedetect = ''
		self.articlelink = []

	def getPage(self,url):
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

	def getArticleLink(self):
		myPage = self.getPage(self.url)
		if self.codedetect != 'utf-8' and self.codedetect != 'gbk' and self.codedetect !='GB2312':
			pass
		else:
			myPage = myPage.replace(u'\u30fb', u'')
			pattern =  re.compile(r'<h3>.*?</h3>',re.M)
			result = pattern.findall(myPage)
			list_length = len(result)
			print('list:',list_length)
			line= ''.join(result)
			for i in range(1,list_length-2):
				p1 = re.compile(r'http.*?\d+',re.M)
				linkstr = ''.join(p1.findall(result[i]))
				self.articlelink.append(linkstr)
	
	def saveData(self,url,title,article):
		symbol = 'baidunews'
		if os.path.exists(str(symbol)):
			pass
		else:
			os.mkdir(str(symbol))
		symbol = 'baidunews/baijia'
		if os.path.exists(str(symbol)):
			pass
		else:
			os.mkdir(str(symbol))
		pattern = re.compile(r'[0-9]+?',re.M)
		result= ''.join(pattern.findall(url))
		filename ='./baidunews/baijia/' + result + '.txt'
		file_object = open(filename, 'w')
		file_object.write(title)
		file_object.write('\n')
		file_object.write(article)
		file_object.close()

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
					p1 = re.compile(r'<p class="text">.+?</p>',re.M)
					articlepart = p1.findall(myPage)
					del(articlepart[-1])
					article1 = []
					for part in articlepart:
						p2 = re.compile(u'([\u2E80-\u9FFF].+[\u2E80-\u9FFF])', re.M)
						part2 = p2.findall(part)
						part2str = ''.join(part2)
						p3 = re.compile(r'<strong>.*</strong>', re.M)
						match = p3.match(part2str)
						if match:
							pass
						else:
							article1.append(part2str)
					article2 = []
					for i in article1:
						p4 = re.compile(r'<.*trong>')
						article2.append(''.join(p4.split(i)))
					articlepaper = ''.join(article2)					
					if len(articlepaper) != 0 :
						self.saveData(link,title,articlepaper)
		print('get BaijiaNews success!!!')

	def getBaijiaNews(self):
		self.getArticleLink()
		self.getArticleFile()
			
