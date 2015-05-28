#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

class setting:
	def __init__(self, xml= None):
		self.x = 1920
		self.y = 1080
		self.percent = 1
		
		if xml is not None:
			self.parseXml(xml)

	def parseXml(self,xml):
		node = xml.find('resolution')
		self.x = int(node.get('x'))
		self.y = int(node.get('y'))
		self.percent = int(node.get('percent'))/100
	
	def toXmlStr(self, head=False):
		txt= ''
		
		if head:
			txt += '<?xml version="1.0" encoding="UTF-8"?>'
		
		txt+='<settings>'
		txt+='<resolution x="'+str(self.x)+'" y="'+str(self.y)+'" percent="'+str(self.pourcent)+'"/>'
		txt+='</settings>'



