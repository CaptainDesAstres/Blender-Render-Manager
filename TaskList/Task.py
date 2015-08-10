#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage task settings'''
import xml.etree.ElementTree as xmlMod
import os, uuid, subprocess, shlex
from save import *
from usefullFunctions import *
from Preferences.PresetList.Preset.Preset import *
from TaskList.FileInfo.FileInfo import *
from TaskList.TaskLog.TaskLog import *

class Task:
	'''class to manage task settings'''
	
	
	def __init__(self, path = None, scene = None, preset = None,\
					fileInfo = None, xml= None):
		'''initialize task object with default settings or saved settings'''
		if xml is None:
			self.defaultInit(path, scene, preset, fileInfo)
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self, path, scene, preset, fileInfo):
		'''initialize Task object with default settings'''
		self.path = path
		self.scene = scene
		self.preset = preset
		self.info = fileInfo
		self.uid = uuid.uuid4().hex
		self.log = None
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize Task object with savedd settings'''
		self.path = xml.get('path')
		self.scene = xml.get('scene')
		self.preset = xml.get('preset')
		self.uid = xml.get('uid', uuid.uuid4().hex)
		self.info = FileInfo(xml.find('fileInfo'))
		
		node = xml.find('log')
		if node is not None:
			self.log = TaskLog(xml = node)
		else:
			self.log = None
	
	
	
	
	
	def toXml(self):
		'''export task settings into xml syntaxed string'''
		xml = '<task path="'+XML.encode(self.path)+'" scene="'+XML.encode(self.scene)\
				+'" preset="'+self.preset+'" uid="'+self.uid+'">\n'\
				+self.info.toXml()
		if self.log is not None:
			xml += self.log.toXml()
		xml += '</task>\n'
		return xml
		
	
	
	
	
	
	def menu(self, log, index, tasks, preferences):
		'''method to edit task settings'''
		log.menuIn('Task n°'+str(index))
		change = False
		started = self.log is not None
		if started:
			menu = '''
    Menu :
(TASK ALREADY STARTED : SOME OPTIONS IS NOT AVAILABLE!)
5- Change list row
6- Erase task
0- Quit and save

'''
		else:
			menu = '''
    Menu :
1- Change scene
2- Change preset
3- Edit preset
4- Active/desactive Renderlayer
5- Change list row
6- Erase task
0- Quit and save

'''
		
		while True:
			log.print()
			
			print('\n        Edit Task n°'+str(index)+' :')
			self.print()
			print(menu)
			
			
			choice= input('action : ').strip().lower()
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			elif choice == '1':
				
				scene = self.info.sceneChoice(log, allChoice = False)[0]
				if scene is not None:
					self.scene = scene
					log.write('Task n°'+str(index)+' : Scene set to «'+self.scene+'»')
					change = True
				
			elif choice == '2':
				
				preset = Task.presetChoice(log, preferences)
				if preset is not None :
					self.preset = preset
					log.write('Task n°'+str(index)+' : Preset set to «'+self.preset+'»')
					change = True
				
			elif choice == '3':
				
				self.editPreset(log, preferences)
				
			elif choice == '4':
				
				confirm = self.info.scenes[self.scene].renderlayerActivator(log)
				if confirm:
					log.write('change task n°'+str(index)+' active renderlayer')
					change = True
				
			elif choice == '5':
				
				confirm, select = tasks.move(log, [index])
				if confirm:
					change = True
					index = select[0]
				
			elif choice == '6':
				
				if tasks.remove(log, [index]):
					log.menuOut()
					log.write('Task n°'+str(index)+' removed')
					return True
				
			else:
				log.error('Unknow request!', False)
	
	
	
	
	
	def print(self):
		'''A method to print task information'''
		print('\n\nPath :          '+self.path)
		print('File Name :     '+self.path.split('/').pop())
		print('Scene :         '+self.scene)
		print('Preset :        '+self.preset+'\n')
		print('\033[4mActive Renderlayer :\033[0m')
		self.info.scenes[self.scene].printActiveRenderlayer()
		print('\n')
	
	
	
	
	
	def renamePreset(self, old, new):
		'''a method to rename used preset'''
		if self.preset == old:
			self.preset = new
	
	
	
	
	
	
	def erasePreset(self, preset):
		'''a method to stop using preset'''
		if self.preset == preset:
			self.preset = '[default]'
	
	
	
	
	
	def getRow(self):
		'''A method to get row to print task list'''
		name = self.path.split('/').pop()
		return columnLimit('  '+name, 25, 5)\
				+columnLimit('  '+self.scene, 25, 5)\
				+columnLimit('  '+self.preset, 25, 5)
	
	
	
	
	
	def presetChoice(log, preferences):
		'''A method to choose a preset'''
		# preset choice
		log.menuIn('Preset Choice')
		log.print()
		print('\n\n        \033[4mPreset Choice :\033[0m\n\n')
		confirm = input('Use «'+preferences.presets.default+'» default preset? (type anything else that y or yes to choose another one)')
		
		
		if confirm in ['', 'y', 'yes']:
			log.menuOut()
			return '[default]'
		else:
			preset = preferences.presets.choose(log)
			log.menuOut()
			return preset
	
	
	
	
	
	
	def editPreset(self, log, preferences):
		'''A method to edit the preset used by the task'''
		log.error('Warning : all change made to the preset will be effective for all task that use it…')
		
		if self.preset == '[default]' :
			name = preferences.presets.default
			preset = preferences.presets.presets[name]
		else:
			name = self.preset
			preset = preferences.presets.presets[name]
		
		if type(preset) is Preset:
			confirm = preset.menu(log, name, preferences.blenderVersion)
		else:
			confirm = preset.menu(log, name, preferences.presets)
		
		if confirm:
			savePreferences(preferences)
	
	
	
	
	
	def copy(self):
		xml = '<?xml version="1.0" encoding="UTF-8"?>\n'+self.toXml()
		xml = xmlMod.fromstring(xml)
		copy = Task(xml = xml)
		copy.uid = uuid.uuid4().hex
		return copy
	
	
	
	
	
	def run(self, index, count, scriptPath, log, preferences):
		'''A method to execute the task'''
		log.menuIn('run Task '+str(index)+' from '+str(count))
		log.print()
		print('\n\nRun task n°'+str(index)+' of '+str(count)+' :\n\n')
		
		if self.log is None:
			# task never have been run before
			self.log = TaskLog(pref = preferences, task = self)
			preferences.output.checkAndCreate(self, preferences)
		
		metapreset = preferences.presets.getPreset(self.preset)
		if type(metapreset) is Preset:
			versions = { metapreset.engine.version : '[default]' }
		else:
			versions = metapreset.getGroupsByBlenderVersion(preferences)
		
		scripts = self.createTaskScript(scriptPath, preferences, versions, metapreset)
		
		results = ''
		for version in versions.keys():
			try:
				result = subprocess.Popen(\
							shlex.split(\
								preferences.blenderVersion.getVersionPath(version)\
								+' -b "'+self.path+'" -P "'\
								+scripts[version]+'"'),\
							stdout = subprocess.PIPE,\
							stdin = subprocess.PIPE,\
							stderr = subprocess.PIPE).communicate()
				results += result[0].decode()+result[1].decode()+'\n\n\n'
			except FileNotFoundError:
				log.write('\033[31mTask n°'+str(index)+' : Blender version call error! Try to verified the path of «'+version+'» blender version!\033[0m')
				pass
		
		self.eraseTaskScript(scripts)
		
		run = ( input(results).strip().lower() == '' )
		log.menuOut()
		return run
	
	
	
	
	
	def createTaskScript(self, scriptPath, preferences, versions, preset):
		'''create a script for each blender versions to run tfhe task'''
		
		start = '''#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
''\'module to manage metapreset''\'
import sys
sys.path.append("'''+scriptPath+'''")
import xml.etree.ElementTree as xmlMod
from Preferences.Preferences import *
from Preferences.PresetList.Preset.Preset import *
from Preferences.PresetList.Preset.Metapreset import *
from TaskList.RenderingTask.RenderingTask import *
from TaskList.Task import *

preferences = Preferences( xml = xmlMod.fromstring(''\''''+preferences.toXml(preset)+'''''\') )
task = Task( xml = xmlMod.fromstring(''\'<?xml version="1.0" encoding="UTF-8"?>\n'''+self.toXml()+'''''\'))
preset = '''
		
		if type(preset) is Preset:
			start += "Preset ( xml = xmlMod.fromstring('''"
		else:
			start += "Metapreset ( xml = xmlMod.fromstring('''"
		
		start += '<?xml version="1.0" encoding="UTF-8"?>\n'\
				+preset.toXml()+"''') )\n"
		
		
		end = '\nRenderingTask(task, preferences, groups, preset)'
		
		paths = {}
		for v, g in versions.items():
			script = start\
					+'groups = ["'+('", "'.join(g) )+'"]\n'\
					+end
			paths[v] = scriptPath+'/TaskList/RenderingTask/TaskScripts/'+self.uid+'-'+v+'.py'
			with open(paths[v],'w') as taskScriptFile:
				taskScriptFile.write( script )
		
		return paths
	
	
	
	
	
	def eraseTaskScript(self, scripts):
		'''erase Task Script files'''
		
		for path in scripts.values():
			os.remove(path)
	
	
	
	
	def getUsefullGroup(self, groups, preferences):
		'''return only usefull group from the list, excluding those who have no renderlayer in this task'''
		renderlayers = self.info.scenes[self.scene].getActiveRenderlayers()
		confirmed = []
		for group in groups:
			for RL in renderlayers:
				if preferences.presets.renderlayers.groups[group].belongTo(RL.name):
					confirmed.append(group)
					break
		return confirmed
	
	
	
	
	
	
	
