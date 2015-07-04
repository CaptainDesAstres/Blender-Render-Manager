#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage Quality settings'''
import xml.etree.ElementTree as xmlMod
from settingMod.Size import *
import os

class Quality:
	'''class to manage Quality settings'''
	
	
	def __init__(self, xml= None):
		'''initialize Quality settings with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize Quality settings with default value'''
		self.pourcent = 100
		self.size = Size('1920x1080')
		self.samples = 1500
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize Quality settings with values extracted from an xml object'''
		node = xml.find('resolution')
		self.pourcent = int(node.get('pourcent'))
		self.size = Size(xml = node)
		self.samples = int(xml.find('samples').get('value'))
	
	
	
	
	
	def toXml(self):
		'''export Quality settings into xml syntaxed string'''
		txt = '<quality>\n'
		txt += '<resolution pourcent="'+str(self.pourcent)+'" '+self.size.toXmlAttr()+' />\n'
		txt += '<samples value="'+str(self.samples)+'" />\n'
		txt += '</quality>\n'
		return txt
	
	
	
	
	
	def see(self, log):
		'''menu to explore and edit Quality settings settings'''
		change = False
		log.menuIn('Quality')
		
		while True:
			os.system('clear')
			log.print()
			
			self.print()
			
			print('''\n\n        Menu :
1- Edit Resolution Size
2- Edit Pourcent setting
3- Edit Cycles Samples
0- Save and quit

''')
			
			choice = input('Action?').strip().lower()
			
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			elif choice == '1':
				change = (self.size.edit(log, 'Resolution Size') or change)
			elif choice in ['2', '3']:
				change = (self.edit(log, int(choice)) or change)
			else:
				log.error('Unvalid menu choice', False)
		
	
	
	
	
	
	def print(self):
		'''a method to print preset'''
		print('Resolution :       '+self.size.toStr()+'@'+str(self.pourcent))
		print('Cycles Samples :   '+str(self.samples))
	
	
	
	
	
	def edit(self, log, choice):
		'''A method to edit pourcent setting'''
		if choice == 2:
			log.menuIn('Edit Resolution Pourcent')
		else:
			log.menuIn('Edit Cycles Samples')
		
		while True:
			os.system('clear')
			log.print()
			
			# print current setting and get new one
			if choice == 2:
				print('\n\n        Edit Pourcent :\nCurrent Pourcent : '+str(self.pourcent)+'\n')
				choice = input('New pourcent setting?').strip().lower()
			else:
				print('\n\n        Edit Cycles Samples :\nCurrent Sammples : '+str(self.samples)+'\n')
				choice = input('New Samples setting?').strip().lower()
			
			# exit menu
			if choice in ['', 'q', 'quit', 'cancel']:
				log.menuOut()
				return False
			
			#check new setting
			try:
				choice = int(choice)
			except ValueError:
				log.error('new setting must be an integer.')
				continue
			
			if choice < 0:
				log.error('new setting must be a positive integer.')
				continue
			
			# apply new setting and exit
			if choice == 2:
				self.pourcent = choice
				log.write('Resolution pourcent setting is set to : '\
							+str(self.pourcent)+'%\n')
			else:
				self.samples = choice
				log.write('Cycles samples set to : '+str(self.samples)+'%\n')
			log.menuOut()
			return True
		
	
	
	
	
	
	
	
	
	
