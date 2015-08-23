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
		self.fullSample = False
		self.size = 1.0
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize antialiasing settings with values extracted from an xml object'''
		boolDict = { 'True':True, 'False':False }
		self.enabled = boolDict[xml.get('enabled')]
		self.samples = int(xml.get('samples'))
		self.fullSample = boolDict[xml.get('fullSample')]
		self.size = float(xml.get('size'))
	
	
	
	
	
	def toXml(self):
		'''export antialiasing settings into xml syntaxed string'''
		txt = '<OSA enabled="'+str(self.enabled)+'" samples="'\
				+str(self.samples)+'" fullSample="'+str(self.fullSample)\
				+'" size="'+str(self.size)+'" />\n'
		return txt
	
	
	
	
	
	def menu(self, log):
		'''menu to explore and edit antialiasing settings'''
		change = False
		log.menuIn('OSA Settings')
		
		while True:
			
			log.print()
			
			self.print()
			
			print('''

(Antialiasing setting only work with blender internal engine and not with Cycles)

        Menu :
1- Switch To Enable Or Disabled OSA
2- Edit OSA Samples
3- Switch To Enable Or Disabled OSA Full Sample Option
0- Quit

''')
			
			choice = input('Action?').strip().lower()
			
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			elif choice == '1':
				change = True
				self.enabled = not self.enabled
			elif choice == '2':
				change = (self.editSamples() or change)
			elif choice == '3':
				change = True
				self.fullSample = not self.fullSample
			else:
				log.error('Unvalid menu choice', False)
		
	
	
	
	
	
	def print(self):
		'''a method to print preset'''
		enable = { True:'enabled', False:'disabled' }
		print('Antialiasing :          '\
					+enable[self.enabled] )
		
		if self.enabled:
			print('OSA Samples :           '+str(self.samples))
			print('OSA filter Size (px):    '+str(round(self.size, 3)) )
			print('Full Sample :           '+enable[self.fullSample])
	
	
	
	
	
	def editSamples(self):
		'''menu to edit OSA sampes setting'''
		log.menuIn('Edit Samples Setting')
		options = [ 5, 8, 11, 16 ]
		
		while True:
			log.print()
			
			print('\n\nCurrent settings : '+str(self.samples)+'samples per pixel.\n\n       available settings choice :\n0- Quit whithout change' )
			
			for opt in options:
				print(str(opt)+'- '+str(opt)+' samples per pixel')
			choice = input().strip().lower()
			
			try:
				choice = int(choice)
			except ValueError:
				log.error('expect integer value.')
				continue
			
			if choice == 0:
				return False
			if choice in options
				self.samples = choice
				return True
			log.error('unexpected «'+str(choice)+'» integer value. expected 0, 5, 8, 11 or 16.')
			
	
	
	
	
	
	
	
	
