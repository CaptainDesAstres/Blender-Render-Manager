#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage antialiasing settings'''
import xml.etree.ElementTree as xmlMod

class OSA:
	'''class to manage antialiasing settings'''
	
	
	def __init__(self, xml= None):
		'''initialize OSA settings with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize antialiasing settings with default value'''
		self.enabled = True
		self.samples = 8
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize antialiasing settings with values extracted from an xml object'''
		self.enabled = { 'True':True, 'False':False }[xml.get('enabled')]
		self.samples = int(xml.get('samples'))
	
	
	
	
	
	def toXml(self):
		'''export antialiasing settings into xml syntaxed string'''
		txt = '<OSA enabled="'+str(self.enabled)+'" samples="'\
				+str(self.samples)+'"/>\n'
		return txt
	
	
	
	
	
	def menu(self, log):
		'''menu to explore and edit antialiasing settings'''
		change = False
		log.menuIn('OSA settings')
		
		while True:
			
			log.print()
			
			self.print()
			
			print('''

(Antialiasing setting only work with blender internal engine and not with Cycles)

        Menu :
1- Switch To Enable Or Disabled OSA
0- Quit

''')
			
			choice = input('Action?').strip().lower()
			
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			elif choice == '1':
				change = True
				self.enabled = not self.enabled
			else:
				log.error('Unvalid menu choice', False)
		
	
	
	
	
	
	def print(self):
		'''a method to print preset'''
		print('Antialiasing :          '\
					+{ True:'enabled', False:'disabled' }[self.enabled] )
		
		if self.enabled:
			print('OSA samples :           '+str(self.samples))
	
	
	
	
	
	
	
	
	
