#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module containing 'preset' class'''
import xml.etree.ElementTree as xmlMod
import os, re

class preset:
	'''class of object representing a preset for rendering task'''
	
	
	def __init__(self, xml= None):
		'''initialize preset object with default value or values extracted from an xml object'''
		# default values of all the attributes
		# animation and resolution attributes
		self.X = 1920
		self.Y = 1080
		self.percent = 1
		self.fps = 30
		self.animation = 0
		
		# rendering engine and output attributes
		self.blender = 'blender'
		self.renderingDevice = 'GPU'
		self.renderingEngine = 'CYCLES'
		self.cyclesSamples = 1500
		self.outputFormat = 'OPEN_EXR_MULTILAYER'
		
		
		# rendering options attributes
		self.zPass = True
		self.objectIndexPass = True
		self.compositingEnable = True
		self.filmExposure = 1
		self.filmTransparentEnable = True
		self.simplify = None
		
		
		# Light Path attributes
		self.transparencyBouncesMin = 4
		self.transparencyBouncesMax = 6
		self.bouncesMin = 3
		self.bouncesMax = 8
		self.diffuseBounces = 4
		self.glossyBounces = 4
		self.transmissionBounces = 12
		self.volumeBounces = 0
		
		if xml is not None:
			self.fromXml(xml)
	
	
	
	
	
	
	def fromXml(self,xml):
		'''extract preset parameters from an xml object'''
		
		# blender version to use
		self.blender = xml.find('blender').get('version')
		
		# get rendering resolution parameters 
		node = xml.find('resolution')
		self.X = int(node.get('x'))
		self.Y = int(node.get('y'))
		self.percent = int(node.get('percent'))/100
		self.outputFormat = node.get('format')
		
		# get animation parameters
		node = xml.find('animation')
		self.fps = int(node.get('fps'))
		self.animation = int(node.get('duration'))
		
		# get engine parameters
		node = xml.find('engine')
		self.renderingEngine = node.get('value')
		
		# get Cycles parameters
		self.cyclesSamples = xml.find('cycles').get('samples')
		self.renderingDevice = xml.find('cycles').find('device').get('value')
		node = xml.find('cycles').find('film')
		self.filmExposure = float(node.get('exposure'))
		self.filmTransparentEnable = node.get('transparent') in ['true', 'True']
		
		# get Cycles Ligth Path parameters
		node = xml.find('cycles').find('bouncesSet')
		self.transparencyBouncesMax = int(node.find('transparency').get('max'))
		self.transparencyBouncesMin = int(node.find('transparency').get('min'))
		self.bouncesMax = int(node.find('bounces').get('max'))
		self.bouncesMin = int(node.find('bounces').get('min'))
		self.diffuseBounces = int(node.find('diffuse').get('bounces'))
		self.glossyBounces = int(node.find('glossy').get('bounces'))
		self.transmissionBounces = int(node.find('transmission').get('bounces'))
		self.volumeBounces = int(node.find('volume').get('bounces'))
		
		# get others parameters
		self.compositingEnable = xml.find('compositing').get('enable') in ['true', 'True']
		
		node = xml.find('simplify')
		if node is None:
			self.simplify = None
		else:
			self.simplify = int(node.get('subdiv'))
		
		node = xml.find('pass')
		self.zPass = node.get('zPass') in ['true', 'True']
		self.objectIndexPass = node.get('objectIndexPass') in ['true', 'True']
		
		
		
	
	
	
	
	
	
	def toXmlStr(self, head=False, root=False):
		'''export preset parameters to an xml syntax string'''
		txt= ''
		
		if head:
			txt += '<?xml version="1.0" encoding="UTF-8"?>\n'
		
		if root:
			txt += '<settings>\n'
		
		txt += '  <blender version="'+self.blender+'" />\n'
		
		# export resolution parameters
		txt += '  <resolution x="'+str(self.X)+'" y="'+str(self.Y)+'" percent="'+str(int(self.percent*100))+'" format="'+self.outputFormat+'" />\n'
		
		# export animation parameters
		txt+= '  <animation fps="'+str(self.fps)+'" duration="'+str(self.animation)+'" />\n'
		
		
		# export engine parameter
		txt += '  <engine value="'+self.renderingEngine+'"/>\n'
		
		# export Cycles parameters
		txt += '  <cycles samples="'+str(self.cyclesSamples)+'">\n'
		txt += '    <device value="'+self.renderingDevice+'"/>\n'
		txt += '    <film exposure="'+str(self.filmExposure)+'" transparent="'+str(self.filmTransparentEnable)+'" />\n'
		
		
		# export lightpath Cycles specific parameters
		txt += '    <bouncesSet>\n'
		txt += '      <transparency max="'+str(self.transparencyBouncesMax)+'" min="'+str(self.transparencyBouncesMin)+'" />\n'
		txt += '      <bounces max="'+str(self.bouncesMax)+'" min="'+str(self.bouncesMin)+'" />\n'
		txt += '      <diffuse bounces="'+str(self.diffuseBounces)+'" />\n'
		txt += '      <glossy bounces="'+str(self.glossyBounces)+'" />\n'
		txt += '      <transmission bounces="'+str(self.transmissionBounces)+'" />\n'
		txt += '      <volume bounces="'+str(self.volumeBounces)+'" />\n'
		txt += '    </bouncesSet>\n'
		
		txt += '  </cycles>\n'
		
		
		# export rendering options
		txt += '  <compositing enable="'+str(self.compositingEnable)+'" />\n'
		if self.simplify is not None:
			txt += '  <simplify subdiv="'+str(self.simplify)+'" />\n'
		txt += '    <pass z="'+str(self.zPass)+'" objectIndex="'+str(self.objectIndexPass)+'" />\n'
		
		
		if root:
			txt += '</settings>'
		
		return txt
	
	
	
	
	
	def print(self):
		'''print preset parameters'''
		enable = {True:'enabled', False:'Disabled'}
		
		print('Blender version :       '+self.blender+'\n')
		
		# print resolution parameters
		print('Résolution :          '+str(self.X)+'x'+str(self.Y)+' (@'+str(int(self.percent*100))+'%)')
		
		# print Cycles sampling parameters
		print('Cycles samples : '+str(self.cyclesSamples))
		
		# print animation and engine parameters
		print('Animation rate :           '+str(self.fps)+' fps')
		print('Animation duration :           '+str(self.animation)+' frames')
		print('Engine :              '+self.renderingEngine.lower()\
							+'('+self.renderingDevice+')\n')
		
		# print output parameters
		print('Output format :                '+self.outputFormat+'\n')
		
		
		# print Ligth path parameters
		print('Ligth path : ')
		print('  bounces :                '+str(self.bouncesMin)+' to '\
								+str(self.bouncesMax))
		print('  transparency :           '+str(self.transparencyBouncesMin)\
								+' to '+str(self.transparencyBouncesMax))
		print('  diffuse / glossy / transmission / volume : \n                           '\
				+str(self.diffuseBounces)+' / '+str(self.glossyBounces)+' / '\
				+str(self.transmissionBounces)+' / '+str(self.volumeBounces)+'\n')
		
		
		# print others parameters
		print('OPtions :')
		print('  z pass :                       '+enable[self.zPass])
		print('  object index pass :            '+enable[self.objectIndexPass])
		print('  compositing :                  '+enable[self.compositingEnable])
		print('  exposure (cycles) :            '+str(self.filmExposure))
		print('  transparent background :       '+enable[self.filmTransparentEnable])
		if self.simplify is None:
			print('  simplify :                     Disabled\n')
		else:
			print('  simplify :                     '+str(self.simplify)+'\n')
		
		
	
	
	
	
	
	def getClone(self):
		'''create another preset object with the same attribut values'''
		
		return setting( xmlMod.fromstring( self.toXmlStr( head = True, root = True) ) )
	
	
	
	
	
	def see(self, log):
		'''print preset and let edit or reset it'''
		change = False
		log.menuIn('Preset')
		
		while True:
			#print log and preset
			os.system('clear')
			log.print()
			print('    preset\n')
			self.print()
			
			#treat available actions
			choice= input('(e)dit, (r)eset or (q)uit (and save): ').strip()
			if choice in ['Q','q']:
				log.write('quit settings\n')
				log.menuOut()# quit preferences menu
				return change
			elif choice in ['e','E']:
				log.write('\033[31medit preset is not yet implemented\033[0m\n')
			elif choice in ['R','r']:
				#reset default settings
				confirm = input('this action will reset to factory settings. confirm (y):').strip()
				if confirm in ['y','Y']:
					self.__init__()
					change = True
					log.write('reset factory settings\n')
			else:
				log.write('\033[31munknow request\033[0m\n')
	
	
	
	
	
