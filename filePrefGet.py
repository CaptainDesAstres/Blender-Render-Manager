#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''Script executed by Blender Python API for recoverring a blender file settings in XML format in standart output'''

import bpy

print('<?xml version="1.0" encoding="UTF-8"?>')
print('<preferences>')

for name in bpy.data.scenes.keys():
	scene = bpy.data.scenes[name]
	
	print('\t<scene name="'+name+'">')
	
	#get resolution and animation parameters
	print('\t\t<resolution x="'+str(scene.render.resolution_x)+'" y="'+str(scene.render.resolution_y)+'" percent="'+str(scene.render.resolution_percentage)+'" />')
	print('\t\t<animation start="'+str(scene.frame_start)+'" end="'+str(scene.frame_end)+'" fps="'+str(scene.render.fps)+'" />')
	
	if scene.render.engine == 'CYCLES':
		#get Cycles specific parameters
		print('\t\t<engine engine="'+scene.render.engine+'" device="'+scene.cycles.device+'" sample="'+str(scene.cycles.samples)+'" />')
		print('\t\t<film exposure="'+str(scene.cycles.film_exposure)+'" transparent="'+str(scene.cycles.film_transparent)+'" />')
		print('\t\t<bouncesSet>')
		print('\t\t\t<transparency min="'+str(scene.cycles.transparent_min_bounces)+'" max="'+str(scene.cycles.transparent_max_bounces)+'" />')
		print('\t\t\t<bounces min="'+str(scene.cycles.min_bounces)+'" max="'+str(scene.cycles.max_bounces)+'" />')
		print('\t\t\t<diffuse bounces="'+str(scene.cycles.diffuse_bounces)+'" />')
		print('\t\t\t<glossy bounces="'+str(scene.cycles.glossy_bounces)+'" />')
		print('\t\t\t<transmission bounces="'+str(scene.cycles.transmission_bounces)+'" />')
		print('\t\t\t<volume bounces="'+str(scene.cycles.volume_bounces)+'" />')
		print('\t\t</bouncesSet>')
	else:
		print('\t\t<engine engine="'+scene.render.engine+'" device="'+scene.cycles.device+'" />')
	
	print('\t\t<output format="'+scene.render.image_settings.file_format+'" />')
	
	#get all Render Layer parameters
	print('\t\t<renderLayerList>')
	for renderLayerName in scene.render.layers.keys():
		layer = scene.render.layers[renderLayerName]
		print('\t\t\t<layer name="'+renderLayerName+'" z="'+str(layer.use_pass_z)+'" objIndex="'+str(layer.use_pass_object_index)+'" />')
	print('\t\t</renderLayerList>')
	
	print('\t</scene>')
print('</preferences>')
