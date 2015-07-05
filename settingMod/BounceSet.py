#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage bounce settings'''
import xml.etree.ElementTree as xmlMod
from settingMod.MinMax import *
import os

class BounceSet:
	'''class to manage bounce settings'''
	
	
	def __init__(self, xml= None):
		'''initialize bounce settings with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize bounce settings with default value'''
		
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize bounce settings with values extracted from an xml object'''
		
	
	
	
	
	
	def toXml(self):
		'''export bounce settings into xml syntaxed string'''
		txt = '<bounceSet>\n'
		
		txt += '</bounceSet>\n'
		return txt
	
	
	
	
	
	def see(self, log):
		'''menu to explore and edit bounce settings settings'''
		change = False
		log.menuIn('Bounces Settings')
		
		while True:
			os.system('clear')
			log.print()
			
			self.print()
			
			print('''\n\n        Menu :
0- Save and quit

''')
			
			choice = input('Action?').strip().lower()
			
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			else:
				log.error('Unvalid menu choice', False)
		
	
	
	
	
	
	def print(self):
		'''a method to print bounce settings'''
		
	
	
	
	
	
	
	
	
	
	
