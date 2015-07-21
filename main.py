#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''program for manage blender rendering task'''
import time, os, sys
import xml.etree.ElementTree as xmlMod
from log import *
from save import *
from Preferences.Preferences import *
from TaskList.TaskList import *





def now(short = True):
	'''return short (HH:MM:SS) or long (DD.MM.AAAA-HH:MM:SS) formated current date strings'''
	if short == True:
		return time.strftime('%H:%M:%S')
	else:
		return time.strftime('%d.%m.%Y-%H:%M:%S')
start = now(False)




log = 'openning of Blender Render Manager\n'+start+' session\n'
scriptPath = os.path.realpath(__file__+'/..')

# check if configuration directorie exist, otherwise create it 
if not os.path.exists('/home/'+os.getlogin()+'/.BlenderRenderManager/'):
	log += 'No configuration directorie, create it: fail'
	os.mkdir('/home/'+os.getlogin()+'/.BlenderRenderManager')
	log = log[:len(log)-4]+'done\n'
else:
	log += 'Find configuration directorie\n'
os.chdir('/home/'+os.getlogin()+'/.BlenderRenderManager')
settingPath = os.getcwd()



# check if lock file exist
if os.path.exists(os.getcwd()+'/lock'):
	log += 'Lock file exist, check it:\n'
	with open(os.getcwd()+'/lock','r') as lockFile:
		PID = lockFile.read( )
	log += 'Lock PID : '+PID+'\n'
	
	# check there is a process with corresponding PID and check this process corespond to the script:
	if os.path.exists('/proc/'+PID+'/'):
		log += 'There is a process for this PID, check it:\n'
		
		with open('/proc/'+PID+'/environ','r') as lockFile:
			PWD = lockFile.read( )
		if PWD.count('PWD='+scriptPath) > 0:
			log += '''The process seem to connespond to a Blender-Render-Manager session! Quit this new Session!

\033[31mBlender-Render-Manager is already running : check the process with '''+PID+''' PID and stop it!\033[0m


'''
			print(log)
			quit()
		else:
			log += 'the process don\'t correspond apparently to a Blender-Render-Manager, lock file ignored.\n'
		
	else:
		log += 'there is no process corresponding to this PID, lock file ignored.\n'
else:
	log += 'No lock file exist, check it:\n'

# create a lock file to prevent multiple call to the script
log += 'create lock file'
createLockFile(str(os.getpid()))



# check if log directorie exist, otherwise create it and create a log file anyway
if not os.path.exists(os.getcwd()+'/log/'):
	log += 'No log directorie, create it: fail'
	os.mkdir(os.getcwd()+'/log')
	log = log[:len(log)-4]+'done\n'
log = Log(start,log)


# check Preferences file exist: create it if necessary and open it
if not os.path.exists(os.getcwd()+'/preferences'):
	log.write('no preferences file, create default file : ', '')
	preferences = Preferences()
	savePreferences(preferences)
	log.write('done')
else:
	log.write('get saved preferences : ', '')
	with open(os.getcwd()+'/preferences','r') as prefFile:
		preferences = Preferences( xmlMod.fromstring( (prefFile.read( ) ) ) )
	log.write('done')



# check task list file exist: create it if necessary and open it
if not os.path.exists(os.getcwd()+'/Tasks'):
	log.write('no task list file, create default file empty file : ', '')
	tasks = TaskList()
	saveTasks(tasks)
	log.write('done')
else:
	log.write('get saved tasks list : ', '')
	with open(os.getcwd()+'/Tasks','r') as tasksFile:
		tasks = TaskList( xmlMod.fromstring( (tasksFile.read( ) ) ) )
	log.write('done')






tasks.menu(log, preferences)
