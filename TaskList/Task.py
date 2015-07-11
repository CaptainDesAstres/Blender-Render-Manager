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
		
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize Task object with savedd settings'''
		
	
	
	
	
	
	def toXml(self):
		'''export task settings into xml syntaxed string'''
		xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
		xml += '<task>\n'
		
		xml += '</task>\n'
		
		return xml
	
	
	
	
	
	def see(self, log, index):
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
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
