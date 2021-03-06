#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage tiles sizes'''
import xml.etree.ElementTree as xmlMod
import os
from Preferences.PresetList.Preset.ValueType.Size import *

class Tiles:
	'''class to manage tiles sizes'''
	
	
	def __init__(self, xml= None):
		'''initialize tiles sizes with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize tiles sizes with default value'''
		self.GPU = Size(XYstr = '256x256')
		self.CPU = Size(XYstr = '32x32')
		self.BI = Size(XYstr = '256x256')
		
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize tiles sizes with values extracted from an xml object'''
		self.GPU = Size(xml = xml.find('GPU'))
		self.CPU = Size(xml = xml.find('CPU'))
		self.BI = Size(xml = xml.find('BI'))
	
	
	
	
	
	def toXml(self):
		'''export tiles sizes into xml syntaxed string'''
		txt = '<tilesSet>\n'
		txt += '  <GPU '+self.GPU.toXmlAttr()+' />\n'
		txt += '  <CPU '+self.CPU.toXmlAttr()+' />\n'
		txt += '  <BI '+self.BI.toXmlAttr()+' />\n'
		txt += '</tilesSet>\n'
		return txt
	
	
	
	
	
	def menu(self, log):
		'''method to see tiles sizes and access edition menu'''
		change = False
		log.menuIn('Tiles Sizes')
		
		while True:
			
			log.print()
			
			print('\n')
			self.print()
			
			print('''\n\n        \033[4mMenu :\033[0m
1- Edit Cycles GPU Tiles Size
2- Edit Cycles CPU Tiles Size
3- Edit Blender Internal Tiles Size
0- Save And Quit

''')
			choice = input().strip().lower()
			
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			elif choice == '1':
				# edit Cycles GPU Tiles Size
				change = (self.GPU.edit(log, 'Cycles GPU Tiles Size') or change)
			elif choice == '2':
				# edit Cycles CPU Tiles Size
				change = (self.CPU.edit(log, 'Cycles CPU Tiles Size') or change)
			elif choice == '3':
				# edit Blender Internal Tiles Size
				change = (self.BI.edit(log, 'Blender Internal Tiles Size') or change)
			else:
				log.error('Unvalid menu index!', False)
	
	
	
	
	
	def print(self):
		'''a method to display the tiles sizes settings'''
		
		print('Cycles GPU Tiles Size :        '+self.GPU.toStr())
		print('Cycles CPU Tiles Size :        '+self.CPU.toStr())
		print('Blender Internal Tiles Size :  '+self.BI.toStr())
	
	
	
	
	
	
	
	
	
	
