#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage blender file info'''
import xml.etree.ElementTree as xmlMod
from TaskList.FileInfo.Scene import *
import os

class FileInfo:
	'''class to manage blender file info'''
	
	
	def __init__(self, xml):
		'''initialize blender file info with default settings or saved settings'''
		self.fromXml(xml)
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize blender file info with savedd settings'''
		self.scenes = {}
		for scene in xml.findall('scene'):
			self.scenes[scene.get('name')] = Scene(scene)
	
	
	
	
	
	def toXml(self):
		'''export blender file info into xml syntaxed string'''
		xml = '<fileInfo>'
		
		for scene in self.scenes:
			xml += scene.toXml()
		
		xml += '</fileInfo>'
		return xml
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
