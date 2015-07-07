#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage Renderlayer list'''
import xml.etree.ElementTree as xmlMod
from settingMod.PresetList.Preset.RenderlayerGroup.RenderlayerGroup import *
import os, re

class RLGroupList:
	'''class to manage Renderlayer list'''
	
	
	def __init__(self, xml= None):
		'''initialize Renderlayer list with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize Renderlayer list with default value'''
		self.groups = {
						'Background':RLGroup(['bck', 'background']),
						'Foreground':RLGroup(['fgd', 'foreground'])
						}
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize Renderlayer list with values extracted from an xml object'''
		self.groups = {}
		for node in xml.findall('RenderlayerGroup'):
			self.groups[node.get('name')] = RLGroup(xml = node)
	
	
	
	
	
	def toXml(self):
		'''export Renderlayer list into xml syntaxed string'''
		txt = '<RLGroupList>\n'
		
		for group in self.groups.keys():
			txt += self.groups[group].toXml(group)
		
		txt += '</RLGroupList>\n'
		return txt
	
	
	
	
	
	def see(self, log):
		'''menu to explore and edit Renderlayer list settings'''
		change = False
		log.menuIn('')
		
		while True:
			
			log.print()
			
			
			
			print('''\n\n        Menu :
1- See/Edit Group
2- Rename Group
3- Create New Group
4- Remove Group
0- Save And Quit

''')
			
			choice = input('Action?').strip().lower()
			
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			else:
				log.error('Unvalid menu choice', False)
		
	
	
	
	
	
	def groupList(self, index = False):
		'''A method to list Renderlayer Group'''
		
	
	
	
	
	
	def choose(self, log):
		'''A method to choose a Renderlayer Group in the list'''
		
	
	
	
	
	
	def newGroupName(self, log):
		'''A method to get user new alias for a Renderlayer Group'''
		
	
	
	
	
	
	def rename(self, log):
		'''A method to rename Renderlayer Group'''
		
	
	
	
	
	
	def create(self, log, versions):
		'''A method to create a new Renderlayer Group'''
		
	
	
	
	
	
	def remove(self, log):
		'''A method to remove a Renderlayer Group from the list'''
		
	
	
	
	
	
	
	
	
	
	
