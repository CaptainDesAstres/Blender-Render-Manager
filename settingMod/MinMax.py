#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage MinMax settings representation'''
import xml.etree.ElementTree as xmlMod
import os, re

class MinMax:
	'''class to represent MinMax settings'''
	
	
	def __init__(self, mMstr = None, xml= None):
		'''initialize MinMax settings with default value or values extracted from an xml object'''
		if mMstr is not None:
			self.fromStr(mMstr)
		else:
			self.fromXml(xml)
	
	
	
	
	
	def fromStr(self, mMstr):
		'''initialize MinMax with default value'''
		mMstr = mMstr.split('to')
		self.min = int(mMstr[0].strip())
		self.max = int(mMstr[1].strip())
		
		if self.min > self.max:
			self.min = self.max
	
	
	
	
	
	def check(mMstr):
		'''class method to check if a string well syntaxed to be used by MinMax.fromStr()'''
		return re.search(r'^\d{1,} *to *\d{1,}$', mMstr) is not None
		
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize MinMax with values extracted from an xml object'''
		self.min = int(xml.get('min'))
		self.max = int(xml.get('max'))
	
	
	
	
	
	def toXmlAttr(self):
		'''export MinMax into xml syntaxed attribute string'''
		return 'min="'+str(self.min)+'" max="'+str(self.max)+'"'
	
	
	
	
	
	def toStr(self):
		'''A method to export settings in a simple string'''
		return str(self.min)+' to '+str(self.max)
	
	
	
	
	
	def print(self):
		'''a method to display the MinMax settings'''
		print(self.toStr(), sep='')
	
	
	
	
	def edit(self, log, label):
		'''a method to edit MinMax object'''
		log.menuIn('Edit '+label)
		
		while True:
			os.system('clear')
			log.print()
			
			print('\n\n        Edit '+label+' :\n\nCurrent '+label+' :'+self.toStr()+'\n')
			choice = input('new min/max settings (syntaxe: MIN to Max):').strip().lower()
			
			if choice in ['', 'q', 'quit', 'cancel']:
				log.menuOut()
				return False
			
			if MinMax.check(choice):
				self.fromStr(choice)
				log.write(label+' set to : '+choice+'\n')
				log.menuOut()
				return True
			else:
				log.error('Unvalid setting syntaxe, respect the syntaxe «MIN to Max», where MIN and MAX are decimal number.')
				continue
			
	
	
	
	
	
