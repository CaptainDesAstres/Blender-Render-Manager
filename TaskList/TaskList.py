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
	
	
	
	
	
	def __del__(self):
		'''Erase lock file in case of crash'''
		eraseLockFile()
		del(self.tasks)
	
	
	
	
	
	def defaultInit(self):
		'''initialize empty task list object'''
		
		self.tasks = []
		self.archive = []
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize task list object with saved task'''
		self.tasks = []
		for node in xml.find('tasks').findall('task'):
			self.tasks.append(Task(xml = node))
		
		self.archive = []
		for node in xml.find('archive').findall('task'):
			self.archive.append(Task(xml = node))
	
	
	
	
	
	def toXml(self):
		'''export task list into xml syntaxed string'''
		xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
		xml += '<tasklist>\n'
		
		xml += '<tasks>\n'
		for task in self.tasks:
			xml += task.toXml()
		xml += '</tasks>\n'
		
		xml += '<archive>\n'
		for task in self.archive:
			xml += task.toXml()
		xml += '</archive>\n'
		
		xml += '</tasklist>\n'
		return xml
	
	
	
	
	
	def menu(self, scriptPath, log, preferences):
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
			elif choice in ['r', 'run']:
				self.run(scriptPath, log, preferences)
				saveTasks(self)
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
			elif choice in ['b', 'batch']:
				if(self.batchEdit(log, preferences)):
					self.save()
			elif choice in ['h', 'help']:
				log.menuIn('Help')
				log.print()
				
				print('''\n\n        \033[4mHELP :\033[0m

Scroll up the list : u or <
Scroll down the list : d or > or just type enter

Add task : a or add or +
Edit/inspect a task : type the index of the task
Batch editing : b or batch
Run tasks : r or run

Preferences access : p or pref or preferences
Help : h or help
Quit : q or quit

Not Yet Implement :
##
##
##See previous sessions logs : l or log
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
				
				if(self.tasks[choice].menu(log, choice, self, preferences)):
					self.save()
	
	
	
	
	
	def print(self, page, selection = None, whole = False):
		'''A method to print the list of the task'''
		print('''
\033[4mID |  File Name              |  Scene                  |  Preset                 |\033[0m''')
		if page > 0:
			print('▲▲▲|▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲|▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲|▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲|')
		
		if selection is None or whole:
			selected = self.tasks[page*25:(page+1)*25]
			index = list(range(page*25, (page+1)*25))
		else:
			selection.sort()
			index = selection
			selected = []
			for i in selection:
				selected.append(self.tasks[i])
		for i,task in enumerate(selected):
			row = columnLimit( index[i], 3, 0)
			row += task.getRow()
			if whole and index[i] in selection:
				row = '\033[7m'+row+'\033[0m'
			print(row)
		
		
		if selection is not None and (page+1)*25 <= len(selected)\
			or selection is None and (page+1)*25 <= len(self.tasks):
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
		print(info)
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
		
	
	
	
	
	
	def remove(self, log, selected):
		'''A method to remove task from the list'''
		log.menuIn('Task(s) Removing')
		log.print()
		print('\n\n        Removing Selected Task :\n')
		self.print(0, selected)
		
		confirm = input('Do you realy want to erase this task?(y) ').strip().lower()
		
		log.menuOut()
		if confirm == 'y':
			selected.sort(reverse = True)
			for i in selected:
				self.tasks.pop(i)
			return True
		else:
			return False
	
	
	
	
	
	def move(self, log, selected):
		'''A method to move tasks into the list'''
		log.menuIn('Task(s) Moving')
		change = False
		selected.sort()
		
		while True:
			log.print()
			print('\n\n        Moving Selected Task :\n')
			self.print(0, selected, True)
			
			choice = input('how to move selected task : (h for help) ').strip().lower()
			
			if choice in ['', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change, selected
			elif choice in ['h', 'help']:
				log.menuIn('Help')
				log.print()
				input('''

        Help :

Move to
    Top of list :          t or top
    First selected task :  f or first
    Last selected task :   l or last
    Bottom of the list :   b or bottom
    Give row position :    Type the number of the row you want
Reverse order (if the task is not contiguous, they will be regroup after the first selected)
                           i or inverse or r or reverse
Save and quit :            empty string or q or quit or cancel
Help :                     h or help

Press enter to continue
''')
			elif re.search(r'^(t|f|l|b|(top)|(first)|(last)|(bottom)|(r)|(i)|(reverse)|(inverse)|(\d+))$', choice):
				reverse = choice in ['r', 'i', 'inverse', 'reverse']
				if choice in ['t', 'top']:
					choice = -1
				elif reverse or choice in ['f', 'first']:
					choice = selected[0]
				elif choice in ['l', 'last']:
					choice = selected[-1]
				elif choice in ['b', 'bottom']:
					choice = len(self.tasks)
				else:
					
					try:
						choice = int(choice)
					except ValueError:
						log.error('Unvalid action', False)
						continue
				
				selected = self.moveTo(log, selected, choice)
				
				if reverse:
					reorder = self.tasks[selected[0]: selected[-1]+1]
					reorder.reverse()
					self.tasks = self.tasks[0: selected[0] ] + reorder \
								+self.tasks[selected[-1]+1:]
				
				# correct task index in menu
				log.menuOut()
				log.menuOut()
				log.menuIn('Task n°'+','.join(str(x) for x in selected))
				log.menuIn('Task(s) Moving')
				
				change = True
			else:
				log.error('Unvalid action', False)
	
	
	
	
	
	def moveTo(self, log, selected, row):
		'''A method to move selected task to a position in the list'''
		selected.sort()
		isRange = selected == list(range(selected[0], selected[-1]+1))
		selected.reverse()
		selection = []
		
		for index in selected:
			selection.append(self.tasks.pop(index))
			if not isRange and row > index:
				row -= 1
		selection.reverse()
		
		if row <= 0:
			self.tasks = selection + self.tasks
			log.write('Task n°«'+','.join(str(x) for x in selected)+'» moved on top of the list')
			selected = list(range(0, len(selected)))
		elif row >= len(selection) + len(self.tasks):
			self.tasks += selection
			log.write('Task n°«'+','.join(str(x) for x in selected)+'» moved on bottom of the list')
			selected = list(range(len(self.tasks)-len(selected)-1 , len(self.tasks)))
		else:
			self.tasks = self.tasks[0:row]+selection+self.tasks[row:]
			log.write('Task n°«'+','.join(str(x) for x in selected)+'» moved on row '+str(row)+' of the list')
			selected = list(range(row, row + len(selected)))
		
		return selected
	
	
	
	
	
	def batchEdit(self, log, preferences):
		'''A method to batch edit task'''
		log.menuIn('Batch Editing')
		select = self.batchSelect(log)
		if len(select) == 0 :
			log.menuOut()
			return False
		
		log.menuIn('Task n°'+','.join(str(x) for x in select))
		change = False
		while True:
			log.print()
			print('\n\n        Batch Edit :\n')
			
			self.print(0, select)
			choice = input('''\nMenu :
1- Apply A Preset (don't work with started task)
2- Copy And Apply A Preset
3- Regroup And Move
4- Remove
5- Lock
6- Unlock
9- Change Selection
0- Quit
''')
			
			if choice in ['q', 'quit', 'cancel', '0']:
				log.menuOut()
				log.menuOut()
				return change
			elif choice == '1':
				change = (self.applyPreset(log, select, preferences) or change)
			elif choice == '2':
				new, confirm = self.copyTasks(log, select, preferences)
				if confirm:
					select = new
					change = True
			elif choice == '3':
				change = (self.move(log, select) or change)
			elif choice == '4':
				if self.remove(log, select):
					log.menuOut()
					log.menuOut()
					return True
			elif choice == '5':
				self.lock(select, log)
				change = True
			elif choice == '6':
				self.unlock(select, log)
				change = True
			elif choice == '9':
				log.menuOut()
				select = self.batchSelect(log, select)
				log.menuIn('Task n°'+','.join(str(x) for x in select))
			else:
				log.error('Unvalid request',False)
	
	
	
	
	
	def lock(self, select, log):
		'''a method to batch lock task'''
		modified = []
		unmodified = []
		for i in select:
			task = self.tasks[i]
			if task.status in ['ready', 'pause']:
				task.status = 'pendinglock'
				modified.append(i)
			elif task.status == 'waiting':
				task.status = 'lock'
				modified.append(i)
			else:
				unmodified.append(i)
		
		if len(modified)>0:
			log.write('Task n°«'+','.join(str(x) for x in modified)+'» have been locked.')
		if len(unmodified)>0:
			log.write('Task n°«'+','.join(str(x) for x in unmodified)+'» were already lock or unlockable.')
	
	
	
	
	
	def unlock(self, select, log):
		'''a method to batch unlock task'''
		modified = []
		unmodified = []
		for i in select:
			task = self.tasks[i]
			if task.status == 'pendinglock':
				task.status = 'pause'
				modified.append(i)
			elif task.status == 'lock':
				task.status = 'wait'
				modified.append(i)
			else:
				unmodified.append(i)
		
		if len(modified)>0:
			log.write('Task n°«'+','.join(str(x) for x in modified)+'» have been unlocked.')
		if len(unmodified)>0:
			log.write('Task n°«'+','.join(str(x) for x in unmodified)+'» were already unlock.')
	
	
	
	
	
	def batchSelect(self, log, select = None):
		'''A method to select multiple task'''
		log.menuIn('Multiple Task Selecting')
		if select is None:
			select = []
		page = 0
		mode = 'ADD'
		msg = 'What task to select [ADD mode] : '
		
		while True:
			log.print()
			print('\n\n        Multiple Selection :\n')
			self.print(page, select, True)
			
			choice = input(msg).strip().lower()
			
			if choice in ['quit', 'q', 'cancel']:
				log.menuOut()
				return select
			if choice in ['h', 'help']:
				log.menuIn('Help')
				log.print()
				
				print('''\n\n        \033[4mHELP :\033[0m

Scroll up the list : u or <
Scroll down the list : d or > or just type enter

\033[4mMode :\033[0m

Additive (ADD) mode : a or add or +
Subtractive (SUB) mode : s or sub or -
Switch (SWT) mode : switch or swt

In ADD mode, you select task by giving them number. In SUB mode, you unselect them the same way. In SWT mode, the same action will select those who are unselect and reciprocally.

\033[4mEnumerating :\033[0m

You can select task one by one by typing them number or select a range of task: 1-5 will select task 1 to 5 include. You can select all by typing all.

Help : h or help
Quit : q or quit

''')
				
				input('Press enter to continue')
				log.menuOut()
			elif choice  in ['u', '<']:
				if page > 0:
					page -= 1
			elif choice  in ['d', '>', '']:
				if page < math.floor((len(self.tasks)-1)/25):
					page += 1
				elif choice == '':
					page = 0
			elif choice  in ['a', 'add', '+']:
				mode = 'ADD'
				msg = 'What task to select [ADD mode] : '
			elif choice  in ['s', 'sub', '-']:
				mode = 'SUB'
				msg = 'What task to unselect [SUB mode] : '
			elif choice  in ['switch', 'swt']:
				mode = 'SWT'
				msg = 'What task to switch selecting [SWT mode] : '
			elif choice  in ['all']:
				if mode == 'ADD':
					select = list(range(0, len(self.tasks)))
				elif mode == 'SUB':
					select = []
				else:
					for i in range(0, len(self.tasks)):
						if i in select:
							select.remove(i)
						else:
							select.append(i)
			elif choice.count('-') == 1:
				try:
					choice = choice.split('-')
					last = min(int(choice.pop().strip()), len(self.tasks)-1)
					first = max(int(choice.pop().strip()), 0)
				except (ValueError, IndexError):
					log.error('your request is unvalid', False)
					continue
				
				inter = list(range(first, last+1))
				
				if mode == 'ADD':
					for i in inter:
						if i not in select:
							select.append(i)
					select.sort()
				elif mode == 'SUB':
					for i in inter:
						if i in select:
							select.remove(i)
				else:
					for i in inter:
						if i in select:
							select.remove(i)
						else:
							select.append(i)
					select.sort()
			else:
				try:
					choice = int(choice)
				except ValueError:
					log.error('your request ('+choice+') is unvalid', False)
					continue
				
				if mode == 'ADD' and choice not in select:
					select.append(choice)
					select.sort()
				elif mode == 'SUB' and choice in select:
					select.remove(choice)
				elif mode == 'SWT':
					if choice in select:
						select.remove(choice)
					else:
						select.append(choice)
						select.sort()
	
	
	
	
	
	def applyPreset(self, log, select, preferences):
		'''A method to apply a preset to multiple tasks'''
		preset = Task.presetChoice(log, preferences)
		
		modified = []
		started = False
		if preset is not None :
			for i in select:
				if self.tasks[i].log is None:
					modified.append(i)
					self.tasks[i].preset = preset
				else:
					started = True
			log.write('Task n°«'+','.join(str(x) for x in modified)+'» : Preset set to «'+preset+'»')
			if started:
				log.write('Some task preset can\'t be modify because they alreandy have been started.')
			return True
		return False
	
	
	
	
	
	def copyTasks(self, log, select, preferences):
		'''A method to copy a selection of task to apply them another preset'''
		log.menuIn('Batch Copy')
		
		log.menuIn('Position Choice')
		while True:
			log.print()
			print('\n\n        Copy : Positon Choice :\n\nChoice : \n\n1- Immediately after original task\n2- At the end of list\n0- Cancel')
			choice = input('choice : ').strip().lower()
			
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				log.menuOut()
				return select, False
			
			if choice in ['1', '2']:
				row = int(choice)
				break
			else:
				log.error('unvalid choice, accepted choice is 0 1 or 2', False)
				continue
		log.menuOut()
		
		preset = Task.presetChoice(log, preferences)
		if preset is None :
			log.menuOut()
			return select, False
		
		copies = []
		select.sort()
		for i in select:
			copies.append(self.tasks[i].copy())
		
		for t in copies:
			t.preset = preset
		
		if row == 2:
			newSelect = list(range(len(self.tasks),len(self.tasks) + len(copies)))
			self.tasks += copies
			log.write('Task n°«'+','.join(str(x) for x in select)+'» copied to row n°'+str(newSelect[0])+' to '+str(newSelect[-1])+' with «'+preset+'» preset')
			log.menuOut()
			return newSelect, True
		else:
			newSelect = []
			gap = 0
			for i in select:
				newSelect.append(i+1+gap)
				gap += 1
				self.tasks.insert(newSelect[-1], copies.pop(0))
			log.write('Task n°«'+','.join(str(x) for x in select)+'» copied to row n°'+','.join(str(x) for x in newSelect)+' with «'+preset+'» preset')
			log.menuOut()
			return newSelect, True
	
	
	
	
	
	def run(self, scriptPath, log, preferences):
		'''A method to run the task of the list'''
		log.menuIn('Run Tasks')
		run = True
		
		for i,task in enumerate(self.tasks):
			if task.status in ['lock', 'pendinglock']:
				run = True
			else:
				run = task.run(i+1, self, scriptPath, log, preferences)
			if not run:
				break
		log.menuOut()
	
	
	
	
	
	def upBackup(self, uid):
		'''up backup level in TaskLog'''
		for task in self.archive:
			if task.uid == uid:
				task.log.backup += 1
				self.save()
				return True
		
		for task in self.tasks:
			if task.uid == uid:
				task.log.backup += 1
				self.save()
				return True
		
		return False
	
	
	
	
	
	def eraseBackup(self, uid):
		'''mark erased task'''
		for task in self.archive:
			if task.uid == uid:
				task.log.status = 'erased'
				self.save()
				return True
		
		for task in self.tasks:
			if task.uid == uid:
				self.tasks.remove(task)
				self.archive.append(task)
				task.log.status = 'erased'
				self.save()
				return True
		
		return False
	
	
	
	
	
	
