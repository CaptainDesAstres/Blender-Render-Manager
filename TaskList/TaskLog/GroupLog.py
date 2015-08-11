#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage task renderlayer group log'''
import xml.etree.ElementTree as xmlMod
from TaskList.TaskLog.FrameLog import *
from Preferences.PresetList.Preset.Preset import *
from Preferences.PresetList.Preset.Metapreset import *
from usefullFunctions import XML


class GroupLog:
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
		if groupName == '[main]':
			self.subpath = ''
			self.naming = '####'
		else:
			self.subpath = preferences.output.getComplementPath(groupName)
			self.naming = preferences.output.getNaming(groupName)
		
		if groupName == '[main]':
			self.presetName = task.preset
			animation = 0
		elif groupName == '[default]':
			self.presetName = preferences.presets.getPreset(task.preset).default
			animation = 0
		else:
			mainPreset = preferences.presets.getPreset(task.preset)
			self.presetName = mainPreset.groups[groupName]
			animation = mainPreset.animation[groupName]
		
		self.preset = preferences.presets.getPreset(self.presetName).copy()
		
		self.renderlayers = []
		if groupName == '[main]':
			self.renderlayers = task.info.scenes[task.scene].getActiveRenderlayers()
			self.renderlayers = list(RL.name for RL in self.renderlayers)
		elif groupName == '[default]':
			self.renderlayers = task.info.scenes[task.scene].getActiveRenderlayers()
			groupsName = list(preferences.presets.getPreset(task.preset).groups.keys())
			for RL in self.renderlayers[:]:
				for group in groupsName:
					if preferences.presets.renderlayers.groups[group].belongTo(RL.name):
						self.renderlayers.remove(RL)
						break
			self.renderlayers = list(RL.name for RL in self.renderlayers)
		else:
			group = preferences.presets.renderlayers.groups[groupName]
			for RL in task.info.scenes[task.scene].getActiveRenderlayers():
				if group.belongTo(RL.name):
					self.renderlayers.append(RL.name)
		
		self.start = task.info.scenes[task.scene].start
		self.end = task.info.scenes[task.scene].end
		if animation != 0:
			self.end = min(self.start+animation-1, self.end)
		
		self.frames = []
		
		self.status = 'ready to start'
		
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize Task renderlayer group log object with saved log'''
		self.name = xml.get('name')
		self.renderlayers = xml.get('renderlayers').split('#;#')
		self.start = int(xml.get('start'))
		self.end = int(xml.get('end'))
		self.status = xml.get('status')
		self.subpath = xml.get('subpath')
		self.naming = xml.get('naming')
		
		presetXML = xml.find('preset')
		if presetXML is None:
			presetXML = xml.find('metapreset')
			self.preset = Metapreset(xml = presetXML)
		else:
			self.preset = Preset(xml = presetXML)
		self.presetName = presetXML.get('alias')
		
		self.frames = []
		for node in xml.findall('frame'):
			self.frames.append(FrameLog(xml = node))
		
	
	
	
	
	
	def toXml(self):
		'''export task renderlayer group log into xml syntaxed string'''
		xml = '<group name="'+self.name\
				+'" renderlayers="'+'#;#'.join(XML.encode(x) for x in self.renderlayers)\
				+'" start="'+str(self.start)\
				+'" end="'+str(self.end)\
				+'" status="'+self.status\
				+'" subpath="'+XML.encode(self.subpath)\
				+'" naming="'+XML.encode(self.naming)+'" >'
		
		xml += self.preset.toXml(self.presetName)
		
		for f in self.frames:
			xml += f.toXml()
		
		xml += '</group>'
		return xml
	
	
	
	
	
	def print(self):
		'''A method to print task renderlayer group log'''
		total = self.end - self.start + 1
		print('╚═ «'+self.name+'» group ('\
				+str(len(self.renderlayers))+'renderlayers) : '\
				+self.status+'\n  '\
				+'preset : «'+self.presetName+'»     '\
				+str(len(self.frames))+'/'+str(total)+' frames ('\
				+str(self.start)+' to '+str(self.end)+')')
	
	
	
	
	
	def confirmFrame(self, frame, path, date, computingTime):
		'''add frame rendering log confirmation to the group'''
		self.frames.append(
							FrameLog(
									frame = frame,
									path = path,
									date = date,
									computingTime = computingTime
									) 
							)
	
	
	
	
	
