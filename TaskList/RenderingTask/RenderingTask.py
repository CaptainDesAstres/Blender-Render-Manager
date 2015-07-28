'''A module to manage task rendering in blender'''
import bpy

def RenderingTask(task, preferences, groups, preset):
	scene = bpy.data.scenes[task.scene]
