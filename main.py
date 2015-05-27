#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import os

#aller dans le dossier de configuration de Blender Render Manager
if not os.path.exists('/home/'+os.getlogin()+'/.BlenderRenderManager'):
	os.mkdir('/home/'+os.getlogin()+'/.BlenderRenderManager')
os.chdir('/home/'+os.getlogin()+'/.BlenderRenderManager')

#vérifier l'existance du dossier des logs et création si necessaire:
if not os.path.exists(os.getcwd()+'/log'):
	os.mkdir(os.getcwd()+'/log')














