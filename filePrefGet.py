#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''Script executed by Blender Python API for recoverring a blender file settings in XML format in standart output'''

import bpy
import sys, os
sys.path.append(os.path.abspath(sys.argv[0]+'/..'))
from setting import *

print('<?xml version="1.0" encoding="UTF-8"?>')
print('<preferences>')

for name in bpy.data.scenes.keys():
	scene = bpy.data.scenes[name]
	
	print('\t<scene name="'+name+'">')
	pref = setting()
	
	
	print('\t\t'+pref.toXmlStr().replace('\n','\n\t\t'))
	print('\t</scene>')
print('</preferences>')
