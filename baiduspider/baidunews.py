# -*- coding: utf-8 -*-
import urllib.request as request
import re
import chardet
	
class BaiduNewsSpider():
	"""docstring for BaiduNewsSpider"""
	def __init__(self, url):
		super(BaiduNewsSpider, self).__init__()
		self.myUrl = url
		self.classTable = {}

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
	
	def getClassTable(self):
		myPage = self.getPage(self.myUrl)
		p1 = re.compile(r'<div id="channel-all">.*?</div>' , re.S)
		part1 = p1.findall(myPage)
		part1str = ''.join(part1)
		p2 = re.compile(r'<a href=.*?</a>' , re.S)
		part2 = p2.findall(part1str)
		list_length = len(part2)

		link = []
		label = []
		for i in range(1,list_length):
			p3 = re.compile(r'http.*?\.com/',re.S)
			linkstr = ''.join(p3.findall(part2[i]))
			link.append(linkstr)
			p4 = re.compile(r'>.+?<',re.S)
			labelstr = ''.join(p4.findall(part2[i]))
			label.append(labelstr[1:-1])   
		self.classTable = dict(zip(label,link))