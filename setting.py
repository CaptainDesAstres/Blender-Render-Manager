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
		# get rendering resolution parameters 
		node = xml.find('resolution')
		self.x = int(node.get('x'))
		self.y = int(node.get('y'))
		self.percent = int(node.get('percent'))/100
		
		# get animation parameters
		node = xml.find('animation')
		self.start = node.get('start', self.start)
		if self.start is not None:
			self.start = int(self.start)
		self.end = node.get('end', self.end)
		if self.end is not None:
			self.end = int(self.end)
		self.fps = int(node.get('fps'))
		self.startEndCheck()
		
		# get engine value
		node = xml.find('engine')
		self.renderingEngine = node.get('value')
		
		# get cycles parameters
		node = xml.find('cycles').find('cpu')
		self.tilesCyclesCPUX = int(node.get('x'))
		self.tilesCyclesCPUY = int(node.get('y'))
		node = xml.find('cycles').find('gpu')
		self.tilesCyclesGPUX = int(node.get('x'))
		self.tilesCyclesGPUY = int(node.get('y'))
		self.renderingDevice = xml.find('cycles').find('device').get('value')
		node = xml.find('cycles').find('film')
		self.filmExposure = node.get('exposure') in ['true', 'True']
		self.filmTransparentEnable = node.get('transparent') in ['true', 'True']
		
		# get cycles Ligth Path parameters
		node = xml.find('cycles').find('bouncesSet')
		self.transparencyMaxBounces = int(node.find('transparency').get('max'))
		self.transparencyMinBounces = int(node.find('transparency').get('min'))
		self.bouncesMax = int(node.find('bounces').get('max'))
		self.bouncesMin = int(node.find('bounces').get('min'))
		self.diffuseBounces = int(node.find('diffuse').get('bounces'))
		self.glossyBounces = int(node.find('glossy').get('bounces'))
		self.transmissionBounces = int(node.find('transmission').get('bounces'))
		self.volumeBounces = int(node.find('volume').get('bounces'))
		
		# get Blender Internal parameters
		node = xml.find('blenderInternal')
		self.tilesBIX = int(node.get('x'))
		self.tilesBIY = int(node.get('y'))
		
		# get others parameters
		self.compositingEnable = xml.find('compositing').get('enable') in ['true', 'True']
		node = xml.find('simplify')
		if node is None:
			self.simplify = None
		else:
			self.simplify = int(node.get('subdiv'))
		
		# get renderlayers liste and parameters if there is some
		node = xml.find('renderLayerList')
		self.renderLayerList = []
		if node is not None:
			for layer in node.findall('layer'):
				self.renderLayerList.append({
						'name' : layer.get('name'),
						'z' : layer.get('z') in ['true', 'True'],
						'object index' : layer.get('objIndex') in ['true', 'True'],
						'use' : layer.get('render') in ['true', 'True']
						})
		
		# get background parameters
		node = xml.find('renderLayerPreferences').find('background')
		self.backgroundCyclesSamples = int(node.get('sample'))
		self.backgroundAnimation = int(node.get('frame'))
		self.backgroundLayersKeywords = []
		for key in node.findall('keywords'):
			self.backgroundLayersKeywords.append(key.get('value'))
		
		
		# get foreground parameters
		node = xml.find('renderLayerPreferences').find('foreground')
		self.foregroundCyclesSamples = int(node.get('sample'))
		self.foregroundAnimation = int(node.get('frame'))
		self.foregroundLayersKeywords = []
		for key in node.findall('keywords'):
			self.foregroundLayersKeywords.append(key.get('value'))
		
		# get main animation parameters
		node = xml.find('renderLayerPreferences').find('main')
		self.mainAnimationCyclesSamples = int(node.get('sample'))
		self.zPass = node.get('zPass') in ['true', 'True']
		self.objectIndexPass = node.get('objectIndexPass') in ['true', 'True']
		
		
		# output parameters
		node = xml.find('output')
		self.outputFormat = node.get('format')
		self.outputPath = node.get('mainpath', self.outputPath)
		self.outputSubPath = node.get('subpath')
		self.outputName = node.get('name')
		
		# blender absolute path
		self.blenderPath = xml.find('blender').get('path')
		
	
	
	
	
	
	
	def startEndCheck(self):
		'''make sure that that start frame and end frame are all set or all None'''
		if self.start is None and self.end is not None:
			self.start = self.end
		elif self.start is not None and self.end is None:
			self.end = self.start
			
	
	
	
	
	
	def toXmlStr(self, head=False, root=False):
		'''export settings to an xml syntaxe string'''
		txt= ''
		
		if head:
			txt += '<?xml version="1.0" encoding="UTF-8"?>\n'
		
		if root:
			txt += '<settings>\n'
			
		#export resolution parameters
		txt += '\t<resolution x="'+str(self.x)+'" y="'+str(self.y)+'" percent="'+str(int(self.percent*100))+'" />\n'
		
		#export animation parameters depending of settings type
		if self.start is None or self.end is None:
			txt+= '\t<animation fps="'+str(self.fps)+'" />\n'
		else:
			txt+= '\t<animation start="'+str(self.start)+'" end="'+str(self.end)+'" fps="'+str(self.fps)+'" />\n'
		
		
		txt += '\t<engine value="'+self.renderingEngine+'"/>\n'
		
		
		txt += '\t<cycles>\n'
		txt += '\t\t<cpu x="'+str(self.tilesCyclesCPUX)+'" y="'+str(self.tilesCyclesCPUY)+'"/>\n'
		txt += '\t\t<gpu x="'+str(self.tilesCyclesGPUX)+'" y="'+str(self.tilesCyclesGPUY)+'"/>\n'
		txt += '\t\t<device value="'+self.renderingDevice+'"/>\n'
		txt += '\t\t<film exposure="'+str(self.filmExposure)+'" transparent="'+str(self.filmTransparentEnable)+'" />\n'
		
		
		txt += '\t\t<bouncesSet>\n'
		txt += '\t\t\t<transparency min="'+str(self.transparencyMaxBounces)+'" max="'+str(self.transparencyMinBounces)+'" />\n'
		txt += '\t\t\t<bounces min="'+str(self.bouncesMax)+'" max="'+str(self.bouncesMin)+'" />\n'
		txt += '\t\t\t<diffuse bounces="'+str(self.diffuseBounces)+'" />\n'
		txt += '\t\t\t<glossy bounces="'+str(self.glossyBounces)+'" />\n'
		txt += '\t\t\t<transmission bounces="'+str(self.transmissionBounces)+'" />\n'
		txt += '\t\t\t<volume bounces="'+str(self.volumeBounces)+'" />\n'
		txt += '\t\t</bouncesSet>\n'
		
		
		
		txt += '\t</cycles>\n'
		
		
		txt += '\t<blenderInternal x="'+str(self.tilesBIX)+'" y="'+str(self.tilesBIY)+'" />\n'

		txt += '\t<compositing enable="'+str(self.compositingEnable)+'" />\n'
		
		if self.simplify is not None:
			txt += '\t<simplify subdiv="'+str(self.simplify)+'" />\n'
		
		
		
		if len(self.renderLayerList)>0:
			txt += '\t<renderLayerList>\n'
			for layer in self.renderLayerList:
				txt += '\t\t<layer name="'+layer['name']+'" z="'+str(layer['z'])+'" objIndex="'+str(layer['object index'])+'" render="'+str(layer['use'])+'"/>\n'
			txt += '\t</renderLayerList>\n'
		
		txt += '\t<renderLayerPreferences>\n'
		
		txt += '\t\t<background sample="'+str(self.backgroundCyclesSamples)+'" frame="'+str(self.backgroundAnimation)+'" >\n'
		for key in self.backgroundLayersKeywords:
			txt += '\t\t\t<keywords value="'+key+'" />\n'
		txt += '\t\t</background>\n'
		
		txt += '\t\t<foreground sample="'+str(self.foregroundCyclesSamples)+'" frame="'+str(self.foregroundAnimation)+'" >\n'
		for key in self.foregroundLayersKeywords:
			txt += '\t\t\t<keywords value="'+key+'" />\n'
		txt += '\t\t</foreground>\n'
		
		txt += '\t\t<main sample="'+str(self.mainAnimationCyclesSamples)+'" zPass="'+str(self.zPass)+'" objectIndexPass="'+str(self.objectIndexPass)+'" />\n'
		
		txt += '\t</renderLayerPreferences>\n'
		
		
		
		txt += '\t<output format="'+self.outputFormat+'" '
		if self.outputPath is not None:
			txt += 'mainpath="'+self.outputPath+'" '
		txt += 'subpath="'+self.outputSubPath+'" name="'+self.outputName+'" />\n'
		
		txt += '\t<blender path="'+self.blenderPath+'" />\n'
		
		if root:
			txt += '</settings>'
		return txt
	
	
	
	
	
	def printPreferences(self):
		'''print settings like preferences settings'''
		enable = {True:'enabled', False:'Disabled'}
		
		print('Blender path : '+self.blenderPath+'\n')
		
		
		print('Résolution : '+str(self.x)+'x'+str(self.y)+' (@'+str(int(self.percent*100))+'%)\n')
		
		# print Cycles sampling parameters
		print('Cycles samples :')
		print('\tmain : '+str(self.mainAnimationCyclesSamples))
		print('\tbackground : '+str(self.backgroundCyclesSamples))
		print('\tforeground : '+str(self.foregroundCyclesSamples)+'\n')
		
		
		print('Animation : '+str(self.fps)+'fps')
		print('Engine : '+self.renderingEngine.lower()+'('+self.renderingDevice+')\n')
		
		# print output parameters
		print('Output : ')
		print('\toutput path (absolute) : '+str(self.outputPath))
		print('\tautomatique subpath (for each task) : '+self.outputSubPath)
		print('\tname : '+self.outputName)
		print('\tformat : '+self.outputFormat+'\n')
		
		
		# print Tiles parameters
		print('Tiles : ')
		print('\tcycles GPU : '+str(self.tilesCyclesGPUX)+'x'+str(self.tilesCyclesGPUY))
		print('\tcycles CPU : '+str(self.tilesCyclesCPUX)+'x'+str(self.tilesCyclesCPUY))
		print('\tblender internal : '+str(self.tilesBIX)+'x'+str(self.tilesBIY)+'\n')
		
		
		# print Ligth path parameters
		print('Ligth path : ')
		print('\tbounces : '+str(self.bouncesMin)+'to'+str(self.bouncesMax))
		print('\ttransparency : '+str(self.transparencyMinBounces)+'to'+str(self.transparencyMaxBounces))
		print('\tdiffuse : '+str(self.diffuseBounces))
		print('\tglossy : '+str(self.glossyBounces))
		print('\ttransmission : '+str(self.transmissionBounces))
		print('\tvolume : '+str(self.volumeBounces)+'\n')
		
		
		# print others parameters
		print('OPtions :')
		print('\tz pass : '+enable[self.zPass])
		print('\tobject index pass : '+enable[self.objectIndexPass])
		print('\tcompositing : '+enable[self.compositingEnable])
		print('\texposure (cycles) : '+str(self.filmExposure))
		print('\ttransparent background : '+enable[self.filmTransparentEnable])
		if self.simplify is None:
			print('\tsimplify : Disabled\n')
		else:
			print('\tsimplify : '+str(self.simplify)+'\n')
		
		print('Keywords :')
		print('\tbackground : '+' | '.join(self.backgroundLayersKeywords))
		print('\tforeground : '+' | '.join(self.foregroundLayersKeywords)+'\n')
		
	
	
	
	
	
	def getClone(self):
		'''create another settings object with the same attribut values
		restart/end attributes value with start/end argument values if set'''
		
		return setting( xmlMod.fromstring( self.toXmlStr( True ) ) )
		
		



