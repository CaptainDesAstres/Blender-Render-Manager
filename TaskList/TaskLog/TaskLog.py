#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage task running log'''
import xml.etree.ElementTree as xmlMod


class TaskLog:
	'''class to manage task running log'''
	
	
	def __init__(self, xml = None, pref = None, task = None):
		'''initialize task log object'''
		if xml is None:
			self.defaultInit(pref, task)
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self, preferences):
		'''initialize Task log object by generating from the task settings'''
		
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize Task log object with saved log'''
		
	
	
	
	
	
	def toXml(self):
		'''export task log into xml syntaxed string'''
		
		
	
	
	
	
	
	def print(self):
		'''A method to print task log'''
		
	
	
	
	
	
