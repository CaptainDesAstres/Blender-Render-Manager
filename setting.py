#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module containing 'setting' class'''
import xml.etree.ElementTree as xmlMod

class setting:
	'''class that contain the script preferences or a rendering task preferences'''
	def __init__(self, xml= None):
		'''initialize settings object with default value or values extracted from an xml object'''
		self.x = 1920
		self.y = 1080
		self.percent = 1
		self.start = 0
		self.end = 0
		self.fps = 30
		
		if xml is not None:
			self.fromXml(xml)

	def fromXml(self,xml):
		'''extract settings from an xml object'''
		#get rendering resolution parameters 
		node = xml.find('resolution')
		self.x = int(node.get('x'))
		self.y = int(node.get('y'))
		self.percent = int(node.get('percent'))/100
		
		#get animation parameters
		node = xml.find('animation')
		if node is not None:
			self.start = int(node.get('start',0))
			self.end = int(node.get('end',0))
			self.fps = int(node.get('fps',30))
			
	
	def toXmlStr(self, head=False):
		'''export settings to an xml syntaxe string'''
		txt= ''
		
		if head:
			txt += '<?xml version="1.0" encoding="UTF-8"?>\n'
		
		txt+='<settings>\n'
		#export resolution parameters
		txt+='<resolution x="'+str(self.x)+'" y="'+str(self.y)+'" percent="'+str(int(self.percent*100))+'" />\n'
		
		#export animation parameters depending of settings type
		if self.start == 0 and self.end == 0:
			txt+= '<animation fps="'+str(self.fps)+'" />\n'
		else:
			txt+= '<animation start="'+str(self.start)+'" end="'+str(self.end)+'" fps="'+str(self.fps)+'" />\n'
		
		txt+='</settings>\n'
		return txt
	
	def printSettings(self):
		'''print settings like preferences settings'''
		print('résolution : '+str(self.x)+'x'+str(self.y)+' (@'+str(int(self.percent*100))+'%)\n')
		print('animation : '+str(self.fps)+'fps\n')
	
	def printSceneSettings(self,default=None):
		'''print settings like render file settings, coloring in red settings who don't match the default settings'''
		if default is None:
			default = self
		
		#write resolution parameters
		txt ='résolution : '
		if self.x != default.x :
			txt += '\033[31m'+str(self.x)+'\033[0mx'
		else:
			txt += str(self.x)+'x'
		
		if self.y != default.y :
			txt+= '\033[31m'+str(self.y)+'\033[0m (@'
		else:
			txt+= str(self.y)+' (@'
		
		if self.percent != default.percent :
			txt+= '\033[31m'+str(int(self.percent*100))+'\033[0m%)\n'
		else:
			txt+= str(int(self.percent*100))+'%)\n'
		
		#write animation parameters
		txt += 'animation : '
		if self.start != 0 or self.end != 0 :
			txt+= 'frame '+str(self.start)+' à '+str(self.end)+' '
		txt+='(@'
		
		if self.fps != default.fps :
			txt+= '\033[31m'+str(self.fps)+'\033[0mfps)\n'
		else:
			txt+= str(self.fps)+'fps)\n'
		
		print(txt)
	
	def getClone(self,start = None, end = None):
		'''create another settings object with the same attribut values
		restart/end attributes value with start/end argument values if set'''
		
		clone = setting( xmlMod.fromstring( self.toXmlStr( True ) ) )
		if start is not None:
			clone.start = start
		if end is not None:
			clone.end = end
		return clone
		



