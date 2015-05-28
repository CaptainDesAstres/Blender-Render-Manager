#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
import time
import os
import sys
import xml.etree.ElementTree as xmlMod
import re
from log import Log
from setting import setting
from queue import queue
from save import *

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
	global log
	os.system('clear')
	path = ''
	while path == '':
		path = input("Add File\n\tchemin absolue du fichier (ou 'cancel')")
		
		if path != 'cancel':
			if path[0] != '/':
				print('ceci n\'est pas un chemin absolue!')
				log.write('chemin non absolue refuser:'+path+'\n')
				path = ''
			elif len(path) < 7 or path[len(path)-6:] !='.blend':
				print('le chemin ne semble pas correspondre à un fichier blender!')
				log.write('le chemin ne correspond pas à un fichier blender:'+path+'\n')
				path = ''
			elif os.path.exists(path):
				prefXml = os.popen('blender -b "'+path+'" -P "'+mainPath+'/filePrefGet.py" ').read()
				prefXml = re.search(r'<\?xml(.|\n)*</preferences>',prefXml).group(0)
				prefXml = xmlMod.fromstring(prefXml).find('scene')
				pref = setting(prefXml)
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
		print('résolution : '+str(scriptSettings.x)+'x'+str(scriptSettings.y)+' (@'+str(int(scriptSettings.percent*100))+'%)\n')
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
		else:
			log.write('choix non compris!\n')











main()
