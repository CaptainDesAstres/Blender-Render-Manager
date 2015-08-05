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
			self.groups = ['[main]']
		else:
			self.groups = []
			for g in self.preset.groups.keys():
				group = preferences.presets.renderlayers.groups[g]
				if group.isUsefull(task.info.scenes[task.scene]):
					self.groups.append(g)
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize Task log object with saved log'''
		node = xmlfind('preset')
		if node is None:
			node = xmlfind('metapreset')
			self.presetName = node.get('alias')
			self.preset = Metapreset(xml = node)
		else:
			self.presetName = node.get('alias')
			self.preset = Preset(xml = node)
	
	
	
	
	
	def toXml(self):
		'''export task log into xml syntaxed string'''
		xml = '<log>'
		xml += self.preset.toXml(self.presetName)
		xml += '</log>'
		return xml
	
	
	
	
	
	def print(self):
		'''A method to print task log'''
		
	
	
	
	
	
