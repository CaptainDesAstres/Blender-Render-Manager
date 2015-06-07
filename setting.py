#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module containing 'setting' class'''
import xml.etree.ElementTree as xmlMod

class setting:
	'''class that contain the script preferences or a rendering task preferences'''
	
	
	def __init__(self, xml= None):
		'''initialize settings object with default value or values extracted from an xml object'''
		#default values of all the attributes
		self.x = 1920
		self.y = 1080
		self.percent = 1
		self.start = None
		self.end = None
		self.fps = 30
		
		self.tilesCyclesCPUX = 32
		self.tilesCyclesCPUY = 32
		self.tilesCyclesGPUX = 256
		self.tilesCyclesGPUY = 256
		self.tilesBIX = 256
		self.tilesBIY = 256
		self.renderingDevice = 'GPU'
		self.renderingEngine = 'CYCLES'
		self.outputFormat = 'EXR'
		self.zPass = True
		self.objectIndexPass = True
		self.renderLayerList = []
		self.backgroundLayersKeywords = ['bck', 'background']
		self.foregroundLayersKeywords = ['fgd', 'foreground']
		self.backgroundCyclesSamples = 1500
		self.foregroundCyclesSamples = 1500
		self.mainAnimationCyclesSamples = 1500
		self.backgroundAnimation = 0
		self.foregroundAnimation = 0
		self.compositingEnable = True
		self.filmExposure = 1
		self.filmTransparentEnable = True
		self.blenderPath = 'blender'
		self.outputPath = None
		self.outputSubPath = '%N-%S'
		self.outputName = '%L-%F'
		self.transparencyMaxBounces = 6
		self.transparencyMinBounces = 4
		self.bouncesMax = 8
		self.bouncesMin = 3
		self.diffuseBounces = 4
		self.glossyBounces = 4
		self.transmissionBounces = 12
		self.volumeBounces = 0
		self.simplify = None
		
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
			self.start = int(node.get('start',None))
			self.end = int(node.get('end',None))
			self.fps = int(node.get('fps',30))
		self.startEndCheck()
	
	
	
	
	
	
	def startEndCheck(self):
		'''make sure that that start frame and end frame are all set or all None'''
		if self.start is None and self.end is not None:
			self.start = self.end
		elif self.start is not None and self.end is None:
			self.end = self.start
			
	
	
	
	
	
	def toXmlStr(self, head=False):
		'''export settings to an xml syntaxe string'''
		txt= ''
		
		if head:
			txt += '<?xml version="1.0" encoding="UTF-8"?>\n'
		
		txt += '<settings>\n'
		#export resolution parameters
		txt += '<resolution x="'+str(self.x)+'" y="'+str(self.y)+'" percent="'+str(int(self.percent*100))+'" />\n'
		
		#export animation parameters depending of settings type
		if self.start is None or self.end is None:
			txt+= '<animation fps="'+str(self.fps)+'" />\n'
		else:
			txt+= '<animation start="'+str(self.start)+'" end="'+str(self.end)+'" fps="'+str(self.fps)+'" />\n'
		
		
		txt += '<engine value="'+self.renderingEngine+'"/>\n'
		
		
		txt += '<cycles>\n'
			txt += '<cpu x="'+str(self.tilesCyclesCPUX)+'" y="'+str(self.tilesCyclesCPUY)+'"/>\n'
			txt += '<cpu x="'+str(self.tilesCyclesGPUX)+'" y="'+str(self.tilesCyclesGPUY)+'"/>\n'
			txt += '<device value="'+self.renderingDevice+'"/>\n'
			txt += '<film exposure="'+str(self.filmExposure)+'" transparent="'+str(self.filmTransparentEnable)+'" />\n'
			
			
			txt += '<bouncesSet>'
				txt += '<transparency min="'+str(self.transparencyMaxBounces)+'" max="'+str(transparencyMinBounces)+'" />'
				txt += '<bounces min="'+str(self.bouncesMax)+'" max="'+str(self.bouncesMin)+'" />'
				txt += '<diffuse bounces="'+str(self.diffuseBounces)+'" />'
				txt += '<glossy bounces="'+str(self.glossyBounces)+'" />'
				txt += '<transmission bounces="'+str(self.transmissionBounces)+'" />'
				txt += '<volume bounces="'+str(self.volumeBounces)+'" />'
			txt += '</bouncesSet>'
			
			
			
		txt += '</cycles>\n'
		
		
		txt += '<blenderInternal x="'+str(self.tilesBIX)+'" y="'+str(self.tilesBIY)+'" />\n'

		txt += '<compositing enable="'+str(self.compositingEnable)+'" />\n'
		if self.simplify is None:
			txt += '<simplify subdiv="0" />\n'
		else:
			txt += '<simplify subdiv="'+str(self.simplify)+'" />\n'
		
		
		
		if len(self.renderLayerList)>0:
			txt += '<renderLayerList>\n'
			for layer in self.renderLayerList:
				txt += '<layer name="'+layer['name']+'" z="'+str(layer['z'])+'" objIndex="'+str(layer['object index'])+'" render="'+str(layer['use'])+'"/>\n'
			txt += '</renderLayerList>\n'
		
		txt += '<renderLayerPreferences>\n'
			
			txt += '<background sample="'+str(self.backgroundCyclesSamples)+'" frame="'+str(self.backgroundAnimation)+'" >\n'
			for key in self.backgroundLayersKeywords:
				txt += '<keywords value="'+key+'" />\n'
			txt += '</background>\n'
			
			txt += '<foreground sample="'+str(self.foregroundCyclesSamples)+'" frame="'+str(self.foregroundAnimation)+'" >\n'
			for key in self.foregroundLayersKeywords:
				txt += '<keywords value="'+key+'" />\n'
			txt += '</foreground>\n'
			
			txt += '<main sample="'+str(self.mainAnimationCyclesSamples)+'" zPass="'+str(self.zPass)+'" objectIndexPass="'+str(self.objectIndexPass)+'" />\n'
			
		txt += '</renderLayerPreferences>\n'
		
		
		
		txt += '<output format="'+self.outputFormat+'" '
		if self.outputPath is not None:
			txt += 'mainpath="'+self.outputPath+'" '
		txt += 'subpath="'+self.outputSubPath+'" name="'+self.outputName+'" />\n'
		
		txt += '<blender path="'+self.blenderPath+'" />\n'
		
		txt += '</settings>\n'
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
		if self.start is not None and self.end is not None :
			txt+= 'frame '+str(self.start)+' à '+str(self.end)+' '
		txt += '(@'
		
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
		clone.startEndCheck()
		return clone
		



