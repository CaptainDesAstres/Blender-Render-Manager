#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage task running log'''
import xml.etree.ElementTree as xmlMod
from TaskList.TaskLog.GroupLog import *
from Preferences.PresetList.Preset.Preset import *
from Preferences.PresetList.Preset.Metapreset import *
from usefullFunctions import XML


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
		if self.presetName == '[default]':
			self.presetName = preferences.presets.default
		self.preset = preferences.presets.getPreset(self.presetName).copy()
		self.backup = 0
		
		fileName = task.path.split('/').pop()
		fileName = fileName[0:fileName.rfind('.blend')]
		self.path = preferences.output.getMainPath(fileName, task.scene, self.presetName)
		
		
		if type(self.preset) is Preset:
			self.groups = [GroupLog(groupName = '[main]', 
									preferences = preferences, 
									task = task)]
		else:
			self.groups = []
			
			for g in self.preset.groups.keys():
				group = preferences.presets.renderlayers.groups[g]
				if group.isUsefull(task.info.scenes[task.scene]):
					self.groups.append(GroupLog(groupName = g,
												preferences = preferences, 
												task = task))
			
			default = GroupLog(groupName = '[default]',
												preferences = preferences, 
												task = task)
			if len(default.renderlayers) > 0:
				self.groups.append(default)
		
		self.status = 'ready'
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize Task log object with saved log'''
		self.path = xml.get('path')
		self.status = xml.get('status')
		self.backup = int(xml.get('backup'))
		
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
		xml = '<log path="'+XML.encode(self.path)+'" status="'+self.status\
				+'" backup="'+str(self.backup)+'" >\n'
		xml += self.preset.toXml(self.presetName)
		for g in self.groups:
			xml += g.toXml()
		xml += '</log>'
		return xml
	
	
	
	
	
	def print(self):
		'''A method to print task log'''
		print('The task have '+str(len(self.groups))+' group(s):')
		ended, total = 0, 0
		for group in self.groups:
			group.runMenuPrint()
			total += (group.end - group.start + 1)
			ended += len(group.frames)
		print('\n\n                  '+str(ended)+'/'+str(total)\
							+'('+str(total-ended)+' remaining')
	
	
	
	
	
	def getGroup(self, g):
		'''a method to get a group by his name'''
		for group in self.groups:
			if g == group.name:
				return group
	
	
	
	
	
	def getMainPath(self):
		'''return the task main path'''
		if self.backup == 0:
			return self.path
		else:
			return self.path+'previous rendering '+str(self.backup)+'/'
	
	
	
	
	
	def isComplete(self):
		'''check if there is still frame waiting to be rendered'''
		for group in self.groups:
			if group.remaining()>0:
				return False
		return True
	
	
	
	
	
	def checkFrames(self):
		'''check for each frame that have been claimed as rendered if there is really a file corresponding to it'''
		path = self.getMainPath()
		for group in self.groups:
			group.checkFrames(path)
		
		return self.isComplete()
	
	
	
	
