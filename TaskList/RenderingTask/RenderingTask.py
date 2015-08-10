'''A module to manage task rendering in blender'''
import bpy, sys, os
sys.path.append(os.path.abspath(sys.argv[4]+'/../../../..'))
from Preferences.PresetList.Preset.Preset import *

def RenderingTask(task, preferences, groups):
	
	
	scene = bpy.data.scenes[task.scene]
	bpy.context.screen.scene = scene
	
	scene.render.use_stamp_time = True
	scene.render.use_stamp_date = True
	scene.render.use_stamp_render_time = True
	scene.render.use_stamp_frame = True
	scene.render.use_stamp_scene = True
	scene.render.use_stamp_camera = True
	scene.render.use_stamp_lens = True
	scene.render.use_stamp_filename = True
	scene.render.use_stamp_marker = True
	scene.render.use_stamp_sequencer_strip = True
	scene.render.use_stamp_note = True
	
	
	metadata = 'uid:'+task.uid+';Main preset :«'+task.preset+'»;'
	version = str(bpy.app.version[0])+'.'+str(bpy.app.version[1])
	
	preset = task.log.preset
	
	if type(preset) is Preset:
		sceneInfo = task.info.scenes[task.scene]
		scene.frame_start = sceneInfo.start
		scene.frame_end = sceneInfo.end
		scene.render.fps = sceneInfo.fps
		
		preset.applyAndRun(bpy, scene, preferences, metadata, version)
	else:
		preset.applyAndRun(bpy, scene, task, preferences, groups, version)








