#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage Rendering Options'''
import xml.etree.ElementTree as xmlMod
import os

class Options:
	'''class to manage Rendering Options'''
	
	RGBA_AVAILABLE = ['IRIS', 'PNG', 'JPEG2000', 'TARGA', 'DPX', 'OPEN_EXR_MULTILAYER', 'OPEN_EXR', 'HDR' ]
	
	def __init__(self, xml= None):
		'''initialize Rendering Options with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize Rendering Options with default value'''
		self.z = True
		self.objectIndex = True
		self.compositing = False
		self.alpha = True
		self.exposureC = 1.0
		self.exposureB = 0.0
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize Rendering Options with values extracted from an xml object'''
		self.z = xml.find('z') is not None
		self.objectIndex = xml.find('objectIndex') is not None
		self.compositing = xml.find('compositing') is not None
		self.alpha = xml.find('alpha') is not None
		self.exposureC = float(xml.find('exposureC').get('value'))
		self.exposureB = float(xml.find('exposureB').get('value'))
	
	
	
	
	
	def toXml(self):
		'''export Rendering Options into xml syntaxed string'''
		txt = '<options>\n'
		
		if self.z:
			txt += '<z />\n'
		
		if self.objectIndex:
			txt += '<objectIndex />\n'
		
		if self.compositing:
			txt += '<compositing />\n'
		
		if self.alpha:
			txt += '<alpha />\n'
		
		txt += '<exposureB value="'+str(self.exposureB)+'" />'
		txt += '<exposureC value="'+str(self.exposureC)+'" />'
		
		txt += '</options>\n'
		return txt
	
	
	
	
	
	def menu(self, log):
		'''menu to explore and edit Rendering Options settings'''
		change = False
		log.menuIn('Rendering Options')
		
		while True:
			
			log.print()
			
			self.print()
			
			print('''\n\n        Menu :
1- Switch Z Pass Setting
2- Switch Object Index Pass Setting
3- Switch Compositing Setting
4- Switch Alpha Background Setting
5- Edit Cycles Exposure
6- Edit Blender Internal Exposure
0- Quit

''')
			
			choice = input('Action?').strip().lower()
			
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			elif choice in ['1', '2', '3', '4']:
				choice = int(choice)-1
				attr = ['z', 'objectIndex', 'compositing', 'alpha'][choice]
				label = ['Z pass', 'Object index pass', 'Compositing',\
						 'Alpha background'][choice]
				setattr(self, attr, not(getattr(self, attr)))
				log.write(label+' '+({True:'Ennabled', False:'Disabled'}[getattr(self, attr)]))
				change = True
			elif choice in ['5', '6']:
				change = (self.editExposure(log, choice == '5') or change)
			else:
				log.error('Unvalid menu choice', False)
		
	
	
	
	
	
	def print(self):
		'''a method to print Rendering Options'''
		ennable = {True:'Ennabled', False:'Disabled'}
		
		print('Z pass :                '+ennable[self.z])
		print('Object index pass :     '+ennable[self.objectIndex])
		print('Compositing :           '+ennable[self.compositing])
		print('Alpha Background :      '+ennable[self.alpha])
		print('Cycles Exposure  :      '+str(self.exposureC))
		print('Blender Int. Exp.  :    '+str(self.exposureB))
	
	
	
	
	
	def editExposure(self, log, cycles):
		'''A method to edit rendering exposure'''
		if cycles:
			log.menuIn('Edit Cycles Exposure')
			attr = 'exposureC'
			label = 'Cycles exposure'
		else:
			log.menuIn('Edit Blender Internal Exposure')
			attr = 'exposureB'
			label = 'Blender Internal exposure'
		
		while True:
			
			log.print()
			
			print('\n\n        Edit '+label.capitalize()+' :')
			print('Current setting : '+str(getattr(self,attr)))
			
			choice = input('New exposure : ').strip().lower()
			
			if choice in ['', 'q', 'quit', 'cancel']:
				log.menuOut()
				return False
			
			try:
				choice = float(choice)
			except ValueError:
				log.error('New value must be numerical.')
				continue
			
			if choice < 0:
				choice = 0.0
			if cycles:
				if choice > 10:
					choice = 10.0
				choice = round(choice, 2)
			else:
				if choice > 1:
					choice = 1.0
				choice = round(choice, 3)
			
			setattr(self, attr, choice)
			log.write(label+' set to : '+str(getattr(self, attr)))
			log.menuOut()
			return True
			
		
	
	
	
	
	
	def apply(self, scene):
		'''apply settings to a blender scene object'''
		import bpy
		for RL in scene.render.layers.values():
			RL.use_pass_z = self.z
			RL.use_pass_object_index = self.objectIndex
		
		scene.cycles.film_exposure = self.exposureC
		
		for w in bpy.data.worlds.values():
			w.exposure = self.exposureB
		
		scene.render.use_compositing = self.compositing
		
		scene.cycles.film_transparent = self.alpha
		scene.render.alpha_mode = { True : 'TRANSPARENT' , False : 'SKY' }[self.alpha]
		if self.alpha and scene.render.image_settings.file_format in RGBA_AVAILABLE:
			scene.render.image_settings.color_mode = 'RGBA'
		
	
	
	
	
