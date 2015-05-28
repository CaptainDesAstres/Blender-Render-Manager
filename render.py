#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
from setting import setting

class render:
	def __init__(self,xml=False):
		self.path = ''
		self.scene = ''
		self.settings = setting()
		self.status='unset'
		
		if xml != False:
			self.fromXml(xml)
	
	def fromXml(self,xml):
		if xml.tag == 'render':
			self.path = xml.get('path')
			self.scene = xml.get('scene')
			self.settings.parseXml(xml.find('settings'))
			self.status = 'ready'
		
	def toXmlStr(self,head=False):
		txt =''
		if head:
			txt+= '<?xml version="1.0" encoding="UTF-8"?>\n'
		txt += '<render path="'+self.path+'" scene="'+self.scene+'">\n'
		txt += self.settings.toXmlStr()
		txt += '</render>\n'
		return txt




