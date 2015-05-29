#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
from render import render

class queue:
	def __init__(self,xml=False):
		self.renders = []
		if xml != False:
			self.fromXml(xml)
	
	def fromXml(self,xml):
		if xml.tag == 'queue':
			for r in xml.findall('render'):
				self.add(render(r))
		
	def toXmlStr(self,head=False):
		txt =''
		if head:
			txt+= '<?xml version="1.0" encoding="UTF-8"?>\n'
		txt += '<queue>\n'
		for r in self.renders:
			txt += r.toXmlStr()
		txt += '</queue>\n'
		return txt
	
	def add(self,added):
		if type(added) == render:
			self.renders.append(added)



