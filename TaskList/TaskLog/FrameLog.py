#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage task Frame log'''
import xml.etree.ElementTree as xmlMod
import datetime

class TaskLog:
	'''class to manage task frame log'''
	
	
	def __init__(self, xml = None, 
					nb = None,
					path = None,
					date = None,
					computingTime = None):
		'''initialize task frame object'''
		if xml is None:
			self.defaultInit(nb, path, date, computingTime)
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self, nb, path, date, computingTime):
		'''initialize Task frame log object'''
		self.frame = nb
		self.path = path
		self.date = date
		self.computingTime = computingTime
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize Task frame log object with saved log'''
		
		self.frame = int(xml.get('frame'))
		self.path = xml.get('path')
		self.date = datetime.datetime.fromtimestamp(float(xml.get('date')))
		self.computingTime = float(xml.get('computingTime'))
	
	
	
	
	
	def toXml(self):
		'''export task frame log into xml syntaxed string'''
		return '<frame frame="'+str(self.frame)\
				+'" path="'+self.path\
				+'" date="'+str(int(self.date.timestamp()))\
				+'" computingTime="'+str(self.computingTime)+'" />'
		
	
	
	
	
	
	def print(self):
		'''A method to print task frame log'''
		
	
	
	
	
	
