#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

class setting:
	def __init__(self, xml= None):
		self.x = 1920
		self.y = 1080
		self.percent = 1
		self.start = 0
		self.end = 0
		self.fps = 30
		
		if xml is not None:
			self.parseXml(xml)

	def parseXml(self,xml):
		node = xml.find('resolution')
		self.x = int(node.get('x'))
		self.y = int(node.get('y'))
		self.percent = int(node.get('percent'))/100
		node = xml.find('animation')
		if node is not None:
			self.start = int(node.get('start',0))
			self.end = int(node.get('end',0))
			self.fps = int(node.get('fps',30))
			
	
	def toXmlStr(self, head=False):
		txt= ''
		
		if head:
			txt += '<?xml version="1.0" encoding="UTF-8"?>\n'
		
		txt+='<settings>\n'
		txt+='<resolution x="'+str(self.x)+'" y="'+str(self.y)+'" percent="'+str(int(self.percent*100))+'" />\n'
		
		if self.start == 0 and self.end == 0:
			txt+= '<animation fps="'+str(self.fps)+'" />\n'
		else:
			txt+= '<animation start="'+str(self.start)+'" end="'+str(self.end)+'" fps="'+str(self.fps)+'" />\n'
		
		txt+='</settings>\n'
		return txt
	
	def printSettings(self):
		print('résolution : '+str(self.x)+'x'+str(self.y)+' (@'+str(int(self.percent*100))+'%)\n')
		print('animation : '+str(self.fps)+'fps\n')



