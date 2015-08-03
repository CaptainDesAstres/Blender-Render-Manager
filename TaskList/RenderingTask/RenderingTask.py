'''A module to manage task rendering in blender'''
import bpy, sys, os
sys.path.append(os.path.abspath(sys.argv[4]+'/../../../..'))
from Preferences.PresetList.Preset.Preset import *

def RenderingTask(task, preferences, groups, preset):
	scene = bpy.data.scenes[task.scene]
	bpy.context.screen.scene = scene
	sceneInfo = task.info.scenes[task.scene]
	scene.frame_start = sceneInfo.start
	scene.frame_end = sceneInfo.end
	scene.render.fps = sceneInfo.fps
	
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
	
	
	for name, RL in scene.render.layers.items():
		RL.use = sceneInfo.renderlayers[name].use
	
	preset.applyAndRun(scene, task, preferences, groups)








