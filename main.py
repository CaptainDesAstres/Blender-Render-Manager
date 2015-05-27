#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
import time
import os

def now(short = True):
	if short == True:
		return time.strftime('%H:%M:%S')
	else:
		return time.strftime('%d/%m/%Y-%H:%M:%S')

log = 'ouverture de Blender Render Manager\nSession du '+now(False)+'\n'

#aller dans le dossier de configuration de Blender Render Manager
if not os.path.exists('/home/'+os.getlogin()+'/.BlenderRenderManager'):
	log += 'No configuration directorie, create it: fail'
	os.mkdir('/home/'+os.getlogin()+'/.BlenderRenderManager')
	log = log[:len(log)-4]+'done\n'
else:
	log += 'Find configuration directorie\n'
os.chdir('/home/'+os.getlogin()+'/.BlenderRenderManager')

#vérifier l'existance du dossier des logs et création si necessaire:
if not os.path.exists(os.getcwd()+'/log'):
	log += 'No log directorie, create it: fail'
	os.mkdir(os.getcwd()+'/log')
	log = log[:len(log)-4]+'done\n'

print(log)













