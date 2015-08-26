#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage task settings'''
import xml.etree.ElementTree as xmlMod
import os, uuid, subprocess, shlex, time, datetime, threading
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
		self.running = False
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
		self.status = 'waiting'
#		self.status possible values:
#		waiting    > the task have been set and is waiting to be run
#		lock       > the task is protected against running
#		pendinglock> same thing for a task that already have been started
#		ready      > the task have been run once and task.log is set
#		running    > the task is running
#		pause      > the task have been started but is now waiting to be continued
#		ended      > the task have been totaly rendered
#		erased     > the task have been erased
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize Task object with savedd settings'''
		self.path = xml.get('path')
		self.scene = xml.get('scene')
		self.preset = xml.get('preset')
		self.uid = xml.get('uid', uuid.uuid4().hex)
		self.status = xml.get('status')
		self.info = FileInfo(xml.find('fileInfo'))
		
		node = xml.find('log')
		if node is not None:
			self.log = TaskLog(xml = node)
		else:
			self.log = None
	
	
	
	
	
	def toXml(self):
		'''export task settings into xml syntaxed string'''
		xml = '<task path="'+XML.encode(self.path)+'" scene="'+XML.encode(self.scene)\
				+'" preset="'+self.preset+'" uid="'+self.uid\
				+'" status="'+self.status+'" >\n'\
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
6- Lock/Unlock task
7- Erase task
8- Copy task
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
6- Lock/Unlock task
7- Erase task
8- Copy task
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
			elif choice == '1' and not started:
				
				scene = self.info.sceneChoice(log, allChoice = False)
				if scene is not None:
					self.scene = scene[0]
					log.write('Task n°'+str(index)+' : Scene set to «'+self.scene+'»')
					change = True
				
			elif choice == '2' and not started:
				
				preset = Task.presetChoice(log, preferences)
				if preset is not None :
					self.preset = preset
					log.write('Task n°'+str(index)+' : Preset set to «'+self.preset+'»')
					change = True
				
			elif choice == '3' and not started:
				
				self.editPreset(log, preferences)
				
			elif choice == '4' and not started:
				
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
				
				if self.status in ['ready', 'pause']:
					self.status = 'pendinglock'
					change = True
					log.write('Task n°'+str(index)+' locked')
				elif self.status == 'waiting':
					self.status = 'lock'
					change = True
					log.write('Task n°'+str(index)+' locked')
				elif self.status == 'pendinglock':
					self.status = 'pause'
					change = True
					log.write('Task n°'+str(index)+' unlocked')
				elif self.status == 'lock':
					self.status = 'waiting'
					change = True
					log.write('Task n°'+str(index)+' unlocked')
				else:
					log.error('Task n°'+str(index)+' is not lockable/unlockable')
				
				
			elif choice == '7':
				
				if tasks.remove(log, [index]):
					log.menuOut()
					log.write('Task n°'+str(index)+' removed')
					return True
				
			elif choice == '8':
				
				new = self.copy()
				new.status = 'waiting'
				new.log = None
				tasks.tasks.append(new)
				log.write('a copy of the task n°'+str(index)+' have been added at the bottom of the task list')
				change = True
				
			else:
				log.error('Unknow request!', False)
	
	
	
	
	
	def print(self):
		'''A method to print task information'''
		print('\n\nStatus :        '+self.status)
		print('Path :          '+self.path)
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
	
	
	
	
	
	def printRunMenu(self, index, count, log):
		'''print current runninge state'''
		log.print()
		print('\n\nRun task n°'+str(index)+' of '+str(count)+' :\n\n')
		if self.log is not None:
			self.log.print()
		log.runPrint()
	
	
	
	
	
	def run(self, index, taskList, scriptPath, log, preferences):
		'''A method to execute the task'''
		log.menuIn('run Task '+str(index)+' from '+str(len(taskList.tasks)))
		
		if self.log is None:
			# task never have been run before
			self.log = TaskLog(pref = preferences, task = self)
			preferences.output.checkAndCreate(self, preferences, taskList)
		
		self.printRunMenu(index, len(taskList.tasks), log)
		
		metapreset = self.log.preset
		if type(metapreset) is Preset:
			if self.log.groups[0].remaining() > 0:
				versions = { metapreset.engine.version : '[default]' }
		else:
			versions = {}
			for group in self.log.groups:
				if group.remaining() > 0:
					if group.preset.engine.version in versions.keys():
						versions[group.preset.engine.version].append(group.name)
					else:
						versions[group.preset.engine.version] = [group.name]
		
		scripts = self.createTaskScript(scriptPath, preferences, versions, metapreset)
		
		results = ''
		for version in versions.keys():
			try:
				l = threading.Thread(target = self.socketAcceptClient,
									args=(taskList, index, log))
				l.start()
				taskList.listenerThreads.append(l)
				
				sub = subprocess.Popen(\
							shlex.split(\
								preferences.blenderVersion.getVersionPath(version)\
								+' -b "'+self.path+'" -P "'\
								+scripts[version]+'"'),\
							stdout = subprocess.PIPE,\
							stdin = subprocess.PIPE,\
							stderr = subprocess.PIPE)
				taskList.renderingSubprocess.append(sub)
				
				result = sub.communicate()
				taskList.renderingSubprocess.remove(sub)
				results += result[0].decode()+result[1].decode()+'\n\n\n'
			except FileNotFoundError:
				log.write('\033[31mTask n°'+str(index)+' : Blender version call error! Try to verify the path of «'+version+'» blender version!\033[0m')
			if taskList.runningMode in [taskList.UNTIL_GROUP_END,\
										taskList.UNTIL_FRAME_END,\
										taskList.STOP_NOW,\
										taskList.STOP_FORCED]:
				break
		self.eraseTaskScript(scripts)
		
		log.menuOut()
		return True
	
	
	
	
	
	def socketAcceptClient(self, taskList, index, log):
		'''A method to manage client connexion when running'''
		client = taskList.socket.accept()[0]
		taskList.listenerSockets.append( 
										{
									'socket':client,
									'uid':self.uid
										} 
										)
		msg = ''
		while taskList.runningMode < taskList.STOP_NOW:
			msg += client.recv(1024).decode()
			if msg == '':
				time.sleep(1)
			elif msg == self.uid+' VersionEnded EOS':
				break
			else:
				msg = self.treatSocketMessage(msg, taskList, index, log)
		client.close()
	
	
	
	
	
	def treatSocketMessage(self, msg, taskList, index, log):
		'''a method to interpret socket message'''
		if msg[-4:] != ' EOS':
			return msg
		
		messages = msg.split(' EOS')
		messages.pop()
		
		for m in messages:
			# normally, the message is to confirm the rendering of a frame, it must follow this sytaxe:
			#uid action(group,frame,date,computingTime) EOS
			#fc9b9d6fd2af4e0fb3f09066f9902f90 ConfirmFrame(groupe1,15,10:09:2014:10:30:40,11111111111111) EOS
			uid = m[0:32]
			action = m[33:m.find('(')]
			info = m[46:-1]
			if uid == self.uid and action == 'debugMsg':
				log.write(info)
			elif uid == self.uid and action == 'ConfirmFrame':
				info = info.split(',')
				group = info[0]
				frame = int(info[1])
				computingTime = float(info[3])
				
				date = info[2].split(':')
				date = datetime.datetime(
							year = int(date[2]),
							month = int(date[1]),
							day = int(date[0]),
							hour = int(date[3]),
							minute = int(date[4]),
							second = int(date[5])
										)
				
				self.log.getGroup(group).confirmFrame(frame, date, computingTime)
				self.printRunMenu(index, len(taskList.tasks), log)
		
		if messages[-1] == self.uid+' VersionEnded':
			return messages[-1]+' EOS'
		else:
			return ''
	
	
	
	
	
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

preferences = Preferences( xml = xmlMod.fromstring(''\''''+preferences.toXml(False)+'''''\') )
task = Task( xml = xmlMod.fromstring(''\'<?xml version="1.0" encoding="UTF-8"?>\n'''+self.toXml()+'''''\'))
'''
		
		end = '\nRenderingTask(task, preferences, groups)'
		
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
	
	
	
	
	
	
	
