#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''Script executed by Blender Python API to export info on a blender file in XML format in standart output'''
import bpy, sys, os
sys.path.append(os.path.abspath(sys.argv[4]+'/../../..'))
from usefullFunctions import XML

print('<?xml version="1.0" encoding="UTF-8"?>')
print('<fileInfo>')

for name in bpy.data.scenes.keys():
	scene = bpy.data.scenes[name]
	
	print('  <scene name="'+XML.encode(name)+'" start="'+str(scene.frame_start)\
			+'" end="'+str(scene.frame_end)+'" fps="'+str(scene.render.fps)+'" >')
	
	for renderlayer in scene.render.layers.keys():
		print('    <renderlayer name="'+XML.encode(renderlayer)+'" use="'+str(scene.render.layers[renderlayer].use)+'" />')
	
	print('  </scene>')

print('</fileInfo>')
