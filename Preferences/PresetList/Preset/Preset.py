#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage preset'''
import xml.etree.ElementTree as xmlMod
from usefullFunctions import *
from Preferences.PresetList.Preset.Quality import *
from Preferences.PresetList.Preset.BounceSet import *
from Preferences.PresetList.Preset.Engine import *
from Preferences.PresetList.Preset.Options import *
import os, time, datetime

class Preset:
	'''class to manage preset'''
	
	def __init__(self, xml= None):
		'''initialize preset with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize preset with default value'''
		self.quality = Quality()
		self.bounce = BounceSet()
		self.engine = Engine()
		self.options = Options()
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize preset with values extracted from an xml object'''
		self.quality = Quality(xml.find('quality'))
		self.bounce = BounceSet(xml.find('bounceSet'))
		self.engine = Engine(xml.find('engine'))
		self.options = Options(xml.find('options'))
	
	
	
	
	
	def toXml(self, alias = ''):
		'''export preset into xml syntaxed string'''
		txt = '<preset alias="'+alias+'" >\n'
		
		txt += self.quality.toXml()
		
		txt += self.bounce.toXml()
		
		txt += self.engine.toXml()
		
		txt += self.options.toXml()
		
		txt += '</preset>\n'
		return txt
	
	
	
	
	
	def menu(self, log, alias, versions):
		'''menu to explore and edit preset settings'''
		change = False
		log.menuIn(alias+' Preset')
		
		while True:
			
			log.print()
			
			self.print()
			
			print('''\n\n        Menu :
1- Edit Quality Settings
2- Edit Bounces Settings (Cycles)
3- Edit Rendering Options
9- Edit Engine Settings
0- Quit

''')
			
			choice = input('Action?').strip().lower()
			
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			elif choice == '1':
				change = (self.quality.menu(log) or change)
			elif choice == '2':
				change = (self.bounce.menu(log) or change)
			elif choice == '3':
				change = (self.options.menu(log) or change)
			elif choice == '9':
				change = (self.engine.menu(log, versions) or change)
			else:
				log.error('Unvalid menu choice', False)
		
	
	
	
	
	
	def print(self):
		'''a method to print preset'''
		self.quality.print()
		print()
		self.bounce.print()
		print()
		self.options.print()
		print()
		self.engine.print()
	
	
	
	
	
	def copy(self):
		'''A method to get a copy of current object'''
		xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
		xml += self.toXml('')
		xml = xmlMod.fromstring(xml)
		return Preset(xml)
		
	
	
	
	
	
	def renameBlenderVersion(self, old, new):
		'''rename a blender Version if used'''
		self.engine.renameBlenderVersion(old, new)
		
	
	
	
	
	
	
	def useBlenderVersion(self, name):
		'''check if blender version is used by this preset'''
		return self.engine.useBlenderVersion(name)
	
	
	
	
	
	
	def eraseBlenderVersion(self, name):
		'''erase blender version in preset who use it'''
		self.engine.eraseBlenderVersion(name)
	
	
	
	
	
	def applyAndRun(self, bpy, preferences, logGroup, socket, task):
		'''apply settings to a blender scene object and render it, frame by frame'''
		scene = bpy.context.screen.scene
		
		self.quality.apply(scene)
		self.bounce.apply(scene)
		self.engine.apply(scene, preferences)
		self.options.apply(scene)
		
		metadata = 'uid:'+task.uid+';Main preset:«'+task.preset+'»;'+\
					'group:«'+logGroup.name+'»;preset:«'+logGroup.presetName+'»;'+\
					'version:«'+self.engine.version+\
					'»('+str(bpy.app.version[0])+'.'+str(bpy.app.version[1])+');'+\
					'engine:'+self.engine.engine+';'
		if self.engine.engine == 'CYCLES':
			metadata += 'device:'+self.engine.device+\
						';samples:'+str(self.quality.samples)+\
						';exposure(cycles):'+str(self.options.exposureC)+\
						';bounces:'+self.bounce.metadata()+';'
		else:
			metadata += 'exposure(BI):'+str(self.options.exposureB)+';'\
						+'OSA:'+{ True:'enabled', False:'disabled' }[self.quality.OSA.enabled]+';'
			
			if self.quality.OSA.enabled:
				metadata += 'OSA(set)'
				
				if self.quality.OSA.fullSample:
					metadata += 'FULL'
				
				metadata += str(self.quality.OSA.samples)\
							+self.quality.OSA.FILTERS[self.quality.OSA.filter]\
							+'@'+str(self.quality.OSA.size)+';'
		
		if self.quality.simplify is not None:
			metadata += 'simplify:'+str(self.quality.simplify)+';'
		
		scene.render.stamp_note_text = metadata
		
		scene.frame_current = scene.frame_start + len(logGroup.frames) 
		while scene.frame_current <= scene.frame_end \
					and task.running != 'until next frame':
			
			start = time.time()
			
			scene.render.filepath = task.log.getMainPath()\
									+logGroup.subpath\
									+(logGroup.naming.replace('####', str(scene.frame_current)))
			bpy.ops.render.render( write_still=True )
			
			endDate = datetime.datetime.today()
			computeTime = time.time() - start
			
			msg = task.uid+' ConfirmFrame('+logGroup.name\
					+','+str(scene.frame_current)+','+endDate.strftime('%d:%m:%Y:%H:%M:%S')\
					+','+str(computeTime)+') EOS'
			socket.sendall(msg.encode())
			
			scene.frame_current += 1
		
		
		
	
	
	
	
	
