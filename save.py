#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
import os

def saveSettings(s):
	global scriptSettings
	setFile = open(os.getcwd()+'/settings','w')
	setFile.write(s.toXmlStr(True))
	setFile.close()

def saveQueue(q):
	global renderQueue
	queueFile = open(os.getcwd()+'/queue','w')
	queueFile.write(q.toXmlStr(True))
	queueFile.close()
