#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage preferences of the script'''
import xml.etree.ElementTree as xmlMod
from settingMod.VersionList import *
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
		
		self.blenderVersionList = VersionList()
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize preferences object with values extracted from an xml object'''
		
		self.blenderVersionList = VersionList( xml.find('versionsList') )
		
	
	
	
	
	
	def toXml(self):
		'''export preferences settings into xml syntaxed string'''
		xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
		
		xml += '<preferences>\n'
		
		# export blender version list
		xml += self.blenderVersionList.toXml()
		
		xml += '</preferences>\n'
		
		return xml
	
	
	
	
	
	def see(self, log):
		'''method to see preferences settings and access edition menu'''
		change = False
		log.menuIn('Preferences')
		
		while True:
			#print log and preferences
			os.system('clear')
			log.print()
			print('''    Preferences\n
1- Blender versions
0- Save and quit''')
			
			
		
			#treat available actions
			choice= input('menu?').strip().lower()
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()# quit preferences menu
				return change
			elif choice == '1':
				change = (self.blenderVersionList.see(log) or change)
			else:
				log.write('\033[31munknow request\033[0m\n')
	
	
	
	
	
	
	
	
	
	
	
