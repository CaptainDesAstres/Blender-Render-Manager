#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage list of all know version of Blender in the system'''
import xml.etree.ElementTree as xmlMod


class VersionList:
	'''class dedicated to Blender version managing'''
	
	
	def __init__(self, xml= None):
		'''initialize Blender version list with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize Blender version list with default value'''
		
		self.alias = ['Standard Blender']
		self.path = ['blender']
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize Blender version list with values extracted from an xml object'''
		
	
	
	
	
	
	def toXml(self):
		'''export Blender version list into xml syntaxed string'''
		return ''
	
	
	
	
	
	def see(self, log):
		'''method to see Blender version list and access edition menu'''
		
	
	
	
	
	
	
	
	
	
	
	
