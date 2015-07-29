#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage bounce settings'''
import xml.etree.ElementTree as xmlMod
from Preferences.PresetList.Preset.ValueType.MinMax import *
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
		self.bounces = MinMax('3to8')
		self.transparency = MinMax('4to6')
		self.diffuse = 4
		self.glossy = 4
		self.transmission = 12
		self.volume = 0
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize bounce settings with values extracted from an xml object'''
		self.bounces = MinMax(xml = xml.find('bounces'))
		self.transparency = MinMax(xml = xml.find('transparency'))
		self.diffuse = int(xml.find('diffuse').get('value'))
		self.glossy = int(xml.find('glossy').get('value'))
		self.transmission = int(xml.find('transmission').get('value'))
		self.volume = int(xml.find('volume').get('value'))
	
	
	
	
	
	def toXml(self):
		'''export bounce settings into xml syntaxed string'''
		txt = '<bounceSet>\n'
		txt += '  <bounces '+self.bounces.toXmlAttr()+' />'
		txt += '  <transparency '+self.transparency.toXmlAttr()+' />'
		txt += '  <diffuse value="'+str(self.diffuse)+'" />'
		txt += '  <glossy value="'+str(self.glossy)+'" />'
		txt += '  <transmission value="'+str(self.transmission)+'" />'
		txt += '  <volume value="'+str(self.volume)+'" />'
		txt += '</bounceSet>\n'
		return txt
	
	
	
	
	
	def menu(self, log):
		'''menu to explore and edit bounce settings settings'''
		change = False
		log.menuIn('Bounces Settings')
		
		while True:
			
			log.print()
			
			self.print()
			
			print('''\n\n        Menu :
1- Edit Bounces Min/Max
2- Edit Transparency Bounces Min/Max
3- Edit Diffuse Bounces
4- Edit Glossy Bounces
5- Edit Transmission Bounces
6- Edit Volume Bounces
0- Quit

''')
			
			choice = input('Action?').strip().lower()
			
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			elif choice == '1':
				change = (self.bounces.edit(log, 'Min/Max Bounces') or change)
			elif choice == '2':
				change = (self.transparency.edit(log, 'Min/Max Transparency Bounces')\
								or change)
			elif choice in ['3', '4', '5', '6']:
				change = (self.edit(log, int(choice)) or change)
			else:
				log.error('Unvalid menu choice', False)
		
	
	
	
	
	
	def print(self):
		'''a method to print bounce settings'''
		
		print('Bounces :               '+self.bounces.toStr())
		print('Transparency bounces :  '+self.transparency.toStr())
		print('Diffuse :               '+str(self.diffuse))
		print('Glossy :                '+str(self.glossy))
		print('Transmission :          '+str(self.transmission))
		print('Volume :                '+str(self.volume))
		
	
	
	
	
	
	def edit(self, log, choice):
		'''a method to edit diffuse/glossy/transmission/volume settings'''
		
		if choice == 3:
			log.menuIn('Edit Diffuse Settings')
			attr = 'diffuse'
		elif choice == 4:
			log.menuIn('Edit Glossy Settings')
			attr = 'glossy'
		elif choice == 5:
			log.menuIn('Edit Transmission Settings')
			attr = 'transmission'
		elif choice == 6:
			log.menuIn('Edit Volume Settings')
			attr = 'volume'
		
		
		while True:
			
			log.print()
			
			print('\n\n        Edit '+attr.capitalize()\
					+' :\n\nCurrent Settings : '+str(getattr(self, attr)))
			
			choice = input('\nNew settings?').strip().lower()
			
			if choice in ['', 'q', 'quit', 'cancel']:
				log.menuOut()
				return False
			
			#check new setting
			try:
				choice = int(choice)
			except ValueError:
				log.error('New setting must be an integer.')
				continue
			
			if choice < 0:
				log.error('New setting must be a positive integer.')
				continue
			
			# apply new setting and exit
			setattr(self, attr, choice)
			log.write(attr.capitalize()+' bounces set to : '+str(getattr(self, attr)))
			log.menuOut()
			return True
	
	
	
	
	
	def apply(self, scene):
		'''apply settings to a blender scene object'''
		c = scene.cycles
		
		c.transparent_max_bounces = self.transparency.max
		c.transparent_min_bounces = self.transparency.min
		c.max_bounces = self.bounces.max
		c.min_bounces = self.bounces.min
		c.diffuse_bounces = self.diffuse
		c.glossy_bounces = self.glossy
		c.transmission_bounces = self.transmission
		c.volume_bounces = self.volume
	
	
	
	
	
	
	
	
	
