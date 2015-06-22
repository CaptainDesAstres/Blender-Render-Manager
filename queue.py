#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module that contain queue class'''
from renderingTask import renderingTask
import os

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
			
			choice = input("action?('q' to quit)").strip().lower()
			
			try:
				if choice in ['q', 'quit', 'cancel']:
					choice = -1
				else:
					choice = int(choice)
			except ValueError:
				choice = -9999
			
			if choice == -1:
				log.menuOut()
				return
			
			
			
	
	
	
	
	
	def getListHeader(self, cols):
		'''a method to get list header and column size for a list of attributes'''
		txt = 'id  |Task File Name                |'
		size = [30]
		
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
				txt += 'B/F Anim|'
				size.append(8)
			elif col == 'status':
				txt += 'Status  |'
				size.append(8)
		
		return txt, size
	
	
	
	
	
