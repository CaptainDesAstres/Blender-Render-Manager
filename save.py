#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''functions to save config file and queue file '''
import os


def savePreferences(s):
	'''function that save preferences 's' in a preferences file'''
	with open(os.getcwd()+'/preferences','w') as prefFile:
		prefFile.write(s.toXml())

def saveTasks(t):
	'''function that save Tasks List in xml file'''
	with open(os.getcwd()+'/Tasks','w') as tasksFile:
		tasksFile.write(t.toXml())

def createLockFile(processInfo):
	'''Function to create lock file'''
	with open(os.getcwd()+'/lock','w') as lockFile:
		lockFile.write(processInfo)

def eraseLockFile():
	'''Function to erase lock file'''
	os.remove(os.getcwd()+'/lock')





