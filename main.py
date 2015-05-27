#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import os
prelog = 'ouverture de Blender Render Manager\n'
#aller dans le dossier de configuration de Blender Render Manager
if not os.path.exists('/home/'+os.getlogin()+'/.BlenderRenderManager'):
	prelog += 'No configuration directorie, create it: fail'
	os.mkdir('/home/'+os.getlogin()+'/.BlenderRenderManager')
	prelog = prelog[:len(prelog)-4]+'done\n'
else:
	prelog += 'Find configuration directorie\n'
os.chdir('/home/'+os.getlogin()+'/.BlenderRenderManager')

#vérifier l'existance du dossier des logs et création si necessaire:
if not os.path.exists(os.getcwd()+'/log'):
	prelog += 'No log directorie, create it: fail'
	os.mkdir(os.getcwd()+'/log')
	prelog = prelog[:len(prelog)-4]+'done\n'

print(prelog)













