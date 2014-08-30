# -*- coding: utf-8 -*-
import baiduspider.baidunews as baidunews
import baiduspider.baijia as baijia
import baiduspider.internet as internet
import baiduspider.guonei as guonei
import baiduspider.guoji as guoji
import baiduspider.mil as mil
import baiduspider.finance as finance
import baiduspider.sports as sports
import baiduspider.yule as yule
import baiduspider.lady as lady
import baiduspider.tech as tech
import baiduspider.fangchan as fangchan
import baiduspider.auto as auto
import baiduspider.shehui as shehui
import baiduspider.youxi as youxi
import baiduspider.jiaoyu as jiaoyu
import baiduNewsXML

url = r'http://news.baidu.com/'
inputfolder = r'./baidunews'
outputfile = r'baidunewslist.xml'
BDN_Spider = baidunews.BaiduNewsSpider(url)
BDN_Spider.getClassTable()
classTable = BDN_Spider.classTable
print(classTable.keys())

BaiJiaSpider = baijia.BaijiaNews(classTable['百家'])
BaiJiaSpider.getBaijiaNews()
InternetSpider = internet.InternetNews(classTable['互联网'])
InternetSpider.getInternetNews()
GuoNeitSpider = guonei.GuoNeiNews(classTable['国内'])
GuoNeitSpider.getGuoNeiNews()
GuoJiSpider = guoji.GuoJiNews(classTable['国际'])
GuoJiSpider.getGuoJiNews()
MilSpider = mil.MilNews(classTable['军事'])
MilSpider.getMilNews()
FinanceSpider = finance.FinanceNews(classTable['财经'])
FinanceSpider.getFinanceNews()
SportsSpider = sports.SportsNews(classTable['体育'])
SportsSpider.getSportsNews()
YuleSpider = yule.YuleNews(classTable['娱乐'])
YuleSpider.getYuleNews()
LadySpider = lady.LadyNews(classTable['女人'])
LadySpider.getLadyNews()
TechSpider = tech.TechNews(classTable['科技'])
TechSpider.getTechNews()
FangchanSpider = fangchan.FangchanNews(classTable['房产'])
FangchanSpider.getFangchanNews()
AutoSpider = auto.AutoNews(classTable['汽车'])
AutoSpider.getAutoNews()
ShehuiSpider = shehui.ShehuiNews(classTable['社会'])
ShehuiSpider.getShehuiNews()
YouXiSpider = youxi.YouXiNews(classTable['游戏'])
YouXiSpider.getYouXiNews()
JiaoyuSpider = jiaoyu.JiaoyuNews(classTable['教育'])
JiaoyuSpider.getJiaoyuNews()

XD = baiduNewsXML.XMLData(inputfolder,outputfile)
XD.getXMLFile()
