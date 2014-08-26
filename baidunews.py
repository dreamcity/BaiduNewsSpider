#encoding=utf-8
import urllib.request as request
import re
import chardet
import baijia		
class BaiduNewsSpider():
	"""docstring for BaiduNewsSpider"""
	def __init__(self, url):
		super(BaiduNewsSpider, self).__init__()
		self.myUrl = url
		self.table = {}
		
	def getPage(self):
		user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
		headers = { 'User-Agent' : user_agent }
		req = request.Request(self.myUrl, headers = headers)
		myResponse = request.urlopen(req)
		myPage = myResponse.read()
		codedetect = chardet.detect(myPage)['encoding']
		myPage =myPage.decode(codedetect,'ignore')
		return myPage
		
	def getTable(self,myPage):
		p1 = re.compile(r'<div id="channel-all">.*?</div>' , re.S)
		part1 = p1.findall(myPage)
		part1str = ''.join(part1)
		p2 = re.compile(r'<a href=.*?</a>' , re.S)
		part2 = p2.findall(part1str)
		list_length = len(part2)

		link = []
		label = []
		for i in range(1,list_length-2):
			p3 = re.compile(r'http.*?\.com/',re.S)
			linkstr = ''.join(p3.findall(part2[i]))
			link.append(linkstr)
			p4 = re.compile(r'>.+?<',re.S)
			labelstr = ''.join(p4.findall(part2[i]))
			label.append(labelstr[1:-1])   
		self.table = dict(zip(label,link))
	
	def getBaijia(self,url):
		baijia.BaijiaNews.getBaiduBaijia(url)

# url = 'http://news.baidu.com/'
# BDN_Spider = BaiduNewsSpider(url)
# myPage = BDN_Spider.getPage()
# BDN_Spider.getTable(myPage)
# print('teble: ', BDN_Spider.table)
url = 'http://baijia.baidu.com/'
BDN_Spider = BaiduNewsSpider(url)
BDN_Spider.getBaijia(url)