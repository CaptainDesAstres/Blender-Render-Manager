#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module containing class 'renderingTask' '''
from setting import setting
from copy import deepcopy

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
			
			# get parameters values that only original file settings have
			self.customSetting.start = self.fileSetting.start
			self.customSetting.end = self.fileSetting.end
			self.customSetting.renderLayerList = deepcopy(self.fileSetting.renderLayerList)
			
			#overwrite renderlayer pass settings
			for layer in self.customSetting.renderLayerList:
				layer['z'] = self.customSetting.zPass
				layer['object index'] = self.customSetting.objectIndexPass 
			
			
			self.status = 'ready'
			
		else:
			# load task from xml argument
			self.path = ''
			self.scene = ''
			self.fileSetting = setting()
			self.customSetting = setting()
			self.status='unset'
			
			self.fromXml(xml)
	
	
	
	
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
	
	
	
	
	
	def taskSettingsMenu(self, pref):
		'''method to access customize task settings menu'''
		change = False
		log.menuIn('Compare Task Settings')
		ref = self.fileSetting
		
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
				choice = int(choice)
			except ValueError:
				choice = 9999
			
			if choice == 0:
				log.menuOut()
				log.write('quit\n')
				return change
			elif choice == 1:
				# manually customize task settings
				print('action not yet implement')
			elif choice == 2:
				# change reference  settings for preferences
				print('action not yet implement')
			elif choice == 3:
				# change reference  settings for original blender file settings
				print('action not yet implement')
			elif choice == 4:
				# overwrite task settings with preferences
				print('action not yet implement')
			elif choice == 5:
				# overwrite task settings with original blender file settings
				print('action not yet implement')
			else:
				log.write('unvalid action choice\n')
			







