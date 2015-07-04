#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage size settings representation'''
import xml.etree.ElementTree as xmlMod
import os

class Tiles:
	'''class to represent size settings'''
	
	
	def __init__(self, XYstr = None, xml= None):
		'''initialize size settings with default value or values extracted from an xml object'''
		if XYstr is not None:
			self.fromStr(XYstr)
		else:
			self.fromXml(xml)
	
	
	
	
	
	def fromStr(self, XYstr):
		'''initialize tiles sizes with default value'''
		
		
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize size with values extracted from an xml object'''
		
	
	
	
	
	
	def toXmlAttr(self):
		'''export size into xml syntaxed attribute string'''
		
	
	
	
	
	
	def print(self, index = False, std = True):
		'''a method to display the size settings'''
		
	
	
	
	
	
	
	
	
	
	
