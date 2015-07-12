#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage blender scene info'''
import xml.etree.ElementTree as xmlMod
from TaskList.FileInfo.Renderlayer import *
import os

class Scene:
	'''class to manage blender scene info'''
	
	
	def __init__(self, xml):
		'''initialize blender scene info with default settings or saved settings'''
		self.fromXml(xml)
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize blender scene info with savedd settings'''
		self.name = xml.get('name')
		self.start = xml.get('start')
		self.end = xml.get('end')
		self.fps = xml.get('fps')
		
		self.renderlayers = {}
		for RL in xml.findall('renderlayer'):
			self.renderlayers[RL.get('name')] = Renderlayer(RL)
	
	
	
	
	
	def toXml(self):
		'''export blender scene info into xml syntaxed string'''
		xml = '<scene name="'+self.name+'" start="'+str(self.start)\
			+'" end="'+str(self.end)+'" fps="'+str(self.fps)+'" >'
		
		for RL in self.renderlayers.values():
			xml += RL.toXml()
		
		xml += '</scene>'
		return xml
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
