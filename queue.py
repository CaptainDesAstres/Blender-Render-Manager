#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module that contain queue class'''
from renderingTask import renderingTask
import os
from usefullFunctions import *

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
	
	
	
	
	
	def list(self, log, scriptSetting):
		'''list task and access editing functions'''
		select = 0
		log.menuIn('Rendering Queue List')
		cols = [ 0, 4, 7, 2, 1 ]
		header, colSize = self.getListHeader(cols)
		
		while True:
			os.system('clear')
			log.print()
			print('RenderList :')
			print(header)
			for i, task in enumerate(self.tasks):
				ident = str(i)+(' '*(4-len(str(i))))+'|'
				if i == select:
					print('\033[30;47m'+ident+task.getListRow(cols, colSize)+'\033[0m')
				else:
					print(ident+task.getListRow(cols, colSize))
			
			choice = input("action?(\'h\' to see help)").strip().lower()
			
			try:
				if choice in ['q', 'quit', 'cancel']:
					choice = -1
				elif choice == 'l':
					choice = -2
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
				if choice >= len(self.tasks):
					log.write('\033[31mTask selecting error : there is no task n°'+str(choice)+'\033[0m\n')
				else:
					select = choice
					log.write('Select task n°'+str(choice)+'\n')
			elif choice == -2:
				cols, header, colSize = self.attrListChoice(log, cols)
			elif choice == -9998:
				os.system('clear')
				log.menuIn('Help')
				log.print()
				print('''        \033[4mRender Queue Help:\033[0m

    \033[4mGeneral action :\033[0m
l => Change the settings displayed in the list
q => Quit 'Render Queue List' menu
h => show this page

    \033[4mIndividual action :\033[0m
the highlight row are selected task. the following action are apply to this task.
to select another task, type the corresponding number
''')
				input('type enter to continue')
				log.menuOut()
			else:
				log.write('\033[31mRendering Queue : unknow action\033[0m\n')
			
	
	
	
	
	
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
	
	
	
	
	
