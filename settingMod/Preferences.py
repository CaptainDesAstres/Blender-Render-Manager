#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage preferences of the script'''
import xml.etree.ElementTree as xmlMod
from settingMod.VersionList import *
from settingMod.Output import *
from settingMod.Tiles import *
from settingMod.PresetList import *
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
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize preferences object with values extracted from an xml object'''
		
		self.blenderVersion = VersionList( xml.find('versionsList') )
		self.output = Output( xml.find('output') )
		self.tiles = Tiles(xml.find('tilesSet'))
		self.presets = PresetList(xml.find('presetList'))
	
	
	
	
	
	def toXml(self):
		'''export preferences settings into xml syntaxed string'''
		xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
		
		xml += '<preferences>\n'
		
		# export blender version list
		xml += self.blenderVersion.toXml()
		
		# export output path
		xml+= self.output.toXml()
		
		# export tiles sizes
		xml+= self.tiles.toXml()
		
		# export preset settings
		xml+= self.presets.toXml()
		
		xml += '</preferences>\n'
		
		return xml
	
	
	
	
	
	def see(self, log):
		'''method to see preferences settings and access edition menu'''
		change = False
		log.menuIn('Preferences')
		
		while True:
			#print log and preferences
			
			log.print()
			print('''\n    \033[4mPreferences Menu :\033[0m
1- Blender versions
2- Output Path
3- Tiles
4- Presets
0- Save and quit

''')
			
			
		
			#treat available actions
			choice= input('menu?').strip().lower()
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()# quit preferences menu
				return change
			elif choice == '1':
				change = (self.blenderVersion.see(log) or change)
			elif choice == '2':
				change = (self.output.see(log) or change)
			elif choice == '3':
				change = (self.tiles.see(log) or change)
			elif choice == '4':
				change = (self.presets.see(log, self.blenderVersion) or change)
			else:
				log.error('Unknow request!', False)
	
	
	
	
	
	
	
	
	
	
	
