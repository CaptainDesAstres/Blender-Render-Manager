#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
import time
import os
from log import Log

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

def main(log):
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
			log.write('accès à une fonction indisponible pour le moment\n')
		elif choice in ['5','L','l']:
			log.write('accès à une fonction indisponible pour le moment\n')
		else:
			log.write('choix inconnue: "'+choice+'"\n')
	
		os.system('clear')
		log.print()




















main(log)

