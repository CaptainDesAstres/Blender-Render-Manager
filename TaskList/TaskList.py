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
	
	
	
	
	
	def menu(self, log, preferences, tasks):
		'''method to see task list and manage it'''
		log.menuIn('Task List')
		
		while True:
			log.print()
			
			choice= input('action (h for help):').strip().lower()
			if choice in ['q', 'quit']:
				log.menuOut()
				return
			elif choice in ['p', 'pref', 'preferences']:
				preferences.menu(log)
			elif choice in ['h', 'help']:
				log.menuIn('Help')
				log.print()
				
				print('''\n\n        \033[4mHELP :\033[0m

Help : h or help
quit : q or quit
Not Yet Implement :
##
##
##Preferences access : p or pref or preferences
##Add task : a or add or +
##Edit/inspect task : type the index of the task
##Batch task editing : b or batch
##See previous sessions logs : l or log
##Run tasks : r or run
##
##

''')
				
				input('Press enter to continue')
				log.menuOut()
			else:
				log.error('Unknow request!', False)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
