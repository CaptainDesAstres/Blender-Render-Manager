#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage preset list'''
import xml.etree.ElementTree as xmlMod
from settingMod.PresetList.Preset.Preset import *
from settingMod.PresetList.RenderlayerGroup.RLGroupList import *
import os, re

class PresetList:
	'''class to manage preset list'''
	
	
	def __init__(self, xml= None):
		'''initialize preset list with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize preset list with default value'''
		self.presets = {'Factory Preset':Preset()}
		self.default = 'Factory Preset'
		self.renderlayers = RLGroupList()
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize preset list with values extracted from an xml object'''
		self.presets = {}
		for node in xml.findall('preset'):
			self.presets[node.get('alias')] = Preset(node)
		
		self.default = xml.get('default')
		
		self.renderlayers = RLGroupList(xml.find('RLGroupList'))
	
	
	
	
	
	def toXml(self):
		'''export preset list into xml syntaxed string'''
		if self.default is not None:
			txt = '<presetList default="'+self.default+'" >\n'
		else:
			txt = '<presetList>\n'
		
		presets = self.presets.keys()
		for p in presets:
			txt += self.presets[p].toXml(p)
		
		txt += self.renderlayers.toXml()
		
		txt += '</presetList>\n'
		return txt
	
	
	
	
	
	def see(self, log, versions):
		'''menu to explore and edit preset list settings'''
		change = False
		log.menuIn('Preferences Preset/Metapreset')
		
		while True:
			
			log.print()
			
			print('\n\nDefault preset : «'+self.default+'»')
			
			print('''\n\n        Menu :
1- See/Edit Preset
2- Rename Preset
3- Create New Preset
4- Create New Preset From Existing
5- Remove Preset
6- Use By Default
7- Manage Renderlayer Group
0- Save And Quit

''')
			
			choice = input('Action?').strip().lower()
			
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			elif choice == '1':
				alias = self.choose(log)
				if alias is not None:
					change = (self.presets[alias].see(log, alias, versions) or change)
			elif choice == '2':
				change = (self.rename(log) or change)
			elif choice == '3':
				change = (self.create(log, versions) or change)
			elif choice == '4':
				change = (self.createFrom(log, versions) or change)
			elif choice == '5':
				change = (self.remove(log) or change)
			elif choice == '6':
				change = (self.setDefault(log) or change)
			elif choice == '7':
				change = (self.renderlayers.see(log) or change)
			else:
				log.error('Unvalid menu choice', False)
		
	
	
	
	
	
	def presetsList(self, index = False, meta = True):
		'''A method to list preset'''
		keys = list(self.presets.keys())
		keys.sort(key = str.lower)
		
		if not meta:
			for k in keys[0:]:
				if type(self.presets[k]) is Metapreset:
					keys.remove(k)
		
		
		if index:
			for i,k in enumerate(keys):
				print(str(i)+'- '+k)
		else:
			for k in keys:
				print(k)
		
		return keys
	
	
	
	
	
	def choose(self, log, meta = True):
		'''A method to choose a preset in the list'''
		
		if len(self.presets) == 0:
			log.error('There is no available preset!')
			return None
		
		while True:
			
			log.print()
			
			print('\n\n        Choose The Preset To Use :')
			presets = self.presetsList(True, meta, exclude)
			
			choice = input('what\' the preset to use?').strip().lower()
			
			if choice in ['', 'q', 'quit', 'cancel']:
				return None
			
			try:
				choice = int(choice)
			except ValueError:
				log.error('integer value expected')
				continue
			
			if choice < 0 or choice >= len(presets):
				log.error('out of available choice range')
				continue
			
			return presets[choice]
	
	
	
	
	
	def newAlias(self, log):
		'''A method to get user new alias for a preset'''
		while True:
			log.print()
			
			print('\n\n        Name Choice :')
			choice = input('What\'s the wanted Name : ').strip()
			
			if choice == '':
				return None
			
			# check size
			if len(choice)<4:
				log.error('4 minimal chars is expected for a valid preset Name')
				continue
			
			# check char
			if re.search(r'^([-a-zA-Z0-9]| |\(|\)|\.){1,}$', choice) is None:
				log.error('unvalid characters. Preset name can only contain alphanumeric (unaccentuated) characters, spaces, parentheses points and "-"')
				continue
			
			# check used
			if choice in self.presets.keys():
				log.error('Name Already used by another preset')
				continue
			
			return choice
	
	
	
	
	
	def rename(self, log):
		'''A method to rename Preset'''
		log.menuIn('Rename Preset')
		
		log.menuIn('Choose Preset')
		old = self.choose(log)
		if old is None:
			return False
		log.menuOut()
		log.menuOut()
		log.menuIn('Rename «'+old+'» Preset')
		
		log.menuIn('New Preset Name')
		new = self.newAlias(log)
		if new is None:
			return False
		log.menuOut()
		log.menuOut()
		
		self.presets[new] = self.presets.pop(old)
		log.write('«'+old+'» preset rename to «'+new+'»\n')
		return True
	
	
	
	
	
	def create(self, log, versions):
		'''A method to create a new Preset'''
		log.menuIn('Create New Preset')
		
		log.menuIn('Preset Or Metapreset Choice')
		while True:
			log.print()
			
			print('''\n\n        Preset Type Choice :
1- Preset
2- Metapreset
0- Cancel''')
			Ptype = input('What kind of preset do you want to create? ').strip().lower()
			
			if Ptype in ['q', 'quit', 'cancel']:
				Ptype = 0
			else:
				try:
					Ptype = int(Ptype)
				except ValueError:
					log.error('expect integer value')
					continue
			
			# check range
			if Ptype < 0 or Ptype > 2:
				log.error('this is not a valid choice!')
				continue
		log.menuOut()
		
		if Ptype == 0:
			log.menuOut()
			return False
		
		log.menuIn('Preset Name Choice')
		name = self.newAlias(log)
		log.menuOut()
		
		if name is None:
			log.menuOut()
			return False
		
		
		if Ptype == 1:
			self.presets[name] = Preset()
			log.write('Create new preset named «'+name+'»\n')
		else:
			self.presets[name] = Metapreset()
			log.write('Create new metapreset named «'+name+'»\n')
		
		
		self.presets[name].see(log, name, versions)
		log.menuOut()
		return True
	
	
	
	
	
	def createFrom(self, log, versions):
		'''A method to create a new preset by copying a old one'''
		log.menuIn('Copy Then Edit Preset')
		
		log.menuIn('Original Preset Choice')
		old = self.choose(log)
		log.menuOut()
		if old is None:
			log.menuOut()
			return False
		
		log.menuIn('Name Choice')
		new = self.newAlias(log)
		log.menuOut()
		if new is None:
			log.menuOut()
			return False
		
		self.presets[new] = self.presets[old].copy()
		if type(self.presets[new]) is Preset:
			log.write('«'+new+'» preset create on «'+old+'» preset base.\n')
		else:
			log.write('«'+new+'» metapreset create on «'+old+'» metapreset base.\n')
		self.presets[new].see(log, new, versions)
		log.menuOut()
		return True
	
	
	
	
	
	def remove(self, log):
		'''A method to remove a preset from the list'''
		
		log.menuIn('Remove A Preset')
		
		log.menuIn('Target Choice')
		target = self.choose(log)
		log.menuOut()
		if target is None:
			log.menuOut()
			return False
		
		choice = input('Do you really want to erase «'+target+'» preset?(y)').strip().lower()
		
		if choice == 'y':
			self.presets.pop(target)
			log.write('«'+target+'» preset erased.\n')
			log.menuOut()
			return True
		log.menuOut()
		return False
	
	
	
	
	
	def setDefault(self, log):
		'''A method to change default Preset'''
		
		log.menuIn('Choose Default Preset')
		
		choice = self.choose(log)
		log.menuOut()
		
		if choice is None:
			return False
		
		self.default = choice
		log.write('Default preset set to «'+choice+'»\n')
		return True
	
	
	
	
	
	
	
	
	
	
