#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

def columnLimit(value, limit, begin = True):
	'''function to make sure to have a good column size'''
	if type(value) is not str:
		value = str(value)
	
	if begin is True:
		begin = limit
	
	if len(value) > limit:
		return value[0:begin-1]+'…'+value[len(value)-(limit-begin):]+'|'
	else:
		return value+(' '*(limit-len(value)))+'|'





def indexPrintList(l):
	'''a function to print a list with element index'''
	
	for i, v in enumerate(l):
		print(str(i)+'- '+str(v))
	





