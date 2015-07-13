#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage preset list'''
import xml.etree.ElementTree as xmlMod
from settingMod.PresetList.Preset.Preset import *
from settingMod.PresetList.Preset.Metapreset import *
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
		
		for node in xml.findall('metapreset'):
			self.presets[node.get('alias')] = Metapreset(node)
		
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
	
	
	
	
	
	def menu(self, log, versions, tasks):
		'''menu to explore and edit preset list settings'''
		change = False
		log.menuIn('Preferences Preset/Metapreset')
		
		while True:
			
			log.print()
			
			if self.default is None:
				print('\n\n\033[31mDefault preset is not set!\033[0m')
			else:
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
				if self.default is None:
					log.error('you must set a default preset before quit!')
					continue
				log.menuOut()
				return change
			elif choice == '1':
				alias = self.choose(log)
				if alias is not None:
					if type(self.presets[alias]) is Preset:
						change = (self.presets[alias].menu(log, alias, versions) or change)
					else:
						change = (self.presets[alias].menu(log, alias, self) or change)
			elif choice == '2':
				change = (self.rename(log, tasks) or change)
			elif choice == '3':
				change = (self.create(log, versions) or change)
			elif choice == '4':
				change = (self.createFrom(log, versions) or change)
			elif choice == '5':
				change = (self.remove(log, tasks) or change)
			elif choice == '6':
				change = (self.setDefault(log) or change)
			elif choice == '7':
				change = (self.renderlayers.menu(log, self) or change)
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
			presets = self.presetsList(True, meta)
			
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
	
	
	
	
	
	def rename(self, log, tasks):
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
		
		if self.default == old:
			self.default = new
		
		tasks.renamePreset(old, new)
		tasks.save()
		
		if type(self.presets[new]) is Preset:
			for preset in self.presets.values():
				if type(preset) is Metapreset:
					preset.renamePreset(old, new)
		
		log.write('«'+old+'» preset rename to «'+new+'»')
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
			break
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
			log.write('Create new preset named «'+name+'»')
			self.presets[name].menu(log, name, versions)
		else:
			self.presets[name] = Metapreset()
			log.write('Create new metapreset named «'+name+'»')
			self.presets[name].menu(log, name, self)
		
		
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
			log.write('«'+new+'» preset create on «'+old+'» preset base.')
			self.presets[new].menu(log, new, versions)
		else:
			log.write('«'+new+'» metapreset create on «'+old+'» metapreset base.')
			self.presets[new].menu(log, new, self)
		log.menuOut()
		return True
	
	
	
	
	
	def remove(self, log, tasks):
		'''A method to remove a preset from the list'''
		
		log.menuIn('Remove A Preset')
		
		log.menuIn('Target Choice')
		target = self.choose(log)
		log.menuOut()
		if target is None:
			log.menuOut()
			return False
		
		print('\033[31mIf preset is used in other metapreset or as default preset, this will be unset\033[0m\n')
		print('\033[31mIf preset is used by a task, the task will be set to use default preset\033[0m\n')
		choice = input('Do you really want to erase «'+target+'» preset?(y)').strip().lower()
		
		if choice == 'y':
			old = self.presets.pop(target)
			log.write('«'+target+'» preset erased.')
			
			if self.default == target:
				self.default = None
			
			if type(old) is Preset:
				for preset in self.presets.values():
					if type(preset) is Metapreset:
						preset.unsetPreset(target)
			
			tasks.erasePreset(target)
			tasks.save()
			
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
		log.write('Default preset set to «'+choice+'»')
		return True
	
	
	
	
	
	def checkGroupUse(self, group):
		'''check if a group is used by one of the metapreset of the list'''
		for preset in self.presets.values():
			if type(preset) is Metapreset and preset.useGroup(group):
				return True
		return False
	
	
	
	
	
	def eraseGroup(self, group):
		'''unset group for all metapreset'''
		for preset in self.presets.values():
			if type(preset) is Metapreset:
				preset.unsetGroup(group)
	
	
	
	
	
	def renameGroup(self, old, new):
		'''rename a group in all metapreset that use it'''
		for preset in self.presets.values():
			if type(preset) is Metapreset:
				preset.renameGroup(old,new)
		
	
	
	
	
	
	def renameBlenderVersion(self, old, new):
		'''rename a blender Version in all preset that use it'''
		for preset in self.presets.values():
			if type(preset) is Preset:
				preset.renameBlenderVersion(old,new)
		
	
	
	
	
	
	def useBlenderVersion(self, name):
		'''check if blender version is used by some preset'''
		for preset in self.presets.values():
			if type(preset) is Preset and preset.useBlenderVersion(name):
				return True
		return False
	
	
	
	
	
	
	def eraseBlenderVersion(self, name):
		'''erase blender version in preset who use it'''
		for preset in self.presets.values():
			if type(preset) is Preset:
				preset.eraseBlenderVersion(name)
	
	
	
	
	
