#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage task list'''
import xml.etree.ElementTree as xmlMod
import os, re, math
from usefullFunctions import *
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
		page = 0
		
		while True:
			log.print()
			
			self.print(page)
			
			choice= input('action (h for help):').strip().lower()
			if choice in ['q', 'quit']:
				log.menuOut()
				return
			elif choice in ['p', 'pref', 'preferences']:
				preferences.menu(log, self)
			elif choice in ['a', 'add', '+']:
				if (self.add(log, preferences)):
					saveTasks(self)
			elif choice in ['d', '>', '']:
				if page < math.floor((len(self.tasks)-1)/25):
					page += 1
				elif choice == '':
					page = 0
			elif choice in ['u', '<']:
				if page > 0:
					page -= 1
			elif choice in ['h', 'help']:
				log.menuIn('Help')
				log.print()
				
				print('''\n\n        \033[4mHELP :\033[0m

Scroll up the list : u or <
Scroll down the list : d or > or just type enter

Add task : a or add or +
Edit/inspect a task : type the index of the task

Preferences access : p or pref or preferences
Help : h or help
Quit : q or quit

Not Yet Implement :
##
##
##Batch preset choice : b or batch
##See previous sessions logs : l or log
##Run tasks : r or run
##
##

''')
				
				input('Press enter to continue')
				log.menuOut()
			else:
				try:
					choice = int(choice)
				except:
					log.error('Unknow request!', False)
					continue
				
				if choice < 0 or choice >= len(self.tasks):
					log.error('There is no task n°'+str(choice)+'!', False)
					continue
				
				if(self.tasks[choice].menu(log, choice, self.tasks, preferences)):
					self.save()
	
	
	
	
	
	def print(self, page):
		'''A method to print the list of the task'''
		print('''
\033[4mID |  File Name              |  Scene                  |  Preset                 |\033[0m''')
		if page > 0:
			print('▲▲▲|▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲|▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲|▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲|')
		for i,task in enumerate(self.tasks[page*25:(page+1)*25]):
			row = columnLimit( (page*25+i), 3, 0)
			row += task.getRow()
			print(row)
		if (page+1)*25 <= len(self.tasks):
			print('▼▼▼|▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼|▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼|▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼|')
	
	
	
	
	
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
		preset = Task.presetChoice(log, preferences)
		
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
	
	
	
	
	
	def renamePreset(self, old, new):
		'''a method to rename used preset'''
		for task in self.tasks:
			task.renamePreset(old, new)
	
	
	
	
	
	
	def erasePreset(self, preset):
		'''a method to stop using preset'''
		for task in self.tasks:
			task.erasePreset(preset)
	
	
	
	
	
	def save(self):
		'''A method to save Tasks list'''
		saveTasks(self)
		
	
	
	
	
	
	
