#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage rendering output path'''
import xml.etree.ElementTree as xmlMod
import os

class Output:
	'''class to manage rendering output path'''
	
	
	def __init__(self, xml= None):
		'''initialize output path with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize output path with default value'''
		
		if not os.path.exists('/home/'+os.getlogin()+'/.BlenderRenderManager/render'):
			os.mkdir('/home/'+os.getlogin()+'/.BlenderRenderManager/render')
		self.path = '/home/'+os.getlogin()+'/.BlenderRenderManager/render'
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize output path with values extracted from an xml object'''
		self.path = xml.get('path')
	
	
	
	
	
	def toXml(self):
		'''export output path into xml syntaxed string'''
		return '<output path="'+self.path+'" />\n'
	
	
	
	
	
	def see(self, log):
		'''method to see output path and access edition menu'''
		
	
	
	
	
	
	def print(self, index = False, std = True):
		'''a method to display the output path settings'''
		
	
