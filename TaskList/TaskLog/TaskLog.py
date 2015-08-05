#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage task running log'''
import xml.etree.ElementTree as xmlMod
from TaskList.TaskLog.GroupLog import *


class TaskLog:
	'''class to manage task running log'''
	
	
	def __init__(self, xml = None, pref = None, task = None):
		'''initialize task log object'''
		if xml is None:
			self.defaultInit(pref, task)
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self, preferences, task):
		'''initialize Task log object by generating from the task settings'''
		self.presetName = task.preset
		self.preset = preferences.presets.getPreset(self.presetName)
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize Task log object with saved log'''
		
	
	
	
	
	
	def toXml(self):
		'''export task log into xml syntaxed string'''
		xml = '<log>'
		xml += self.preset.toXml(self.presetName)
		xml += '</log>'
		return xml
	
	
	
	
	
	def print(self):
		'''A method to print task log'''
		
	
	
	
	
	
