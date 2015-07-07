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
	
	
	
	
	
	def see(self, log, RLGlist, name):
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
				log.menuOut()
				return change
			elif choice == '1':
				change = (self.add(log, RLGlist) or change)
			elif choice == '2':
				change = (self.remove(log, name) or change)
			elif choice == '3':
				change = (self.rename(log, RLGlist, name) or change)
			elif choice == '4':
				change = (self.erase(log, RLGlist, name) or change)
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
			
			self.print(True)
			
			choice = input('\n\nkeywords Choice').strip().lower()
			
			if choice in ['', 'q', 'quit', 'cancel']:
				log.menuOut()
				return None
			
			try:
				choice = int(choice)
			except ValueError:
				log.error('Integer value expected!')
				continue
			
			if choice < 0 or choice >= len(self.keywords)
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
			
			
			error = error.strip()
			if error > 0:
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
	
	
	
	
	
	def rename(self, log):
		'''A method to remove a keyword'''
		
	
	
	
	
	
	def erase(self, log):
		'''A method to remove a keyword'''
		
	
	
	
	
	
	
	
	
	
	
