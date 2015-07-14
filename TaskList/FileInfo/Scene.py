#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage blender scene info'''
import xml.etree.ElementTree as xmlMod
from TaskList.FileInfo.Renderlayer import *
import os

class Scene:
	'''class to manage blender scene info'''
	
	
	def __init__(self, xml):
		'''initialize blender scene info with default settings or saved settings'''
		self.fromXml(xml)
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize blender scene info with savedd settings'''
		self.name = xml.get('name')
		self.start = xml.get('start')
		self.end = xml.get('end')
		self.fps = xml.get('fps')
		
		self.renderlayers = {}
		for RL in xml.findall('renderlayer'):
			self.renderlayers[RL.get('name')] = Renderlayer(RL)
	
	
	
	
	
	def toXml(self):
		'''export blender scene info into xml syntaxed string'''
		xml = '    <scene name="'+self.name+'" start="'+str(self.start)\
			+'" end="'+str(self.end)+'" fps="'+str(self.fps)+'" >\n'
		
		for RL in self.renderlayers.values():
			xml += RL.toXml()
		
		xml += '    </scene>\n'
		return xml
	
	
	
	
	
	def printActiveRenderlayer(self):
		'''A method to print scene renderlayer'''
		for RL in self.renderlayers.values():
			if RL.use:
				print('    '+RL.name)
	
	
	
	
	
	def printRenderlayer(self):
		'''A method to list all renderlayer'''
		renderlayers = list(self.renderlayers.keys())
		renderlayers.sort(key = str.lower)
		
		for i, RL in enumerate(renderlayers):
			if self.renderlayers[RL].use:
				print(str(i)+'- '+RL)
			else:
				print(str(i)+'- \033[31m'+RL+'(DISABLED)\033[0m')
		return renderlayers
	
	
	
	
	
	def renderlayerActivator(self, log):
		'''A method to activate/desactivate renderlayer'''
		log.menuIn('Task Renderlayer Activation')
		change = False
		
		while True:
			log.print()
			print('\n\n        Renderlayer Activation :\n')
			
			renderlayers = self.printRenderlayer()
			
			choice = input('''

Type "a" to activate All renderlayer
Type "n" to desactivate All renderlayer
Type "s" to switch All renderlayer
Type the number of a renderlayer to switch his state
Type "q" to confirm and quit

action : ''').strip().lower()
			
			if choice in ['', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			
			if choice == 'a' or choice == 'n':
				use = {'a':True,'n':False}[choice]
				for RL in self.renderlayers.values():
					RL.use = use
				change = True
			elif choice == 's':
				for RL in self.renderlayers.values():
					RL.use = not RL.use
				change = True
			else:
				try:
					choice = int(choice)
				except ValueError:
					log.error('unvalid choice, expect a integer or a/s/n/q character.')
					continue
				
				if choice < 0 or choice >= len(renderlayers):
					log.error('the number you give correspond to nothing!')
					continue
				
				self.renderlayers[renderlayers[choice]].use = not self.renderlayers[renderlayers[choice]].use
				change = True
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
