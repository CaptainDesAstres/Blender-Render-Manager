#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage preset list'''
import xml.etree.ElementTree as xmlMod
from settingMod.Preset import *
import os

class PresetList:
	'''class to manage preset list'''
	
	
	def __init__(self, xml= None):
		'''initialize preset list with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize preset list with default value'''
		self.presets = {'Factory Preset':Preset()}
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize preset list with values extracted from an xml object'''
		self.presets = {}
		for node in xml.findall('preset'):
			self.presets[node.get('alias')] = Preset(node)
	
	
	
	
	
	def toXml(self):
		'''export preset list into xml syntaxed string'''
		txt = '<presetList>\n'
		presets = self.presets.keys()
		for p in presets:
			txt += self.presets[p].toXml(p)
		txt += '</presetList>\n'
		return txt
	
	
	
	
	
	def see(self, log, versions):
		'''menu to explore and edit preset list settings'''
		change = False
		log.menuIn('Preferences Preset/Metapreset')
		
		while True:
			os.system('clear')
			log.print()
			
			print('''\n\n        Menu :
1- Manage Preset
2- Manage Metapreset
3- choose Default Preset/Metapreset
0- Save and quit

''')
			
			choice = input('Action?').strip().lower()
			
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			elif choice == '1':
				change = (self.presetMenu(log) or change)
			elif choice == '2':
				change = (self.metapresetMenu(log) or change)
			elif choice == '3':
				change = (self.chooseDefault(log) or change)
			else:
				log.error('Unvalid menu choice', False)
		
	
	
	
	
	
	def presetsList(self, index = False):
		'''A method to list preset'''
		keys = list(self.presets.keys())
		keys.sort(key = str.lower)
		
		if index:
			for i,k in enumerate(keys):
				print(str(i)+'- '+k)
		else:
			for k in keys:
				print(k)
		
		return keys
	
	
	
	
	
	def presetMenu(self, log):
		'''A method to manage preset list'''
		print('not yet implement')
		input('press enter to continue')
	
	
	
	
	
	def metapresetMenu(self, log):
		'''A method to manage metapreset list'''
		print('not yet implement')
		input('press enter to continue')
	
	
	
	
	
	def chooseDefault(self, log):
		'''A method to choose the default preset or metapreset'''
		print('not yet implement')
		input('press enter to continue')
	
	
	
	
	
	
	
	
	
	
	
	
	
	
