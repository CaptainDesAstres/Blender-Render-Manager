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
		'headerLabel':'Resolution |',				'limit':11},
		
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
		'headerLabel':'Vol.|',						'limit':4}
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
		
	
	
	
	
	
	def getListHeader(self, cols):
		'''a method to get list header and column size for a list of attributes'''
		header = 'id  |Task File Name                |'
		size = []
		
		for col in cols:
			header += queue.menu[col]['headerLabel']
			size.append(queue.menu[col]['limit'])
		
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
#- Apply A Settings
#- Edit Quality
#- Edit Animation Settings
#- Edit Performance Settings
#- Edit Output Settings
#- Edit Options Settings
#- Edit Cycles Lightpath Settings'
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
					select = self.multiSelect(log, cols, colSize, header)
				elif len(select) == 0:
					log.write('\033[31mNothing selected, so nothing to do!\033[0m\n')
				elif choice == 2:
					select = self.queueEditMenu(log, cols, colSize, header, select)
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
#- erase selection
#- clone selection at bottom and select
#- clone selection at original position and select
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
	
	
	
	
	
	
	
	
	
	
	
	
	
