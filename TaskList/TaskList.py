#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage task list'''
import xml.etree.ElementTree as xmlMod
import os

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
		
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize task list object with saved task'''
		
	
	
	
	
	
	def toXml(self):
		'''export task list into xml syntaxed string'''
		xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
		xml += '<tasks>\n'
		
		xml += '</tasks>\n'
		
		return xml
	
	
	
	
	
	def menu(self, log):
		'''method to see task list and manage it'''
		log.menuIn('Task List')
		
		while True:
			log.print()
			
			choice= input('no action yet implement (q tou quit):').strip().lower()
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return
			else:
				log.error('Unknow request!', False)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
