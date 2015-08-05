#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage task running log'''
import xml.etree.ElementTree as xmlMod
from TaskList.TaskLog.GroupLog import *
from Preferences.PresetList.Preset.Preset import *
from Preferences.PresetList.Preset.Metapreset import *



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
		
		if type(self.preset) is Preset:
			self.groups = [GroupLog('[main]', preferences, task)]
		else:
			self.groups = []
			for g in self.preset.groups.keys():
				group = preferences.presets.renderlayers.groups[g]
				if group.isUsefull(task.info.scenes[task.scene]):
					self.groups.append(GroupLog(g, preferences, task))
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize Task log object with saved log'''
		node = xml.find('preset')
		if node is None:
			node = xml.find('metapreset')
			self.presetName = node.get('alias')
			self.preset = Metapreset(xml = node)
		else:
			self.presetName = node.get('alias')
			self.preset = Preset(xml = node)
		
		self.groups = []
		for node in xml.findall('group'):
			self.groups.append(GroupLog(xml = node))
	
	
	
	
	
	def toXml(self):
		'''export task log into xml syntaxed string'''
		xml = '<log>\n'
		xml += self.preset.toXml(self.presetName)
		for g in self.groups:
			xml += g.toXml()
		xml += '</log>'
		return xml
	
	
	
	
	
	def print(self):
		'''A method to print task log'''
		
	
	
	
	
	
