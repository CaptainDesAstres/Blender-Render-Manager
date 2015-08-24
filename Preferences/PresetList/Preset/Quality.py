#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage Quality settings'''
import xml.etree.ElementTree as xmlMod
from usefullFunctions import *
from Preferences.PresetList.Preset.OSA import *
from Preferences.PresetList.Preset.ValueType.Size import *
import os

class Quality:
	'''class to manage Quality settings'''
	FORMATS = [ 'BMP', 'IRIS', 'PNG', 'JPEG', 'JPEG2000', 'TARGA', 'TARGA_RAW',\
				'CINEON', 'DPX', 'OPEN_EXR_MULTILAYER', 'OPEN_EXR', 'HDR', 'TIFF']
	COLOR_DEPTH = {
					'BMP'					:		[8],
					'IRIS'					:		[8],
					'JPEG'					:		[8],
					'TARGA'					:		[8],
					'TARGA_RAW'				:		[8],
					'CINEON'				:		[10],
					'PNG'					:		[8, 16],
					'TIFF'					:		[8, 16],
					'JPEG2000'				:		[8, 12, 16],
					'DPX'					:		[8, 10, 12, 16],
					'OPEN_EXR'				:		[16, 32],
					'OPEN_EXR_MULTILAYER'	:		[32],
					'HDR'					:		[32]
					}
	
	def __init__(self, xml= None):
		'''initialize Quality settings with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize Quality settings with default value'''
		self.pourcent = 100
		self.size = Size('1920x1080')
		self.samples = 1500
		self.simplify = None
		
		self.format = 'OPEN_EXR_MULTILAYER'
		self.colorDepth = 32
		self.JPEGquality = 100
		self.PNGcompression = 0 
		
		self.JPEGcodec = 'J2K'
		self.JPEGcinema = False
		self.JPEGcinema48 = False
		self.JPEGycc = False
		self.DPXlog = False
		self.EXRcodec = 'NONE'
		self.EXRzbuffer = True
		self.EXRpreviews = False
		
		self.OSA = OSA()
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize Quality settings with values extracted from an xml object'''
		node = xml.find('resolution')
		self.pourcent = int(node.get('pourcent'))
		self.size = Size(xml = node)
		self.samples = int(xml.find('samples').get('value'))
		if xml.find('simplify') is not None:
			self.simplify = int(xml.find('simplify').get('value'))
		else:
			self.simplify = None
		node = xml.find('format')
		self.format = node.get('value')
		self.colorDepth = int(node.get('depth'))
		self.JPEGquality = int(node.get('quality'))
		self.PNGcompression = int(node.get('compression'))
		
		self.JPEGcodec = node.get('jpegCodec')
		self.EXRcodec = node.get('exrCodec')
		
		
		self.JPEGcinema = node.get('cinema', '0') == '1'
		self.JPEGcinema48 = node.get('cinema48', '0') == '1'
		self.JPEGycc = node.get('ycc', '0') == '1'
		self.DPXlog = node.get('dpxlog', '0') == '1'
		self.EXRzbuffer = node.get('zbuffer', '0') == '1'
		self.EXRpreviews = node.get('previews', '0') == '1'
		
		self.OSA = OSA(xml.find('OSA'))
	
	
	
	
	
	def toXml(self):
		'''export Quality settings into xml syntaxed string'''
		txt = '<quality>\n'
		txt += '  <resolution pourcent="'+str(self.pourcent)+'" '+self.size.toXmlAttr()+' />\n'
		txt += '  <samples value="'+str(self.samples)+'" />\n'
		
		if self.simplify is not None:
			txt += '  <simplify value="'+str(self.simplify)+'" />\n'
		
		txt += '  <format value="'+self.format+'" depth="'+str(self.colorDepth)\
				+'" quality="'+str(self.JPEGquality)\
				+'" compression="'+str(self.PNGcompression)\
				+'" jpegCodec="'+self.JPEGcodec+'" exrCodec="'+self.EXRcodec+'" '
		
		if self.JPEGcinema:
			txt += 'cinema="1" '
		if self.JPEGcinema48:
			txt += 'cinema48="1" '
		if self.JPEGycc:
			txt += 'ycc="1" '
		if self.DPXlog:
			txt += 'dpxlog="1" '
		if self.EXRzbuffer:
			txt += 'zbuffer="1" '
		if self.EXRpreviews:
			txt += 'preview="1" '
		
		txt += ' />\n'
		
		txt += self.OSA.toXml()
		
		txt += '</quality>\n'
		return txt
	
	
	
	
	
	def menu(self, log):
		'''menu to explore and edit Quality settings settings'''
		change = False
		log.menuIn('Quality')
		
		while True:
			
			log.print()
			
			self.print()
			
			print('''\n\n        Menu :
1- Edit Resolution Size
2- Edit Pourcent Setting
3- Edit Cycles Samples
4- Edit OSA settings (for Blender Render only)
5- Edit Simplify Setting
6- Edit Format''')
			
			if len(self.COLOR_DEPTH[self.format]) > 1:
				print('7- Change Color Depth')
			
			if self.format == 'PNG':
				print('8- Edit Compression Settings')
			elif self.format in ['JPEG', 'JPEG2000']:
				print('8- Edit Quality Settings')
			
			if self.format == 'JPEG2000':
				print('9- Edit JPEG2000 Codec Options')
			elif self.format == 'DPX':
				
				if self.DPXlog:
					print('9- Disable DPX Logarithmic colorspace')
				else:
					print('9- Enable DPX Logarithmic colorspace')
				
			elif self.format in ['OPEN_EXR', 'OPEN_EXR_MULTILAYER']:
				print('9- Edit EXR Codec Options')
			
			print('0- Quit\n\n')
			
			choice = input('Action?').strip().lower()
			
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			elif choice == '1':
				change = (self.size.edit(log, 'Resolution Size') or change)
			elif choice in ['2', '3']:
				change = (self.edit(log, int(choice)) or change)
			elif choice == '4':
				change = (self.OSA.menu(log) or change)
			elif choice == '5':
				change = (self.editSimplify(log) or change)
			elif choice == '6':
				change = (self.editFormat(log) or change)
			elif choice == '7' and len(self.COLOR_DEPTH[self.format]) > 1:
				change = (self.editColorDepth(log) or change)
			elif choice == '8' and self.format in ['PNG','JPEG', 'JPEG2000']:
				change = (self.editCompressionQuality(log) or change)
			elif choice == '9' and self.format in ['OPEN_EXR', 'OPEN_EXR_MULTILAYER', 'DPX', 'JPEG2000']:
				if self.format == 'DPX':
					self.DPXlog = not self.DPXlog
					log.write('DPX Logarithmic color space '\
							+{ True:'enabled', False:'disabled' }[self.DPXlog]+'.')
					change = True
				elif self.format == 'JPEG2000':
					change = (self.editJpeg2000(log) or change)
				elif self.format == 'OPEN_EXR':
					change = (self.editExr(log) or change)
				else:
					change = (self.editExrCodec(log) or change)
			else:
				log.error('Unvalid menu choice', False)
		
	
	
	
	
	
	def print(self):
		'''a method to print preset'''
		enable = { True:'enabled', False:'disabled' }
		print('Resolution :            '+self.size.toStr()+'@'+str(self.pourcent))
		print('Cycles Samples :        '+str(self.samples))
		print('Simplify :              '+self.getSimplify())
		
		if self.format in ['JPEG', 'JPEG2000']:
			print('Format :                '+self.format+' (@'\
						+str(self.JPEGquality)+'%)')
		elif self.format == 'PNG':
			print('Format :                '+self.format+' (@'\
						+str(self.PNGcompression)+'%)')
		else:
			print('Format :                '+self.format)
		
		print('Color Depth :           '+str(self.colorDepth))
		
		if self.format == 'JPEG2000':
			print('JPEG2000 Codec :        '+self.JPEGcodec)
			opt = ''
			if self.JPEGcinema:
				opt += 'cinema '
			if self.JPEGcinema48:
				opt += 'cinema48 '
			if self.JPEGycc:
				opt += 'YCC'
			print('JPEG2000 options :      '+opt)
		elif self.format == 'DPX':
			print('DPX Log :               '\
				+enable[self.DPXlog])
		elif self.format in ['OPEN_EXR', 'OPEN_EXR_MULTILAYER']:
			print('EXR codec :             '+self.EXRcodec)
			if self.format == 'OPEN_EXR':
				print('EXR zbuffer :           '+enable[self.EXRzbuffer])
				print('EXR previews :          '+enable[self.EXRpreviews])
		
		self.OSA.print()
	
	
	
	
	
	def getSimplify(self):
		'''A method to get simplify setting'''
		if self.simplify is None:
			return 'Disabled'
		else:
			return str(self.simplify)+' subdiv'
	
	
	
	
	def edit(self, log, choice):
		'''A method to edit pourcent setting'''
		if choice == 2:
			log.menuIn('Edit Resolution Pourcent')
		else:
			log.menuIn('Edit Cycles Samples')
		
		while True:
			
			log.print()
			
			# print current setting and get new one
			if choice == 2:
				print('\n\n        Edit Pourcent :\nCurrent Pourcent : '+str(self.pourcent)+'\n')
				new = input('New pourcent setting?').strip().lower()
			else:
				print('\n\n        Edit Cycles Samples :\nCurrent Sammples : '+str(self.samples)+'\n')
				new = input('New Samples setting?').strip().lower()
			
			# exit menu
			if new in ['', 'q', 'quit', 'cancel']:
				log.menuOut()
				return False
			
			#check new setting
			try:
				new = int(new)
			except ValueError:
				log.error('New setting must be an integer.')
				continue
			
			if new < 0:
				log.error('New setting must be a positive integer.')
				continue
			
			# apply new setting and exit
			if choice == 2:
				self.pourcent = new
				log.write('Resolution pourcent setting is set to : '\
							+str(self.pourcent)+'%')
			else:
				self.samples = new
				log.write('Cycles samples set to : '+str(self.samples)+'%')
			log.menuOut()
			return True
		
	
	
	
	
	
	def editSimplify(self, log):
		'''A method to Edit Simplify settings'''
		log.menuIn('Edit Simplify settings')
		
		while True:
			
			log.print()
			
			# print current setting and get new one
			print('\n\n        Edit Simplify Settings :\nCurrent settings : '+self.getSimplify()+'\n')
			choice = input('New setting?').strip().lower()
			
			# exit menu
			if choice in ['', 'q', 'quit', 'cancel']:
				log.menuOut()
				return False
			
			#check new setting
			try:
				choice = int(choice)
			except ValueError:
				log.error('New setting must be an integer.')
				continue
			
			if choice < 0:
				log.error('New setting must be a positive integer.')
				continue
			
			if choice < 11:
				self.simplify = choice
			else:
				self.simplify = None
			log.write('Simplify set to : '+self.getSimplify())
			log.menuOut()
			return True
		
	
	
	
	
	
	def editFormat(self, log):
		'''A method to edit format settings'''
		
		log.menuIn('Choose Output Format')
		
		while True:
			
			log.print()
			
			print('\n\n        Edit Output Format :\n\nCurrent format : '+self.format)
			
			indexPrintList(self.FORMATS)
			
			choice = input('new format?').strip()
			
			if choice.lower() in ['', 'q', 'quit', 'cancel']:
				log.menuOut()
				return False
			
			try:
				choice = int(choice)
			except ValueError:
				log.error('An integer is expected!')
				continue
			
			if choice < 0 or choice >= len(self.FORMATS):
				log.error('Out of choice range!')
				continue
			
			self.format = self.FORMATS[choice]
			self.checkDepth(log)
			self.checkEXRcodec(log)
			log.write('Output format is set to : '+self.format)
			log.menuOut()
			return True
	
	
	
	
	
	def checkDepth(self, log):
		'''a method to check if current color depth is coherent with new set format'''
		depths = self.COLOR_DEPTH[self.format]
		
		if len(depths) == 1:
			self.colorDepth = depths[0]
		elif self.colorDepth not in depths:
			if self.colorDepth == 32:
				self.colorDepth = depths[-1]
			else:
				self.colorDepth = 16
		log.write('Color depth automatically set to '+str(self.colorDepth))
	
	
	
	
	
	def checkEXRcodec(self, log):
		'''check that EXR 16bit don't use B44 or B44A codec'''
		if self.format in ['OPEN_EXR', 'OPEN_EXR_MULTILAYER']\
			and self.colorDepth == 32 and self.EXRcodec in ['B44', 'B44A']:
			self.EXRcodec = 'NONE'
	
	
	
	
	
	def editColorDepth(self, log):
		'''a method to change color depth setting'''
		log.menuIn('Change Color Depth')
		depths = self.COLOR_DEPTH[self.format]
		while True:
			log.print()
			choice = input('\n\ncurrent settings : '+str(self.colorDepth)+' bits\n\navailable depth :['+ (','.join(str(x) for x in depths)) +'].\nwhat\'s the new depth (\'q\' to quit) :').lower().strip()
			
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return False
			
			try:
				choice = int(choice)
			except ValueError:
				log.error('error, integer value expected!')
				continue
			
			if choice in depths:
				self.colorDepth = choice
				log.write('Color depth set to '+str(self.colorDepth))
				self.checkEXRcodec(log)
				log.menuOut()
				return True
			else:
				log.error('error, unvalid value! excpeted value are:'+(','.join(str(x) for x in depths)))
	
	
	
	
	
	def editCompressionQuality(self, log):
		'''a method to edit output compression (png) or quality (jpg)'''
		png = (self.format == 'PNG')
		if png:
			log.menuIn('Edit Compression')
			current = self.PNGcompression
		else:
			log.menuIn('Edit Quality')
			current = self.JPEGquality
		
		while True:
			log.print()
			
			choice = input('\n\nCurrent setting : '+str(current)\
					+'%\n\nNew settings (integer between 0 and 100 or "q" to quit) : ').strip().lower()
			
			if choice in ['q', 'quit', 'cancel']:
				log.menuOut()
				return False
			
			try:
				choice = int(choice)
			except ValueError:
				log.error('error, integer value expected!')
				continue
			
			if choice >= 0 and choice <= 100:
				if png:
					self.PNGcompression = choice
					log.write('PNG compression set to '+str(self.PNGcompression)+'.')
				else:
					self.JPEGquality = choice
					log.write('JPEG quality set to '+str(self.JPEGquality)+'.')
				
				log.menuOut()
				return True
			else:
				log.error('error, expect a value between 0 and 100, not «'+str(choice)+'»!')
	
	
	
	
	
	def editJpeg2000(self, log):
		'''a method to edit JPEG2000 codec specific settings'''
		enable = {True:'enabled', False: 'disabled'}
		action = {True:'Disable', False: 'Enable'}
		change = False
		log.menuIn('Edit JPEG2000 Settings')
		while True:
			log.print()
			
			self.print()
			
			print('\n\n        Menu:')
			
			if self.JPEGcodec == 'J2K':
				print('1- switch to JP2 codec')
			else:
				print('1- switch to J2K codec')
			
			print('2- '+action[self.JPEGcinema]+' cinema Option')
			print('3- '+action[self.JPEGcinema48]+' cinema48 Option')
			print('4- '+action[self.JPEGycc]+' YCC Option')
			
			menu = input('0- Quit\n\nMenu choice :').strip().lower()
			
			if menu in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			
			if menu == '1':
				if self.JPEGcodec == 'J2K':
					self.JPEGcodec = 'JP2'
				else:
					self.JPEGcodec = 'J2K'
				change = True
				log.write('JPEG2000 codec set to '+self.JPEGcodec)
			elif menu == '2':
				self.JPEGcinema = not self.JPEGcinema
				change = True
				log.write ('JPEG2000 cinema option '+enable[self.JPEGcinema])
			elif menu == '3':
				self.JPEGcinema48 = not self.JPEGcinema48
				change = True
				log.write ('JPEG2000 cinema48 option '+enable[self.JPEGcinema48])
			elif menu == '4':
				self.JPEGycc = not self.JPEGycc
				change = True
				log.write ('JPEG2000 YCC option '+enable[self.JPEGycc])
			else:
				log.error('Unvalid choice, expect an integer value between 0 and 4')
	
	
	
	
	
	def editExr(self, log):
		'''a method to edit EXR codec specific settings'''
		enable = {True:'enabled', False: 'disabled'}
		action = {True:'Disable', False: 'Enable'}
		change = False
		log.menuIn('Edit EXR Settings')
		while True:
			log.print()
			
			self.print()
			
			print('\n\n        Menu:\n1- Choose EXR Codec')
			print('2- '+action[self.EXRzbuffer]+' zbuffer Option')
			print('3- '+action[self.EXRpreviews]+' previews Option')
			
			menu = input('0- Quit\n\nMenu choice :').strip().lower()
			
			if menu in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			
			if menu == '1':
				change = (self.editExrCodec(log) or change)
			elif menu == '2':
				self.EXRzbuffer = not self.EXRzbuffer
				change = True
				log.write ('EXR Z buffer '+enable[self.EXRzbuffer])
			elif menu == '3':
				self.EXRpreviews = not self.EXRpreviews
				change = True
				log.write ('EXR previews '+enable[self.EXRpreviews])
			else:
				log.error('Unvalid choice, expect an integer value between 0 and 3')
	
	
	
	
	
	def editExrCodec(self, log):
		'''a method to choose EXR codec'''
		log.menuIn('Choose EXR Codec')
		
		codecs = ['quit', 'NONE', 'PXR24', 'ZIP', 'PIZ', 'RLE', 'ZIPS', 'DWAA', 'DWAB']
		
		if self.colorDepth == 16:
			codecs.append('B44')
			codecs.append('B44A')
		
		while True:
			log.print()
			
			self.print()
			
			print('\n\nCurrent EXR Codec : '+self.EXRcodec+'\n')
			
			indexPrintList(codecs)
			
			menu = input('\n\nMenu choice :').strip().lower()
			
			if menu in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return False
			
			try:
				menu = int(menu)
			except ValueError:
				log.error('integer value expected')
				continue
			
			if menu > 0 and menu < len(codecs):
				self.EXRcodec = codecs[menu]
				log.write('EXR codec set to '+self.EXRcodec)
				log.menuOut()
				return True
			else:
				log.error('unvalid choice, expect a value between 0 and '+str(len(codecs)-1)+'!')
			
	
	
	
	
	def apply(self, scene):
		'''apply settings to a blender scene object'''
		scene.render.resolution_percentage = self.pourcent
		scene.render.resolution_x = self.size.X
		scene.render.resolution_y = self.size.Y
		
		scene.cycles.use_square_samples = False
		scene.cycles.samples = self.samples
		
		if self.simplify is None:
			scene.render.use_simplify = False
		else:
			scene.render.use_simplify = True
			scene.render.simplify_subdivision_render
		
		scene.render.image_settings.file_format = self.format
		scene.render.image_settings.color_depth = str(self.colorDepth)
		scene.render.image_settings.quality = self.JPEGquality
		scene.render.image_settings.compression = self.PNGcompression
		
		self.OSA.apply(scene)
	
	
	
	
	
	def getExtension(self):
		'''return file extension'''
		if self.format == 'PNG':
			return '.png'
		if self.format == 'JPEG':
			return '.jpg'
		return '.exr'
	
	
	
	
	
	
	
