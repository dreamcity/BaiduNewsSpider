#encoding=utf-8
import urllib.request as request
from urllib.error import HTTPError
import chardet
import re
import os

class BaijiaNews(object):
	"""docstring for BaijiaNews"""
	def __init__(self,url):
		super(BaijiaNews, self).__init__()
		self.url = url
		self.codedetect = ''
		self.table = {}

	def getPage(self,url):
		user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
		headers = { 'User-Agent' : user_agent }
		req = request.Request(url, headers = headers)
		myResponse = request.urlopen(req)
		myPage = myResponse.read()
		self.codedetect = chardet.detect(myPage)['encoding']
		if self.codedetect:		
			myPage =myPage.decode(self.codedetect,'ignore')
		return myPage

	def getArticleTable(self):
		myPage = self.getPage(self.url)
		pattern =  re.compile(r'<h3 style=.*?</h3>',re.S)
		result = pattern.findall(myPage)
		list_length = len(result)
		# print(list_length)
		line= ''.join(result)

		link = []
		label = []
		for i in range(1,list_length-2):
			p1 = re.compile(r'http.*?\d+',re.S)
			linkstr = ''.join(p1.findall(result[i]))
			link.append(linkstr)

			p2 = re.compile(r'mon=.+?>.+</a>',re.S)
			labelstrtmp = ''.join(p2.findall(result[i]))
			p3 = re.compile(r'>.+<',re.S)
			labelstr = ''.join(p3.findall(labelstrtmp))
			label.append(labelstr[1:-1])

		self.table = dict(zip(label,link))
		# return table	
	
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

		filename ='./baidunews/baijia/' + url[-5:]+'.txt'

		file_object = open(filename, 'w')
		file_object.write(title)
		file_object.write('\n')
		file_object.write(article)
		file_object.close()

	def getArticleFile(self):
		articlelink =  list(self.table.values())
		# print('articlelink:',articlelink)
		for link in articlelink:
			try:
				myPage = self.getPage(link)
			except HTTPError as e:
				pos = self.articlelink.index(link)
				del(self.articlelink[pos])
				continue
			
			# myPage = myPage.replace(u'\u2022', u'')
			pattern = re.compile(r'<title>.+</title>',re.S)
			# title = ''.join(pattern.findall(myPage))
			# title = title[7:-14]

			titlelist = pattern.findall(myPage)
			for i in titlelist:
				i = i.replace(u"\u2022", u" ")
			titletmp = ''.join(titlelist)

			pattern = re.compile(u'([\u2E80-\u9FFF].+[\u2E80-\u9FFF])', re.M)
			# pattern = re.compile(u'([\u4e00-\u9fa5]+)', re.M)
			title = ''.join(pattern.findall(titletmp))
			title = title[:-6]
			# title = title[7:-8]
			print("title: ", title)
			# print('done!1436')
			p1 = re.compile(r'<p class="text">.+?</p>',re.S)
			articlepart = p1.findall(myPage)
			del(articlepart[-1])
			# print('result0: ', articlepart)
			article1 = []
			for part in articlepart:
				part = part.replace(u"\u2022", u"")
				# print('result: ',i)
				# part1= i
				p2 = re.compile(u'([\u2E80-\u9FFF].+[\u2E80-\u9FFF])', re.S)
				# p2 = re.compile(u'([\u4e00-\u9fa5].+[\u4e00-\u9fa5])', re.S)
				part2 = p2.findall(part)
				# print('part2:',part2)
				part2str = ''.join(part2)
				p3 = re.compile(r'<strong>.*</strong>', re.S)
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
			# print('link: ', link)
			# print('title: ', title)
			self.saveData(link,title,articlepaper)
		print('getArticleFile success')

	def getBaiduBaijia(self):
		# myPage = self.getPage(self.url)
		self.getArticleTable()
		self.getArticleFile()
			
		
url = 'http://baijia.baidu.com/'
BJNews = BaijiaNews(url)
BJNews.getBaiduBaijia()
# getBaiduBaijia(url)
