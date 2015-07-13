#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage blender file info'''
import xml.etree.ElementTree as xmlMod
from TaskList.FileInfo.Scene import *
import os

class FileInfo:
	'''class to manage blender file info'''
	
	
	def __init__(self, xml):
		'''initialize blender file info with default settings or saved settings'''
		self.fromXml(xml)
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize blender file info with savedd settings'''
		self.scenes = {}
		for scene in xml.findall('scene'):
			self.scenes[scene.get('name')] = Scene(scene)
	
	
	
	
	
	def toXml(self):
		'''export blender file info into xml syntaxed string'''
		xml = '<fileInfo>'
		
		for scene in self.scenes.values():
			xml += scene.toXml()
		
		xml += '</fileInfo>'
		return xml
	
	
	
	
	
	def sceneChoice(self, log):
		'''a methode to choose a scene, return None or a list of one or more scenes'''
		scenes = list(self.scenes.keys())
		scenes.sort(key = str.lower)
		
		if len(scenes) == 0:
			log.error('  no scene in this file… Abort')
			return None
		
		if len(scenes) == 1:
			log.write('  Only one scene in file. Use «'+scenes[0]+'» scene.')
			return [ scenes[0] ]
		
		log.menuIn('Scene Choice')
		while True:
			log.print()
			print('\n\n        \033[4mScene Choice :\033[0m\n\nChoice :\nA- All scene (a task will be create with each scene)')
			for i, scene in enumerate(scenes):
				print(str(i)+'- '+scene)
			
			choice = input('\nscene choice?').strip().lower()
			
			if choice in ['', 'q', 'quit', 'cancel']:
				log.menuOut()
				log.write('  Abort at scene choice')
				return None
			
			if choice == 'a':
				log.menuOut()
				log.write('  Add all scenes')
				return scenes
			
			try:
				choice = int(choice)
			except ValueError:
				log.error('Expect a integer value or "a" or "q"', False)
				continue
			
			if choice < 0 or choice >= len(scenes):
				log.error('Your scene choice correspond to nothing', False)
				continue
			
			log.menuOut()
			log.write('  Add «'+scenes[choice]+'» scenes')
			return [ scenes[choice] ]
		
	
	
	
	
	
	
	
	
	
