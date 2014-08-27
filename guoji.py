# -*- coding: utf-8 -*-
import urllib.request as request
from urllib.error import HTTPError
import chardet
import re
import os

class GuoJiNews(object):
	"""docstring for GuoJiNews"""
	def __init__(self,url):
		super(GuoJiNews, self).__init__()
		self.url = url
		self.codedetect = ''
		self.articlelink = []

	def getPage(self, url):
		user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
		headers = { 'User-Agent' : user_agent }
		req = request.Request(url, headers = headers)
		myResponse = request.urlopen(req)
		myPage = myResponse.read()
		self.codedetect = chardet.detect(myPage)['encoding']
		if self.codedetect:
			myPage =myPage.decode(self.codedetect,'ignore')
		return myPage

	def saveData(self,url,title,article):
		symbol = 'baidunews'
		if os.path.exists(str(symbol)):
			pass
		else:
			os.mkdir(str(symbol))
		symbol = 'baidunews/guoji'
		if os.path.exists(str(symbol)):
			pass
		else:
			os.mkdir(str(symbol))
		pattern = re.compile(r'[0-9]+?',re.S)
		result= ''.join(pattern.findall(url))
		# print('result: ', result )
		filename ='./baidunews/guoji/' + result + '.txt'
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
			pattern = re.compile(r'<li><a href="http://.*target="_blank".*mon.*</a></li>|<li><a href="http://.*mon.*target="_blank".*</a></li>')
			result = pattern.findall(myPage)
			# print('result:', result)
			print('l:',len(result))
			for x in result:
				pattern = re.compile(r'<a href=".+?"')
				result = ''.join(pattern.findall(x))
				line = result[9:-1]
				self.articlelink.append(line)
				# print('line:', line)
			# pattern = re.compile(r'<a href="http:.+?<span class="s">',re.M)

	def getArticleFile(self):
		for link in self.articlelink:
			try:
				myPage = self.getPage(link)
			except HTTPError as e:
				pos = self.articlelink.index(link)
				del(self.articlelink[pos])
				continue
			if self.codedetect != 'utf-8' and self.codedetect != 'gbk' and self.codedetect !='GB2312':
				# print('error')
				continue
			else:
				myPage = myPage.replace(u'\u30fb', u'')
				myPage = myPage.replace(u'\u3000', u'')
				patten = re.compile(r'<title>.*?</title>',re.M)
				match = patten.search(myPage)
				if match:
					title = match.group()
					title = title[7:-8]
					print('title: ', title)
				article = []
				patten = re.compile(r'(<p>.*?</p>|<p style.*?</p>)', re.S|re.I)
				# patten = re.compile(r'(<P>.*?</P>|<p>.*?</p>|<p style.*?</p>)', re.S)
				result = patten.findall(myPage)
				# print('result: ', result)
				for x in result:
					patten = re.compile(r'.*?href="http:.*?',re.S)
					match = patten.match(x)
					# print(match)
					if match:
						pass
					else:		
						patten = re.compile(u'([\u2E80-\u9FFF]+)', re.M)
						line = ''.join(patten.findall(x))
						article.append(line)
						# print('line: ', line)
				articlepaper = ''.join(article)
				self.saveData(link,title,articlepaper)
				# print('article: ',article)
		print('getArticleFile success')

	def getBaiduGuoJi(self):
		self.getArticleLink()
		self.getArticleFile()
url = 'http://guoji.news.baidu.com/'
GJSpider = GuoJiNews(url)
GJSpider.getBaiduGuoJi()

# print('link: ', GNNews.articlelink)