#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''functions to save config file and queue file '''
import os, re


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

def checkLogLimit(limit):
	'''a function tou limit the session log number'''
	content = os.listdir(os.getcwd()+'/log/')
	
	if len(content) > limit:
		logRegex = re.compile(r'^session (\d{2})\.(\d{2})\.(\d{4})-(\d{2}):(\d{2}):(\d{2})\.log$')
		logs = {}
		for f in content:
			match = logRegex.match(f)
			if match is not None:
				t = int(match.group(3))*12+int(match.group(2))
				t = t*31+int(match.group(1))
				t = t*24+int(match.group(4))
				t = t*60+int(match.group(5))
				t = t*60+int(match.group(6))
				logs[t] = f
		
		if len(logs) > limit:
			keys = list(logs.keys())
			keys.sort()
			while len(logs) > limit:
				k = keys.pop(0)
				f = logs.pop(k)
				os.remove(os.getcwd()+'/log/'+f)




