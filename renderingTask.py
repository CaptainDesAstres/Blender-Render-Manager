#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module containing class 'renderingTask' '''
from setting import setting

class renderingTask:
	'''class that contain the parameter for a rendering task'''
	
	def __init__(self,
					path = None, 
					scene = None, 
					fileXmlSetting = None,
					preferences = None,
					xml = None):
		'''renderingTask object initialisation
		if there is no xml argument paste to the function, the status of the object is set to 'unset', path and scene is an empty strings and settings is a setting object with default value'''
		if xml is None:
			print('renderingTask initialisation whithout xml done not yet implement')
		else:
			self.path = ''
			self.scene = ''
			self.fileSetting = setting()
			self.customSetting = setting()
			self.status='unset'
			
			self.fromXml(xml)
	
	def fromXml(self,xml):
		'''method that set the object attributes with the value extracted from an xml object with 'task' tag name '''
		if xml.tag == 'task':
			self.path = xml.get('path')
			self.scene = xml.get('scene')
			self.fileSetting.fromXml(xml.find('fileSet'))
			self.customSetting.fromXml(xml.find('taskSet'))
			self.status = 'ready'
		
	def toXmlStr(self,head=False):
		'''export the object values into an xml formated strings'''
		txt =''
		if head:
			txt+= '<?xml version="1.0" encoding="UTF-8"?>\n'
		txt += '<task path="'+self.path+'" scene="'+self.scene+'">\n'
		txt += '<taskSet>\n'+self.customSetting.toXmlStr()+'</taskSet>\n'
		txt += '<fileSet>\n'+self.fileSetting.toXmlStr()+'</fileSet>\n'
		txt += '</task>\n'
		return txt




