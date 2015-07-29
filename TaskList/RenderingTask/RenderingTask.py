'''A module to manage task rendering in blender'''
import bpy

def RenderingTask(task, preferences, groups, preset):
	scene = bpy.data.scenes[task.scene]
	bpy.context.screen.scene = scene
	sceneInfo = task.info.scenes[task.scene]
	scene.frame_start = sceneInfo.start
	scene.frame_end = sceneInfo.end
	scene.render.fps = sceneInfo.fps
	
	for name, RL in scene.render.layers.items():
		RL.use = sceneInfo.renderlayers[name].use
	
	
