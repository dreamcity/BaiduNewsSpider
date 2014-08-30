# -*- coding: utf-8 -*-
from xml.dom.minidom import Document
import os
import glob
global filelist,filedict
class XMLData:
	"""docstring for XMLData"""
	def __init__(self, sourcedir, outputfile):
		super(XMLData, self).__init__()
		self.sourcedir = sourcedir
		self.outfile = outputfile
		self.filelist = []
		self.filedict = {}

	def traversalFileFolder(self,path):
		for fn in glob.glob(path+os.sep+"*") :
			if os.path.isdir(fn):			
				self.filelist =[]
				self.traversalFileFolder(fn)
			else:
				self.filelist.append(fn)
				dirtemp = os.path.dirname(fn)
				dirname = dirtemp[2:].split('\\')[-1]
				self.filedict[dirname] = self.filelist

	def getXMLFile(self):
		self.traversalFileFolder(self.sourcedir)
		doc = Document()
		doc.appendChild(doc.createComment("Simple xml document__chapter 8")) 

		data_storage = doc.createElement('data_storage')
		doc.appendChild(data_storage)

		source = doc.createElement('source')
		data_storage.appendChild(source)
		source_data = doc.createTextNode(self.sourcedir[self.sourcedir.index('/')+1:])
		source.appendChild(source_data)

		classtype = doc.createElement('classtype')
		data_storage.appendChild(classtype)

		listlabel = list(self.filedict.keys())
		listlabel.sort()
		for key in listlabel:
			classlabel = doc.createElement(key)
			classtype.appendChild(classlabel)
			label = doc.createElement('label')
			label_text = doc.createTextNode(str(listlabel.index(key)))
			label.appendChild(label_text)
			classlabel.appendChild(label)

			values = self.filedict[key]
			for value in values:
				li = doc.createElement('li')
				li_text = doc.createTextNode(value)
				li.appendChild(li_text)
				classlabel.appendChild(li)
	
		file_object = open(self.outfile,'w')
		file_object.write(doc.toprettyxml())
		file_object.close()

# inputfolder = r'./baidunews'
# outputfile = r'baidunewslist.xml'
# XD = XMLData(inputfolder,outputfile)
# XD.getXMLFile()