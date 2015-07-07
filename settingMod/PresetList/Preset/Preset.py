#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage preset'''
import xml.etree.ElementTree as xmlMod
from usefullFunctions import *
from settingMod.PresetList.Preset.Quality import *
from settingMod.PresetList.Preset.BounceSet import *
from settingMod.PresetList.Preset.Engine import *
from settingMod.PresetList.Preset.Options import *
import os

class Preset:
	'''class to manage preset'''
	
	anim = [
			'[On Demand]',
			'All Animation',
			'Fix (First Frame)',
			'Loop 1',
			'Loop 2',
			'Loop 3',
			'Loop 4',
			'Loop 5'
			]
	
	def __init__(self, xml= None):
		'''initialize preset with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize preset with default value'''
		self.animation = 1
		self.quality = Quality()
		self.bounce = BounceSet()
		self.engine = Engine()
		self.options = Options()
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize preset with values extracted from an xml object'''
		self.animation = int(xml.get('animation'))
		self.quality = Quality(xml.find('quality'))
		self.bounce = BounceSet(xml.find('bounceSet'))
		self.engine = Engine(xml.find('engine'))
		self.options = Options(xml.find('options'))
	
	
	
	
	
	def toXml(self, alias):
		'''export preset into xml syntaxed string'''
		txt = '<preset animation="'+str(self.animation)+'" alias="'+alias+'" >\n'
		
		txt += self.quality.toXml()
		
		txt += self.bounce.toXml()
		
		txt += self.engine.toXml()
		
		txt += self.options.toXml()
		
		txt += '</preset>\n'
		return txt
	
	
	
	
	
	def see(self, log, alias, versions):
		'''menu to explore and edit preset settings'''
		change = False
		log.menuIn(alias+' Preset')
		
		while True:
			
			log.print()
			
			self.print()
			
			print('''\n\n        Menu :
1- Edit Quality Settings
2- Edit Bounces Settings (Cycles)
3- Edit Rendering Options
4- Edit Animation Setting
9- Edit Engine Settings
0- Save and quit

''')
			
			choice = input('Action?').strip().lower()
			
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			elif choice == '1':
				change = (self.quality.see(log) or change)
			elif choice == '2':
				change = (self.bounce.see(log) or change)
			elif choice == '3':
				change = (self.options.see(log) or change)
			elif choice == '4':
				change = (self.editAnimation(log) or change)
			elif choice == '9':
				change = (self.engine.see(log, versions) or change)
			else:
				log.error('Unvalid menu choice', False)
		
	
	
	
	
	
	def print(self):
		'''a method to print preset'''
		self.quality.print()
		print('Animation :             '+Preset.anim[self.animation])
		print()
		self.bounce.print()
		print()
		self.options.print()
		print()
		self.engine.print()
	
	
	
	
	
	def editAnimation(self, log):
		'''A method to edit animation settings'''
		log.menuIn('Edit Animation Setting')
		
		while True:
			
			log.print()
			
			print('\n\n        Edit Animation Setting :\n\n')
			print('Current setting : '+Preset.anim[self.animation]+'\n\n    Menu :')
			indexPrintList(Preset.anim)
			choice = input('New animation settings (h for help) : ').strip().lower()
			
			if choice in ['', 'q', 'quit', 'cancel']:
				log.menuOut()
				return False
			elif choice in ['h', 'help']:
				# print help
				log.menuIn('Edit Animation Setting')
				
				log.print()
				print('''\n\n        HELP :
[On Demand]       : Animation length will be asked for each file
All Animation     : Animation length will correspond to file animation length
Fix (First Frame) : Only the first frame will be render (for fixe background)
Loop 1 to 5       : Animation length will correspond to loop length of the loopset of the file or of the metapreset

''')
				input('Press enter to continue…')
				log.menuOut()
				continue
			
			try:
				choice = int(choice)
			except ValueError:
				log.error('unvalid settings, integer expected!')
				continue
			
			if choice < 0 or choice >= len(Preset.anim):
				log.error('Choice out of available option range!')
				continue
			
			self.animation = choice
			log.write('Animation set to : '+Preset.anim[self.animation])
			log.menuOut()
			return True
	
	
	
	
	
	def copy(self):
		'''A method to get a copy of current object'''
		xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
		xml += self.toXml('')
		xml = xmlMod.fromstring(xml)
		return Preset(xml)
		
	
	
	
	
	
	
