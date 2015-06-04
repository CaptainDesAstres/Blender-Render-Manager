#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module that contain queue class'''
from render import render

class queue:
	'''class who contain the list of all the rendering task to manage'''
	def __init__(self,xml=False):
		'''initialize queue object with empty queue who is filled with values extract from an xml object if paste to the function'''
		self.renders = []
		if xml != False:
			self.fromXml(xml)
	
	def fromXml(self,xml):
		'''extract rendering task parameters from an xml object and add them to the queue'''
		if xml.tag == 'queue':
			for r in xml.findall('render'):
				self.add(render(r))
		
	def toXmlStr(self,head=False):
		'''export rendering task queue to an xml syntax string '''
		txt =''
		if head:
			txt+= '<?xml version="1.0" encoding="UTF-8"?>\n'
		txt += '<queue>\n'
		for r in self.renders:
			txt += r.toXmlStr()
		txt += '</queue>\n'
		return txt
	
	def add(self,added):
		'''add rendering task to the queue''' 
		if type(added) == render:
			self.renders.append(added)



