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
		self.name = groupName
		
		if groupName = '[main]':
			self.presetName = task.preset
			animation = 0
		else
			mainPreset = preferences.presets.getPreset(task.preset)
			self.presetName = mainPreset.groups[groupName]
			animation = mainPreset.animation[groupName]
		
		self.preset = preferences.presets.getPreset(self.presetName).copy()
		
		group = preferences.presets.renderlayers.groups[groupName]
		
		self.renderlayers = []
		for RL in task.info.scenes[task.scene].getActiveRenderlayers():
			if group.belongTo(RL.name)
				self.renderlayers.append(RL.name)
		
		self.start = task.info.scenes[task.scene].start
		self.end = task.info.scenes[task.scene].end
		if animation != 0:
			self.end = min(self.start+animation-1, self.end)
		
		self.frames = []
		
		self.status = 'ready to start'
		
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize Task renderlayer group log object with saved log'''
		
	
	
	
	
	
	def toXml(self):
		'''export task renderlayer group log into xml syntaxed string'''
		
		
	
	
	
	
	
	def print(self):
		'''A method to print task renderlayer group log'''
		
	
	
	
	
	
