#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''functions to save config file and queue file '''
import os

def saveSettings(s):
	'''function that save preferences 's' in a configuration file'''
	with open(os.getcwd()+'/settings','w') as setFile:
		setFile.write(s.toXmlStr(True, True))

def savePreferences(s):
	'''function that save preferences 's' in a preferences file'''
	with open(os.getcwd()+'/preferences','w') as prefFile:
		prefFile.write(s.toXml())

def saveQueue(q):
	'''function that save queue 'q' in queue xml file'''
	with open(os.getcwd()+'/queue','w') as queueFile:
		queueFile.write(q.toXmlStr(True))

