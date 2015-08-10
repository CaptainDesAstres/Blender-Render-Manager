#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

def columnLimit(value, limit, begin = True, sep = '|'):
	'''function to make sure to have a good column size'''
	if type(value) is not str:
		value = str(value)
	
	if begin is True:
		begin = limit
	
	if len(value) > limit:
		return value[0:begin-1]+'…'+value[len(value)-(limit-begin):]+sep
	else:
		return value+(' '*(limit-len(value)))+sep





def indexPrintList(l):
	'''a function to print a list with element index'''
	
	for i, v in enumerate(l):
		print(str(i)+'- '+str(v))
	





class XML:
	''' a class containing usefull method for XML'''
	
	entities = {
				'\'':'&apos;',
				'"':'&quot;',
				'<':'&lt;',
				'>':'&gt;'
				}
	
	
	
	
	
	def encode(txt):
		'''a method to replace XML entities by XML representation'''
		
		txt.replace('&', '&amp;')
		
		for entity, code in XML.entities.items():
			txt.replace(entity, code)
	
	
	
	
	
	def decode(txt):
		'''a method to replace XML representation of entities by the original entities'''
		
		for entity, code in XML.entities.items():
			txt.replace(code, entity)
		
		txt.replace('&amp;', '&')





