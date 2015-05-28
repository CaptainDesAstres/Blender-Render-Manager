#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
import os

def saveSettings(s):
	global scriptSettings
	with open(os.getcwd()+'/settings','w') as setFile:
		setFile.write(s.toXmlStr(True))

def saveQueue(q):
	global renderQueue
	with open(os.getcwd()+'/queue','w') as queueFile:
		queueFile.write(q.toXmlStr(True))

