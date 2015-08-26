#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage task Frame log'''
import xml.etree.ElementTree as xmlMod
import datetime
from usefullFunctions import *


class FrameLog:
	'''class to manage task frame log'''
	
	
	def __init__(self, xml = None, 
					frame = None,
					date = None,
					computingTime = None):
		'''initialize task frame object'''
		if xml is None:
			self.defaultInit(frame, date, computingTime)
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self, frame, date, computingTime):
		'''initialize Task frame log object'''
		self.frame = frame
		self.date = date
		self.computingTime = computingTime
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize Task frame log object with saved log'''
		self.frame = int(xml.get('frame'))
		self.date = datetime.datetime.fromtimestamp(float(xml.get('date')))
		self.computingTime = float(xml.get('computingTime'))
	
	
	
	
	
	def toXml(self):
		'''export task frame log into xml syntaxed string'''
		return '<frame frame="'+str(self.frame)\
				+'" date="'+str(int(self.date.timestamp()))\
				+'" computingTime="'+str(self.computingTime)+'" />'
		
	
	
	
	
	
	def print(self):
		'''A method to print task frame log'''
		print(' ╚═ '+columnLimit((str(self.frame)), 9, sep = '')\
			 +self.date.strftime('%d/%m/%Y at %H:%M')\
			 +'            '+str(round(self.computingTime, 2)) )
	
	
	
	
	
