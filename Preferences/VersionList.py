#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage list of all know version of Blender in the system'''
import xml.etree.ElementTree as xmlMod
import re
import os

class VersionList:
	'''class dedicated to Blender version managing'''
	
	
	def __init__(self, xml= None):
		'''initialize Blender version list with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize Blender version list with default value'''
		
		self.list = {'Standard Blender':'blender'}
		self.default = 'Standard Blender'
		
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize Blender version list with values extracted from an xml object'''
		self.list = {}
		for version in xml.findall('version'):
			self.list[version.get('alias')] = version.get('path')
		self.default = xml.get('default')
	
	
	
	
	
	def toXml(self):
		'''export Blender version list into xml syntaxed string'''
		
		xml = '  <versionsList default ="'+self.default+'" >\n'
		for k, v in self.list.items():
			xml += '    <version alias="'+k+'" path="'+v+'" />\n'
		xml += '  </versionsList>\n'
		
		return xml
	
	
	
	
	
	def menu(self, log, preferences):
		'''method to see Blender version list and access edition menu'''
		change = False
		log.menuIn('Blender Version List')
		
		while True:
			# print log and Blender versions list
			
			log.print()
			
			self.print()
			
			print('''\n    \033[4mMenu :\033[0m
1- Add version
2- Auto add version
3- Rename version
4- Remove version
5- Change Default Version
0- Save And Quit

''')
			
			
		
			#treat available actions
			choice= input('menu?').strip().lower()
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()# quit preferences menu
				return change
			elif choice == '1':
				change = (self.add(log) or change)
			elif choice == '2':
				change = (self.addAuto(log) or change)
			elif choice == '3':
				change = (self.rename(log, preferences) or change)
			elif choice == '4':
				change = (self.remove(log, preferences) or change)
			elif choice == '5':
				change = (self.chooseDefault(log) or change)
			else:
				log.error('Unknow request', False)
	
	
	
	
	
	def print(self, index = False, std = True, default = False):
		'''a method to display the Blender version list'''
		print('\n            \033[4mBlender Version List :\033[0m\n')
		
		keys = list(self.list.keys())
		keys.sort(key = str.lower)
		
		if not std:
			# don't display Standard Blender version if std is False
			keys.remove('Standard Blender')
		
		if index:
			for i, k in enumerate(keys):
				print(str(i)+'- '+k+' :\n    '+self.list[k]+'\n')
		else:
			for k in keys:
				print(k+' :\n    '+self.list[k]+'\n')
		
		if default and index:
			print(str(i+1)+'- [default] \n')
			keys.append('[default]')
		
		if not index:
			print('\n\nDefault version : '+self.default)
		
		return keys
	
	
	
	
	
	def add(self, log):
		'''a method to add a Blender version to the list'''
		log.menuIn('Add A Version')
		
		while True:
			# print log 
			
			log.print()
			
			# get new version path
			choice= input('\nPath of the new version?').strip()
			
			if choice == '':# quit
				log.menuOut()
				return False
			
			#remove quote mark and apostrophe in first and last character
			if choice[0] in ['\'', '"'] and choice[-1] == choice[0]:
				choice  = choice[1:len(choice)-1]
			
			# check that the path is absolute: begin by '/'
			if choice[0] != '/':
				log.error('The path must be absolute (begin by «/»)!')
				continue
			
			# check path exist 
			if not os.path.exists(choice):
				log.error('This path correspond to nothing!')
				continue
			
			# check path is a file
			if not os.path.isfile(choice):
				log.error('This path is not a file!')
				continue
			
			# check path is executable
			if not os.access(choice, os.X_OK):
				log.error('This file is not executable or you don\'t have the permission to do it!')
				continue
			
			# get blender version from blender path
			path = choice
			version = os.popen('"'+path+'" -b -P "'+os.path.realpath(__file__+'/..')+'/getter/getBlenderVersion.py" ').read()
			version = re.search(r'<\?xml(.|\n)*</root>',version).group(0)
			version = xmlMod.fromstring(version).find('version').get('version')
			alias = 'Blender ('+version+')'
			
			# recommand an unused alias
			if alias in self.list.keys():
				i = 0
				while alias+'('+str(i)+')' in self.list.keys():
					i+=1
				alias = alias+'('+str(i)+')'
			
			
			# get user alias confirmation
			log.menuIn('Choose An Alias')
			while True:
				# print log 
				
				log.print()
				print('\n\n\033[4mRecommanded alias :\033[0m '+alias)
				
				# get alias
				choice= input('\nPress enter to use recommanded alias or type wanted alias :').strip()
				
				if choice == '':
					log.menuOut()
					break
				elif re.search(r'^([-a-zA-Z0-9]| |\(|\)|\.){1,}$', choice) is None:
					log.error('alias can only contain alphanumeric (unaccented) characters, spaces, parentheses points and -')
					continue
				elif choice in self.list.keys():
					log.error('Alias already use for another version!')
					continue
				elif len(choice) < 7:
					log.error('Too small alias name (7 characters minimal)!')
					continue
				else:
					alias = choice
					log.menuOut()
					break
			
			# add version
			self.list[alias] = path
			log.write('('+alias+' : '+path+') Blender version added to list')
			log.menuOut()
			return True
	
	
	
	
	
	def addAuto(self, log):
		'''a method to automatically add to the list numerous Blender version that is located in the same directory'''
		log.menuIn('Automatically Add Versions')
		
		while True:
			# print log 
			
			log.print()
			print('\n\nAll Blender version directory must be directly in a same directory. Script will not recursivly search for blender version')
			
			# get new version path
			choice= input('\nPath of the main directory?').strip()
			
			if choice == '':# quit
				log.menuOut()
				return False
			
			# remove quote mark and apostrophe in first and last character
			if choice[0] in ['\'', '"'] and choice[-1] == choice[0]:
				choice  = choice[1:len(choice)-1]
			
			# check that the path is absolute: begin by '/'
			if choice[0] != '/':
				log.error('The path must be absolute (begin by «/»)!')
				continue
			
			# check path exist 
			if not os.path.exists(choice):
				log.error('This path correspond to nothing!')
				continue
			
			# check path is a file
			if not os.path.isdir(choice):
				log.error('This path is not a directory!')
				continue
			
			path = choice
			if path[-1] != '/':
				path += '/'
			subdirectories = os.listdir(path)
			for sub in subdirectories:
				
				# check if ther is a blender version in this directory
				versionPath = path+sub+'/blender'
				if os.path.isdir(path+sub)\
						and os.path.exists(versionPath)\
						and os.path.isfile(versionPath)\
						and os.access(versionPath, os.X_OK):
					
					# get Blender version
					version = os.popen('"'+versionPath+'" -b -P "'+os.path.realpath(__file__+'/..')+'/getter/getBlenderVersion.py" ').read()
					version = re.search(r'<\?xml(.|\n)*</root>',version).group(0)
					version = xmlMod.fromstring(version).find('version').get('version')
					
					# generate an alias
					alias = 'Blender ('+version+')'
					if alias in self.list.keys():
						i = 0
						while alias+'('+str(i)+')' in self.list.keys():
							i+=1
						alias = alias+'('+str(i)+')'
					
					# add to the list
					self.list[alias] = versionPath
					log.write('('+alias+' : '+versionPath+') Blender version added to list')
			
			log.menuOut()
			return True
			
	
	
	
	
	
	def rename(self, log, preferences):
		'''display a menu to rename version in the list'''
		log.menuIn('Rename Version')
		
		# choose version
		oldAlias = self.choose(log)
		if oldAlias is None:
			return False
		
		while True:
			
			log.print()
			
			print('\n\n        \033[4mRename version :\033[0m')
			print(oldAlias+'\n    '+self.list[oldAlias])
			
			choice = input('\nNew name :').strip()
			
			if choice == '':
				log.menuOut()
				return False
			
			if choice in self.list.keys():
				log.error('This alias name is already use by another version.')
				continue
			
			self.list[choice] = self.list[oldAlias]
			self.list.pop(oldAlias)
			if self.default == oldAlias:
				self.default = choice
			
			preferences.presets.renameBlenderVersion( oldAlias, choice)
			
			log.write(oldAlias+' version rename in '+choice+'.')
			log.menuOut()
			return True
	
	
	
	
	
	def choose(self, log, std = False, default = False):
		'''display a menu to choose a version to working on'''
		log.menuIn('Choose Version')
		
		while True:
			
			log.print()
			
			print('\n\n')
			keys = self.print(True, std, default)
			choice = input('\nIndex of the version that you want to use :').strip()
			
			if choice == '':
				log.menuOut()
				return None
			
			try:
				choice = int(choice)
			except ValueError:
				log.error('Unvalid version choice : must be an irteger or an empty string')
				continue
			
			if choice >= 0 and choice < len(keys):
				log.menuOut()
				return keys[choice]
			else:
				log.error('Unvalid version choice : bad index.')
				continue
	
	
	
	
	
	def remove(self, log, preferences):
		'''A method to manually remove version from the list'''
		log.menuIn('Remove Version')
		
		# choose version
		alias = self.choose(log)
		if alias is None:
			log.menuOut()
			return False
		
		
		log.print()
		
		print('\n\n        \033[4mRemove version :\033[0m')
		print(alias+'\n    '+self.list[alias])
		
		
		if self.default == alias:
			print('\n\033[31mthis is actually the default version. if you erase it, default version will be set to de blender standard command.\033[0m')
		versionUsed = preferences.presets.useBlenderVersion(alias)
		if versionUsed:
			print('\n\033[31mThis version is actually used by some preset. If you erase it, the preset will automatically be changed to use default version.\033[0m')
		choice = input('\nDo you realy want to erase this version (y)?').strip().lower()
		
		
		
		if choice in ['y', 'yes']:
			self.list.pop(alias)
			if self.default == alias:
				self.default = 'Standard Blender'
			if versionUsed:
				preferences.presets.eraseBlenderVersion(alias)
			log.write('Remove "'+alias+'" version.')
			log.menuOut()
			return True
		log.menuOut()
		return False
	
	
	
	
	
	
	def chooseDefault(self, log):
		'''A method to choose the default version to use'''
		log.menuIn('Choose Default Version')
		
		# choose version
		alias = self.choose(log, True)
		
		if alias is None:
			log.menuOut()
			return False
		
		self.default = alias
		log.write('Default version set to "'+self.default+'" version.')
		log.menuOut()
		return True
	
	
	
	
	
	def getDefaultPath(self):
		'''a method to get the path of the default version'''
		return self.getVersionPath(self.default)
	
	
	
	
	
	def getVersionPath(self, versionName):
		'''a method to get the path of a version'''
		if versionName == '[default]':
			versionName = self.default
		path = self.list[versionName]
		if path != 'blender':
			path = '"'+path+'"'
		return path
		
	
	
	
	
	
	
	
