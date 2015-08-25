#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage preferences of the script'''
import xml.etree.ElementTree as xmlMod
from save import *
from Preferences.VersionList import *
from Preferences.Output import *
from Preferences.Tiles import *
from Preferences.PresetList.PresetList import *
import os

class Preferences:
	'''class dedicated to script preferences settings'''
	
	
	def __init__(self, xml= None):
		'''initialize preferences object with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize preferences object with default value'''
		
		self.blenderVersion = VersionList()
		self.output = Output()
		self.tiles = Tiles()
		self.presets = PresetList()
		self.port = 55814
		self.archiveLimit = 1000
		self.logLimit = 100
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize preferences object with values extracted from an xml object'''
		
		self.blenderVersion = VersionList( xml.find('versionsList') )
		self.output = Output( xml.find('output') )
		self.tiles = Tiles(xml.find('tilesSet'))
		self.presets = PresetList(xml.find('presetList'))
		
		self.port = int(xml.find('port').get('value'))
		self.archiveLimit = int(xml.get('archive'))
		self.logLimit = int(xml.get('log'))
	
	
	
	
	
	def toXml(self, preset = True, head = True):
		'''export preferences settings into xml syntaxed string'''
		xml = ''
		
		if head:
			xml += '<?xml version="1.0" encoding="UTF-8"?>\n'
		
		xml += '<preferences archive="'+str(self.archiveLimit)\
				+'" log="'+str(self.logLimit)+'" >\n'
		
		if preset:
			# export blender version list
			xml += self.blenderVersion.toXml()
		
		# export output path
		xml+= self.output.toXml()
		
		# export tiles sizes
		xml+= self.tiles.toXml()
		
		# export preset settings
		xml+= self.presets.toXml(preset)
		
		xml+= '<port value="'+str(self.port)+'" />'
		
		xml += '</preferences>\n'
		
		return xml
	
	
	
	
	
	def menu(self, log, tasks):
		'''method to see preferences settings and access edition menu'''
		log.menuIn('Preferences')
		change = False
		
		while True:
			log.print()
			self.print()
			
			print('''\n    \033[4mPreferences Menu :\033[0m
1- Blender versions
2- Output Path
3- Tiles
4- Presets
9- Change Net Port
0- Save and quit

''')
			
			
		
			#treat available actions
			choice= input('menu?').strip().lower()
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()# quit preferences menu
				return
			elif choice == '1':
				change = self.blenderVersion.menu(log, self)
			elif choice == '2':
				change = self.output.menu(log)
			elif choice == '3':
				change = self.tiles.menu(log)
			elif choice == '4':
				change = self.presets.menu(log, self.blenderVersion, tasks)
			elif choice == '9':
				change = self.editPort(log)
			else:
				log.error('Unknow request!', False)
			
			if change:
				change = False
				savePreferences(self)
				log.write('New preferences saved')
	
	
	
	
	
	def print(self):
		'''a method to display preferences settings'''
		print('Socket Port : '+str(self.port))
		print('Session Log Limit : '+str(self.logLimit))
		print('Archive Limit : '+str(self.archiveLimit))
	
	
	
	
	
	def editPort(self, log):
		'''A method to change the net port to communicate with blender instance'''
		log.menuIn('Edit Net Port')
		while True:
			log.print()
			
			choice = input('''

        Edit Net Port :

Current port :'''+str(self.port)+'''

Type the wanted port between 1024 and 65535 or q to quit or h for help :''').strip().lower()
			
			if choice in ['q', 'quit', 'cancel']:
				log.menuOut()
				return False
			
			if choice in ['h', 'help']:
				log.menuIn('Help')
				log.print()
				input('''

        Help :
When Blender Render Manager is running blender to render a picture, it communicate with Blender via a web socket to stay informed of the status. This setting is the port that the script use for the socket. be sure to use a port who is not used by another process.

enter to continue
''')
				log.menuOut()
				continue
			
			try:
				choice = int(choice)
			except ValueError:
				log.error('integer value expected!',False)
				continue
			
			if choice < 1024 or choice > 65535:
				log.error('the port value must be between 1024 and 65535!',False)
				continue
			
			self.port = choice
			log.write('the socket port is set to '+str(self.port))
			log.menuOut()
			return True
			
			
			
	
	
	
	
	
	
	
	
	
