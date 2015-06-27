#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module that contain queue class'''
from renderingTask import renderingTask
import os, re
from usefullFunctions import *
from save import *
import xml.etree.ElementTree as xmlMod

class queue:
	'''class who contain the list of all the rendering task to manage'''
	
	menu = [
		{'menuEntry':'Scene Name',					'id':0,
		'headerLabel':'Scene Name          |',		'limit':20},
		
		{'menuEntry':'Status',						'id':1,
		'headerLabel':'Status  |',					'limit':8},
		
		{'menuEntry':'Back/Foreground animation',	'id':2,
		'headerLabel':'B/F Anim |',					'limit':9},
		
		{'menuEntry':'Animation Rate (fps)',		'id':3,
		'headerLabel':'Fps|',						'limit':3},
		
		{'menuEntry':'Duration',					'id':4,
		'headerLabel':'Duration|',					'limit':8},
		
		{'menuEntry':'Start/End Frame',				'id':5,
		'headerLabel':'Start-End|',					'limit':9},
		
		
		
		{'menuEntry':'Blender Path',				'id':6,
		'headerLabel':'Blender             |',		'limit':20},
		
		{'menuEntry':'Engine (Devices)',			'id':7,
		'headerLabel':'eng.(Dev)|',					'limit':9},
		
		{'menuEntry':'Tiles Size',					'id':8,
		'headerLabel':'Tiles  |',					'limit':7},
		
		{'menuEntry':'Resolution',					'id':9,
		'headerLabel':'Resolution     |',			'limit':15},
		
		{'menuEntry':'Samples Main/Back/Fore',		'id':10,
		'headerLabel':'Samples A./B./F. |',			'limit':17},
		
		{'menuEntry':'Simplify',					'id':11,
		'headerLabel':'Simp.|',						'limit':5},
		
		
		
		{'menuEntry':'Output Format',				'id':12,
		'headerLabel':'Format|',					'limit':6},
		
		{'menuEntry':'Transparent Background',		'id':13,
		'headerLabel':'Alpha Back.|',				'limit':11},
		
		{'menuEntry':'Z Pass',						'id':14,
		'headerLabel':'Z Pass|',					'limit':6},
		
		{'menuEntry':'Object Index Pass',			'id':15,
		'headerLabel':'Obj. Ind.|',					'limit':9},
		
		{'menuEntry':'Compositing',					'id':16,
		'headerLabel':'Compo.|',					'limit':6},
		
		{'menuEntry':'Exposure',					'id':17,
		'headerLabel':'Expos.|',					'limit':6},
		
		
		
		{'menuEntry':'Bounces Min/Max',				'id':18,
		'headerLabel':'Bounces m/M|',				'limit':11},
		
		{'menuEntry':'Transparent Bou. Min/Max',	'id':19,
		'headerLabel':'Transparence m/M|',			'limit':16},
		
		{'menuEntry':'Dif./Glo./Tra./Vol.',			'id':20,
		'headerLabel':'Di/Gl/Tr/Vo|',				'limit':11},
		
		{'menuEntry':'Diffuse Bounces',				'id':21,
		'headerLabel':'Diff.|',						'limit':5},
		
		{'menuEntry':'Glossy Bounces',				'id':22,
		'headerLabel':'Glo.|',						'limit':4},
		
		{'menuEntry':'Transmission Bounces',		'id':23,
		'headerLabel':'Trans.|',					'limit':6},
		
		{'menuEntry':'Volumes Bounces',				'id':24,
		'headerLabel':'Vol.|',						'limit':4},
		
		
		
		{'menuEntry':'BI Tiles',				'id':25,
		'headerLabel':'BI Tiles |',						'limit':9},
		
		{'menuEntry':'GPU Tiles',				'id':26,
		'headerLabel':'GPU Tiles|',						'limit':9},
		
		{'menuEntry':'CPU Tiles',				'id':27,
		'headerLabel':'CPU Tiles|',						'limit':9}
		]
	
	def __init__(self,xml=False):
		'''initialize queue object with empty queue who is filled with values extract from an xml object if paste to the function'''
		self.tasks = []
		if xml != False:
			self.fromXml(xml)
	
	
	
	
	def fromXml(self,xml):
		'''extract rendering task parameters from an xml object and add them to the queue'''
		if xml.tag == 'queue':
			for t in xml.findall('task'):
				self.add(renderingTask(xml = t))
	
	
	
	
	
	def toXmlStr(self,head=False):
		'''export rendering task queue to an xml syntax string '''
		txt =''
		if head:
			txt+= '<?xml version="1.0" encoding="UTF-8"?>\n'
		txt += '<queue>\n'
		for r in self.tasks:
			txt += r.toXmlStr()
		txt += '</queue>\n'
		return txt
	
	
	
	
	
	def add(self,added):
		'''add rendering task to the queue''' 
		if type(added) == renderingTask:
			self.tasks.append(added)
	
	
	
	
	
	def list(self, log, pref, mainPath):
		'''list task and access editing functions'''
		select = 0
		log.menuIn('Rendering Queue List')
		cols = [ 0, 4, 7, 2, 1 ]
		header, colSize = self.getListHeader(cols)
		
		while True:
			os.system('clear')
			log.print()
			
			print('	Render list :\n')
			print('\033[4m'+header+'\033[0m')
			self.printList(cols, colSize, select)
			
			choice = input("action?(\'h\' to see help)").strip().lower()
			
			try:
				if choice in ['q', 'quit', 'cancel']:
					choice = -1
				elif choice == 'l':
					choice = -2
				elif choice == 'a':
					choice = -3
				elif choice == 'r':
					choice = -4
				elif choice == 'e':
					choice = -5
				elif choice in['u', '+']:
					choice = -6
				elif choice in['d', '-']:
					choice = -7
				elif choice in['t', '++']:
					choice = -8
				elif choice in['b', '--']:
					choice = -9
				elif choice == 'm':
					choice = -10
				elif choice in ['h', 'help', 'man', 'manual', 'wtf']:
					choice = -9998
				else:
					choice = int(choice)
			except ValueError:
				choice = -9999
			
			if choice == -1:
				log.menuOut()
				return
			
			if choice >= 0:
				# select a task
				if choice >= len(self.tasks):
					log.write('\033[31mTask selecting error : there is no task n°'+str(choice)+'\033[0m\n')
				else:
					select = choice
					log.write('Select task n°'+str(choice)+'\n')
				
			elif choice == -2:
				# change displayed attribute of the list
				cols, header, colSize = self.attrListChoice(log, cols)
				
			elif choice == -3:
				# add task ot the list
				self.addTask(log, pref, mainPath)
				select = len(self.tasks)-1
				
			elif choice == -4:
				# remove the task from the queue
				if len(self.tasks)>0:
					self.tasks.pop(select)
					if select >= len(self.tasks):
						select -= 1
					saveQueue(self)
				
			elif choice == -5:
				# edit settings of the selected task
				self.tasks[select].taskSettingsMenu(log, pref)
				saveQueue(self)
				
			elif choice in [-6, -7, -8, -9]:
				# move selected task
				t = self.tasks.pop(select)
				if choice == -6:
					# move up
					select -= 1
					if select < 0:
						select = 0
				elif choice == -7:
					# move down
					select += 1
					if select > len(self.tasks):
						select -=1
				elif choice == -8:
					# move to top
					select = 0
				elif choice == -9:
					# move to bottom
					select = len(self.tasks)
				self.tasks.insert(select, t)
				saveQueue(self)
				
			elif choice == -10:
				self.multiEdit(log, pref, cols, colSize, header)
				#saveQueue(self)
				
			elif choice == -9998:
				os.system('clear')
				log.menuIn('Help')
				log.print()
				print('''        \033[4mRender Queue Help:\033[0m

    \033[4mGeneral action :\033[0m
l =>	Change the settings displayed in the list
q =>	Quit 'Render Queue List' menu
h =>	Show this page
a =>	Add task
m =>	edit settings for multiple tasks

    \033[4mIndividual action :\033[0m
The highlight row are selected task. the following action are apply to this task.
To select another task, type the corresponding number
r =>	Remove selected task
e =>	Edit settings of selected task

u =>	Move up the selected task
+ =>	Alias for u
d =>	Move down the selected task
- =>	Alias for d

t =>	Move selected task to the top of the list
++ =>	Alias for t
b =>	Move selected task to the bottom of the list
-- =>	Alias for b
''')
				input('type enter to continue')
				log.menuOut()
			else:
				log.write('\033[31mRendering Queue : unknow action\033[0m\n')
			
	
	
	
	
	def printList(self, cols, colSize, select = None, onlySelected = False):
		'''a method to print the list of all task in the queue'''
		if onlySelected and type(select) is list:
			for i in select:
				ident = str(i)+(' '*(4-len(str(i))))+'|'
				print(ident+self.tasks[i].getListRow(cols, colSize))
			
		elif select is None or select == []:
			for i, task in enumerate(self.tasks):
				ident = str(i)+(' '*(4-len(str(i))))+'|'
				print(ident+task.getListRow(cols, colSize))
			
		else:
			if type(select) is int:
				select = [select]
			for i, task in enumerate(self.tasks):
				ident = str(i)+(' '*(4-len(str(i))))+'|'
				if i in select:
					print('\033[30;47m'+ident+task.getListRow(cols, colSize)+'\033[0m')
				else:
					print(ident+task.getListRow(cols, colSize))
		
	
	
	
	
	
	def getListHeader(self, cols, thirdLimit = True):
		'''a method to get list header and column size for a list of attributes'''
		header = 'id  |Task File Name                |'
		size = []
		
		for col in cols:
			header += queue.menu[col]['headerLabel']
			size.append(queue.menu[col]['limit'])
		
		if thirdLimit == False and len(size) == 3:
			header = header.rstrip('|')+(' '* (60-size[2]) )+'|'
			size[2] = 60
		
		return header, size
	
	
	
	
	
	def attrListChoice(self, log, cols):
		'''a method to choose the attribut to display in the list'''
		os.system('clear')
		log.menuIn('list attribute choice')
		log.print()
		
		
		while True:
			# print attributes choice
			y = 0
			txt =''
			while y < 6:
				x = 0
				while x < 4:
					n = y + (6 * x)
					txt += columnLimit(str(n)+'- '+queue.menu[n]['menuEntry'], 30)
					x += 1
				txt += '\n'
				y += 1
			n += 1
			txt += (' '*30+'|')*3\
					+columnLimit(str(n)+'- '+queue.menu[n]['menuEntry'], 30)+'\n'
			print(txt)
			
			# explain and get user choice
			print('choice attribute to display by typing there number, split by "." character and in wanted order (5 max).\nexample : «0.4.7.2.1» (correspond to default attribute displayed)')
			choice = input("'q' to quit : ").strip().lower()
			
			# get quit choice
			if choice in ['q', 'quit', 'cancel', '']:
				log.menuOut()
				header, colSize = self.getListHeader(cols)
				return cols, header, colSize 
			
			# convert choice in int list
			choice = choice.split('.')
			error = False
			for i, n in enumerate(choice):
				try:
					choice[i] = int(choice[i].strip())
				except ValueError:
					error = True
					break
			
			# treat non-numeric entries
			if error:
				log.write('\033[31mList Attribute Choice Error : only numerical value is accept!\033[0m\n')
				continue
			
			# check there is no more than 5 columns
			if len(choice) > 5:
				log.write('\033[31mList Attribute Choice Error : only 5 attributes can be simultaneously display in the list!\033[0m\n')
				continue
			
			# check all number correspond to an existing menu entry
			for n in choice:
				if n > 24 or n < 0:
					error = True
					break
			if error:
				log.write('\033[31mList Attribute Choice Error : one of the number is unvalid!\033[0m\n')
				continue
			log.write('List Attribute Choice : '+'.'.join(str(x) for x in choice)+'\n')
			header, size = self.getListHeader(choice)
			log.menuOut()
			return choice, header, size
	
	
	
	
	
	def addTask(self, log, pref, mainPath):
		'''method to manually add rendering task'''
		
		log.menuIn('Add Task')
		log.menuIn('Give File Path')
		
		while True:
			os.system('clear')
			log.print()
			path = input("Add File\n  ABSOLUTE path of the blender file (or 'cancel')").strip()
			
			if path in ['cancel', 'quit', 'CANCEL', 'QUIT', 'q', 'Q']:
				#cancel action
				log.write('\033[31mquit add task menu\033[0m\n')
				log.menuOut()# quit Add Task
				log.menuOut()# quit Give File Path
				return
			
			
			if path[0] in ['\'', '"'] and path[-1] in ['\'', '"']:
				#remove quote mark and apostrophe in first and last character
				path = path[1:len(path)-1]
				print(path)
			
			if path[0] != '/':
				#check if path is absolute (begin by '/')
				print('it\'s not an absolute path!')
				log.write('\033[31munabsolute path reject :'+path+'\033[0m\n')
				continue
				
			elif len(path) < 7 or path[len(path)-6:] !='.blend':
				#check if path point to a .blend file
				print('the path don\'t seemed to be a blender file (need .blend extension)!')
				log.write('\033[31mit\'s not a blender file path :'+path+'\033[0m\n')
				continue
				
			elif not os.path.exists(path) or not os.path.isfile(path) :
				#check if the file exist
				print('this path didn\'t exist or is not a file!')
				log.write('\033[31mno corresponding file to this path :'+path+'\033[0m\n')
				continue 
			
			
			#open the file and get settings
			log.write('prepare the adding of : '+path+'\n')
			
			
			prefXml = os.popen('"'+pref.blenderPath+'" -b "'+path+'" -P "'+mainPath+'/filePrefGet.py" ').read()
			
			
			
			prefXml = re.search(r'<\?xml(.|\n)*</preferences>',prefXml).group(0)
			prefXml = xmlMod.fromstring(prefXml).findall('scene')
			os.system('clear')
			log.menuIn('Scene Choice')
			log.print()
			
			
			# select scene to use 
			if len(prefXml)==1:
				scene = prefXml[0]
				log.write('only one scene in file, automatically use it : '+scene.get('name')+'\n')
				log.menuOut()# quit Scene Choice menu
			else:
				# print scene list
				print('  there is more than one scene in the file :\n\n')
				i=0
				for s in prefXml:
					print(str(i)+'- '+s.get('name'))
					i+=1
				
				# scene choice
				while True:
					choice = input('scene to use (or \'cancel\'):').strip()
					
					try:
						if choice in ['q', 'Q', 'cancel', 'CANCEL', 'quit', 'QUIT']:
							choice = -1
						else:
							choice = int(choice)
					except ValueError:
						choice = -2
				
					if choice < i and choice >= 0 :
						scene = prefXml[choice]
						log.write('use «'+scene.get('name')+'» scene\n')
						log.menuOut()# quit scene choice menu
						break
					elif choice == -1:
						log.menuOut()# quit scene choice menu
						log.menuOut()# quit path choice menu
						log.menuOut()# quit add task menu
						return
					else:
						print('\033[31mincorrect scene choice\033[0m\n')
			
			
			#add the task and save the queue
			task = renderingTask(
									path = path, 
									scene = scene.get('name'), 
									fileXmlSetting = scene,
									preferences = pref)
			
			self.add(task)
			saveQueue(self)
			log.write('file and scene added\n')
			
			task.taskSettingsMenu(log, pref)
			saveQueue(self)
			log.write('task settings saved\n')
	
	
	
	
	
	def multiEdit(self, log, pref, cols, colSize, header):
		'''a method to batch edit task settings '''
		def mainMenu(select):
			'''print multiple task edition main menu'''
			if select:
				print('''\n        \033[4mAction :\033[0m
1- Modify selection
2- Edit Queue Composition
3- Apply A Settings
4- Edit Quality
5- Edit Animation Settings
6- Edit Performance Settings
7- Edit Output Settings
8- Edit Options Settings
9- Edit Cycles Lightpath Settings'
0- Save and quit
(# means not yet implement action)''')
			else:
				print('''\n        \033[4mAction :\033[0m
1- Modify selection
0- Save and quit
    \033[31m-You must select something to acess other action!-\033[0m
(# means not yet implement action)''')
		
		
		
		
		
		log.menuIn('Batch task Editing')
		
		# initial selection
		select = self.multiSelect(log, cols, colSize, header)
		log.menuIn('Action Choice')
		
		while True:
			os.system('clear')
			log.print()
			
			print('Selection :\n')
			print('\033[4m'+header+'\033[0m')
			self.printList(cols, colSize, select, True)
			mainMenu( len(select) > 0 )
			
			choice = input('action?').strip().lower()
			
			if choice in ['q', 'quit', 'cancel', '0']:
				log.menuOut() # quit action choice
				log.menuOut() # quit Batch task Editing
				return
			else:
				try:
					choice = int(choice)
				except ValueError:
					choice = -9999
				if choice == 1:
					select = self.multiSelect(log, cols, colSize, header, select)
				elif len(select) == 0:
					log.write('\033[31mNothing selected, so nothing to do!\033[0m\n')
				elif choice == 2:
					select = self.queueEditMenu(log, cols, colSize, header, select)
				elif choice == 3:
					self.applySettingsMenu(log, cols, colSize, header, select, pref)
				elif choice == 4:
					self.qualityMenu(log, cols, colSize, header, select, pref)
				elif choice == 5:
					self.animationMenu(log, cols, colSize, header, select, pref)
				elif choice == 6:
					self.performanceMenu(log, cols, colSize, header, select, pref)
				elif choice == 7:
					self.outputMenu(log, cols, colSize, header, select, pref)
				elif choice == 8:
					self.optionMenu(log, cols, colSize, header, select, pref)
				elif choice == 9:
					self.lightpathMenu(log, cols, colSize, header, select, pref)
				else:
					log.write('\033[31mUnknow action!\033[0m\n')
			
		
	
	
	
	
	
	def multiSelect(self, log, cols, colSize, header, selected = None):
		'''method to select multiple task'''
		log.menuIn('Select Multiple Task')
		if selected is None:
			selected = []
		
		while True:
			os.system('clear')
			log.print()
			
			print('Multiple selection :\n')
			print('\033[4m'+header+'\033[0m')
			self.printList(cols, colSize, selected)
			
			choice = input('add? (\'h\' for help)').strip().lower()
			
			if choice in ['h', 'help', 'man', 'manual']:
				os.system('clear')
				log.menuIn('Help')
				log.print()
				
				print('''
h =>	Show this page
q =>	Confirm selection and quit (empty input make the same)
a =>	All : select all task
n =>	Nothing : unselect all task
i =>	invert selection
u =>	switch to unselecting mode

select task by typing their corresponding number one by one
or type multiple numbers seperate by '.'
example : '2.5.10' select task 2, 5 and 10.
''')
				input('enter to continue')
				log.menuOut()
			elif choice in ['q', 'quit', '']:
				log.menuOut()
				return selected
			elif choice == 'a':
				selected = list(range(0, len(self.tasks)))
				log.write('Multiple selection : all task selected\n')
			elif choice == 'n':
				selected = []
				log.write('Multiple selection : all task unselect\n')
			elif choice == 'i':
				for i in range(0, len(self.tasks)):
					if i in selected:
						selected.pop(selected.index(i))
					else:
						selected.append(i)
				log.write('Multiple selection invert : task n°'+('.'.join(str(x) for x in selected))+'\n')
			elif choice == 'u':
				log.menuOut()
				return self.multiUnselect(log, cols, colSize, header, selected)
			else:
				choice = choice.split('.')
				
				# convert to int
				try:
					for i, s in enumerate(choice):
						choice[i] = int(s.strip())
				except ValueError:
					log.write('\033[31mMultiple selection error : non numeric input, selection ignore\033[0m\n')
					continue
				
				for s in choice:
					if s >= len(self.tasks) or s < 0:
						log.write('\033[31mMultiple selection error : selection of inexistant task n°'+str(s)+' have been ignore\033[0m\n')
					elif s not in selected:
						selected.append(s)
				
				selected.sort()
				log.write('Multiple selection : task n°'+('.'.join(str(x) for x in selected))+'\n')
	
	
	
	
	
	def multiUnselect(self, log, cols, colSize, header, selected = None):
		'''method to unselect multiple task'''
		log.menuIn('Select Multiple Task (unselect mode)')
		
		if selected is None:
			selected = []
		
		while True:
			os.system('clear')
			log.print()
			
			print('Multiple unselection :\n(only selected task are display)\n')
			print('\033[4m'+header+'\033[0m')
			self.printList(cols, colSize, selected, True)
			
			choice = input('remove? (\'h\' for help)').strip().lower()
			
			if choice in ['h', 'help', 'man', 'manual']:
				os.system('clear')
				log.menuIn('Help')
				log.print()
				
				print('''
h =>	Show this page
q =>	Confirm selection and quit (empty input make the same)
a =>	All : select all task
n =>	Nothing : unselect all task
i =>	invert selection
s =>	switch to selecting mode

unselect task by typing their corresponding number one by one
or type multiple numbers seperate by '.'
example : '2.5.10' unselect task 2, 5 and 10.
''')
				input('enter to continue')
				log.menuOut()
			elif choice in ['q', 'quit', '']:
				log.menuOut()
				return selected
			elif choice == 'a':
				selected = list(range(0, len(self.tasks)))
				log.write('Multiple selection : all task selected\n')
			elif choice == 'n':
				selected = []
				log.write('Multiple selection : all task unselect\n')
			elif choice == 'i':
				for i in range(0, len(self.tasks)):
					if i in selected:
						selected.pop(selected.index(i))
					else:
						selected.append(i)
				log.write('Multiple selection invert : task n°'+('.'.join(str(x) for x in selected))+'\n')
			elif choice == 's':
				log.menuOut()
				return self.multiSelect(log, cols, colSize, header, selected)
			else:
				choice = choice.split('.')
				
				# convert to int
				try:
					for i, s in enumerate(choice):
						choice[i] = int(s.strip())
				except ValueError:
					log.write('\033[31mMultiple unselection error : non numeric input, unselection ignore\033[0m\n')
					continue
				
				for s in choice:
					if s not in selected:
						log.write('\033[31mMultiple unselection error : task n°'+str(s)+' is not selected, ignore\033[0m\n')
					else:
						selected.pop(selected.index(s))
				
				log.write('Multiple selection : task n°'+('.'.join(str(x) for x in selected))+'\n')
	
	
	
	
	
	def queueEditMenu(self, log, cols, colSize, header, select):
		'''menu to edit selection inside queue'''
		log.menuIn('Edit Queue Composition')
		
		while True:
			os.system('clear')
			log.print()
		
			print('Selection :\n')
			print('\033[4m'+header+'\033[0m')
			self.printList(cols, colSize, select, True)
			print('''        Queue edition :
1- regroup on top
2- regroup at first task position
3- regroup at last task position
4- regroup at bottom
5- move up
6- move down
7- erase selection
8- duplicate selection at bottom and select
9- duplicate selection just after original position and select
0- quit''')
			choice = input('action?').strip().lower()
			
			if choice in ['q', 'quit', 'cancel', '0']:
				log.menuOut()
				return select
			
			try:
				choice = int(choice)
			except ValueError:
				choice = -9999
			
			if choice > 0 and choice < 5:
				# regroup selection
				select = self.regroup(log, choice, select)
				
			elif choice == 5:
				# move up
				select = self.moveSelected(log, select)
				
			elif choice == 6:
				# move down
				select = self.moveSelected(log, select, False)
				
			elif choice == 7:
				# erase selection
				select = self.eraseSelected(log, select)
				
			elif choice in [8, 9]:
				# duplicate selection
				select = self.duplicateSelected(log, select, choice == 8)
				
			else:
				log.write('\033[31mUnknow action index!\033[0m\n')
	
	
	
	
	
	def regroup(self, log, choice, select):
		'''regroup selected task in the queue'''
		log.write('task n°'+('.'.join(str(x) for x in select)))
		group = []
		for i in select:
			group.append(self.tasks.pop(i-len(group)))
		
		# place group in the good place:
		if choice == 1:
			# place on top of the list
			self.tasks = group+self.tasks
			select = list( range( 0, len(select) ) )
		elif choice == 2:
			# place at first task position
			i = select[0]
			self.tasks = self.tasks[0:i] + group + self.tasks[i:]
			select = list( range(i, i + len(select)) )
		elif choice == 3:
			# place at last task position
			i = select[len(select)-1] - (len(group)-1)
			self.tasks = self.tasks[0:i] + group + self.tasks[i:]
			select = list( range(i, i + len(select)) )
		else:
			# place on bottom of the list
			self.tasks.extend(group)
			select = list( range( len(self.tasks)-len(select), len(self.tasks) ) )
		log.write(' regroup to row n°'+('.'.join(str(x) for x in select))+'\n')
		return select
	
	
	
	
	
	def moveSelected(self, log, select, way = True):
		'''move selected task up (way is True) or down'''
		log.write('task n°'+('.'.join(str(x) for x in select)))
		
		newSelect = []
		if way:
			# move up
			for i in select:
				if i != 0 and i-1 not in newSelect:
					self.tasks.insert(i-1, self.tasks.pop(i))
					newSelect.append(i-1)
				else:
					newSelect.append(i)
		else:
			# move down
			select.reverse()
			for i in select:
				if i != len(self.tasks)-1 and i+1 not in newSelect:
					self.tasks.insert(i+1, self.tasks.pop(i))
					newSelect.append(i+1)
				else:
					newSelect.append(i)
			newSelect.reverse()
		
		log.write(' move to row n°'+('.'.join(str(x) for x in newSelect))+'\n')
		
		return newSelect
	
	
	
	
	
	def eraseSelected(self, log, select):
		'''a method to erase selected task'''
		
		if input('Are you sure that you want to erase all this task? (y to confirm) ').strip().lower() in ['y', 'yes']:
			select.reverse()
			for i in select:
				self.tasks.pop(i)
				log.write('\033[31merase task n°'+str(i)+'\033[0m\n')
			select = []
		
		return select
	
	
	
	
	
	def duplicateSelected(self, log, select, bottom):
		'''a method to duplicate selected tasks'''
		if input('Are you sure that you want to duplicate all this task? (y to confirm) ').strip().lower() in ['y', 'yes']:
			newSelect = []
			if bottom:
				for i in select:
					self.tasks.append(self.tasks[i].getClone())
					log.write('Task n°'+str(i)+' duplicate at row n°'+str(len(self.tasks)-1)+'\n')
					newSelect.append(len(self.tasks)-1)
			else:
				
				for i in select:
					print(i)
					n = i + len(newSelect)
					self.tasks.insert( n+1 , self.tasks[n].getClone())
					log.write('Task n°'+str(i)+' duplicate at row n°'+str( n+1 )+'\n')
					newSelect.append( n + 1 )
			return newSelect
		
		return select
	
	
	
	
	
	def applySettingsMenu(self, log, cols, colSize, header, select, pref):
		'''Display menu to choose a references settings to apply to selected tasks'''
		log.menuIn('Apply Settings To Selected Task')
		log.menuIn('Settings Choice')
		
		while True:
			os.system('clear')
			log.print()
			
			print('	selection :\n')
			print('\033[4m'+header+'\033[0m')
			self.printList(cols, colSize, select, True)
			
			print('''\n\n        Choice of settings to apply :
1- Preferences Settings
2- Blender Files Settings
3- Settings of one of the selected task
0- Quit''')
			
			choice = input('choice?').strip().lower()
			
			if choice in ['q', 'quit', 'cancel', '0']:
				log.menuOut()
				log.menuOut()
				return
			
			if choice == '1':
				# apply preferences settings to selected task
				log.menuOut()
				self.applySettings(log, select, pref, cols, colSize, header)
				log.menuIn('Settings Choice')
				
			elif choice == '2':
				# apply file settings settings to selected task
				log.menuOut()
				self.applySettings(log, select, 'file settings', cols, colSize, header)
				log.menuIn('Settings Choice')
				
			elif choice == '3':
				# choose a task to use
				choice = input('what task to use?(q to cancel)').strip().lower()
				if choice in ['q', 'quit', 'cancel']:
					continue
				
				try:
					choice = int(choice)
				except ValueError:
					log.write('\033[31mApply task settings to selected task error : invalid choice\033[0m\n')
					continue
				
				if choice not in select:
					log.write('\033[31mApply task settings to selected task error : task not in selected tasks\033[0m\n')
				else:
					# apply task settings to selected task
					log.menuOut()
					self.applySettings(log, select, choice, cols, colSize, header)
					log.menuIn('Settings Choice')
				
			else:
				log.write('\033[31merror, unvalid input\033[0m\n')
	
	
	
	
	
	def applySettings(self, log, select, ref, cols, colSize, header):
		'''a method to apply a settings to all selected task'''
		log.menuIn('Confirmation')
		
		while True:
			os.system('clear')
			log.print()
			
			print('	selection :\n')
			print('\033[4m'+header+'\033[0m')
			self.printList(cols, colSize, select, True)
			
			print('        Apply Settings Confirmation :\n')
			if ref == 'file settings':
				print('Are you sure that you want to apply blender file settings to all task?\n\033[5m(blender file settings are not reload from the file)\033[0m\n')
			else:
				print('Are you sure that you want to apply this settings to all selected task?\n\033[5mAll settings gone be overwrite except start/end frame settings!\nrenderlayer pass settings will be overwrite too!\033[0m\n')
			
			
			choice = input('confirm (y)').strip().lower()
			
			if choice not in ['y', 'yes']:
				log.menuOut()
				log.write('\033[31msettings application canceled\033[0m\n')
				return
			else:
				if ref == 'file settings':
					for i in select:
						task = self.tasks[i]
						task.apply( task.fileSetting, False)
					
					log.write('File settings apply to task n°'\
								+('.'.join(str(x) for x in select))+'\n')
					
				else:
					if type(ref) is int:
						log.write('Settings of task n°'+str(ref)+' applied to task n°'\
								+('.'.join(str(x) for x in select))+'\n')
						ref = self.tasks[ref].customSetting.getClone()
					else:
						log.write('Preference settings applied to task n°'\
								+('.'.join(str(x) for x in select))+'\n')
					
					ref.start = None
					ref.end = None
					
					for i in select:
						task = self.tasks[i]
						task.apply( ref, True)
					
				
				log.menuOut()
				return
			
			
	
	
	
	
	
	def qualityMenu(self, log, cols, colSize, header, select, pref):
		'''display the menu to choose a quality settings to change'''
		log.menuIn('Edit Quality Settings')
		
		while True:
			os.system('clear')
			log.print()
		
			print('Selection :\n')
			print('\033[4m'+header+'\033[0m')
			self.printList(cols, colSize, select, True)
			print('''        Quality edition :
1- X resolution
2- Y resolution
3- Resolution percent
4- File format
5- Simplify
6- Main animation samples 
7- Background samples
8- Foreground samples
9- Background renderlayers keywords
10- Foreground renderlayers keywords
0- quit\n\n''')
			choice = input('action?').strip().lower()
			
			if choice in ['q', 'quit', 'cancel', '0']:
				log.menuOut()
				return
			
			try:
				choice = int(choice)
			except ValueError:
				choice = -9999
			
			if choice == 1:
				self.batchEditIntAttr(log, 'X', 'X resolution', pref, select, 9, 1)
			elif choice == 2:
				self.batchEditIntAttr(log, 'Y', 'Y resolution', pref, select, 9, 1)
			elif choice == 3:
				self.batchEditIntAttr(log, 'percent', 'resolution percent', pref,\
											select, 9, 1)
			elif choice == 4:
				self.batchEditListAttr(log, 'outputFormat', 'render format', pref, select, 12)
			elif choice == 5:
				self.batchEditIntAttr(log, 'simplify', 'simplify', pref, select, 11)
			elif choice == 6:
				self.batchEditIntAttr(log, 'mainAnimationCyclesSamples',\
						'main samples', pref, select, 10, 0)
			elif choice == 7:
				self.batchEditIntAttr(log, 'backgroundCyclesSamples',\
						'background renderlayer Samples', pref, select, 10, 0)
			elif choice == 8:
				self.batchEditIntAttr(log, 'foregroundCyclesSamples',\
						'foreground renderlayer Samples', pref, select, 10, 0)
			elif choice == 9:
				self.batchEditKeywordMenu(log, pref, select, 'background')
			elif choice == 10:
				self.batchEditKeywordMenu(log, pref, select, 'foreground')
			else:
				log.write('\033[31mUnknow action index!\033[0m\n')
	
	
	
	
	
	
	def animationMenu(self, log, cols, colSize, header, select, pref):
		'''display the menu to choose a animation settings to change'''
		log.menuIn('Edit animation Settings')
		
		while True:
			os.system('clear')
			log.print()
		
			print('Selection :\n')
			print('\033[4m'+header+'\033[0m')
			self.printList(cols, colSize, select, True)
			print('''        Animation settings edition :
1- Animation rate
2- Start frame
3- End Frame
4- Background Animation
5- Foreground Animation
6- Background renderlayers keywords
7- Foreground renderlayers keywords
0- quit\n\n''')
			choice = input('action?').strip().lower()
			
			if choice in ['q', 'quit', 'cancel', '0']:
				log.menuOut()
				return
			
			try:
				choice = int(choice)
			except ValueError:
				choice = -9999
			
			if choice == 1: # animation rate
				self.batchEditIntAttr(log, 'fps', 'animation rate', pref, select, 3, 1)
			elif choice == 2: # start frame
				self.batchEditIntAttr(log, 'start', 'start frame', pref, select, 5)
			elif choice == 3: # end frame
				self.batchEditIntAttr(log, 'end', 'end frame', pref, select, 5)
			elif choice == 4: # background animation
				self.batchEditIntAttr(log, 'backgroundAnimation', \
						'background animation duration', pref, select, 2, 0)
			elif choice == 5: # foreground animation
				self.batchEditIntAttr(log, 'foregroundAnimation', \
						'foreground animation duration', pref, select, 2, 0)
			elif choice == 6: # background keyword
				self.batchEditKeywordMenu(log, pref, select, 'background')
			elif choice == 7: # foreground keyword
				self.batchEditKeywordMenu(log, pref, select, 'foreground')
			else:
				log.write('\033[31mUnknow action index!\033[0m\n')
	
	
	
	
	def performanceMenu(self, log, cols, colSize, header, select, pref):
		'''display the menu to choose a performance settings to change'''
		log.menuIn('Edit Performance Settings')
		
		while True:
			os.system('clear')
			log.print()
		
			print('Selection :\n')
			print('\033[4m'+header+'\033[0m')
			self.printList(cols, colSize, select, True)
			print('''        Performance settings edition :
1- Blender Internal Tiles X size
2- Blender Internal Tiles Y size
3- Cycles CPU Tiles X size
4- Cycles CPU Tiles Y size
5- Cycles GPU Tiles X size
6- Cycles GPU Tiles Y size
7- Rendering engine
8- Rendering device (for Cycles engine)
9- Blender path
0- quit\n\n''')
			choice = input('action?').strip().lower()
			
			if choice in ['q', 'quit', 'cancel', '0']:
				log.menuOut()
				return
			
			try:
				choice = int(choice)
			except ValueError:
				choice = -9999
			
			if choice == 1: # Blender Internal Tiles X size
				self.batchEditIntAttr(log, 'tilesBIX', 'X Blender Internal tiles size',\
									 pref, select, 25, 1)
				
			elif choice == 2: # Blender Internal Tiles Y size
				self.batchEditIntAttr(log, 'tilesBIY', 'Y Blender Internal tiles size',\
									pref, select, 25, 1)
				
			elif choice == 3: # Cycles CPU Tiles X size
				self.batchEditIntAttr(log, 'tilesCyclesCPUX', 'X Cycles CPU tiles size',\
									pref, select, 27, 1)
				
			elif choice == 4: # Cycles CPU Tiles Y size
				self.batchEditIntAttr(log, 'tilesCyclesCPUY', 'Y Cycles CPU tiles size',\
									pref, select, 27, 1)
				
			elif choice == 5: # Cycles GPU Tiles X size
				self.batchEditIntAttr(log, 'tilesCyclesGPUX', 'X Cycles GPU tiles size',\
									pref, select, 26, 1)
				
			elif choice == 6: # Cycles GPU Tiles Y size
				self.batchEditIntAttr(log, 'tilesCyclesGPUY', 'Y Cycles GPU tiles size',\
									pref, select, 26, 1)
				
			elif choice == 7: # Rendering engine
				log.write('\033[31mNot yet implemented…\033[0m\n')
				
			elif choice == 8: # Rendering device (for Cycles engine)
				log.write('\033[31mNot yet implemented…\033[0m\n')
				
			elif choice == 9: # Blender version
				log.write('\033[31mNot yet implemented…\033[0m\n')
			else:
				log.write('\033[31mUnknow action index!\033[0m\n')
	
	
	
	
	
	def outputMenu(self, log, cols, colSize, header, select, pref):
		'''display the menu to choose a output settings to change'''
	
	
	
	
	
	def optionMenu(self, log, cols, colSize, header, select, pref):
		'''display the menu to choose a option settings to change'''
	
	
	
	
	
	def lightpathMenu(self, log, cols, colSize, header, select, pref):
		'''display the menu to choose a Cycles lightpath settings to change'''
		log.menuIn('Edit Cycles Lightpath Settings')
		
		while True:
			os.system('clear')
			log.print()
		
			print('Selection :\n')
			print('\033[4m'+header+'\033[0m')
			self.printList(cols, colSize, select, True)
			print('''        Cycles lightpath settings edition :
1- Max bounces
2- Min bounces
3- Max transparency bounces
4- Min transparency bounces
5- Diffuse bounces
6- Glossy bounces
7- Transmission bounces
8- Volume bounces
0- quit\n\n''')
			choice = input('action?').strip().lower()
			
			if choice in ['q', 'quit', 'cancel', '0']:
				log.menuOut()
				return
			
			try:
				choice = int(choice)
			except ValueError:
				choice = -9999
			
			if choice == 1: # Max bounces
				self.batchEditIntAttr(log, 'bouncesMax',\
						'maximal bounces', pref, select, 18, 0)
			elif choice == 2: # Min bounces
				self.batchEditIntAttr(log, 'bouncesMin',\
						'minimal bounces', pref, select, 18, 0)
			elif choice == 3: # Max transparency bounces
				self.batchEditIntAttr(log, 'transparencyBouncesMax',\
						'maximal transparency bounces', pref, select, 19, 0)
			elif choice == 4: # Min transparency bounces
				self.batchEditIntAttr(log, 'transparencyBouncesMin',\
						'minimal transparency bounces', pref, select, 19, 0)
			elif choice == 5: # Diffuse bounces
				self.batchEditIntAttr(log, 'diffuseBounces',\
						'diffuse bounces', pref, select, 21, 0)
			elif choice == 6: # Glossy bounces
				self.batchEditIntAttr(log, 'glossyBounces',\
						'glossy bounces', pref, select, 22, 0)
			elif choice == 7: # Transmission bounces
				self.batchEditIntAttr(log, 'transmissionBounces',\
						'transmission bounces', pref, select, 23, 0)
			elif choice == 8: # Volume bounces
				self.batchEditIntAttr(log, 'volumeBounces',\
						'volume bounces', pref, select, 24, 0)
			else:
				log.write('\033[31mUnknow action index!\033[0m\n')
	
	
	
	
	def batchEditIntAttr(self, log, attr, label, pref, select, colId, m = None, M = None):
		'''a method to edit standard numerical attribute'''
		log.menuIn('Edit '+label+' setting')
		
		# get list header
		cols = [0, 1, colId]
		header, colSize = self.getListHeader(cols, False)
		
		while True:
			os.system('clear')
			log.print()
			
			# print list
			print('Selection :\n')
			print('\033[4m'+header+'\033[0m')
			self.printList(cols, colSize, select, True)
			
			# print pref settings
			if attr == 'percent':
				print('\nPreference '+label+' settings : '+str( int(getattr(pref, attr)*100) )+'\n\n' )
			elif attr == 'simplify' and getattr(pref, attr) is None:
				print('\nPreference '+label+' settings : Disabled\n\n' )
			else:
				print('\nPreference '+label+' settings : '+str( getattr(pref, attr) )+'\n\n' )
			
			# get input
			choice = input('New '+label+' setting value (or q) : ').strip().lower()
			
			# check if quit
			if choice in ['q', 'quit', 'cancel', '']:
				log.menuOut()
				log.write('\033[31mcancel batch editing of '+label+' setting.\033[0m\n')
				return
			
			# convert input
			try:
				choice = int(choice)
			except ValueError:
				log.write('\033[31mValueError while batch editing '+label+' setting, must be an integer.\033[0m\n')
				continue
			
			# test input
			if (m is not None and choice < m) \
				or (M is not None and choice > M):
				log.write('\033[31mBatch editing of '+label+' setting abort : out of range value.\033[0m\n')
				continue
			
			# apply new settings and quit
			if attr == 'percent':
				choice /= 100
			elif attr == 'simplify':
				if choice < 0:
					choice = 0
				elif choice > 10:
					choice = None
			
			if attr == 'start':
				for i in select:
					self.tasks[i].customSetting.start = min(choice, \
								self.tasks[i].customSetting.end)
			elif attr == 'end':
				for i in select:
					self.tasks[i].customSetting.end = max(choice, \
								self.tasks[i].customSetting.start)
			elif attr in ['backgroundAnimation', 'foregroundAnimation']:
				for i in select:
					val = min( choice, self.tasks[i].customSetting.duration() )
					setattr( self.tasks[i].customSetting, attr, val)
			else:
				for i in select:
					setattr( self.tasks[i].customSetting, attr, choice)
			
			if choice is None:
				log.write(label+' option disabled for task n°'+('.'.join( str(x) for x in select))+'\n')
			else:
				log.write(label+' setting set to '+str(choice)+' for task n°'+('.'.join( str(x) for x in select))+'\n')
			log.menuOut()
			return
	
	
	
	
	
	def batchEditListAttr(self, log, attr, label, pref, select, colId):
		'''a method to edit settings with available value list'''
		log.menuIn('Edit '+label+' setting')
		
		if attr == 'outputFormat':
			options = ['PNG', 'JPEG', 'OPEN_EXR', 'OPEN_EXR_MULTILAYER']
		
		# get list header
		cols = [0, 1, colId]
		header, colSize = self.getListHeader(cols, False)
		
		while True:
			os.system('clear')
			log.print()
			
			# print list
			print('Selection :\n')
			print('\033[4m'+header+'\033[0m')
			self.printList(cols, colSize, select, True)
			
			# print pref settings
			print('\nPreference '+label+' settings : '+getattr(pref, attr)+'\n\n' )
			
			# print available value
			print('Available settings :\n')
			for i, opt in enumerate(options):
				print(str(i)+'- '+opt)
			
			# get input
			choice = input('New '+label+' setting (or q) : ').strip().lower()
			
			# check if quit
			if choice in ['q', 'quit', 'cancel', '']:
				log.menuOut()
				log.write('\033[31mcancel batch editing of '+label+' setting.\033[0m\n')
				return
			
			# convert input
			try:
				choice = int(choice)
			except ValueError:
				log.write('\033[31mValueError while batch editing '+label+' setting, choice must be an integer.\033[0m\n')
				continue
			
			# test input
			if choice < 0 or choice >= len(options):
				log.write('\033[31mBatch editing of '+label+' setting abort : choice don\'t correspond to an available option.\033[0m\n')
				continue
			
			# apply new settings and quit
			choice = options[choice]
			
			for i in select:
				setattr( self.tasks[i].customSetting, attr, choice)
			
			log.write(label+' setting set to '+choice+' for task n°'+('.'.join( str(x) for x in select))+'\n')
			log.menuOut()
			return
	
	
	
	
	
	def batchEditKeywordMenu(self, log, pref, select, ground):
		'''a method to display a menu to choose a way to batch edit keywords list'''
		log.menuIn('Edit '+ground+' keywords list')
		
		attr = {'background' : 'backgroundLayersKeywords',\
				 'foreground' : 'foregroundLayersKeywords'}[ground]
		
		while True:
			os.system('clear')
			log.print()
			
			# print list
			self.printListKeywords(select, pref, attr, ground)
			
			# print menu
			print('''Action :
1- Add Keywords
2- Remove Keyword
3- Empty keyword lists
4- overwrite keyword lists manually
5- overwrite keyword lists with preferences keyword list
6- overwrite keyword lists with inventory keyword list
7- overwrite keyword lists with a selected task keyword list
0- quit
''')
			
			
			# get input
			choice = input('action? ').strip().lower()
			
			# check if quit
			if choice in ['q', 'quit', 'cancel', '0']:
				log.menuOut()
				log.write('\033[31mcancel batch editing of '+ground+' keywords list.\033[0m\n')
				return
			
			# convert input
			try:
				choice = int(choice)
			except ValueError:
				log.write('\033[31mError : choice must be an integer.\033[0m\n')
				continue
			
			# test menu choice
			if choice in [1,2,3,4,5,6,7]:
				self.batchEditKeyword(log, pref, select, ground, choice)
			else:
				log.write('\033[31mError : unknow action.\033[0m\n')
				continue
	
	
	
	
	
	def printListKeywords(self, select, pref, attr, ground):
		'''a method to print all selected tasks background/foreground keywords and return inventory of it'''
		allKeys = []
		print('Selection :\n')
		print('\033[4m'\
			+'id  |Task File Name                |Scene Name          |Status  |'\
			+ground+' keywords                                         |'
			+'\033[0m')
		for i in select:
			row = columnLimit(i, 4)
			row += columnLimit(self.tasks[i].path.split('/').pop(), 30)
			row += columnLimit(self.tasks[i].scene, 20)
			row += columnLimit(self.tasks[i].status, 8)
			
			keys = getattr(self.tasks[i].customSetting, attr)
			for k in keys:
				if k not in allKeys:
					allKeys.append(k)
			
			val = '|'.join(keys)
			row += columnLimit(val, 60)
			print(row)
		
		# print pref settings
		val = '|'.join( getattr(pref, attr) )
		print('\nPreference '+ground+' keywords list :\n'+val+'\n\n' )
		
		#print all keywords inventory
		print('\nAll '+ground+' keywords inventoried : \n'\
				+('|'.join(allKeys))+'\n\n' )
		
		return allKeys
	
	
	
	
	
	def batchEditKeyword(self, log, pref, select, ground, mode):
		'''a method to batch edit keyword list'''
		menu = [
				'Error',
				'Add Keyword',
				'Remove Keyword',
				'Empty Lists',
				'Manually Overwrite Lists',
				'Overwrite With Preferences',
				'Overwrite With Inventory',
				'Overwrite With Task'
				]
		log.menuIn(menu[mode])
		
		attr = {'background' : 'backgroundLayersKeywords',\
				 'foreground' : 'foregroundLayersKeywords'}[ground]
		
		
		# print list
		os.system('clear')
		log.print()
		inventory = self.printListKeywords(select, pref, attr, ground)
		
		# ask confirmation or settings
		msg = [
				'Error',
				'Keyword to add (empty input to cancel)?',
				'Keyword to remove (empty input to cancel)?',
				'Do you really want to erase the '+ground+' keyword of all this tasks (y)?',
				'List the keyword to replace current lists of all tasks (empty input to cancel)?',
				'Do you really want to overwrite all selected tasks '+ground+' keyword lists with the preferences one (y)?',
				'Do you really want to overwrite all selected tasks '+ground+' keyword lists with the Inventory one (y)?',
				'overwrite all selected tasks '+ground+' keyword with wich one tasks keyword list (empty input to cancel)?'
				]
		choice = input(msg[mode]).strip().lower()
		
		# quit menu whithout action
		if choice == '':
			log.write('\033[31mQuit '+ground+' keywords batch editing.\033[0m\n')
			log.menuOut()
			return
		
		
		#check keyword list
		if mode in [1,2,4]:
			choice = choice.split('|')
			
			for i,k in enumerate(choice):
				choice[i] = choice[i].strip() # remove useless space
			
			while '' in choice:
				choice.remove('') # remove empty string
			
			# check keyword composition
			for k in choice:
				match = re.search(r'^[-0-9a-zA-Z_]{3,}*$', k)
				if match is None:
					log.write('''\033[31munvalid keyword : the keyword must only contains letters, numbers or '-' or '_', they can be split by '|' and space\033[0m\n''')
					log.menuOut()
					return
			
			# check there is keyword
			if len(choice) == 0:
				log.write('''\033[31mNo valid keyword! Quit!\033[0m\n''')
				log.menuOut()
				return
		
		
		
		if mode == 1:
			# add keywords to all selected keywords list that don't contains it
			for i in select:
				selectKeys = getattr(self.tasks[i].customSetting, attr)
				for k in choice:
					if k not in selectKeys:
						selectKeys.append(k)
			
			log.write('keywords ['+('|'.join(choice))+'] have been added to '+ground+' keywords list of task n°'+('.'.join(str(x) for x in select))+'\n')
			
			
		elif mode == 2:
			# remove keywords from all selected keywords list that contains it
			for i in select:
				selectKeys = getattr(self.tasks[i].customSetting, attr)
				for k in choice:
					if k in selectKeys:
						selectKeys.remove(k)
			
			log.write('keywords ['+('|'.join(choice))+'] have been removed from '+ground+' keywords list of task n°'+('.'.join(str(x) for x in select))+'\n')
			
			
		elif mode == 3 and choice in ['y', 'yes']:
			# empty all selected keywords list
			for i in select:
				setattr(self.tasks[i].customSetting, attr, [])
			log.write('Erase '+ground+' keyword list of task n°'+('.'.join(str(x) for x in select))+'\n')
			
			
		elif (mode in [5,6] and choice in ['y', 'yes'])\
			or mode in [4, 7] :
			
			if mode == 4:
				# overwrite all list with manually typed list
				ref = choice
				
			elif mode == 5:
				# overwrite all list with preference list
				ref = getattr(pref, attr)
				
			elif mode == 6:
				# overwrite all list with inventory list
				ref = inventory
				
			elif mode == 7:
				# overwrite all list with a selected task list
				try:
					ref = getattr(self.tasks[int(choice)].customSetting, attr)
				except ValueError:
					log.write('\033[31mError : '+choice+'don\'tcorrespond to aselected task.\033[0m\n')
					log.menuOut()
					return
			
			# apply list
			for i in select:
				setattr(self.tasks[i].customSetting, attr, ref[:])
			
			# log confirm action
			log.write('Overwrite '+ground+' keyword list of task n°'\
					+('.'.join(str(x) for x in select))+' with : '\
					+'|'.join(ref)+'\n')
					
		else:
			log.write('\033[31mError : abort '+ground+' keywords batch editing.\033[0m\n')
		
		log.menuOut()
		return
	
	
	
	
	
