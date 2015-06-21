#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module containing class 'renderingTask' '''
from setting import setting
from copy import deepcopy
import os

class renderingTask:
	'''class that contain the parameter for a rendering task'''
	
	def __init__(self,
					path = '', 
					scene = '', 
					fileXmlSetting = setting(),
					preferences = setting(),
					xml = None):
		'''renderingTask object initialisation
		if there is an xml argument paste to the function, the others are ignore'''
		if xml is None:
			# create new task with path, scene, fileXmlSetting and preferences arguments
			self.path = path
			self.scene = scene
			self.fileSetting = setting(fileXmlSetting)
			self.customSetting = preferences.getClone()
			
			# check task specific parameters
			self.checkSpecificSettings()
			
			
			self.status = 'ready'
			
		else:
			# load task from xml argument
			self.path = ''
			self.scene = ''
			self.fileSetting = setting()
			self.customSetting = setting()
			self.status='unset'
			
			self.fromXml(xml)
	
	
	
	
	
	def checkSpecificSettings(self):
		'''check if task setting have settings for the parameter that is not in global preferences (start/end frame and renderlayer list) '''
		# get parameters values that only original file settings have
		if self.customSetting.start is None:
			self.customSetting.start = self.fileSetting.start
		
		if self.customSetting.end is None:
			self.customSetting.end = self.fileSetting.end
		
		if len(self.customSetting.renderLayerList) == 0:
			self.customSetting.renderLayerList = deepcopy(self.fileSetting.renderLayerList)
			#overwrite renderlayer pass settings
			for layer in self.customSetting.renderLayerList:
				layer['z'] = self.customSetting.zPass
				layer['object index'] = self.customSetting.objectIndexPass 
	
	
	
	
	
	def fromXml(self,xml):
		'''method that set the object attributes with the value extracted from an xml object with 'task' tag name '''
		if xml.tag == 'task':
			self.path = xml.get('path')
			self.scene = xml.get('scene')
			self.fileSetting.fromXml(xml.find('fileSet'))
			self.customSetting.fromXml(xml.find('taskSet'))
			self.status = 'ready'
	
	
	
	
	
	def toXmlStr(self,head=False):
		'''export the object values into an xml formated strings'''
		txt =''
		if head:
			txt+= '<?xml version="1.0" encoding="UTF-8"?>\n'
		txt += '<task path="'+self.path+'" scene="'+self.scene+'">\n'
		txt += '<taskSet>\n'+self.customSetting.toXmlStr()+'</taskSet>\n'
		txt += '<fileSet>\n'+self.fileSetting.toXmlStr()+'</fileSet>\n'
		txt += '</task>\n'
		return txt
	
	
	
	
	
	def settingsCompare(self, ref = None):
		'''method to comapare task settings to original file settings or to other settings'''
		if ref is None:
			ref = self.fileSetting
		return self.customSetting.compare(ref)
	
	
	
	
	
	def printCompare(self, ref):
		'''method to print the task custom settings compared to another settings'''
		
		def getValue(attr, xy = False, to = False, frame = False,\
						 custom = self.customSetting, ref = ref):
			enable = {True:'Enabled', False:'Disabled'}
			
			if attr == 'renderLayerList':
				out = 'name => z pass => object index Pass => layer activated\n'
				for i, layerCus in enumerate(getattr(custom, attr)):
					layerRef = getattr(ref, attr)[i]
					
					out += layerCus['name']
					for key in ['z', 'object index', 'use']:
						if layerCus[key] == layerRef[key]:
							out += ' => \033[32m'
						else:
							out += ' => \033[31m'
						out += enable[layerCus[key]]+'\033[0m'
					out += '\n'
				return out
				
			if xy or to or frame:
				if xy :
					sep = 'x'
					first = 'X'
					last = 'Y'
				elif to:
					sep = ' to '
					first = 'Min'
					last = 'Max'
				elif frame:
					sep = ' to '
					first = 'start'
					last = 'end'
				cusVal = str(getattr(custom, attr+first))+sep+str(getattr(custom, attr+last))
				refVal = str(getattr(ref, attr+first))+sep+str(getattr(ref, attr+last))
			elif attr in ['backgroundLayersKeywords', 'foregroundLayersKeywords']:
				cusVal = ' | '.join(getattr(custom, attr))
				refVal = ' | '.join(getattr(ref, attr))
			else:
				cusVal = getattr(custom, attr)
				refVal = getattr(ref, attr)
				
				if attr == 'percent':
					cusVal *= 100
					refVal *= 100
				
				if type(cusVal) == type(True):
					cusVal = enable[cusVal]
				elif cusVal is None:
					cusVal = 'Disabled'
				else:
					cusVal = str(cusVal)
				
				if type(refVal) == type(True):
					refVal = enable[refVal]
				elif refVal is None:
					refVal = 'Disabled'
				else:
					refVal = str(refVal)
			
			if cusVal == refVal:
				return '\033[32m'+cusVal+'\033[0m'
			else:
				if cusVal in enable.values() and refVal in enable.values():
					return '\033[31m'+cusVal+'\033[0m'
				else:
					return '\033[31m'+cusVal+' ('\
					+refVal+')\033[0m'
		
		
		print('Blender path :        '+getValue('blenderPath')+'\n')
		
		# print resolution parameters
		print('Résolution :           '+getValue('',xy = True)+' (@'+getValue('percent')+'%)')
		
		# print Cycles sampling parameters
		print('Cycles samples :')
		print('  main / background / foreground : \n                       '\
				+getValue('mainAnimationCyclesSamples')+' / '\
				+getValue('backgroundCyclesSamples')+' / '\
				+getValue('foregroundCyclesSamples'))
		
		# print animation and engine parameters
		print('Animation :            '+getValue('',frame = True)+' ('+getValue('fps')+'fps)')
		print('background animation : '+getValue('backgroundAnimation')+' frames')
		print('foreground animation : '+getValue('foregroundAnimation')+' frames')
		print('Engine :               '+getValue('renderingEngine').lower()\
							+'('+getValue('renderingDevice')+')\n')
		
		# print output parameters
		print('Output : ')
		print('  output path (absolute) :                    '+getValue('outputPath'))
		print('  automatique subpath (for each task) :       '+getValue('outputSubPath'))
		print('  name :                                      '+getValue('outputName'))
		print('  format :                                    '+getValue('outputFormat')+'\n')
		
		
		# print Tiles parameters
		print('Tiles : ')
		print('  cycles GPU :             '+getValue('tilesCyclesGPU', xy = True))
		print('  cycles CPU :             '+getValue('tilesCyclesCPU', xy = True))
		print('  blender internal :       '+getValue('tilesBI', xy = True))
		
		
		# print Ligth path parameters
		print('Ligth path : ')
		print('  bounces :                '+getValue('bounces', to = True))
		print('  transparency :           '+getValue('transparencyBounces', to = True))
		print('  diffuse / glossy / transmission / volume : \n                           '\
				+getValue('diffuseBounces')+' / '+getValue('glossyBounces')+' / '\
				+getValue('transmissionBounces')+' / '+getValue('volumeBounces')+'\n')
		
		
		# print others parameters
		print('OPtions :')
		print('  z pass :                       '+getValue('zPass'))
		print('  object index pass :            '+getValue('objectIndexPass'))
		print('  compositing :                  '+getValue('compositingEnable'))
		print('  exposure (cycles) :            '+getValue('filmExposure'))
		print('  transparent background :       '+getValue('filmTransparentEnable'))
		print('  simplify :                     '+getValue('simplify')+'\n')
		
		print('Keywords :')
		print('  background : '+getValue('backgroundLayersKeywords'))
		print('  foreground : '+getValue('foregroundLayersKeywords')+'\n')
		
		print('Renderlayer List : ')
		print(getValue('renderLayerList'))
	
	
	
	
	
	def taskSettingsMenu(self, log, pref):
		'''method to access customize task settings menu'''
		change = False
		log.menuIn('Compare Task Settings')
		ref = self.fileSetting
		
		red = '\033[31m'
		rest = '\033[0m'
		green = '\033[32m'
		
		while True:
			os.system('clear')
			log.write('Task settings menu : ')
			log.print()
			
			self.printCompare(ref)
			
			choice = input('''Available Action:
1- manually customize task settings
2- compare task settings to preferences
3- compare task settings to original blender file settings
4- overwrite task settings with preferences
5- overwrite task settings with original blender file settings
0- save & quit
action?''').strip()
			
			try:
				if choice in ['q', 'Q', 'cancel', 'CANCEL']:
					choice = 0
				else:
					choice = int(choice)
			except ValueError:
				choice = 9999
			
			if choice == 0:
				log.menuOut()
				log.write(red+'quit\n'+rest)
				return change
			elif choice == 1:
				# manually customize task settings
				self.customSetting.edit(log, True)
			elif choice == 2:
				# change reference settings for preferences
				ref = pref
				log.write(green+'switch references settings to preference\n'+rest)
			elif choice == 3:
				# change reference settings for original blender file settings
				ref = self.fileSetting
				log.write(green+'switch references settings to original file settings\n'+rest)
			elif choice == 4:
				# overwrite task settings with preferences
				os.system('clear')
				log.menuIn('Overwrite With Preference Settings')
				log.write('overwrite with preference settings : ')
				log.print()
				
				confirm = input('do you realy want to overwrite current task settings with global preference settings? (y)').strip().lower()
				
				if confirm in ['y', 'yes']:
					self.customSetting = pref.getClone()
					self.checkSpecificSettings()
					log.write(green+'confirmed\n'+rest)
				else:
					log.write(red+'canceled\n'+rest)
				
				log.menuOut()
				
			elif choice == 5:
				# overwrite task settings with original blender file settings
				os.system('clear')
				log.menuIn('Overwrite With Original Blender File Settings')
				log.write('overwrite with original Blender file settings : ')
				log.print()
				
				confirm = input('do you realy want to overwrite current task settings with the original settings of the plender file (and ignore the preferences)? (y)').strip().lower()
				
				if confirm in ['y', 'yes']:
					self.customSetting = self.fileSetting.getClone()
					self.customSetting.blenderPath = pref.blenderPath
					self.customSetting.backgroundLayersKeywords = pref.backgroundLayersKeywords[:]
					self.customSetting.foregroundLayersKeywords = pref.foregroundLayersKeywords[:]
					log.write(green+'confirmed\n'+rest)
				else:
					log.write(red+'canceled\n'+rest)
				
				log.menuOut()
				
			else:
				log.write(red+'unvalid action choice\n'+rest)
			







