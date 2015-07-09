#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage metapreset'''
import xml.etree.ElementTree as xmlMod
from usefullFunctions import *
import os

class Metapreset:
	'''class to manage metapreset'''
	
	def __init__(self, xml= None):
		'''initialize metapreset with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize metapreset with default value'''
		self.default = None
		self.groups = {}
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize metapreset with values extracted from an xml object'''
		self.default = xml.get('default')
		
		self.groups = {}
		for node in xml.findall('group'):
			self.groups[node.get('name')] = node.get('preset')
		
	
	
	
	
	
	def toXml(self, alias):
		'''export metapreset into xml syntaxed string'''
		if self.default is None:
			txt = '<metapreset alias="'+alias+'" >\n'
		else:
			txt = '<metapreset alias="'+alias+'" default="'+self.default+'" >\n'
		
		for group, preset in self.groups.items():
			print('  <group name="'+group+'" preset="'+preset+'" />')
		
		txt += '</metapreset>\n'
		return txt
	
	
	
	
	
	def see(self, log):
		'''menu to explore and edit metapreset settings'''
		change = False
		log.menuIn(alias+' Metapreset')
		
		while True:
			
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
		'''a method to print Metapreset'''
		if self.default is None:
			print('Default Preset : \033[31mnot set!\033[0m')
		else:
			print('Default Preset : '+self.default)
		print()
		
		for group, preset in self.groups.items():
			print(columnLimit(group, 25, sep = ''),' : ',columnLimit(preset, 25, sep = ''))
	
	
	
	
	
	def copy(self):
		'''A method to get a copy of current object'''
		xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
		xml += self.toXml('')
		xml = xmlMod.fromstring(xml)
		return Metapreset(xml)
		
	
	
	
	
	
	
