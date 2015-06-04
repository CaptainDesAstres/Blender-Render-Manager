#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''functions to save config file and queue file '''
import os

def saveSettings(s):
	'''function that save preferences 's' in a configuration file'''
	with open(os.getcwd()+'/settings','w') as setFile:
		setFile.write(s.toXmlStr(True))

def saveQueue(q):
	'''function that save queue 'q' in queue xml file'''
	with open(os.getcwd()+'/queue','w') as queueFile:
		queueFile.write(q.toXmlStr(True))

