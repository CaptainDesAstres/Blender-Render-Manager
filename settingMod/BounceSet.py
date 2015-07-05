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
		self.bounces = MinMax('3to8')
		self.transparency = MinMax('4to6')
		self.diffuse = 4
		self.glossy = 4
		self.transmission = 12
		self.volume = 0
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize bounce settings with values extracted from an xml object'''
		self.bounces = MinMax(xml.find('bounces'))
		self.transparency = MinMax(xml.find('transparency'))
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
		
	
	
	
	
	
	
	
	
	
	
