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
	scriptSettings = setting()
	saveSettings(scriptSettings)
	log.write('done\n')
else:
	log.write('get saved preferences:')
	with open(os.getcwd()+'/settings','r') as setFile:
		scriptSettings = setting( xmlMod.fromstring( (setFile.read( ) ) ) )
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
			addFile();
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

def addFile():
	'''function to manage manual rendering task adding'''
	global log, renderQueue
	os.system('clear')
	path = ''
	
	while path == '':
		path = input("Add File\n\tABSOLUTE path of the blender file (or 'cancel')").strip()
		
		
		if path != 'cancel':
			if path[0] in ['\'', '"'] and path[-1] in ['\'', '"']:
				path = path[1:len(path)-1]
				print(path)
			
			if path[0] != '/':
				print('it\'s not an absolute path!')
				log.write('unabsolute path reject :'+path+'\n')
				path = ''
			elif len(path) < 7 or path[len(path)-6:] !='.blend':
				print('the path don\'t seemed to be a blender file (need .blend extension)!')
				log.write('it\'s not a blender file path :'+path+'\n')
				path = ''
			elif os.path.exists(path):
				log.write('prepare the adding of : '+path+'\n')
				prefXml = os.popen('blender -b "'+path+'" -P "'+mainPath+'/filePrefGet.py" ').read()
				prefXml = re.search(r'<\?xml(.|\n)*</preferences>',prefXml).group(0)
				
				prefXml = xmlMod.fromstring(prefXml).findall('scene')
				
				if len(prefXml)>1:
					os.system('clear')
					log.print()
					print('\tthere is more than one scene in the file :\n\n')
					i=0
					
					for s in prefXml:
						print(str(i)+'- '+s.get('name'))
						i+=1
					
					sceneChoiceRecquired = True
					while sceneChoiceRecquired:
						choice = input('scene to use :')
						if(re.search(r'^\d+$',choice) and int(choice)<i):
							scene = prefXml[int(choice)]
							log.write('use «'+scene.get('name')+'» scene\n')
							sceneChoiceRecquired=False
						else:
							print('incorrect scene choice\n')
				else:
					scene = prefXml[0]
					log.write('only one scene in file, automatically use it : '+scene.get('name')+'\n')
				
				pref = setting(scene)
				print('''		rendering task base settings choice
	use file settings (f) :
	''')
				pref.printSceneSettings(scriptSettings)
				print('\tuse preferences settings (d) :\n')
				scriptSettings.printSceneSettings()
				print('''	edit from file settings (ef)
	edit from preferences settings (ed)''')
				choice = input('choice (or «q»):')
				
				if choice in ['d', 'D', 'ED', 'ed']:
					pref = scriptSettings.getClone(pref.start, pref.end)
				
				if choice != 'q':
					if choice in ['ef', 'ed', 'EF', 'ED']:
						print()
					add = render()
					add.path = path
					add.scene = scene.get('name')
					add.settings = pref
					add.status = 'ready'
					renderQueue.add(add)
					saveQueue(renderQueue)
			else:
				print('this file didn\'t exist!')
				log.write('no corresponding file to this path :'+path+'\n')
				path = ''	
		else:
			log.write('canceled action\n')

def preference():
	global scriptSettings
	global log
	prefStay = True
	while prefStay:
		os.system('clear')
		log.print()
		print('\t\tPreferences\n')
		scriptSettings.printSettings()
		choice= input('(e)dit, (r)eset or (q)uit: ')
		if choice in ['e','E']:
			log.write('edit preferences\n')
			prefEdit()
		elif choice in ['Q','q']:
			log.write('quit preferences\n')
			prefStay = False
		elif choice in ['R','r']:
			confirm = input('this action will reset to factory settings. confirm (y):')
			if confirm in ['y','Y']:
				scriptSettings = setting()
				saveSettings(scriptSettings)
				log.write('reset factory settings\n')
			else:
				log.write('abort settings reset\n')
		else:
			log.write('unknow request\n')

def prefEdit():
	global log
	global scriptSettings
	stay = True
	while stay:
		os.system('clear')
		log.print()
		print('''		preferences editing:
	1- Resolution
	2- Animation rate
	''')
		
		choice = input('what\'s the parameter to edit ?(or \'cancel\')')
		if choice in ['cancel','CANCEL','QUIT','quit','Q','q']:
			stay=False
		elif choice in ['1','r','R']:
			os.system('clear')
			log.write('resolution editing: ')
			log.print()
			print('current resolution :'+str(scriptSettings.x)+'x'+str(scriptSettings.y)+'@'+str(int(scriptSettings.percent*100))+'\n\n')
			choice = input('new resolution ? (1920x1080@100 for example or \'cancel\')')
			match = re.search(r'^(\d{3,5})x(\d{3,5})@(\d{2,3})$',choice)
			if match is not None:
				scriptSettings.x = int(match.group(1))
				scriptSettings.y = int(match.group(2))
				scriptSettings.percent = int(match.group(3))/100
				saveSettings(scriptSettings)
				log.write(choice+'\n')
			elif choice in ['cancel','CANCEL','QUIT','quit','Q','q']:
				log.write('cancel\n')
			else:
				log.write('error, change canceled, retry\n')
		elif choice in ['2','a','A']:
			os.system('clear')
			log.write('edit animation rate : ')
			log.print()
			print('current animation rate: '+str(scriptSettings.fps)+'fps\n\n')
			choice = input('new animation rate? ( 30 for example or \'cancel\')')
			match = re.search(r'^(\d{1,})(fps)?$',choice)
			if match is not None:
				scriptSettings.fps = int(match.group(1))
				saveSettings(scriptSettings)
				log.write(match.group(1)+'fps\n')
			elif choice == 'cancel':
				log.write('cancel\n')
			else:
				log.write('error, change canceled, retry\n')
		else:
			log.write('unknow request!\n')











main()
