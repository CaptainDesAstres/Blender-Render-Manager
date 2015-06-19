#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''program for manage blender rendering task'''
import time
import os
import sys
import xml.etree.ElementTree as xmlMod
import re
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
	global log
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

	choice (hit corresponding number or first letter) :

	''')
		
		# menu choice
		choice = input().strip()
		if choice in ['0','q','Q']: 
			log.write('choice : close Blender Render Manager\n')
			return
		elif choice in ['1','A','a']:
			log.write('choice : add rendering task\n')
			addTask();
		elif choice in ['2','L','l']:
			log.write('choice : actualy unavailable function,not yet coded\n')
		elif choice in ['3','R','r']:
			log.write('choice : actualy unavailable function,not yet coded\n')
		elif choice in ['4','P','p']:
			log.write('choice : watch / edit preferences\n')
			if(scriptSetting.see(log)):
				# save if there is a setting change
				saveSettings(scriptSetting)
				log.write('preferences saved\n')
		elif choice in ['5','L','l']:
			log.write('choice : actualy unavailable function,not yet coded\n')
		else:
			log.write('unknow choice: "'+choice+'"\n')
		
		os.system('clear')



def addTask():
	'''function to manage manual rendering task adding'''
	global log, renderQueue, scriptSetting
	log.menuIn('Add Task')
	log.menuIn('Give File Path')
	
	while True:
		os.system('clear')
		log.print()
		path = input("Add File\n  ABSOLUTE path of the blender file (or 'cancel')").strip()
		
		if path in ['cancel', 'quit', 'CANCEL', 'QUIT', 'q', 'Q']:
			#cancel action
			log.write('\033[31mquit add task menu\033[0m\n')
			log.menuOut()# quit Add Task
			log.menuOut()# quit Give File Path
			return
		
		
		if path[0] in ['\'', '"'] and path[-1] in ['\'', '"']:
			#remove quote mark and apostrophe in first and last character
			path = path[1:len(path)-1]
			print(path)
		
		if path[0] != '/':
			#check if path is absolute (begin by '/')
			print('it\'s not an absolute path!')
			log.write('\033[31munabsolute path reject :'+path+'\033[0m\n')
			continue
			
		elif len(path) < 7 or path[len(path)-6:] !='.blend':
			#check if path point to a .blend file
			print('the path don\'t seemed to be a blender file (need .blend extension)!')
			log.write('\033[31mit\'s not a blender file path :'+path+'\033[0m\n')
			continue
			
		elif not os.path.exists(path) or not os.path.isfile(path) :
			#check if the file exist
			print('this path didn\'t exist or is not a file!')
			log.write('\033[31mno corresponding file to this path :'+path+'\033[0m\n')
			continue 
		
		
		#open the file and get settings
		log.write('prepare the adding of : '+path+'\n')
		
		os.chdir(mainPath)
		prefXml = os.popen('"'+scriptSetting.blenderPath+'" -b "'+path+'" -P "'+mainPath+'/filePrefGet.py" ').read()
		os.chdir(settingPath)
		
		
		prefXml = re.search(r'<\?xml(.|\n)*</preferences>',prefXml).group(0)
		prefXml = xmlMod.fromstring(prefXml).findall('scene')
		os.system('clear')
		log.menuIn('Scene Choice')
		log.print()
		
		
		# select scene to use 
		if len(prefXml)==1:
			scene = prefXml[0]
			log.write('only one scene in file, automatically use it : '+scene.get('name')+'\n')
		else:
			# print scene list
			print('  there is more than one scene in the file :\n\n')
			i=0
			for s in prefXml:
				print(str(i)+'- '+s.get('name'))
				i+=1
			
			# scene choice
			while True:
				
				choice = input('scene to use (or \'cancel\'):').strip()
				if(re.search(r'^\d+$',choice) and int(choice)<i):
					scene = prefXml[int(choice)]
					log.write('use «'+scene.get('name')+'» scene\n')
					log.menuOut()# quit scene choice menu
					break
				elif choice in ['cancel', 'quit', 'CANCEL', 'QUIT', 'q', 'Q']:
					log.menuOut()# quit scene choice menu
					log.menuOut()# quit path choice menu
					log.menuOut()# quit add task menu
					return
				else:
					print('\033[31mincorrect scene choice\033[0m\n')
		
		
		#add the task and save the queue
		task = renderingTask(
								path = path, 
								scene = scene.get('name'), 
								fileXmlSetting = scene,
								preferences = scriptSetting)
		
		renderQueue.add(task)
		saveQueue(renderQueue)
		log.write('file and scene added\n')
		
		task.taskSettingsMenu(log, scriptSetting)
		saveQueue(renderQueue)
		log.write('task settings saved\n')

















main()
