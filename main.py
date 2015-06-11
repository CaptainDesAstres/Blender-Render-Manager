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
from render import *

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

#check if configuration directorie exist, otherwise create it 
if not os.path.exists('/home/'+os.getlogin()+'/.BlenderRenderManager/'):
	log += 'No configuration directorie, create it: fail'
	os.mkdir('/home/'+os.getlogin()+'/.BlenderRenderManager')
	log = log[:len(log)-4]+'done\n'
else:
	log += 'Find configuration directorie\n'
os.chdir('/home/'+os.getlogin()+'/.BlenderRenderManager')


#check if log directorie exist, otherwise create it and create a log file anyway
if not os.path.exists(os.getcwd()+'/log/'):
	log += 'No log directorie, create it: fail'
	os.mkdir(os.getcwd()+'/log')
	log = log[:len(log)-4]+'done\n'
log = Log(start,log)

#check configuration file exist: create it if necessary and open it
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

#check if a queue file exist and create or load it
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
	
	continu =True
	while continu:
		#print log and main menu
		log.print()
		log.write('Main menu\n')
		print('''	Main Menu
			1- Add
			2- List
			3- Run
			4- Preferences
			5- Log
			0- Quit

	choice (hit corresponding number or first letter) :

	''')
		
		#treat menu choice
		choice = input()
		if choice in ['0','q','Q']: 
			log.write('choice : close Blender Render Manager\n')
			continu=False
		elif choice in ['1','A','a']:
			log.write('choice : add rendering task\n')
			addTask();
		elif choice in ['2','L','l']:
			log.write('choice : actualy unavailable function,not yet coded\n')
		elif choice in ['3','R','r']:
			log.write('choice : actualy unavailable function,not yet coded\n')
		elif choice in ['4','P','p']:
			log.write('choice : watch / edit preferences\n')
			preference()
		elif choice in ['5','L','l']:
			log.write('choice : actualy unavailable function,not yet coded\n')
		else:
			log.write('unknow choice: "'+choice+'"\n')
		
		os.system('clear')



def addTask():
	'''function to manage manual rendering task adding'''
	global log, renderQueue
	os.system('clear')
	path = ''
	
	while path == '':
		path = input("Add File\n\tABSOLUTE path of the blender file (or 'cancel')").strip()
		
		if path in ['cancel', 'quit', 'CANCEL', 'QUIT', 'q', 'Q']:
			#cancel action
			log.write('canceled action\n')
			return
		
		
		if path[0] in ['\'', '"'] and path[-1] in ['\'', '"']:
			#remove quote mark and apostrophe in first and last character
			path = path[1:len(path)-1]
			print(path)
			
		if path[0] != '/':
			#check if path is absolute (begin by '/')
			print('it\'s not an absolute path!')
			log.write('unabsolute path reject :'+path+'\n')
			path = ''
			continue
		
		elif len(path) < 7 or path[len(path)-6:] !='.blend':
			#check if path point to a .blend file
			print('the path don\'t seemed to be a blender file (need .blend extension)!')
			log.write('it\'s not a blender file path :'+path+'\n')
			path = ''
			continue
		
		elif not os.path.exists(path):
			#check if the file exist
			print('this file didn\'t exist!')
			log.write('no corresponding file to this path :'+path+'\n')
			path = ''
			continue 
		
		#open the file and get settings
		log.write('prepare the adding of : '+path+'\n')
		prefXml = os.popen('blender -b "'+path+'" -P "'+mainPath+'/filePrefGet.py" ').read()
		prefXml = re.search(r'<\?xml(.|\n)*</preferences>',prefXml).group(0)
		prefXml = xmlMod.fromstring(prefXml).findall('scene')
		os.system('clear')
		log.print()
		
		# select scene to use 
		if len(prefXml)==1:
			scene = prefXml[0]
			log.write('only one scene in file, automatically use it : '+scene.get('name')+'\n')
		else:
			print('\tthere is more than one scene in the file :\n\n')
			i=0
			for s in prefXml:
				print(str(i)+'- '+s.get('name'))
				i+=1
			
			sceneChoiceRecquired = True
			while sceneChoiceRecquired:
				choice = input('scene to use (or \'cancel\'):')
				if(re.search(r'^\d+$',choice) and int(choice)<i):
					scene = prefXml[int(choice)]
					log.write('use «'+scene.get('name')+'» scene\n')
					sceneChoiceRecquired=False
				elif choice in ['cancel', 'quit', 'CANCEL', 'QUIT', 'q', 'Q']:
					return
				else:
					print('incorrect scene choice\n')
			
		
		
		#add the task and save the queue
		task = render()
		task.path = path
		task.scene = scene.get('name')
		renderQueue.add(task)
		saveQueue(renderQueue)
		
		

def preference():
	'''print script preferences and let edit or reset it'''
	global scriptSetting
	global log
	
	while True:
		#print log and preferences
		os.system('clear')
		log.print()
		print('\t\tPreferences\n')
		scriptSetting.printPreferences()
		
		#treat available actions
		choice= input('(e)dit, (r)eset or (q)uit: ')
		if choice in ['Q','q']:
			log.write('quit preferences\n')
			return
		elif choice in ['e','E']:
			log.write('edit preferences\n')
			prefEdit()
		elif choice in ['R','r']:
			#reset default settings
			confirm = input('this action will reset to factory settings. confirm (y):')
			if confirm in ['y','Y']:
				scriptSetting = setting()
				saveSettings(scriptSetting)
				log.write('reset factory settings\n')
			else:
				log.write('abort settings reset\n')
		else:
			log.write('unknow request\n')

def prefEdit():
	'''edit script preferences'''
	global log
	global scriptSetting
	
	while True:
		#print log and edit preferences menu
		os.system('clear')
		log.print()
		print('''		preferences editing:
	1- Resolution
	2- Animation rate
	''')
		
		#treat available actions
		choice = input('what\'s the parameter to edit ?(or \'cancel\')')
		if choice in ['cancel','CANCEL','QUIT','quit','Q','q']:
			return
		elif choice in ['1','r','R']:
			#edit resolution setting
			#print current resolution settings and ask new settings
			os.system('clear')
			log.write('resolution editing: ')
			log.print()
			print('current resolution :'+str(scriptSetting.x)+'x'+str(scriptSetting.y)+'@'+str(int(scriptSetting.percent*100))+'\n\n')
			choice = input('new resolution ? (1920x1080@100 for example or \'cancel\')')
			
			
			#parse new settings and check it
			match = re.search(r'^(\d{3,5})x(\d{3,5})@(\d{2,3})$',choice)
			if match is None:
				if choice in ['cancel','CANCEL','QUIT','quit','Q','q']:
					log.write('resolution change canceled\n')
				else:
					log.write('error, resolution change canceled, retry\n')
				continue
			
			#apply new settings and save it
			scriptSetting.x = int(match.group(1))
			scriptSetting.y = int(match.group(2))
			scriptSetting.percent = int(match.group(3))/100
			saveSettings(scriptSetting)
			log.write(choice+'\n')
			
		elif choice in ['2','a','A']:
			#edit animation frame rate
			#print log and current animation settings and ask new settings
			os.system('clear')
			log.write('edit animation rate : ')
			log.print()
			print('current animation rate: '+str(scriptSetting.fps)+'fps\n\n')
			choice = input('new animation rate? ( 30 for example or \'cancel\')')
			
			#parse new settings and check it
			match = re.search(r'^(\d{1,})(fps)?$',choice)
			if match is None:
				if choice in ['cancel','CANCEL','QUIT','quit','Q','q']:
					log.write('animation frame rate change canceled\n')
				else:
					log.write('error, animation frame rate change canceled, retry\n')
				continue
			
			#apply new settings and save it
			scriptSetting.fps = int(match.group(1))
			saveSettings(scriptSetting)
			log.write(match.group(1)+'fps\n')
			
		else:
			log.write('unknow request!\n')











main()
