#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''program for manage blender rendering task'''
import time, os, sys
import xml.etree.ElementTree as xmlMod
from log import *
from save import *
from settingMod.Preferences import *
from TaskList.TaskList import *





def now(short = True):
	'''return short (HH:MM:SS) or long (DD.MM.AAAA-HH:MM:SS) formated current date strings'''
	if short == True:
		return time.strftime('%H:%M:%S')
	else:
		return time.strftime('%d.%m.%Y-%H:%M:%S')
start = now(False)




log = 'openning of Blender Render Manager\n'+start+' session\n'


# check if configuration directorie exist, otherwise create it 
if not os.path.exists('/home/'+os.getlogin()+'/.BlenderRenderManager/'):
	log += 'No configuration directorie, create it: fail'
	os.mkdir('/home/'+os.getlogin()+'/.BlenderRenderManager')
	log = log[:len(log)-4]+'done\n'
else:
	log += 'Find configuration directorie\n'
os.chdir('/home/'+os.getlogin()+'/.BlenderRenderManager')
settingPath = os.getcwd()


# check if log directorie exist, otherwise create it and create a log file anyway
if not os.path.exists(os.getcwd()+'/log/'):
	log += 'No log directorie, create it: fail'
	os.mkdir(os.getcwd()+'/log')
	log = log[:len(log)-4]+'done\n'
log = Log(start,log)


# check Preferences file exist: create it if necessary and open it
if not os.path.exists(os.getcwd()+'/preferences'):
	log.write('no preferences file, create default file:')
	preferences = Preferences()
	savePreferences(preferences)
	log.write('done\n')
else:
	log.write('get saved preferences:')
	with open(os.getcwd()+'/preferences','r') as prefFile:
		preferences = Preferences( xmlMod.fromstring( (prefFile.read( ) ) ) )
	log.write('done\n')



# check task list file exist: create it if necessary and open it
if not os.path.exists(os.getcwd()+'/taskList'):
	log.write('no task list file, create default file empty file:')
	tasks = TaskList()
	saveTasks(tasks)
	log.write('done\n')
else:
	log.write('get saved preferences:')
	with open(os.getcwd()+'/taskList','r') as tasksFile:
		tasks = TaskList( xmlMod.fromstring( (tasksFile.read( ) ) ) )
	log.write('done\n')







def main():
	'''main function to execute'''
	global log, preferences
	
	
	while True:
		#print log and main menu
		log.print()
		print('''	Main Menu
			#1- Add (not yet implement)
			#2- List (not yet implement)
			#3- Run (not yet implement)
			#8- Log (not yet implement)
			9- NEW PREFERENCES IMPLEMENTATION
			0- Quit

	choice (hit corresponding number) :

	''')
		
		# menu choice
		choice = input().strip().lower()
		
		
		if choice in ['0', 'q', 'cancel', 'quit']: 
			log.write('choice : close Blender Render Manager\n')
			return
		elif choice == '9':
			# acces new prefenences implementation
			if(preferences.menu(log)):
				# save if there is a setting change
				savePreferences(preferences)
				log.write('preferences saved\n')
		else:
			log.error('Main menu choice unvalid: "'+choice+'"', False)
		
		





















main()
