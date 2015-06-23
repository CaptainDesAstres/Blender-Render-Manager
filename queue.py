#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module that contain queue class'''
from renderingTask import renderingTask
import os
from usefullFunctions import *

class queue:
	'''class who contain the list of all the rendering task to manage'''
	
	menu = [
		{'menuEntry':'Scene Name',					'key':'scene',
		'headerLabel':'Scene Name          |',		'limit':20},
		
		{'menuEntry':'Status',						'key':'status',
		'headerLabel':'Status  |',					'limit':8},
		
		{'menuEntry':'Back/Foreground animation',	'key':'B/Fground Anim',
		'headerLabel':'B/F Anim |',					'limit':9},
		
		{'menuEntry':'Animation Rate (fps)',		'key':'fps',
		'headerLabel':'Fps|',						'limit':3},
		
		{'menuEntry':'Duration',					'key':'duration',
		'headerLabel':'Duration|',					'limit':8},
		
		{'menuEntry':'Start/End Frame',				'key':'start/end',
		'headerLabel':'Start-End|',					'limit':9},
		
		
		
		{'menuEntry':'Blender Path',				'key':'blender',
		'headerLabel':'Blender             |',		'limit':20},
		
		{'menuEntry':'Engine (Devices)',			'key':'engine',
		'headerLabel':'eng.(Dev)|',					'limit':9},
		
		{'menuEntry':'Tiles Size',					'key':'tiles',
		'headerLabel':'Tiles  |',					'limit':7},
		
		{'menuEntry':'Resolution',					'key':'resolution',
		'headerLabel':'Resolution |',				'limit':11},
		
		{'menuEntry':'Samples Main/Back/Fore',		'key':'samples',
		'headerLabel':'Samples A./B./F. |',			'limit':17},
		
		{'menuEntry':'Simplify',					'key':'simplify',
		'headerLabel':'Simp.|',						'limit':5},
		
		
		
		{'menuEntry':'Output Format',				'key':'format',
		'headerLabel':'Format|',					'limit':6},
		
		{'menuEntry':'Transparent Background',		'key':'alpha',
		'headerLabel':'Alpha Back.|',				'limit':11},
		
		{'menuEntry':'Z Pass',						'key':'Zpass',
		'headerLabel':'Z Pass|',					'limit':6},
		
		{'menuEntry':'Object Index Pass',			'key':'OIpass',
		'headerLabel':'Obj. Ind.|',					'limit':9},
		
		{'menuEntry':'Compositing',					'key':'compositing',
		'headerLabel':'Compo.|',					'limit':6},
		
		{'menuEntry':'Exposure',					'key':'exposure',
		'headerLabel':'Expos.|',					'limit':6},
		
		
		
		{'menuEntry':'Bounces Min/Max',				'key':'bounces m/M',
		'headerLabel':'Bounces m/M|',				'limit':11},
		
		{'menuEntry':'Transparent Bou. Min/Max',	'key':'T bounces m/M',
		'headerLabel':'Transparence m/M|',			'limit':16},
		
		{'menuEntry':'Dif./Glo./Tra./Vol.',			'key':'DGTV',
		'headerLabel':'Di/Gl/Tr/Vo|',				'limit':11},
		
		{'menuEntry':'Diffuse Bounces',				'key':'diffuse',
		'headerLabel':'Diff.|',						'limit':5},
		
		{'menuEntry':'Glossy Bounces',				'key':'glossy',
		'headerLabel':'Glo.|',						'limit':4},
		
		{'menuEntry':'Transmission Bounces',		'key':'transmission',
		'headerLabel':'Trans.|',					'limit':6},
		
		{'menuEntry':'Volumes Bounces',				'key':'volume',
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
		os.system('clear')
		log.menuIn('Rendering Queue')
		cols = ['scene', 'duration', 'engine', 'B/Fground Anim', 'status']
		
		while True:
			log.print()
			print('RenderList :')
			header, colSize = self.getListHeader(cols)
			print(header)
			for i, task in enumerate(self.tasks):
				ident = str(i)+(' '*(4-len(str(i))))+'|'
				print(ident+task.getListRow(cols, colSize))
			print('(l)ist | (q)uit')
			choice = input("action?").strip().lower()
			
			try:
				if choice in ['q', 'quit', 'cancel']:
					choice = -1
				elif choice == 'l':
					choice = -2
				else:
					choice = int(choice)
			except ValueError:
				choice = -9999
			
			if choice == -1:
				log.menuOut()
				return
			
			if choice == -2:
				cols = self.attrList(log, cols)
			
			
	
	
	
	
	
	def getListHeader(self, cols):
		'''a method to get list header and column size for a list of attributes'''
		txt = 'id  |Task File Name                |'
		size = []
		
		for col in cols:
			if col == 'scene':
				txt += 'Scene Name          |'
				size.append(20)
			elif col == 'duration':
				txt += 'Duration|'
				size.append(8)
			elif col == 'engine':
				txt += 'eng.(Dev)|'
				size.append(9)
			elif col == 'B/Fground Anim':
				txt += 'B/F Anim |'
				size.append(9)
			elif col == 'status':
				txt += 'Status  |'
				size.append(8)
		
		return txt, size
	
	
	
	def attrList(self, log, cols):
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
				return cols
			
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
			newCols = []
			for n in choice:
				if n > 24 or n < 0:
					error = True
					break
				else:
					newCols.append(queue.menu[n]['key'])
			if error:
				log.write('\033[31mList Attribute Choice Error : one of the number is unvalid!\033[0m\n')
				continue
			log.write('List Attribute Choice : '+'.'.join(newCols)+'\n')
			log.menuOut()
			return newCols
	
	
	
	
	
