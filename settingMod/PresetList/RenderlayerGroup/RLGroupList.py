#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage Renderlayer list'''
import xml.etree.ElementTree as xmlMod
from Preferences.PresetList.RenderlayerGroup.RenderlayerGroup import *
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
	
	
	
	
	
	def menu(self, log, presetList):
		'''menu to explore and edit Renderlayer list settings'''
		change = False
		log.menuIn('Group List Management')
		
		while True:
			log.print()
			
			print('\n\n        Manage Renderlayer Group :\n')
			self.list()
			
			print('''\n\n        Menu :
1- Edit Group
2- Create New Group
0- Quit

''')
			
			choice = input('Action?').strip().lower()
			
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			elif choice == '1':
				if len(self.groups) == 0:
					log.error('Empty group list! Create group before thinking to edit it')
					continue
				
				change = (self.edit(log, presetList) or change)
			elif choice == '2':
				change = (self.create(log, presetList) or change)
			else:
				log.error('Unvalid menu choice', False)
		
	
	
	
	
	
	def usedKey(self, key):
		'''A method to check if a keyword is used by one of the group'''
		
		
		for group in self.groups.values():
			if group.search(key):
				return True
		
		return False
	
	
	
	
	
	def collideKey(self, k):
		'''A method to check that a keyword don't collide with already existing keywords'''
		for group in self.groups.keys():
			key = self.groups[group].collide(k)
			if key is not None:
				return key
		return None
	
	
	
	
	
	def list(self, index = False, exclude = []):
		'''A method to list Renderlayer Group'''
		groups = list(self.groups.keys())
		groups.sort(key = str.lower)
		
		for k in groups[0:]:
			if k in exclude:
				groups.remove(k)
		
		if index:
			for i, g in enumerate(groups):
				print(str(i)+'- '+g)
		else:
			for g in groups:
				print(g+' :\n    '+','.join(self.groups[g].keywords))
		
		return groups
	
	
	
	
	
	def choose(self, log, exclude = []):
		'''A method to choose a Renderlayer Group in the list'''
		log.menuIn('Group Choice')
		
		while True:
			log.print()
			print('\n\n        Group Choice :\n\n')
			
			groups = self.list(True, exclude)
			
			choice = input('group to use : ').strip().lower()
			
			if choice in ['', 'q', 'quit', 'cancel']:
				log.menuOut()
				return None
			
			try:
				choice = int(choice)
			except ValueError:
				log.error('expect integer value')
				continue
			
			if choice < 0 or choice >= len(groups):
				log.error('out of available choices range!')
				continue
			
			log.menuOut()
			return groups[choice]
	
	
	
	
	
	def edit(self, log, presetList):
		'''A method to edit renderlayer group'''
		log.menuIn('Edit Renderlayer Group')
		target = self.choose(log)
		
		log.menuOut()
		if target is None:
			return False
		
		return self.groups[target].menu(log, self, target, presetList)
	
	
	
	
	
	def newGroupName(self, log, name = None):
		'''a name to create a new group name'''
		log.menuIn('Name Choice')
		
		while True:
			log.print()
			
			print('\n\n        New Group Name Choice :')
			
			new = input('type new group name :').strip()
			
			if new.lower() in ['', 'q', 'quit', 'cancel', name]:
				log.menuOut()
				return None
			
			if len(new) < 6:
				log.error('the name must have 6 or more characters!')
				continue
			
			if re.search(r'^[-0-9a-zA-Z_ ()]{1,}$', new) is None:
				log.error('Unvalid characters : accepted characters are unaccentuated aplhanumeric character, -, _, parenteses and spaces!')
				continue
			
			if new in self.groups.keys():
				log.error('This name is already use by another group!')
				continue
			
			log.menuOut()
			return new
	
	
	
	
	
	def create(self, log, presetList):
		'''A method to create a new Renderlayer Group'''
		log.menuIn('Create A New Group')
		
		name = self.newGroupName(log)
		if name is not None:
			self.groups[name] = RLGroup([])
			log.write('create «'+name+'» new renderlayer group')
			self.groups[name].menu(log, self, name, presetList)
			log.menuOut()
			return True
		else:
			log.menuOut()
			return False
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
