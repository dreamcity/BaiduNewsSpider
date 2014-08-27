#encoding=utf-8
import urllib.request as request
import chardet
import re
import os

class InternetNews(object):
	"""docstring for InternetNews"""
	def __init__(self,url):
		super(InternetNews, self).__init__()
		self.url = url
		self.codedetect = ''
		self.labelTable = {}
		self.articlelink = []

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

	def saveData(self,url,title,article):
		symbol = 'baidunews'
		if os.path.exists(str(symbol)):
			pass
		else:
			os.mkdir(str(symbol))
		symbol = 'baidunews/internet'
		if os.path.exists(str(symbol)):
			pass
		else:
			os.mkdir(str(symbol))
		pattern = re.compile(r'[0-9]+?',re.S)
		result= ''.join(pattern.findall(url))
		# print('result: ', result )
		filename ='./baidunews/internet/' + result + '.txt'

		file_object = open(filename, 'w')
		file_object.write(title)
		file_object.write('\n')
		file_object.write(article)
		file_object.close()
	def getLabelTable(self):
		myPage = self.getPage(self.url)
		pattern = re.compile(r'<div class="widget-submenu">.+?</div>', re.S)
		result = pattern.findall(myPage)
		for i in result:
			i = i.replace(u'\u30fb', u'')
		line = ''.join(result)
		linkhttp = []
		labelhttp = []
		p1 = re.compile(r'<a href=".+target', re.M)
		linktemp = p1.findall(line)
		for link in linktemp:
			pattern = re.compile(r'".+"')
			link1 = ''.join(pattern.findall(link))
			link2 = self.url + link1[2:-1]
			linkhttp.append(link2)
		p2 = re.compile(r'>.+</a>', re.M)
		labeltemp = p2.findall(line)
		for label in labeltemp:
			labelhttp.append(label[1:-4])
		self.labelTable = dict(zip(labelhttp,linkhttp))

	def getArticleLink(self):
		labellink =  list(self.labelTable.values())
		for link in labellink:
			myPage = self.getPage(link)
			myPage = myPage.replace(u'\u30fb', u'')
			pattern = re.compile(r'<a href="http:.+?<span class="s">',re.M)	
			result = ''.join(pattern.findall(myPage))
			# print('result: ', result)
			articlelink = []
			pattern = re.compile(r'http:.+?"',re.M)
			linktemp = pattern.findall(result)
			for link in linktemp:
		 		self.articlelink.append(link[:-1])

	def getArticleFile(self):
		for link in self.articlelink:
			# print('link: ', link)
			myPage = self.getPage(link)
			if self.codedetect != 'utf-8' and self.codedetect != 'gbk' and self.codedetect !='GB2312':
				# print('error')
				continue
			else:
				myPage = myPage.replace(u'\u30fb', u'')
				pattern = re.compile(r'<title>.*?</title>',re.M)
				match = pattern.search(myPage)
				if match:
					title = match.group()
					title = title[7:-8]
					print('title: ', title)
				article = []
				pattern = re.compile(r'(<p>.*?</p>|<p style.*?</p>)', re.S|re.I)
				# pattern = re.compile(r'(<P>.*?</P>|<p>.*?</p>|<p style.*?</p>)', re.S)
				result = pattern.findall(myPage)
				# print('result: ', result)
				for x in result:
					pattern = re.compile(r'.*?href="http:.*?',re.S)
					match = pattern.match(x)
					# print(match)
					if match:
						pass
					else:		
						pattern = re.compile(u'([\u2E80-\u9FFF]+)', re.M)
						line = ''.join(pattern.findall(x))
						article.append(line)
						# print('line: ', line)
				articlepaper = ''.join(article)
				self.saveData(link,title,articlepaper)

				# print('article: ',article)
		print('getArticleFile success')

	def getBaiduInternet(self):
		self.getLabelTable()
		self.getArticleLink()
		self.getArticleFile()

url = 'http://internet.baidu.com/'
INSpider = InternetNews(url)
INSpider.getBaiduInternet()
# print(INSpider.labelTable)
# print(INSpider.articlelink)
