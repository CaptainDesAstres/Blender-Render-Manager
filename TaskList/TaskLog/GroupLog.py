#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage task renderlayer group log'''
import xml.etree.ElementTree as xmlMod
from TaskList.TaskLog.FrameLog import *
from Preferences.PresetList.Preset.Preset import *
from Preferences.PresetList.Preset.Metapreset import *
from usefullFunctions import XML
import os


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
	
	
	
	
	
	def menu(self, log, path):
		'''see detail of the group rendering'''
		log.menuIn('«'+self.name+'» group details')
		page = 0
		while True:
			log.print()
			print('\n\n        «'+self.name+'» group details :\n')
			self.print(page, path)
			choice = input('\n\nq to quit').strip().lower()
			
			if choice in ['0', 'cancel', 'q', 'quit']:
				log.menuOut()
				return
	
	
	
	
	
	def print(self, page, path):
		'''A method to print task renderlayer group log'''
		total = self.end - self.start + 1
		remain = total - len(self.frames)
		
		print('Status          : '+self.status)
		print('Rendering path  : '+path+self.subpath)
		print('Preset Name     : '+self.presetName)
		print('This preset may differ from the current preferences because it\'s the preset as it were when first rendering task starting. Type p to see preset.\n')
		
		print('Renderlayer in the group : '+str(len(self.renderlayers)))
		for rl in self.renderlayers:
			print('    ╚═'+rl)
		
		print('\nRendered / total (remaining) : '+str(len(self.frames))+' / '\
				+str(total)+'              ( remain '+str(remain)+' frames )')
		print('Start to End : '+str(self.start)+' to '+str(self.end))
		print('Extract : ')
		for fr in self.frames[page*10:(page+1)*10]:
			fr.print()
		
	
	
	
	
	
	def runMenuPrint(self, index = None):
		total = self.end - self.start + 1
		if index is not None:
			index = str(index)+'-  '
		else:
			index = '╚═ '
		print(index+'«'+self.name+'» group : '+str(len(self.frames))+'/'+str(total)\
					+' frames, '+str(total - len(self.frames))\
					+' remaining frames,\n     Average time by frame : '+str(self.average()))
	
	
	
	
	
	def average(self):
		'''return frame average rendering time'''
		if len(self.frames)>0:
			count = 0
			time = 0
			for f in self.frames:
				count += 1
				time += f.computingTime
			average = time / count
			return average
		else:
			return 0.0
	
	
	
	
	
	def remaining(self):
		'''return the count of frames that don't have been rendered'''
		return (self.end - self.start + 1 - len(self.frames) )
	
	
	
	
	
	def confirmFrame(self, frame, date, computingTime):
		'''add frame rendering log confirmation to the group'''
		self.frames.append(
							FrameLog(
									frame = frame,
									date = date,
									computingTime = computingTime
									) 
							)
	
	
	
	
	
	def checkFrames(self, mainPath):
		'''check for each frame that have been claimed as rendered if there is really a file corresponding to it'''
		extension = self.preset.quality.getExtension()
		for frame in self.frames[:]:
			path = mainPath+self.subpath+(self.naming.replace('####', str(frame.frame)))+extension
			if not os.path.exists(path) or not os.path.isfile(path):
				self.frames.remove(frame)
			elif os.stat(path).st_size < 3:
				self.frames.remove(frame)
				os.remove(path)
	
	
	
	
	
