#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage resolution settings'''
import xml.etree.ElementTree as xmlMod
from settingMod.Size import *
import os

class Resolution:
	'''class to manage resolution settings'''
	
	
	def __init__(self, xml= None):
		'''initialize resolution settings with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize resolution settings with default value'''
		
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize resolution settings with values extracted from an xml object'''
		
	
	
	
	
	
	def toXml(self):
		'''export resolution settings into xml syntaxed string'''
		
	
	
	
	
	
	def see(self, log):
		'''menu to explore and edit resolution settings settings'''
		
	
	
	
	
	
	def print(self):
		'''a method to print preset'''
		
	
	
	
	
	
	
	
	
	
	
