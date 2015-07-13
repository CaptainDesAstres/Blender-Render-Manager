#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage task list'''
import xml.etree.ElementTree as xmlMod
import os, re
from save import *
from TaskList.Task import *
from TaskList.FileInfo.FileInfo import *

class TaskList:
	'''class to manage task list'''
	
	
	def __init__(self, xml= None):
		'''initialize task list object, empty or with saved task'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize empty task list object'''
		
		self.tasks = []
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize task list object with saved task'''
		self.tasks = []
		for node in xml.findall('task'):
			self.tasks.append(Task(xml = node))
	
	
	
	
	
	def toXml(self):
		'''export task list into xml syntaxed string'''
		xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
		xml += '<tasks>\n'
		
		for task in self.tasks:
			xml += task.toXml()
		
		xml += '</tasks>\n'
		return xml
	
	
	
	
	
	def menu(self, log, preferences):
		'''method to see task list and manage it'''
		log.menuIn('Task List')
		
		while True:
			log.print()
			
			choice= input('action (h for help):').strip().lower()
			if choice in ['q', 'quit']:
				log.menuOut()
				return
			elif choice in ['p', 'pref', 'preferences']:
				preferences.menu(log)
			elif choice in ['a', 'add', '+']:
				if (self.add(log, preferences)):
					saveTasks(self)
			elif choice in ['h', 'help']:
				log.menuIn('Help')
				log.print()
				
				print('''\n\n        \033[4mHELP :\033[0m

Add task : a or add or +
Help : h or help
Quit : q or quit
Preferences access : p or pref or preferences
Not Yet Implement :
##
##
##Edit/inspect task : type the index of the task to edit
##Batch task editing : b or batch
##See previous sessions logs : l or log
##Run tasks : r or run
##
##

''')
				
				input('Press enter to continue')
				log.menuOut()
			else:
				log.error('Unknow request!', False)
	
	
	
	
	
	def add(self, log, preferences):
		log.menuIn('Add Task')
		
		log.menuIn('File Path')
		while True:
			log.print()
			
			print('\n\n        Add File :')
			
			path = input("\n\nWhat's the absolute path of the file to add (empty input to quit)").strip()
			
			if path.lower() in ['', 'cancel', 'quit', 'q']:
				# cancel action
				log.menuOut()# quit Add Task
				log.menuOut()# quit Give File Path
				return False
			
			
			if path[0] in ['\'', '"'] and path[-1] == path[0]:
				# remove quote mark and apostrophe in first and last character
				path = path[1:len(path)-1]
			
			if path[0] != '/':
				# check if path is absolute (begin by '/')
				log.error('"'+path+'" path is not absolute (need to begin by "/").')
				continue
			elif len(path) < 7 or re.search(r'.blend\d{0,10}$', path) is None:
				# check if path point to a .blend file
				log.error('"'+path+'" path don\'t seemed to be a blender file (need .blend extension).')
				continue
			elif not os.path.exists(path) or not os.path.isfile(path) or not os.access(path, os.R_OK):
				# check if the file exist
				log.error('"'+path+'" didn\'t exist, is not a file or is not readable!')
				continue 
			log.menuOut()
			break
		
		# open the file and get settings
		log.write('Try to add "'+path+'" task:')
		
		# try to open file and get infos
		info = os.popen('('+preferences.blenderVersion.getDefaultPath()\
			+' -b "'+path+'" -P "'\
			+os.path.realpath(__file__+'/..')+'/getter/getFileTaskInfos.py") || echo \'BlenderVersionError\' ').read()
		
		if info.count('BlenderVersionError') != 0:
			log.error('Blender version call error! Try to verified the path of default blender version!', False)
			log.menuOut()
			log.write('  Blender Version Error : abort task adding')
			return False
		
		info = re.search(r'<\?xml(.|\n)*</fileInfo>',info).group(0)
		info = xmlMod.fromstring(info)
		info = FileInfo(info)
		
		# scene choice
		scenes = info.sceneChoice(log)
		if scenes is None:
			log.menuOut()
			return False
		
		
		# preset choice
		log.menuIn('Preset Choice')
		log.print()
		print('\n\n        \033[4mPreset Choice :\033[0m\n\n')
		confirm = input('Use «'+preferences.presets.default+'» default preset? (type anything else that y or yes to choose another one)')
		
		if confirm in ['', 'y', 'yes']:
			preset = preferences.presets.default
		else:
			preset = preferences.presets.choose(log)
		log.menuOut()
		
		if preset is None:
			log.menuOut()
			log.write('  No preset choose, abort')
			return False
		
		log.write('  Use «'+preset+'» preset')
		
		# add the task(s)
		for scene in scenes:
			self.tasks.append( Task(
								path = path,
								scene = scene,
								preset = preset,
								fileInfo = info
								) )
		if len(scenes) == 1:
			log.write('  Task added')
		else:
			log.write('  '+str(len(scenes))+' tasks added')
		
		log.menuOut()
		return True
	
	
	
	
	
	
	
	
	
	
	
