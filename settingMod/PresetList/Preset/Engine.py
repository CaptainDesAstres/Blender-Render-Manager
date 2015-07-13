#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage Engine Settings'''
import xml.etree.ElementTree as xmlMod
import os

class Engine:
	'''class to manage Engine Settings'''
	
	
	def __init__(self, xml= None):
		'''initialize Engine Settings with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize Engine Settings with default value'''
		self.version = '[default]'
		self.engine = 'CYCLES'
		self.device = 'GPU'
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize Engine Settings with values extracted from an xml object'''
		self.version = xml.get('version')
		self.engine = xml.get('engine')
		self.device = xml.get('device')
	
	
	
	
	
	
	def toXml(self):
		'''export Engine Settings into xml syntaxed string'''
		return '<engine version="'+self.version\
					+'" engine="'+self.engine\
					+'" device="'+self.device+'" />\n'
		
	
	
	
	
	
	def menu(self, log, versions):
		'''menu to explore and edit Engine Settings settings'''
		change = False
		log.menuIn('Engine')
		
		while True:
			
			log.print()
			
			self.print()
			
			print('''\n\n        Menu :
1- Edit Blender Version
2- Switch Engine
3- Switch Device (for Cycles)
0- Quit

''')
			
			choice = input('Action?').strip().lower()
			
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			elif choice == '1':
				change = (self.chooseVersion(log, versions) or change)
			elif choice in ['2', '3']:
				self.switch(log, choice == '2')
				change = True
			else:
				log.error('Unvalid menu choice', False)
		
	
	
	
	
	
	def print(self):
		'''a method to print Engine Settings'''
		print('Blender Version :       '+self.version)
		print('Engine :                '+self.engine.capitalize())
		print('Cycles Device :         '+self.device)
	
	
	
	
	
	def chooseVersion(self, log, versions):
		'''A method to set the blender version to use with a preset'''
		choice = versions.choose(log, True, True)
		
		if choice is not None:
			self.version = choice
			log.write('Version set to : '+self.version)
			return True
		return False
	
	
	
	
	
	def switch(self, log, engine):
		'''A method to switch between available settings for engine and device'''
		
		if engine:
			# switch engine
			if self.engine == 'CYCLES':
				self.engine = 'BLENDER_RENDER'
			else:
				self.engine = 'CYCLES'
			log.write('Engine set to '+self.engine)
		else:
			# switch device
			if self.device == 'GPU':
				self.device = 'CPU'
			else:
				self.device = 'GPU'
			log.write('Cycles rendering device set to '+self.device)
			
	
	
	
	
	
	def renameBlenderVersion(self, old, new):
		'''rename a blender Version if used'''
		if self.version == old:
			self.version = new
	
	
	
	
	
	
	
	
	
