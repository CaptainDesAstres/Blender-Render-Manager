#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage Renderlayer group'''
import xml.etree.ElementTree as xmlMod
import os, re

class RLGroupList:
	'''class to manage Renderlayer group'''
	
	
	def __init__(self, xml= None):
		'''initialize Renderlayer group with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize Renderlayer group with default value'''
		
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize Renderlayer group with values extracted from an xml object'''
		
	
	
	
	
	
	def toXml(self):
		'''export Renderlayer group into xml syntaxed string'''
		txt = '<RenderlayerGroup />\n'
		
		return txt
	
	
	
	
	
	def see(self, log, versions):
		'''menu to explore and edit Renderlayer group settings'''
		change = False
		log.menuIn('')
		
		while True:
			
			log.print()
			
			
			
			print('''\n\n        Menu :
0- Save And Quit

''')
			
			choice = input('Action?').strip().lower()
			
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			else:
				log.error('Unvalid menu choice', False)
		
	
	
	
	
	
	def list(self, index = False):
		'''A method to list keyword of the Renderlayer Group'''
		
	
	
	
	
	
	def choose(self, log):
		'''A method to choose a keyword'''
		
	
	
	
	
	
	
	def add(self, log, versions):
		'''A method to add a new keyword'''
		
	
	
	
	
	
	def remove(self, log):
		'''A method to remove a keyword'''
		
	
	
	
	
	
	
	
	
	
	
