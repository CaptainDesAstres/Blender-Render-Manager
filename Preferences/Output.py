#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage rendering output path'''
import xml.etree.ElementTree as xmlMod
import os, re
from shutil import rmtree as rmdir
from usefullFunctions import indexPrintList, XML
from Preferences.PresetList.Preset.Metapreset import *

class Output:
	'''class to manage rendering output path'''
	
	
	def __init__(self, xml= None):
		'''initialize output path with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize output path with default value'''
		
		if not os.path.exists('/home/'+os.getlogin()+'/.BlenderRenderManager/render'):
			os.mkdir('/home/'+os.getlogin()+'/.BlenderRenderManager/render')
		self.path = '/home/'+os.getlogin()+'/.BlenderRenderManager/render/'
		self.pattern = 'N/S/M/V/L/F'
		self.overwrite = False
		self.backupLimit = 5
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize output path with values extracted from an xml object'''
		self.path = xml.get('path')
		self.pattern = xml.get('pattern')
		self.overwrite = {'True':True, 'False':False}[xml.get('overwrite')]
		self.backupLimit = int(xml.get('backup'))
	
	
	
	
	
	def toXml(self):
		'''export output path into xml syntaxed string'''
		return '<output path="'+XML.encode(self.path)+'" pattern="'+self.pattern\
			+'" overwrite="'+str(self.overwrite)+'" backup="'+str(self.backupLimit)+'" />\n'
	
	
	
	
	
	def menu(self, log):
		'''method to see output path and access edition menu'''
		change = False
		log.menuIn('Output')
		
		while True:
			
			log.print()
			
			print('\n')
			self.print()
			
			print('''\n\n        \033[4mMenu :\033[0m
1- Edit path
2- Edit patterns
3- Switch overwrite mode
4- Change backup limit (only in «backup» overwriting mode)
0- Save And Quit

''')
			choice = input().strip().lower()
			
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			elif choice == '1':
				# edit output path
				change = (self.editPath(log) or change)
			elif choice == '2':
				# edit output pattern
				change = (self.editPattern(log) or change)
			elif choice == '3':
				# switch overwriting mode
				change = (self.switchOverwrite(log) or change)
			elif choice == '4':
				# edit backup limit
				change = (self.editBackupLimit(log) or change)
			else:
				log.error('Unvalid menu index!', False)
	
	
	
	
	
	def print(self):
		'''a method to display the output path settings'''
		
		print('\033[4mOutput path :\033[0m')
		print('      '+self.path)
		print('\n\033[4mOutput pattern :\033[0m')
		print('      '+self.pattern)
		print('\n\033[4mOverwriting :\033[0m')
		print('      '+{True:'enabled', False:'backup'}[self.overwrite])
		if not self.overwrite:
			print('\n\033[4mBackup limit :\033[0m')
			if self.backupLimit == 0:
				print('      No limit')
			else:
				print('      '+str(self.backupLimit))
	
	
	
	
	
	def editPath(self, log):
		'''method to manually edit output path'''
		log.menuIn('Edit Path')
		
		while True:
			
			log.print()
			
			#print current path and ask the new one
			print('\nCurrent output path : '+self.path)
			choice = input('\n\nwhat\'s the path to use ?(absolute path required, surround path by \' or " if it contains space)').strip()
			if choice == '':
				log.menuOut()
				return False
			
			
			# remove ' and/or "
			if choice[0] in ['\'', '"'] and choice[-1] == choice[0]:
				choice  = choice[1:len(choice)-1]
			
			# check it's absolute path
			if choice[0] != '/':
				log.error('The path must be absolute (begin by «/»)!')
				continue
			
			# check path exist 
			if not os.path.exists(choice):
				log.error('This path correspond to nothing!')
				continue
			
			# check path is a directory
			if not os.path.isdir(choice):
				log.error('This path don\'t correspond to a directory!')
				continue
			
			# check path is writable
			if not os.access(choice, os.W_OK):
				log.error('You don\'t have the permission to write in this directory!')
				continue
			
			if choice[-1] != '/':
				choice += '/'
			
			# apply path settings and confirm
			self.path = choice
			log.write('Output path set to : '+self.path)
			log.menuOut()
			return True
	
	
	
	
	
	def editPattern(self, log):
		'''method to manually edit output pattern'''
		log.menuIn('Edit Pattern')
		# list available pattern
		patterns = [
					'M/N/S/V/L/F',
					'M/N/S/V/L - F',
					'M/N/S/V/F - L',
					'M/N - S/V/L/F',
					'M/N - S/V/L - F',
					'M/N - S/V/F - L',
					'N/S/M/V/L/F',
					'N/S/M/V/L - F',
					'N/S/M/V/F - L',
					'N - S/M/V/L/F',
					'N - S/M/V/L - F',
					'N - S/M/V/F - L'
					]
		
		
		while True:
			
			log.print()
			print('\n\n')
			
			# print available pattern and current one and ask the new one
			indexPrintList(patterns)
			print('\nCurrent pattern : '+self.pattern)
			choice = input('\n\nwhat\'s the pattern to use?(h for help)').strip().lower()
			
			# quit menu
			if choice in ['', 'q', 'quit', 'cancel']:
				log.menuOut()
				return False
			
			#display help
			if choice == 'h':
				
				log.menuIn('Help')
				log.print()
				print('''\n        \033[4mPattern Help\033[0m

Choose a pattern for output file naming and directory tree. 
Part delimited by '/' will be directory and final part will be the output file name. 
part separate by '-' will be in the same directory/file name.

«N» will be replace by the file name
«S» will be replace by the scene name
«L» will be replace by the renderlayer group alias (only if metapreset is used)
«F» will be replace by the number of the frame
«M» will be replace by the name of the preset/metapreset used to render it

«V» will be used only if overwrite mode is set to backup and if a previous rendering output is detect in target path. the previous rendering will be moved to a directory called «previous rendering 1» and, if this directory already exist, it will be renamed in «previous rendering 2» and recursively until backup setting limit

Press enter to continue''')
				input()
				log.menuOut()
				continue
			
			# convert choice in int
			try:
				choice = int(choice)
			except ValueError:
				log.error('Unvalid pattern choice')
				continue
			
			# check choice is valid
			if choice < 0 or choice >= len(patterns):
				log.error('Out of range pattern choice.')
				continue
			
			# apply new settings and quit
			self.pattern = patterns[choice]
			log.write('Pattern set to : '+patterns[choice])
			log.menuOut()
			return True
	
	
	
	
	
	def switchOverwrite(self, log):
		'''A method to switch Overwrite settings'''
		self.overwrite = not self.overwrite
		log.write('Overwrite mode set to '+{True:'enabled', False:'backup'}[self.overwrite])
		return True
	
	
	
	
	
	def editBackupLimit(self, log):
		'''A method to edit Backup limit'''
		log.print()
		
		print('\n\n        Backup limit :\n\n')
		print('Current Backup Limit : '+str(self.backupLimit))
		print('\n\nThis setting define the maximal number of backup to keep when overwrite mode is set to backup. Type the limit you want or 0 for no limit. If you really want no backup at all, switch to overwrite «enabled» mode.\n\n')
		limit = input('new limit :').strip().lower()
		
		try:
			limit = int(limit)
		except ValueError:
			log.error('Integer value expected!', False)
			return False
		
		if limit < 0:
			log.error('Positive value expected!', False)
			return False
		
		self.backupLimit = limit
		if self.backupLimit == 0:
			log.write('Backup limit disabled')
		else:
			log.write('Backup limit set to '+str(self.backupLimit))
		return True
	
	
	
	
	
	def backup(self, path, taskList):
		'''make backup moving operation'''
		# level up the backup
		self.upBackup(path, 1, taskList)
		
		# list content of path and split backup element in dedicated list
		content = os.listdir(path)
		backup = []
		backupRegex = re.compile(r'^previous rendering \d+$')
		for c in content[:]:
			if backupRegex.match(c) is not None:
				backup.append(c)
				content.remove(c)
		
		# move all remaining file in new first level backup directory
		if len(content) > 0:
			if os.path.exists(path+'task.setting') and os.path.isfile(path+'task.setting')\
					and os.access(path+'task.setting', os.R_OK):
				with open(path+'task.setting','r') as taskFile:
					uid =  xmlMod.fromstring(taskFile.read()).get('uid')
				taskList.upBackup(uid)
			os.mkdir(path+'previous rendering 1')
			for c in content:
				os.rename(path+c,path+'previous rendering 1/'+c )
		
		# apply backup limitation by erasing greater level backup
		if self.backupLimit > 0:
			for b in backup:
				level = int(b[19:])
				if level > self.backupLimit:
					
					settingPath = path+b+'/task.setting'
					if os.path.exists(settingPath) and os.path.isfile(settingPath)\
							and os.access(settingPath, os.R_OK):
						with open(settingPath,'r') as taskFile:
							uid =  xmlMod.fromstring(taskFile.read()).get('uid')
						taskList.eraseBackup(uid)
					
					rmdir(path+b)
		
		
	
	
	
	
	
	def upBackup(self, path, level, taskList):
		'''check recursivly if level backup exist and up there level'''
		if os.path.exists(path+'previous rendering '+str(level)):
			self.upBackup(path, level+1, taskList)
			settingPath = path+'previous rendering '+str(level)+'/task.setting'
			if os.path.exists(settingPath) and os.path.isfile(settingPath)\
					and os.access(settingPath, os.R_OK):
				with open(settingPath,'r') as taskFile:
					uid =  xmlMod.fromstring(taskFile.read()).get('uid')
				taskList.upBackup(uid)
			os.rename(path+'previous rendering '+str(level), path+'previous rendering '+str(level+1))
	
	
	
	
	
	def checkAndCreate(self, task, preferences, taskList):
		'''check if output directory exist and create it if they don't. check if there is path colliding/previous rendering and resolve the maters.'''
		
		# check main output path
		if not os.path.exists(self.path):
			log.write('\033[31mOutput path don\'t exist!\033[0m')
			return False
		if not os.path.isdir(self.path):
			log.write('\033[31mOutput path is not a directory!\033[0m')
			return False
		if not os.access(self.path, os.W_OK):
			log.write('\033[31mYou don\'t have the right to write in the output path!\033[0m')
			return False
		
		# get necessary naming info
		fileName = task.path.split('/').pop()
		ext = fileName.rfind('.blend')
		if ext != -1 :
			fileName = fileName[0:ext]
		
		scene = task.scene
		
		preset = task.preset
		if preset == '[default]':
			preset = preferences.presets.default
		
		if type(preferences.presets.getPreset(preset)) is Metapreset:
			groups = list(preferences.presets.getPreset(preset).groups.keys())
			groups = task.getUsefullGroup(groups, preferences)
		else:
			groups = []
		
		# generate the path dedicated to the blender file/scene and the preset used by the task
		mainPath = self.getMainPath(fileName, scene, preset)
		
		# check the path with preset file name and scene name exist
		if os.path.exists(mainPath):
			# if the path exist, check for old render and move it in backup directory or erase it
			if self.overwrite:
				content = os.listdir(mainPath)
				for f in content:
					if os.path.isfile(mainPath+f):
						os.remove(mainPath+f)
					else:
						rmdir(mainpath+f)
			else:
				self.backup(mainPath, taskList)
		else:
			# if the path didn't exist, make it
			os.makedirs(mainPath)
		
		if self.pattern.count('/L/')>0:
			for g in groups:
				os.mkdir(mainPath+g)
		
		# create file to let know the state and settings of the task
		self.outputTaskInfo(task, groups, preferences, mainPath)
	
	
	
	
	
	def outputTaskInfo(self, task, groups, preferences, path):
		'''create a file containing the settings of the task in the output path'''
		taskInfo = '<?xml version="1.0" encoding="UTF-8"?>\n<root status="ready" uid="'+task.uid+'">\n'
		
		maxAnim = task.info.scenes[task.scene].end- task.info.scenes[task.scene].start + 1
		for g in groups:
			taskInfo += '<group name="'+g+'" anim="'
			anim = preferences.presets.getPreset(task.preset).animation[g]
			if anim == 0 or anim > maxAnim:
				taskInfo += str(maxAnim)+'" />\n'
			else:
				taskInfo += str(anim)+'" />\n'
		
		taskInfo += '<setting>\n'
		taskInfo += task.toXml()
		taskInfo += preferences.toXml(preferences.presets.getPreset(task.preset), False)
		taskInfo += '</setting>\n'
		
		taskInfo += '</root>\n'
		with open(path+'task.setting','w') as taskFile:
			taskFile.write(taskInfo)
	
	
	
	
	
	def getMainPath(self, fileName, sceneName, mainPreset):
		'''return main path of the task (the path that contains all group)'''
		pattern = self.pattern[0:self.pattern.find('/V')].split('/')
		mainpath = self.path
		
		for c in pattern:
			if c == 'M':
				mainpath += mainPreset+'/'
			elif c == 'N':
				mainpath += fileName+'/'
			elif c == 'S':
				mainpath += sceneName+'/'
			elif c == 'N - S':
				mainpath += fileName+' - '+sceneName+'/'
		
		return mainpath
	
	
	
	
	
	def getComplementPath(self, group):
		'''return output path complement'''
		if self.pattern.count('/L/') > 0:
			return group+'/'
		else:
			return ''
	
	
	
	
	
	def getNaming(self, group):
		'''return output file naming'''
		naming = self.pattern.split('/').pop()
		if naming == 'F':
			return '####'
		elif naming == 'L - F':
			return group+' - ####'
		elif naming == 'F - L':
			return '#### - '+group
		else:
			return None
	
	
	
	
	
	
	
	
	
