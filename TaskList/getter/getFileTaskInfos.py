#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''Script executed by Blender Python API to export info on a blender file in XML format in standart output'''
import bpy
import sys, os, re

print('<?xml version="1.0" encoding="UTF-8"?>')
print('<fileInfo>')

for name in bpy.data.scenes.keys():
	scene = bpy.data.scenes[name]
	
	print('  <scene name="'+name+'" start="'+str(scene.frame_start)\
			+'" end="'+str(scene.frame_end)+'" fps="'+str(scene.render.fps)+'" >')
	
	for renderlayer in scene.render.layers.keys():
		print('    <renderlayer name="'+renderlayer+'" use="'+str(scene.render.layers[renderlayer].use)+'" />')
	
	print('  </scene>')

print('</fileInfo>')
