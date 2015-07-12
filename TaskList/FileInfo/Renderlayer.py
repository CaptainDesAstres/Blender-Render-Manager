#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage blender Renderlayer info'''
import xml.etree.ElementTree as xmlMod
import os

class Renderlayer:
	'''class to manage blender Renderlayer info'''
	
	
	def __init__(self, xml):
		'''initialize blender Renderlayer info with default settings or saved settings'''
		self.fromXml(xml)
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize blender Renderlayer info with savedd settings'''
		self.name = xml.get('name')
		self.use = {'True':True, 'False':False}[xml.get('use')]
	
	
	
	
	
	def toXml(self):
		'''export blender Renderlayer info into xml syntaxed string'''
		return '<renderlayer name="'+self.name+'" use="'+str(self.use)+'" />'
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
