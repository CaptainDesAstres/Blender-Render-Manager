#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage task renderlayer group log'''
import xml.etree.ElementTree as xmlMod
from TaskList.TaskLog.FrameLog import *


class TaskLog:
	'''class to manage task renderlayer group log'''
	
	
	def __init__(self, xml = None,
						groupName = None,
						preferences = None, 
						task = None):
		'''initialize task renderlayer group log object'''
		if xml is None:
			self.defaultInit(groupName, preferences, task)
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self, groupName, preferences, task):
		'''initialize Task renderlayer group log object by generating from the task settings'''
		
		
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize Task renderlayer group log object with saved log'''
		
	
	
	
	
	
	def toXml(self):
		'''export task renderlayer group log into xml syntaxed string'''
		
		
	
	
	
	
	
	def print(self):
		'''A method to print task renderlayer group log'''
		
	
	
	
	
	
