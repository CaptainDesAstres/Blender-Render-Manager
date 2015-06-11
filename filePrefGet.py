#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''Script executed by Blender Python API for recoverring a blender file settings in XML format in standart output'''

import bpy
import sys, os, re
sys.path.append(os.path.abspath(sys.argv[0]+'/..'))
from setting import *

print('<?xml version="1.0" encoding="UTF-8"?>')
print('<preferences>')

for name in bpy.data.scenes.keys():
	scene = bpy.data.scenes[name]
	
	print('\t<scene name="'+name+'">')
	pref = setting()
	
	# render resolution
	pref.x = scene.render.resolution_x
	pref.y = scene.render.resolution_y
	pref.percent = scene.render.resolution_percentage
	
	# animation parameters
	pref.start = scene.frame_start
	pref.end = scene.frame_end
	pref.fps = scene.render.fps
	
	# performance tile size
	pref.tilesCyclesCPUX = pref.tilesBIX = pref.tilesCyclesGPUX = scene.render.tile_x
	pref.tilesCyclesCPUY = pref.tilesBIY = pref.tilesCyclesGPUY = scene.render.tile_y
	
	#rendering engine parameters
	pref.renderingEngine = scene.render.engine
	pref.renderingDevice = scene.cycles.device
	pref.filmExposure = scene.cycles.film_exposure
	if pref.renderingEngine == 'CYCLES':
		pref.filmTransparentEnable = scene.cycles.film_transparent
	else:
		pref.filmTransparentEnable = (scene.render.alpha_mode == 'TRANSPARENT')
	pref.backgroundCyclesSamples = pref.foregroundCyclesSamples = pref.mainAnimationCyclesSamples = scene.cycles.samples
	
	
	#cycles ligth path parameters
	pref.transparencyMaxBounces = scene.cycles.transparent_max_bounces
	pref.transparencyMinBounces = scene.cycles.transparent_min_bounces
	pref.bouncesMax = scene.cycles.max_bounces
	pref.bouncesMin = scene.cycles.min_bounces
	pref.diffuseBounces = scene.cycles.diffuse_bounces
	pref.glossyBounces = scene.cycles.glossy_bounces
	pref.transmissionBounces = scene.cycles.transmission_bounces
	pref.volumeBounces = scene.cycles.volume_bounces
	
	
	pref.backgroundLayersKeywords = []
	pref.foregroundLayersKeywords = []
	
	#list the render layers and their specific parameters
	pref.renderLayerList = []
	pref.objectIndexPass = pref.zPass = False
	for name in scene.render.layers.keys():
		layer = scene.render.layers[name]
		pref.renderLayerList.append({ 
						'name' : name , 
						'z' : layer.use_pass_z , 
						'object index' : layer.use_pass_object_index , 
						'use' : layer.use 
						})
		if layer.use_pass_z:
			pref.zPass = True
		if layer.use_pass_object_index:
			pref.objectIndexPass = True
	
	
	#output parameters
	pref.outputFormat = scene.render.image_settings.file_format
	pref.outputPath = bpy.path.abspath(scene.render.filepath)
	if pref.outputPath[len(pref.outputPath)-1] == '/':
		pref.outputName = '%N - %S - %L - %F'+scene.render.file_extension
	else:
		parsePath = pref.outputPath.split('/')
		pref.outputName = re.replace(r'#+','%F',parsePath.pop())
		pref.outputPath = '/'.join(parsePath)+'/'
	pref.outputSubPath = ''
	pref.blenderPath = bpy.app.binary_path
	
	#other option
	pref.compositingEnable = scene.render.use_compositing
	if scene.render.use_simplify:
		pref.simplify = scene.render.simplify_subdivision
	
	
	print('\t\t'+pref.toXmlStr().replace('\n','\n\t\t'))
	print('\t</scene>')
print('</preferences>')
