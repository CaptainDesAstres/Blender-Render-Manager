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
		self.x = node.get('x')
		self.y = node.get('y')
		self.percent = int(node.get('proportion'))/100
		



