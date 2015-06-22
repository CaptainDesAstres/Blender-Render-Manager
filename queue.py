#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module that contain queue class'''
from renderingTask import renderingTask
import os
from usefullFunctions import *

class queue:
	'''class who contain the list of all the rendering task to manage'''
	
	
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
		menu = [
				{'menuEntry':'Scene Name', 'key':'scene'},
				{'menuEntry':'Status', 'key':'status'},
				{'menuEntry':'Back/Foreground animation', 'key':'B/Fground Anim'},
				{'menuEntry':'Animation Rate (fps)', 'key':'fps'},
				{'menuEntry':'Duration', 'key':'duration'},
				{'menuEntry':'Start/End Frame', 'key':'start/end'},
				
				{'menuEntry':'Blender Path', 'key':'blender'},
				{'menuEntry':'Engine (Devices)', 'key':'engine'},
				{'menuEntry':'Tiles Size', 'key':'tiles'},
				{'menuEntry':'Résolution', 'key':'resolution'},
				{'menuEntry':'Samples', 'key':'samples'},
				{'menuEntry':'Simplify', 'key':'simplify'},
				
				{'menuEntry':'Output Format', 'key':'format'},
				{'menuEntry':'Transparent Background', 'key':'alpha'},
				{'menuEntry':'Z Pass', 'key':'Zpass'},
				{'menuEntry':'Object Index Pass', 'key':'OIpass'},
				{'menuEntry':'Compositing', 'key':'compositing'},
				{'menuEntry':'Exposure', 'key':'exposure'},
				
				{'menuEntry':'Bounces Min/Max', 'key':'bounces m/M'},
				{'menuEntry':'Transparent Bou. Min/Max', 'key':'T bounces m/M'},
				{'menuEntry':'Dif./Glo./Tra./Vol.', 'key':'DGTV'},
				{'menuEntry':'Diffuse Bounces', 'key':'diffuse'},
				{'menuEntry':'Glossy Bounces', 'key':'glossy'},
				{'menuEntry':'Transmission Bounces', 'key':'transmission'},
				{'menuEntry':'Volumes Bounces', 'key':'volume'}
				]
		while True:
			y = 0
			txt =''
			while y < 6:
				x = 0
				while x < 4:
					n = y + (6 * x)
					txt += columnLimit(str(n)+'- '+menu[n]['menuEntry'], 30)
					x += 1
				txt += '\n'
				y += 1
			n += 1
			txt += (' '*30+'|')*3\
					+columnLimit(str(n)+'- '+menu[n]['menuEntry'], 30)+'\n'
			
			print(txt)
			
			
			choice = input("'q' to quit").strip().lower()
			
			if choice in ['q', 'quit', 'cancel']:
				log.menuOut()
				return cols
			
			
	
	
	
	
	
