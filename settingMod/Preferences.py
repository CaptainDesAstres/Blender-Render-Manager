#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage preferences of the script'''
import xml.etree.ElementTree as xmlMod
from settingMod.VersionList import *

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
		
		self.blenderVersionList = VersionList( xml.find('versionsList') )
		
	
	
	
	
	
	def toXml(self):
		'''export preferences settings into xml syntaxed string'''
		xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
		
		xml += '<preferences>\n'
		
		# export blender version list
		xml += self.blenderVersionList.toXml()
		
		xml += '</preferences>\n'
		
		return xml
	
	
	
	
	
	def see(self, log):
		'''method to see preferences settings and access edition menu'''
		
	
	
	
	
	
	
	
	
	
	
	
