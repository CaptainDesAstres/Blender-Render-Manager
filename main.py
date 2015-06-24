#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''program for manage blender rendering task'''
import time
import os
import sys
import xml.etree.ElementTree as xmlMod
from log import *
from setting import *
from queue import *
from save import *
from renderingTask import *

#get path to the script directories
mainPath = os.path.abspath(sys.argv[0]+'/..')




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


# check configuration file exist: create it if necessary and open it
if not os.path.exists(os.getcwd()+'/settings'):
	log.write('no configuration file, create default file:')
	scriptSetting = setting()
	saveSettings(scriptSetting)
	log.write('done\n')
else:
	log.write('get saved preferences:')
	with open(os.getcwd()+'/settings','r') as setFile:
		scriptSetting = setting( xmlMod.fromstring( (setFile.read( ) ) ) )
	log.write('done\n')


# check if a queue file exist and create or load it
if not os.path.exists(os.getcwd()+'/queue'):
	log.write('no saved queue, create empty queue file:')
	renderQueue = queue()
	saveQueue(renderQueue)
	log.write('done\n')
else:
	log.write('saved queue loading:')
	with open(os.getcwd()+'/queue','r') as queueFile:
		renderQueue = queue( xmlMod.fromstring( (queueFile.read( ) ) ) )
	log.write('done\n')




def main():
	'''main function to execute'''
	global log, renderQueue, scriptSetting
	#clear standart output
	os.system('clear')
	
	
	while True:
		#print log and main menu
		log.write('Main menu\n')
		log.print()
		print('''	Main Menu
			1- Add
			2- List
			3- Run
			4- Preferences
			5- Log
			0- Quit

	choice (hit corresponding number) :

	''')
		
		# menu choice
		choice = input().strip()
		
		try:
			if choice in ['q', 'Q', 'cancel', 'CANCEL']:
				choice = 0
			else:
				choice = int(choice)
		except ValueError:
			choice = 9999
		
		if choice == 0: 
			log.write('choice : close Blender Render Manager\n')
			return
		elif choice == 1:
			log.write('choice : add rendering task\n')
			renderQueue.addTask(log, scriptSetting, mainPath);
		elif choice == 2:
			log.write('choice : look rendering list\n')
			renderQueue.list(log, scriptSetting)
		elif choice == 3:
			log.write('choice : actualy unavailable function,not yet coded\n')
		elif choice == 4:
			log.write('choice : watch / edit preferences\n')
			if(scriptSetting.see(log)):
				# save if there is a setting change
				saveSettings(scriptSetting)
				log.write('preferences saved\n')
				os.system('clear')
				log.menuIn('Apply Preferences To All Task')
				log.print()
				choice = input('preferences have been changed. Do you want to apply preferences to all task in queue? (\'y\')').strip().lower()
				
				if choice in ['y', 'yes']:
					passBool = input('Do you want z pass and object index pass settings to be apply to all renderlayers? (\'y\')').strip().lower() in ['y', 'yes']
					
					for task in renderQueue.tasks:
						task.apply(scriptSetting, passBool)
					saveQueue(renderQueue)
					log.write('new preferences applied to all task (renderlayer applied : '+str(passBool)+')\n')
				log.menuOut()
				
		elif choice == 5:
			log.write('choice : actualy unavailable function,not yet coded\n')
		else:
			log.write('unknow choice: "'+str(choice)+'"\n')
		
		os.system('clear')





















main()
