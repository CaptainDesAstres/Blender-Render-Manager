#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
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

mainPath = os.path.abspath(sys.argv[0]+'/..')

def now(short = True):
	if short == True:
		return time.strftime('%H:%M:%S')
	else:
		return time.strftime('%d.%m.%Y-%H:%M:%S')
		
start = now(False)
log = 'ouverture de Blender Render Manager\nSession du '+start+'\n'

#aller dans le dossier de configuration de Blender Render Manager
if not os.path.exists('/home/'+os.getlogin()+'/.BlenderRenderManager/'):
	log += 'No configuration directorie, create it: fail'
	os.mkdir('/home/'+os.getlogin()+'/.BlenderRenderManager')
	log = log[:len(log)-4]+'done\n'
else:
	log += 'Find configuration directorie\n'
os.chdir('/home/'+os.getlogin()+'/.BlenderRenderManager')

#vérifier l'existance du dossier des logs et création si necessaire:
if not os.path.exists(os.getcwd()+'/log/'):
	log += 'No log directorie, create it: fail'
	os.mkdir(os.getcwd()+'/log')
	log = log[:len(log)-4]+'done\n'

#création du fichier de log
log = Log(start,log)

#vérification de l'existence d'un fichier de configuration
if not os.path.exists(os.getcwd()+'/settings'):
	log.write('aucun fichier de configuration, création d\'un fichier par défaut:')
	scriptSettings = setting()
	saveSettings(scriptSettings)
	log.write('done\n')
else:
	log.write('récupération des préférences:')
	with open(os.getcwd()+'/settings','r') as setFile:
		scriptSettings = setting( xmlMod.fromstring( (setFile.read( ) ) ) )
	log.write('done\n')

#vérification de l'existence d'une liste de rendu
if not os.path.exists(os.getcwd()+'/queue'):
	log.write('aucune liste existante, création d\'une queue vide:')
	renderQueue = queue()
	saveQueue(renderQueue)
	log.write('done\n')
else:
	log.write('lecture de la queue:')
	with open(os.getcwd()+'/queue','r') as queueFile:
		renderQueue = queue( xmlMod.fromstring( (queueFile.read( ) ) ) )
	log.write('done\n')




def main():
	global log
	#affichage du menu
	os.system('clear')
	continu =True

	while continu:
		log.write('Menu principal\n')
		print('''	Main Menu
			1- Add
			2- List
			3- Run
			4- Preferences
			5- Log
			0- Quit

	hit corresponding number or first letter :

	''')
	
		choice = input()
		if choice in ['0','q','Q']: 
			log.write('fermeture de Blender Render Manager\n')
			continu=False
		elif choice in ['1','A','a']:
			log.write('choix: ajout de fichier\n')
			addFile();
		elif choice in ['2','L','l']:
			log.write('accès à une fonction indisponible pour le moment\n')
		elif choice in ['3','R','r']:
			log.write('accès à une fonction indisponible pour le moment\n')
		elif choice in ['4','P','p']:
			log.write('voir les préférences\n')
			preference()
		elif choice in ['5','L','l']:
			log.write('accès à une fonction indisponible pour le moment\n')
		else:
			log.write('choix inconnue: "'+choice+'"\n')
	
		os.system('clear')
		log.print()

def addFile():
	global log, renderQueue
	os.system('clear')
	path = ''
	while path == '':
		path = input("Add File\n\tchemin absolue du fichier (ou 'cancel')").strip()
		
		
		if path != 'cancel':
			if path[0] in ['\'', '"'] and path[-1] in ['\'', '"']:
				path = path[1:len(path)-1]
				print(path)
			
			if path[0] != '/':
				print('ceci n\'est pas un chemin absolue!')
				log.write('chemin non absolue refuser:'+path+'\n')
				path = ''
			elif len(path) < 7 or path[len(path)-6:] !='.blend':
				print('le chemin ne semble pas correspondre à un fichier blender!')
				log.write('le chemin ne correspond pas à un fichier blender:'+path+'\n')
				path = ''
			elif os.path.exists(path):
				log.write('préparation de l\'ajout du fichier dans la liste :'+path+'\n')
				prefXml = os.popen('blender -b "'+path+'" -P "'+mainPath+'/filePrefGet.py" ').read()
				prefXml = re.search(r'<\?xml(.|\n)*</preferences>',prefXml).group(0)
				
				prefXml = xmlMod.fromstring(prefXml).findall('scene')
				
				if len(prefXml)>1:
					os.system('clear')
					log.print()
					print('\til y a plusieurs scenes dans le fichier :\n\n')
					i=0
					
					for s in prefXml:
						print(str(i)+'- '+s.get('name'))
						i+=1
					
					sceneChoiceRecquired = True
					while sceneChoiceRecquired:
						choice = input('scene à utiliser:')
						if(re.search(r'^\d+$',choice) and int(choice)<i):
							scene = prefXml[int(choice)]
							log.write('utilisation de la scene «'+scene.get('name')+'»\n')
							sceneChoiceRecquired=False
						else:
							print('choix de scene invalide\n')
				else:
					scene = prefXml[0]
					log.write('utilisation de la seule scene du fichier:'+scene.get('name')+'\n')
				
				pref = setting(scene)
				print('''		choix des réglages à utiliser pour ce fichier
	réglage du fichier (f) :
	''')
				pref.printSceneSettings(scriptSettings)
				print('\tréglage par défaut (d) :\n')
				scriptSettings.printSceneSettings()
				print('''	éditer depuis les réglages du fichier (ef)
	éditer depuis les réglages par défaut (ed)''')
				choice = input('choix (ou q):')
				
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
				print('ce fichier n\'existe pas!')
				log.write('le fichier n\'existe pas:'+path+'\n')
				path = ''	
		else:
			log.write('action annulée\n')

def preference():
	global scriptSettings
	global log
	prefStay = True
	while prefStay:
		os.system('clear')
		log.print()
		print('\t\tPréférences\n')
		scriptSettings.printSettings()
		choice= input('(e)dit, (r)eset ou (q)uit: ')
		if choice in ['e','E']:
			log.write('éditer des préférences\n')
			prefEdit()
		elif choice in ['Q','q']:
			log.write('quitter les préférences\n')
			prefStay = False
		elif choice in ['R','r']:
			confirm = input('cet action rétablira les réglages par défaut. confirmer (y/n):')
			if confirm in ['y','Y']:
				scriptSettings = setting()
				saveSettings(scriptSettings)
				log.write('rétablissement des préférences par défaut\n')
			else:
				log.write('rétablissement des préférences aborté\n')
		else:
			log.write('demande incomprise\n')

def prefEdit():
	global log
	global scriptSettings
	stay = True
	while stay:
		os.system('clear')
		log.print()
		print('''		Edition des Préférences
	1- Résolution
	2- Animation rate
	''')
		
		choice = input('quel réglage voulais vous éditer?(\'cancel\' pour annuler)')
		if choice in ['cancel','CANCEL','QUIT','quit']:
			stay=False
		elif choice in ['1','r','R']:
			os.system('clear')
			log.write('modification de la résolution: ')
			log.print()
			print('résolution actuel:'+str(scriptSettings.x)+'x'+str(scriptSettings.y)+'@'+str(int(scriptSettings.percent*100))+'\n\n')
			choice = input('nouvelle résolution? (1920x1080@100 par exemple ou \'cancel\' pour annuler)')
			match = re.search(r'^(\d{3,5})x(\d{3,5})@(\d{2,3})$',choice)
			if match is not None:
				scriptSettings.x = int(match.group(1))
				scriptSettings.y = int(match.group(2))
				scriptSettings.percent = int(match.group(3))/100
				saveSettings(scriptSettings)
				log.write(choice+'\n')
			elif choice == 'cancel':
				log.write('annulé\n')
			else:
				log.write('erreur, changement annulé\n')
		elif choice in ['2','a','A']:
			os.system('clear')
			log.write('modification de la vitesse d\'animation : ')
			log.print()
			print('animation actuel : '+str(scriptSettings.fps)+'fps\n\n')
			choice = input('vitesse? ( 30 par exemple ou \'cancel\' pour annuler)')
			match = re.search(r'^(\d{1,})(fps)?$',choice)
			if match is not None:
				scriptSettings.fps = int(match.group(1))
				saveSettings(scriptSettings)
				log.write(match.group(1)+'fps\n')
			elif choice == 'cancel':
				log.write('annulé\n')
			else:
				log.write('erreur, changement annulé\n')
		else:
			log.write('choix non compris!\n')











main()
