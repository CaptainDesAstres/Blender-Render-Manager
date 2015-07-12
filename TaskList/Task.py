#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage task settings'''
import xml.etree.ElementTree as xmlMod
import os

class Task:
	'''class to manage task settings'''
	
	
	def __init__(self, xml= None):
		'''initialize task object with default settings or saved settings'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize Task object with default settings'''
		self.path = None
		self.scene = None
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize Task object with savedd settings'''
		self.path = xml.get('path')
		self.scene = xml.get('scene')
	
	
	
	
	
	def toXml(self):
		'''export task settings into xml syntaxed string'''
		xml = '<task path="'+self.path+'" scene="'+self.scene+'" />\n'
		return xml
	
	
	
	
	
	def menu(self, log, index):
		'''method to edit task settings'''
		log.menuIn('task n°'+str(index))
		
		while True:
			log.print()
			
			choice= input('no action yet implement?').strip().lower()
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()# quit preferences menu
				return change
			else:
				log.error('Unknow request!', False)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
