#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import os

#on vas dans le dossier dédié a blender manager
os.chdir('/home/'+os.getlogin()+'/')
try:
	os.listdir(os.getcwd()).index('.BlenderRenderManager')
except ValueError:
	#si le dossier n'existe pas on le créer
	os.mkdir('.BlenderRenderManager')
os.chdir('/home/'+os.getlogin()+'/.BlenderRenderManager')


