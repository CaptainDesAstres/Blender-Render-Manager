#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage preset'''
import xml.etree.ElementTree as xmlMod
from settingMod.Resolution import *
import os

class Preset:
	'''class to manage preset'''
	
	
	def __init__(self, xml= None):
		'''initialize preset with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize preset with default value'''
		
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize preset with values extracted from an xml object'''
		
	
	
	
	
	
	def toXml(self):
		'''export preset into xml syntaxed string'''
		
	
	
	
	
	
	def see(self, log):
		'''menu to explore and edit preset settings'''
		
	
	
	
	
	
	def print(self):
		'''a method to print preset'''
		
	
	
	
	
	
	
	
	
	
	
