#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage preferences of the script'''
import xml.etree.ElementTree as xmlMod


class Preferences:
	'''class dedicated to script preferences settings'''
	
	
	def __init__(self, xml= None):
		'''initialize preferences object with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize preferences object with default value'''
		
		self.blenderVersionList = VersionList()
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize preferences object with values extracted from an xml object'''
		
	
	
	
	
	
	def toXml(self):
		'''export preferences settings into xml syntaxed string'''
		return ''
	
	
	
	
	
	def see(self, log):
		'''method to see preferences settings and access edition menu'''
		
	
	
	
	
	
	
	
	
	
	
	
