#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage Renderlayer group'''
import xml.etree.ElementTree as xmlMod
import os, re

class RLGroup:
	'''class to manage Renderlayer group'''
	
	
	def __init__(self, keywords = None, xml= None):
		'''initialize Renderlayer group with default value or values extracted from an xml object'''
		if keywords is not None:
			self.defaultInit(keywords)
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self, keywords):
		'''initialize Renderlayer group with default value'''
		self.keywords = keywords
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize Renderlayer group with values extracted from an xml object'''
		self.keywords = xml.get('keywords').split(';')
	
	
	
	
	
	def toXml(self, name):
		'''export Renderlayer group into xml syntaxed string'''
		txt = '<RenderlayerGroup keywords="'+';'.join(self.keywords)+'" name="'+name+'" />\n'
		
		return txt
	
	
	
	
	
	def menu(self, log, RLGlist, name, presetList):
		'''menu to explore and edit Renderlayer group settings'''
		change = False
		log.menuIn('«'+name+'» Renderlayer Group')
		
		while True:
			log.print()
			
			print('\n\n        «'+name+'» Renderlayer Group :\n')
			self.list()
			
			print('''\n\n        Menu :
1- Add Keywords
2- Remove Keywords
3- Rename Group
4- Erase Group
0- Save And Quit

''')
			
			choice = input('Action?').strip().lower()
			
			if choice in ['0', 'q', 'quit', 'cancel']:
				if len(self.keywords) == 0:
					log.print()
					if input('\033[31mWarning: the group have no keyword. If you quit now, it will be erase! confirm (y) : \033[0m').strip().lower() == 'y' and self.eraseGroupUseTest(log, name, presetList):
						
						RLGlist.groups.pop(name)
						log.write('«'+name+'» group erased because he don\'t have keyword\n')
					else:
						continue
				
				log.menuOut()
				return change
			elif choice == '1':
				change = (self.add(log, RLGlist) or change)
			elif choice == '2':
				change = (self.remove(log, name) or change)
			elif choice == '3':
				confirm, name = self.rename(log, RLGlist, name, presetList)
				change = (confirm or change)
			elif choice == '4':
				if self.erase(log, RLGlist, name, presetList):
					log.menuOut()
					return True
			else:
				log.error('Unvalid menu choice', False)
		
	
	
	
	
	
	def list(self, index = False):
		'''A method to list keyword of the Renderlayer Group'''
		print('Group Keywords :')
		if index:
			for i, k in enumerate(self.keywords):
				print('  '+str(i)+'- '+k)
		else:
			for k in self.keywords:
				print('    '+k)
	
	
	
	
	
	def choose(self, log):
		'''A method to choose a keyword'''
		log.menuIn('Keywords Choice')
		
		while True:
			log.print()
			
			print('\n\n        Keywords Choice')
			
			self.list(True)
			
			choice = input('\n\nkeywords Choice').strip().lower()
			
			if choice in ['', 'q', 'quit', 'cancel']:
				log.menuOut()
				return None
			
			try:
				choice = int(choice)
			except ValueError:
				log.error('Integer value expected!')
				continue
			
			if choice < 0 or choice >= len(self.keywords):
				log.error('No keywords corresponding to this index number!')
				continue
			
			log.menuOut()
			return choice
	
	
	
	
	
	
	def search(self, key):
		'''A method to check if a keyword is used by the group'''
		return key in self.keywords
	
	
	
	
	
	
	def add(self, log, RLGlist):
		'''A method to add a new keyword'''
		log.menuIn('Add Keywords')
		
		while True:
			log.print()
			
			print('\n\n        Add Keyword :\n\n')
			
			keys = input('Type keywords to add (separed by ";") : ').strip()
			
			if keys.lower() in ['', 'q']:
				log.menuOut()
				return False
			
			keys = keys.split(';')
			for i,k in enumerate(keys):
				keys[i] = keys[i].strip()
			
			unique = []
			for k in keys:
				if k not in unique:
					unique.append(k)
			keys = unique
			
			error = ''
			for k in keys[0:]:
				if len(k) < 3:
					error += '«'+k+'» will not be added because it\'s to short!\n'
					keys.remove(k)
				elif re.search(r'^([a-zA-Z0-9_]){1,}$', k) is None:
					error += '«'+k+'» will not be added because contained unvalid characters (only unaccentuated alphanumeric characters and _ are accept)!\n'
					keys.remove(k)
				elif RLGlist.usedKey(k):
					error += '«'+k+'» will not be added because it already set for another group!\n'
					keys.remove(k)
				else:
					collide = RLGlist.collideKey(k)
					if collide is not None:
						error += '«'+k+'» will not be added because it collide with already set keyword «'+collide+'» of another group!\n'
						keys.remove(k)
			
			
			error = error.strip()
			if len(error) > 0:
				log.error(error, False)
			
			if len(keys) == 0:
				continue
			
			self.keywords += keys
			log.write('«'+'», «'.join(keys)+'» have been added to the group keywords\n')
			log.menuOut()
			return True
			
	
	
	
	
	
	def remove(self, log, name):
		'''A method to remove a keyword'''
		log.menuIn('Remove Keyword')
		
		target = self.choose(log)
		log.menuOut()
		if target is None:
			return False
		
		target = self.keywords.pop(target)
		log.write('«'+target+'» keyword remove from «'+name+'» renderlayer group\n')
		return True
	
	
	
	
	
	def rename(self, log, RLGlist, name, presetList):
		'''A method to rename the group'''
		log.menuIn('Rename «'+name+'» Renderlayer Group')
		
		new = RLGlist.newGroupName(log, name)
		
		log.menuOut()
		if new is None:
			return False
		
		RLGlist.groups[new] = self
		RLGlist.groups.pop(name)
		presetList.renameGroup(name, new)
		log.write('«'+name+'» group rename in «'+new+'»\n')
		return True, new
	
	
	
	
	
	def erase(self, log, RLGlist, name, presetList):
		'''A method to erase the group'''
		log.menuIn('Erase «'+name+'» renderlayer group')
		
		log.print()
		print('\n\n        Erase «'+name+'» renderlayer group')
		confirm = input('Do you realy want to erase this group?(y)').strip().lower() == 'y'
		
		log.menuOut()
		if confirm and self.eraseGroupUseTest(log, name, presetList):
			RLGlist.groups.pop(name)
			log.write('«'+name+'» group erased\n')
			return True
		else:
			return False
	
	
	
	
	
	def eraseGroupUseTest(self, log, name, presetList):
		'''check if the group is used before to erase it'''
		if not presetList.checkGroupUse(name):
			return True
		
		log.print()
		if input('\n\nRender Layer Group «'+name+'» is used by some metapreset. if you erase it, it will be unset for all this metapreset… confirm (y)').strip().lower() == 'y':
			presetList.eraseGroup(name)
			return True
		return False
	
	
	
	
	
	def collide(self, key):
		'''check if key collide with keyword used by the group'''
		for keyword in self.keywords:
			if keyword.count(key) + key.count(keyword) > 0:
				return keyword
		return None
	
	
	
	
	
	
	
	
	
