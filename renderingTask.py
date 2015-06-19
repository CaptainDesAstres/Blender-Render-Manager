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
				log.write(red+'manually customize task settings : action not yet implement\n'+rest)
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
			







