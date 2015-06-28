#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module containing 'preset' class'''
import xml.etree.ElementTree as xmlMod
import os, re

class preset:
	'''class of object representing a preset for rendering task'''
	
	
	def __init__(self, xml= None):
		'''initialize preset object with default value or values extracted from an xml object'''
		# default values of all the attributes
		# animation and resolution attributes
		self.X = 1920
		self.Y = 1080
		self.percent = 1
		self.fps = 30
		self.animation = 0
		
		# rendering engine and output attributes
		self.blender = 'blender'
		self.renderingDevice = 'GPU'
		self.renderingEngine = 'CYCLES'
		self.cyclesSamples = 1500
		self.outputFormat = 'OPEN_EXR_MULTILAYER'
		
		
		# rendering options attributes
		self.zPass = True
		self.objectIndexPass = True
		self.compositingEnable = True
		self.filmExposure = 1
		self.filmTransparentEnable = True
		self.simplify = None
		
		
		# Light Path attributes
		self.transparencyBouncesMin = 4
		self.transparencyBouncesMax = 6
		self.bouncesMin = 3
		self.bouncesMax = 8
		self.diffuseBounces = 4
		self.glossyBounces = 4
		self.transmissionBounces = 12
		self.volumeBounces = 0
		
		if xml is not None:
			self.fromXml(xml)
	
	
	
	
	
	
	def fromXml(self,xml):
		'''extract preset parameters from an xml object'''
		
		# blender version to use
		self.blender = xml.find('blender').get('version')
		
		# get rendering resolution parameters 
		node = xml.find('resolution')
		self.X = int(node.get('x'))
		self.Y = int(node.get('y'))
		self.percent = int(node.get('percent'))/100
		self.outputFormat = node.get('format')
		
		# get animation parameters
		node = xml.find('animation')
		self.fps = int(node.get('fps'))
		self.animation = int(node.get('duration'))
		
		# get engine parameters
		node = xml.find('engine')
		self.renderingEngine = node.get('value')
		
		# get Cycles parameters
		self.cyclesSamples = xml.find('cycles').get('samples')
		self.renderingDevice = xml.find('cycles').find('device').get('value')
		node = xml.find('cycles').find('film')
		self.filmExposure = float(node.get('exposure'))
		self.filmTransparentEnable = node.get('transparent') in ['true', 'True']
		
		# get Cycles Ligth Path parameters
		node = xml.find('cycles').find('bouncesSet')
		self.transparencyBouncesMax = int(node.find('transparency').get('max'))
		self.transparencyBouncesMin = int(node.find('transparency').get('min'))
		self.bouncesMax = int(node.find('bounces').get('max'))
		self.bouncesMin = int(node.find('bounces').get('min'))
		self.diffuseBounces = int(node.find('diffuse').get('bounces'))
		self.glossyBounces = int(node.find('glossy').get('bounces'))
		self.transmissionBounces = int(node.find('transmission').get('bounces'))
		self.volumeBounces = int(node.find('volume').get('bounces'))
		
		# get others parameters
		self.compositingEnable = xml.find('compositing').get('enable') in ['true', 'True']
		
		node = xml.find('simplify')
		if node is None:
			self.simplify = None
		else:
			self.simplify = int(node.get('subdiv'))
		
		node = xml.find('pass')
		self.zPass = node.get('zPass') in ['true', 'True']
		self.objectIndexPass = node.get('objectIndexPass') in ['true', 'True']
		
		
		
	
	
	
	
	
	
	def toXmlStr(self, head=False, root=False):
		'''export preset parameters to an xml syntax string'''
		txt= ''
		
		if head:
			txt += '<?xml version="1.0" encoding="UTF-8"?>\n'
		
		if root:
			txt += '<settings>\n'
		
		txt += '  <blender version="'+self.blender+'" />\n'
		
		# export resolution parameters
		txt += '  <resolution x="'+str(self.X)+'" y="'+str(self.Y)+'" percent="'+str(int(self.percent*100))+'" format="'+self.outputFormat+'" />\n'
		
		# export animation parameters
		txt+= '  <animation fps="'+str(self.fps)+'" duration="'+str(self.animation)+'" />\n'
		
		
		# export engine parameter
		txt += '  <engine value="'+self.renderingEngine+'"/>\n'
		
		# export Cycles parameters
		txt += '  <cycles samples="'+str(self.cyclesSamples)+'">\n'
		txt += '    <device value="'+self.renderingDevice+'"/>\n'
		txt += '    <film exposure="'+str(self.filmExposure)+'" transparent="'+str(self.filmTransparentEnable)+'" />\n'
		
		
		# export lightpath Cycles specific parameters
		txt += '    <bouncesSet>\n'
		txt += '      <transparency max="'+str(self.transparencyBouncesMax)+'" min="'+str(self.transparencyBouncesMin)+'" />\n'
		txt += '      <bounces max="'+str(self.bouncesMax)+'" min="'+str(self.bouncesMin)+'" />\n'
		txt += '      <diffuse bounces="'+str(self.diffuseBounces)+'" />\n'
		txt += '      <glossy bounces="'+str(self.glossyBounces)+'" />\n'
		txt += '      <transmission bounces="'+str(self.transmissionBounces)+'" />\n'
		txt += '      <volume bounces="'+str(self.volumeBounces)+'" />\n'
		txt += '    </bouncesSet>\n'
		
		txt += '  </cycles>\n'
		
		
		# export rendering options
		txt += '  <compositing enable="'+str(self.compositingEnable)+'" />\n'
		if self.simplify is not None:
			txt += '  <simplify subdiv="'+str(self.simplify)+'" />\n'
		txt += '    <pass z="'+str(self.zPass)+'" objectIndex="'+str(self.objectIndexPass)+'" />\n'
		
		
		if root:
			txt += '</settings>'
		
		return txt
	
	
	
	
	
	def print(self):
		'''print preset parameters'''
		enable = {True:'enabled', False:'Disabled'}
		
		print('Blender version :       '+self.blender+'\n')
		
		# print resolution parameters
		print('Résolution :          '+str(self.X)+'x'+str(self.Y)+' (@'+str(int(self.percent*100))+'%)')
		
		# print Cycles sampling parameters
		print('Cycles samples : '+str(self.cyclesSamples))
		
		# print animation and engine parameters
		print('Animation rate :           '+str(self.fps)+' fps')
		print('Animation duration :           '+str(self.animation)+' frames')
		print('Engine :              '+self.renderingEngine.lower()\
							+'('+self.renderingDevice+')\n')
		
		# print output parameters
		print('Output format :                '+self.outputFormat+'\n')
		
		
		# print Ligth path parameters
		print('Ligth path : ')
		print('  bounces :                '+str(self.bouncesMin)+' to '\
								+str(self.bouncesMax))
		print('  transparency :           '+str(self.transparencyBouncesMin)\
								+' to '+str(self.transparencyBouncesMax))
		print('  diffuse / glossy / transmission / volume : \n                           '\
				+str(self.diffuseBounces)+' / '+str(self.glossyBounces)+' / '\
				+str(self.transmissionBounces)+' / '+str(self.volumeBounces)+'\n')
		
		
		# print others parameters
		print('OPtions :')
		print('  z pass :                       '+enable[self.zPass])
		print('  object index pass :            '+enable[self.objectIndexPass])
		print('  compositing :                  '+enable[self.compositingEnable])
		print('  exposure (cycles) :            '+str(self.filmExposure))
		print('  transparent background :       '+enable[self.filmTransparentEnable])
		if self.simplify is None:
			print('  simplify :                     Disabled\n')
		else:
			print('  simplify :                     '+str(self.simplify)+'\n')
		
		
	
	
	
	
	
	def getClone(self):
		'''create another preset object with the same attribut values'''
		
		return setting( xmlMod.fromstring( self.toXmlStr( head = True, root = True) ) )
	
	
	
	
	
	def see(self, log):
		'''print preset and let edit or reset it'''
		change = False
		log.menuIn('Preset')
		
		while True:
			#print log and preset
			os.system('clear')
			log.print()
			print('    preset\n')
			self.print()
			
			#treat available actions
			choice= input('(e)dit, (r)eset or (q)uit (and save): ').strip()
			if choice in ['Q','q']:
				log.write('quit settings\n')
				log.menuOut()# quit preferences menu
				return change
			elif choice in ['e','E']:
				log.write('edit settings\n')
				change = (self.edit(log) or change)
			elif choice in ['R','r']:
				#reset default settings
				confirm = input('this action will reset to factory settings. confirm (y):').strip()
				if confirm in ['y','Y']:
					self.__init__()
					change = True
					log.write('reset factory settings\n')
			else:
				log.write('\033[31munknow request\033[0m\n')
	
	
	
	
	
	def edit(self, log):
		'''method to edit preset'''
		change = False
		
		log.menuIn('Edit Preset')
		log.write('Edit preset\n')
		menu = '''		customize task settings :
		0- Blender version
		1- Resolution
		2- Animation
		3- Engine
		4- Ligth path
		5- OPtions'''
		
		
		while True:
			#print log and edit preset menu
			os.system('clear')
			log.print()
			
			
			print(menu)
		
			#treat available actions
			choice = input('what\'s the parameter to edit ?(number or \'q\')').strip().lower()
			
			try:
				if choice in ['q', 'cancel', 'quit']:
					choice = -1
				else:
					choice = int(choice)
			except ValueError:
				choice = 9999
			
			
			if choice == -1 :
				log.write('\033[31mquit\033[0m\n')
				log.menuOut()
				return change
			elif choice == 0:
				#edit blender path
				change = (self.editBlenderVersion(log) or change)
			elif choice == 1:
				#edit resolution setting
				change = (self.editResolution(log) or change)
			elif choice == 2:
				#edit animation settings
				change = (self.editAnimationMenu(log) or change)
			elif choice == 3:
				#edit Engine settings
				change = (self.editEngine(log) or change)
			elif choice == 4:
				#edit Ligth path settings
				change = (self.editLight(log) or change)
			elif choice == 5:
				#edit OPtions settings
				change = (self.editOption(log) or change)
			else:
				log.write('\033[31munknow request!\033[0m\n')
	
	
	
	
	
	
	def editBlenderVersion(self, log):
		'''method to change Blender version to use'''
		
		change = False
		#print current blender version and ask a new one
		os.system('clear')
		log.menuIn('Blender Version')
		log.write('blender version choice : ')
		log.print()
		print('current version :'+self.blenderPath+'\n\n')
		
		choice = input('''new absolute path ? ( 'blender' '/home/user/Download/blender' for example or 'cancel')''').strip()
		
		if choice[0] in ['\'', '"'] and choice[-1] == choice[0]:
			#remove quote mark and apostrophe in first and last character
			choice  = choice[1:len(choice)-1]
	
		#parse new settings and check it
		match = re.search(r'(^blender$)|(^/(.+/)blender$)',choice)
		if match is None:
			if choice in ['cancel','CANCEL','QUIT','quit','Q','q']:
				log.write('\033[31mblender path change canceled\033[0m\n')
			else:
				log.write("\033[31merror, the path must be an absolute path(beginng by '/' and ending by 'blender') or the 'blender' command\n blender path change canceled, retry!\033[0m\n")
			log.menuOut()
			return change
		elif choice == 'blender':
			# apply new settings
			self.blenderPath = choice
			change = True
			log.write(choice+'\n')
		else:
			if os.path.exists(choice) and os.path.isfile(choice)\
						and os.access(choice, os.X_OK):
				self.blenderPath = choice
				change = True
				log.write(choice+'\n')
			else:
				log.write("\033[31merror: the file didn't exist or is not a file or is not executable\n blender path change canceled, retry\033[0m\n")
		log.menuOut()
		return change
	
	
	
	
	
	
	def editResolution(self, log):
		'''method to edit the render resolution to use'''
		#edit resolution setting
		#print current resolution settings and ask new settings
		os.system('clear')
		log.write('resolution editing: ')
		log.menuIn('Resolution')
		log.print()
		print('current resolution :'+str(self.X)+'x'+str(self.Y)+'@'+str(int(self.percent*100))+'\n\n')
		choice = input('new resolution ? (1920x1080@100 for example or \'cancel\')').strip()
		
		
		#parse new settings and check it
		match = re.search(r'^(\d{3,5})x(\d{3,5})@(\d{2,3})$',choice)
		if match is None:
			if choice in ['cancel','CANCEL','QUIT','quit','Q','q']:
				log.write('\033[31mquit resolution editing\033[0m\n')
			else:
				log.write('\033[31merror, resolution change unvalid, retry\033[0m\n')
			log.menuOut()
			return False
		
		
		#apply new settings and save it
		self.X = int(match.group(1))
		self.Y = int(match.group(2))
		self.percent = int(match.group(3))/100
		log.write(choice+'\n')
		log.menuOut()
		return True
	
	
	
	
	
	def editAnimation(self, log):
		'''method to display a menu to access extended animation settings editing'''
		# menu to edit extended animation settings
		change = False
		log.menuIn('Animation Settings')
		
		while True:
			os.system('clear')
			log.print()
			
			print('		Edit animation setting :')
			print('1- animation rate           ('+str(self.fps)+'fps)')
			print('2- start frame              ('+str(self.start)+')')
			print('3- end frame                ('+str(self.end)+')')
			print('4- background animation     ('+str(self.backgroundAnimation)\
																+' frame(s))')
			print('5- foreground animation     ('+str(self.foregroundAnimation)\
																+' frame(s))')
			choice = input('action? (\'q\' to quit)').strip().lower()
			
			try:
				if choice in ['q', 'cancel', 'quit']:
					choice = -1
				else:
					choice = int(choice)
			except ValueError:
				choice = -2
			
			if choice == -1:
				log.menuOut()
				return change
			
			if choice < 1 or choice > 5:
				log.write('animation setting edit : \033[31munvalid action\033[0m\n')
				continue
			
			if choice == 1:
				# edit animation rate
				change = (self.editAnimationRate(log) or change)
				continue
			
			if choice == 2:
				# start frame reminder
				print('		Edit Start Frame :')
				print('Current Start Frame : '+str(self.start)+'\n')
			elif choice == 3:
				# end frame reminder
				print('		Edit End Frame :')
				print('Current End Frame : '+str(self.end)+'\n')
				
			elif choice == 4:
				# background animation duration reminder
				print('		Edit background animation duration :')
				print('Current background animation duration : '\
							+str(self.backgroundAnimation)+'\n')
				
			elif choice == 5:
				# foreground animation duration reminder
				print('		Edit foreground animation duration :')
				print('Current foreground animation duration : '\
							+str(self.foregroundAnimation)+'\n')
			
			new = input('new settings?').strip().lower()
			
			try:
				new = int(new)
			except ValueError:
				new = None
			
			if new is None:
				log.write('animation setting edit : \033[31mError : new value must be an integer\033[0m\n')
				continue
			
			if choice == 2:
				# start frame reminder
				if new > self.end:
					log.write('start frame edit : \033[31m'+str(new)+' : Error : start frame must be lower than end frame!\033[0m\n')
				else:
					self.start = new
					log.write('start frame edit : '+str(new)+'\n')
					change = True
			elif choice == 3:
				# end frame reminder
				if new < self.start:
					log.write('end frame edit : \033[31m'+str(new)+' : Error : end frame must be bigger than start frame!\033[0m\n')
				else:
					self.end = new
					log.write('end frame edit : '+str(new)+'\n')
					change = True
			elif choice == 4:
				# background animation duration reminder
				if new < 0:
					self.backgroundAnimation = 0
				else:
					self.backgroundAnimation = new
				log.write('Background animation duration set to : '\
									+str(self.backgroundAnimation)+'\n')
				change = True
			elif choice == 5:
				# foreground animation duration reminder
				if new < 0:
					self.foregroundAnimation = 0
				else:
					self.foregroundAnimation = new
				log.write('Foreground animation duration set to : '\
									+str(self.foregroundAnimation)+'\n')
				change = True
	
	
	
	
	
	def editAnimationRate(self, log):
		'''method to use to change the animation rate of the render'''
		#edit animation frame rate
		#print log and current animation settings and ask new settings
		os.system('clear')
		log.write('edit animation rate : ')
		log.menuIn('Animation Rate')
		log.print()
		print('current animation rate: '+str(self.fps)+'fps\n\n')
		choice = input('new animation rate? ( 30 for example or \'cancel\')').strip().lower()
	
		#parse new settings and check it
		try:
			if choice in ['q', 'cancel', 'quit']:
				choice = -1
			else:
				choice = int(choice)
		except ValueError:
			choice = -2
		
		if choice < 0:
			if choice == -1:
				log.write('\033[31manimation frame rate change canceled\033[0m\n')
			else:
				log.write('\033[31merror, animation frame rate change canceled, retry\033[0m\n')
			log.menuOut()
			return False
		
		#apply new settings and save it
		self.fps = choice
		log.write(str(choice)+'fps\n')
		log.menuOut()
		return True
	
	
	
	
	
	def editSample(self, log):
		'''method to change the sample settings of Cycles renders'''
		# edit Cycles samples settings
		change = False
		log.menuIn('Cycles Samples')
		# print current settings
		while True:
			os.system('clear')
			log.write('edit Cycles sample settings : ')
			log.print()
			print('current Cycles sample settings: '\
					+'\n  1- Main sample : '+str(self.mainAnimationCyclesSamples)\
					+'\n  2- Background sample : '+str(self.backgroundCyclesSamples)\
					+'\n  3- Foreground sample : '+str(self.foregroundCyclesSamples)\
					+'\n\n')
			
			# choice of the parameters to edit
			choice = input('what\'s the parameter to edit? ( number or \'q\'):').strip().lower()
			try:
				if choice in ['q', 'cancel', 'quit']:
					choice = -1
				else:
					choice = int(choice)
			except ValueError:
				choice = 9999
			
			if choice == -1:
				# quit Cycles sample settings edition
				log.write('\033[31mquit sample editing\033[0m\n')
				log.menuOut()
				return change
			
			if choice > 3 or choice < 0:
				log.write('\033[31munvalid choice : '+str(choice)+'\033[0m\n')
				print('unvalid choice : '+str(choice))
				continue
			
			# edit sample settings
			name = ['main animation', 'background', 'foreground'][choice-1]
			value = [str(self.mainAnimationCyclesSamples), 
					str(self.backgroundCyclesSamples), 
					str(self.foregroundCyclesSamples)][choice-1]
			
			# print current setting
			os.system('clear')
			log.menuIn(name.capitalize())
			log.write(name+' : ')
			log.print()
			print('current '+name+' sample settings : '\
					+value+'\n\n')
			
			# get user choice
			new = input('new '+name+' sample? (an integer or \'q\')').strip().lower()
			try:
				if new in ['q', 'cancel', 'quit']:
					new = -1
				else:
					new = int(new)
			except ValueError:
				new = -2
			
			# if user input is not an integer, quit cycle sample setting edition
			
			if new == -1 :
				log.write('\033[31munvalid settings :'+new\
						+'\033[0m\nretry\n')
				log.menuOut()
				log.menuOut()
				return change
			elif new < 0:
				log.write('\033[31mcanceled\033[0m\n')
				log.menuOut()
				continue
			
			# apply a good new setting
			log.write(str(new)+'\n')
			if choice == 1:
				self.mainAnimationCyclesSamples = new
			elif choice == 2:
				self.backgroundCyclesSamples = new
			elif choice == 3:
				self.foregroundCyclesSamples = new
			log.menuOut()
			change = True
	
	
	
	
	
	def editEngine(self, log):
		'''method to change the default rendering engine '''
		#edit Engine settings
		change = False
		log.menuIn('Engine')
		# print old settings
		while True:
			os.system('clear')
			log.write('change default engine Settings : ')
			log.print()
			print('current engine : '+self.renderingEngine\
						+'\ncurrent rendering device : '+self.renderingDevice+' (Cycles only)\n\n')
			
			choice = input('''choice :
	1- switch rendering Engine
	2- switch rendering Device
	0- Quit
''').strip().lower()
			
			try:
				if choice in ['q', 'cancel', 'quit']:
					choice = 0
				else:
					choice = int(choice)
			except ValueError:
				choice = 9999
			
			if choice == 0:
				log.write('\033[31mend\033[0m\n')
				log.menuOut()
				return change
			elif choice == 1:
				if self.renderingEngine == 'CYCLES':
					self.renderingEngine = 'BLENDER_RENDER'
				else:
					self.renderingEngine = 'CYCLES'
				change = True
				log.write('engine switch to '+self.renderingEngine+'\n')
			elif choice == 2:
				if self.renderingDevice == 'GPU':
					self.renderingDevice = 'CPU'
				else:
					self.renderingDevice = 'GPU'
				change = True
				log.write('device switch to '+self.renderingDevice+'\n')
			else:
				log.write('\033[31munvalid choice : '+str(choice)+'\033[0m\nretry\n')
			
	
	
	
	
	
	def editOutput(self, log):
		'''method to change all the output settings'''
		#edit Output settings
		change = False
		log.menuIn('Output Settings')
		while True:
			os.system('clear')
			log.write('change output Settings : ')
			log.print()
			
			# print old settings
			print('current output settings : '\
					+'\n  1- Output path (absolute) : '+str(self.outputPath)\
					+'\n  2- Subpath : '+self.outputSubPath\
					+'\n  3- Name : '+self.outputName\
					+'\n  4- Format : '+self.outputFormat\
					+'\n  0- Quit\n\n')
			choice = input('''What's the setting to edit?''').strip().lower()
			
			try:
				if choice in ['q', 'cancel', 'quit']:
					choice = 0
				else:
					choice = int(choice)
			except ValueError:
				choice = -2
			
			if choice == 0:
				# quit edition
				log.write('\033[31mend\033[0m\n')
				log.menuOut()
				return change
			elif choice == 1:
				# edit output path
				change = (self.editOutputPath(log) or change)
			elif choice == 2:
				# edit subpath
				change = (self.editOutputSubpath(log) or change)
			elif choice == 3:
				# edit output naming
				change = (self.editOutputName(log) or change)
			elif choice == 4:
				# edit output format
				change = (self.editOutputFormat(log) or change)
			else:
				log.write('\033[31munvalid choice :'+str(choice)+'\033[0m\nretry\n')
			
	
	
	
	
	
	def editOutputFormat(self, log):
		'''method to change output format'''
		# edit output format
		# print old setting
		log.write('edit output format :')
		log.menuIn('Output Format')
		os.system('clear')
		log.print()
		print('current output format : '+self.outputFormat) 
		new = input('new format (available: png / jpeg / open_exr / open_exr_multilayer):').strip().upper()
		
		if new in ['PNG', 'JPEG', 'OPEN_EXR', 'OPEN_EXR_MULTILAYER']:
			# change format if the one is one of the available
			self.outputFormat = new
			log.write(new+'\n')
			log.menuOut()
			return True
		
		log.write('\033[31munvalid format : "'+new+'"\033[0m\n')
		log.menuOut()
		return False
	
	
	
	
	
	
	def editLight(self, log):
		'''method to change light path settings of Cycles'''
		#edit Ligth path settings
		change = False
		log.menuIn('Light Path')
		
		while True:
			os.system('clear')
			log.write('change Light path settings : ')
			log.print()
			# get current settings
			name = ['bounces', 'transparency', 'diffuse', 'glossy', 'transmission', 'volume']
			value = [ str(self.bouncesMin)+' to '+str(self.bouncesMax),
						str(self.transparencyBouncesMin)+' to '+str(self.transparencyBouncesMax),
						str(self.diffuseBounces),
						str(self.glossyBounces),
						str(self.transmissionBounces),
						str(self.volumeBounces)
						]
			
			# print current light path settings
			print('current light path settings :')
			i=0
			while i < 6:
				print('    '+str(i+1)+'- '+name[i]+' : '+value[i])
				i += 1
			
			# get index of parameter to edit
			choice = input('''what's the parameter to edit?('q' to quit)''').strip().lower()
			
			try:
				if choice in ['q', 'cancel', 'quit']:
					choice = -1
				else:
					choice = int(choice)
			except ValueError:
				choice = -2
			
			# if user want to quit menu
			if choice == -1:
				log.write('\033[31mend\033[0m\n')
				log.menuOut()
				return change
			
			# if user don't make a valid choice
			if choice < 1 or choice > 6:
				log.write('\033[31munvalid choice : "'+str(choice)+'"\033[0m\n')
				continue
			
			# get choice corresponding value
			choice -= 1
			name = name[choice]
			value = value[choice]
			log.write(name+' : ')
			if choice < 2:
				syntax = '3 to 15'
			else:
				syntax = '8'
			
			# get new value
			print(name+' current value : '+value+'\n')
			new = input('new setting( respect "'+syntax+'" syntax)').strip().lower()
			
			if choice >= 2:
				# treat value that represent only one number
				try:
					new = int(new)
				except ValueError:
					new = -1
				
				if new < 0:
					log.write('\033[31munvalid value : "'+str(new)+'"\033[0m\nretry\n')
					continue
				
				# change corresponding settings
				if choice == 2:
					self.diffuseBounces = new
				elif choice == 3:
					self.glossyBounces = new
				elif choice == 4:
					self.transmissionBounces = new
				elif choice == 5:
					self.volumeBounces = new
				
				# confirm change
				log.write(str(new)+'\n')
				change = True
			else:
				# treat value that contain 2 number ('1to10'syntax)
				match = re.search(r'^(\d{1,}) ?to ?(\d{1,})$',new)
				if match is None:
					log.write('\033[31munvalid value : "'+new+'"\033[0m\nretry\n')
					continue
				
				# get value and check it
				mini = match.group(1)
				maxi = match.group(2)
				if maxi < mini:
					log.write('\033[31munvalid value : "'+new+'" : second value must be greater or equal to first\033[0m\nretry\n')
					continue
				
				# change corresponding settings
				if choice == 0:
					self.bouncesMin = mini
					self.bouncesMax = maxi
				elif choice == 1:
					self.transparencyBouncesMin = mini
					self.transparencyBouncesMax = maxi
				
				# confirm change
				log.write(new+'\n')
				change = True
				
	
	
	
	
	
	def editOption(self, log):
		'''method to enable/disable rendering options'''
		#edit OPtions settings
		change = False
		log.menuIn('Rendering Options')
		enable = { True : 'Enabled' , False : 'Disabled' }
		
		while True:
			os.system('clear')
			log.write('change rendering option : ')
			log.print()
			
			# print current rendering options settings
			print('current rendering option settings :'\
				+'\n  1- z pass : '+enable[self.zPass]\
				+'\n  2- object index pass : '+enable[self.objectIndexPass]\
				+'\n  3- compositing : '+enable[self.compositingEnable]\
				+'\n  4- transparent background : '+enable[self.filmTransparentEnable])
			if self.simplify is None:
				print('  5- simplify : Disabled')
			else:
				print('  5- simplify : '+str(self.simplify))
			print('  6- exposure (Cycles) : '+str(self.filmExposure))
			
			# get index of parameter to edit
			choice = input('''what's the option to switch/edit?('q' to quit)''').strip().lower()
			
			try:
				if choice in ['q', 'cancel', 'quit']:
					choice = -1
				else:
					choice = int(choice)
			except ValueError:
				choice = -2
			
			# if user want to quit menu
			if choice == -1:
				log.write('\033[31mend\033[0m\n')
				log.menuOut()
				return change
			
			# check if user make a valid choice
			if choice < 1 or choice > 6:
				log.write('\033[31munvalid choice : "'+str(choice)+'"\033[0m\n')
				continue
			
			
			if choice == 1:
				# switch corresponding settings
				self.zPass = not(self.zPass)
				log.write('z pass set to : "'+enable[self.zPass]+'"\n')
				change = True
				
				choice = input('apply to all renderlayer?(y)').strip().lower()
				if choice in ['y', 'yes']:
					for layer in self.renderLayerList:
						layer['z'] = self.zPass
					log.write('z pass settings apply to all renderlayer\n')
				else:
					log.write('\033[31mz pass settings not apply to renderlayer\033[0m\n')
			elif choice == 2:
				# switch corresponding settings
				self.objectIndexPass = not(self.objectIndexPass)
				log.write('object index pass set to : "'+enable[self.objectIndexPass]+'"\n')
				change = True
				
				choice = input('apply to all renderlayer?(y)').strip().lower()
				if choice in ['y', 'yes']:
					for layer in self.renderLayerList:
						layer['object index'] = self.objectIndexPass
					log.write('object index pass settings apply to all renderlayer\n')
				else:
					log.write('\033[31mobject index pass settings not apply to renderlayer\033[0m\n')
			elif choice == 3:
				# switch corresponding settings
				self.compositingEnable = not(self.compositingEnable)
				log.write('compositing set to : "'+enable[self.compositingEnable]+'"\n')
				change = True
			elif choice == 4:
				# switch corresponding settings
				self.filmTransparentEnable = not(self.filmTransparentEnable)
				log.write('transparent background set to : "'+enable[self.filmTransparentEnable]+'"\n')
				change = True
			
			elif choice == 5 :
				log.write('simplify : ')
				choice = input('new simplify value (a integer (11 or higher for disabled)) : ').strip()
				
				try:
					choice = int(choice)
				except ValueError:
					choice = -1
				
				# check value
				if choice == -1:
					log.write('\033[31munvalid value : "'+str(choice)+'" : must be a positive integer\033[0m\nretry\n')
					continue
				
				# apply new value
				if choice > 10:
					self.simplify = None
					log.write('Disabled\n')
				else:
					self.simplify = choice
					log.write(str(choice)+'\n')
				change = True
				
			elif choice == 6 :
				log.write('exposure : ')
				choice = input('new exposure value (a float) : ').strip()
				
				try:
					choice = float(choice)
				except ValueError:
					choice = -1
				
				# check value
				if choice == -1:
					log.write('\033[31munvalid value : "'+str(choice)+'" : must be a number\033[0m\nretry\n')
					continue
				
				# apply new value
				self.filmExposure = choice
				log.write(str(choice)+'\n')
				change = True
	
	
	
	
	
	
