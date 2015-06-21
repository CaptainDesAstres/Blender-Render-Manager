#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module containing 'setting' class'''
import xml.etree.ElementTree as xmlMod
import os, re

class setting:
	'''class that contain the script preferences or a rendering task preferences'''
	
	
	def __init__(self, xml= None):
		'''initialize settings object with default value or values extracted from an xml object'''
		# default values of all the attributes
		# animation and resolution attributes
		self.X = 1920
		self.Y = 1080
		self.percent = 1
		self.start = None
		self.end = None
		self.fps = 30
		
		# tiles size attributes
		self.tilesCyclesCPUX = 32
		self.tilesCyclesCPUY = 32
		self.tilesCyclesGPUX = 256
		self.tilesCyclesGPUY = 256
		self.tilesBIX = 256
		self.tilesBIY = 256
		
		# rendering engine and output attributes
		self.blenderPath = 'blender'
		self.renderingDevice = 'GPU'
		self.renderingEngine = 'CYCLES'
		self.outputFormat = 'OPEN_EXR_MULTILAYER'
		self.outputPath = None
		self.outputSubPath = '%N-%S'
		self.outputName = '%L-%F'
		
		# rendering options attributes
		self.zPass = True
		self.objectIndexPass = True
		self.compositingEnable = True
		self.filmExposure = 1
		self.filmTransparentEnable = True
		self.simplify = None
		
		# renderlayer parameters attributes
		self.renderLayerList = []
		self.backgroundLayersKeywords = ['bck', 'background']
		self.foregroundLayersKeywords = ['fgd', 'foreground']
		self.backgroundCyclesSamples = 1500
		self.foregroundCyclesSamples = 1500
		self.mainAnimationCyclesSamples = 1500
		self.backgroundAnimation = 0
		self.foregroundAnimation = 0
		
		# Light Path attributes
		self.transparencyBouncesMax = 6
		self.transparencyBouncesMin = 4
		self.bouncesMax = 8
		self.bouncesMin = 3
		self.diffuseBounces = 4
		self.glossyBounces = 4
		self.transmissionBounces = 12
		self.volumeBounces = 0
		
		if xml is not None:
			self.fromXml(xml)
	
	
	
	
	
	
	def fromXml(self,xml):
		'''extract settings from an xml object'''
		
		# get rendering resolution parameters 
		node = xml.find('resolution')
		self.X = int(node.get('x'))
		self.Y = int(node.get('y'))
		self.percent = int(node.get('percent'))/100
		
		# get animation parameters
		node = xml.find('animation')
		self.start = node.get('start', self.start)
		if self.start is not None:
			self.start = int(self.start)
		self.end = node.get('end', self.end)
		if self.end is not None:
			self.end = int(self.end)
		self.fps = int(node.get('fps'))
		self.startEndCheck()
		
		# get engine value
		node = xml.find('engine')
		self.renderingEngine = node.get('value')
		
		# get cycles parameters
		node = xml.find('cycles').find('cpu')
		self.tilesCyclesCPUX = int(node.get('x'))
		self.tilesCyclesCPUY = int(node.get('y'))
		node = xml.find('cycles').find('gpu')
		self.tilesCyclesGPUX = int(node.get('x'))
		self.tilesCyclesGPUY = int(node.get('y'))
		self.renderingDevice = xml.find('cycles').find('device').get('value')
		node = xml.find('cycles').find('film')
		self.filmExposure = float(node.get('exposure'))
		self.filmTransparentEnable = node.get('transparent') in ['true', 'True']
		
		# get cycles Ligth Path parameters
		node = xml.find('cycles').find('bouncesSet')
		self.transparencyBouncesMax = int(node.find('transparency').get('max'))
		self.transparencyBouncesMin = int(node.find('transparency').get('min'))
		self.bouncesMax = int(node.find('bounces').get('max'))
		self.bouncesMin = int(node.find('bounces').get('min'))
		self.diffuseBounces = int(node.find('diffuse').get('bounces'))
		self.glossyBounces = int(node.find('glossy').get('bounces'))
		self.transmissionBounces = int(node.find('transmission').get('bounces'))
		self.volumeBounces = int(node.find('volume').get('bounces'))
		
		# get Blender Internal parameters
		node = xml.find('blenderInternal')
		self.tilesBIX = int(node.get('x'))
		self.tilesBIY = int(node.get('y'))
		
		# get others parameters
		self.compositingEnable = xml.find('compositing').get('enable') in ['true', 'True']
		node = xml.find('simplify')
		if node is None:
			self.simplify = None
		else:
			self.simplify = int(node.get('subdiv'))
		
		# get renderlayers list and parameters if there is some
		node = xml.find('renderLayerList')
		self.renderLayerList = []
		if node is not None:
			for layer in node.findall('layer'):
				self.renderLayerList.append({
						'name' : layer.get('name'),
						'z' : layer.get('z') in ['true', 'True'],
						'object index' : layer.get('objIndex') in ['true', 'True'],
						'use' : layer.get('render') in ['true', 'True']
						})
		
		# get background parameters
		node = xml.find('renderLayerPreferences').find('background')
		self.backgroundCyclesSamples = int(node.get('sample'))
		self.backgroundAnimation = int(node.get('frame'))
		self.backgroundLayersKeywords = []
		for key in node.findall('keywords'):
			self.backgroundLayersKeywords.append(key.get('value'))
		
		
		# get foreground parameters
		node = xml.find('renderLayerPreferences').find('foreground')
		self.foregroundCyclesSamples = int(node.get('sample'))
		self.foregroundAnimation = int(node.get('frame'))
		self.foregroundLayersKeywords = []
		for key in node.findall('keywords'):
			self.foregroundLayersKeywords.append(key.get('value'))
		
		# get main animation parameters
		node = xml.find('renderLayerPreferences').find('main')
		self.mainAnimationCyclesSamples = int(node.get('sample'))
		self.zPass = node.get('zPass') in ['true', 'True']
		self.objectIndexPass = node.get('objectIndexPass') in ['true', 'True']
		
		
		# output parameters
		node = xml.find('output')
		self.outputFormat = node.get('format')
		self.outputPath = node.get('mainpath', self.outputPath)
		self.outputSubPath = node.get('subpath')
		self.outputName = node.get('name')
		
		# blender absolute path
		self.blenderPath = xml.find('blender').get('path')
		
	
	
	
	
	
	
	def startEndCheck(self):
		'''make sure that that start frame and end frame are all set or all None'''
		if self.start is None and self.end is not None:
			self.start = self.end
		elif self.start is not None and self.end is None:
			self.end = self.start
		
	
	
	
	
	
	def toXmlStr(self, head=False, root=False):
		'''export settings to an xml syntaxe string'''
		txt= ''
		
		if head:
			txt += '<?xml version="1.0" encoding="UTF-8"?>\n'
		
		if root:
			txt += '<settings>\n'
			
		# export resolution parameters
		txt += '  <resolution x="'+str(self.X)+'" y="'+str(self.Y)+'" percent="'+str(int(self.percent*100))+'" />\n'
		
		# export animation parameters depending of settings type
		if self.start is None or self.end is None:
			txt+= '  <animation fps="'+str(self.fps)+'" />\n'
		else:
			txt+= '  <animation start="'+str(self.start)+'" end="'+str(self.end)+'" fps="'+str(self.fps)+'" />\n'
		
		# export engine parameter
		txt += '  <engine value="'+self.renderingEngine+'"/>\n'
		
		# export Cycles specific  parameters
		txt += '  <cycles>\n'
		txt += '    <cpu x="'+str(self.tilesCyclesCPUX)+'" y="'+str(self.tilesCyclesCPUY)+'"/>\n'
		txt += '    <gpu x="'+str(self.tilesCyclesGPUX)+'" y="'+str(self.tilesCyclesGPUY)+'"/>\n'
		txt += '    <device value="'+self.renderingDevice+'"/>\n'
		txt += '    <film exposure="'+str(self.filmExposure)+'" transparent="'+str(self.filmTransparentEnable)+'" />\n'
		
		# export light path Cycles specific  parameters
		txt += '    <bouncesSet>\n'
		txt += '      <transparency max="'+str(self.transparencyBouncesMax)+'" min="'+str(self.transparencyBouncesMin)+'" />\n'
		txt += '      <bounces max="'+str(self.bouncesMax)+'" min="'+str(self.bouncesMin)+'" />\n'
		txt += '      <diffuse bounces="'+str(self.diffuseBounces)+'" />\n'
		txt += '      <glossy bounces="'+str(self.glossyBounces)+'" />\n'
		txt += '      <transmission bounces="'+str(self.transmissionBounces)+'" />\n'
		txt += '      <volume bounces="'+str(self.volumeBounces)+'" />\n'
		txt += '    </bouncesSet>\n'
		
		
		
		txt += '  </cycles>\n'
		
		# export Blender Internal engine specific  parameters
		txt += '  <blenderInternal x="'+str(self.tilesBIX)+'" y="'+str(self.tilesBIY)+'" />\n'

		# export rendering options
		txt += '  <compositing enable="'+str(self.compositingEnable)+'" />\n'
		if self.simplify is not None:
			txt += '  <simplify subdiv="'+str(self.simplify)+'" />\n'
		
		
		# export renderlayer list and parameters
		if len(self.renderLayerList)>0:
			txt += '  <renderLayerList>\n'
			for layer in self.renderLayerList:
				txt += '    <layer name="'+layer['name']+'" z="'+str(layer['z'])+'" objIndex="'+str(layer['object index'])+'" render="'+str(layer['use'])+'"/>\n'
			txt += '  </renderLayerList>\n'
		
		
		txt += '  <renderLayerPreferences>\n'
		
		# export background render layers specific parameters
		txt += '    <background sample="'+str(self.backgroundCyclesSamples)+'" frame="'+str(self.backgroundAnimation)+'" >\n'
		for key in self.backgroundLayersKeywords:
			txt += '      <keywords value="'+key+'" />\n'
		txt += '    </background>\n'
		
		# export foreground render layers specific parameters
		txt += '    <foreground sample="'+str(self.foregroundCyclesSamples)+'" frame="'+str(self.foregroundAnimation)+'" >\n'
		for key in self.foregroundLayersKeywords:
			txt += '      <keywords value="'+key+'" />\n'
		txt += '    </foreground>\n'
		
		# export animation render layers specific parameters
		txt += '    <main sample="'+str(self.mainAnimationCyclesSamples)+'" zPass="'+str(self.zPass)+'" objectIndexPass="'+str(self.objectIndexPass)+'" />\n'
		
		txt += '  </renderLayerPreferences>\n'
		
		
		# export rendering output parameters
		txt += '  <output format="'+self.outputFormat+'" '
		if self.outputPath is not None:
			txt += 'mainpath="'+self.outputPath+'" '
		txt += 'subpath="'+self.outputSubPath+'" name="'+self.outputName+'" />\n'
		
		txt += '  <blender path="'+self.blenderPath+'" />\n'
		
		if root:
			txt += '</settings>'
		return txt
	
	
	
	
	
	def print(self):
		'''print settings like preferences settings'''
		enable = {True:'enabled', False:'Disabled'}
		
		print('Blender path :       '+self.blenderPath+'\n')
		
		# print resolution parameters
		print('Résolution :          '+str(self.X)+'x'+str(self.Y)+' (@'+str(int(self.percent*100))+'%)')
		
		# print Cycles sampling parameters
		print('Cycles samples :')
		print('  main / background / foreground : \n                      '\
				+str(self.mainAnimationCyclesSamples)+' / '\
				+str(self.backgroundCyclesSamples)+' / '\
				+str(self.foregroundCyclesSamples))
		
		# print animation and engine parameters
		print('Animation :           '+str(self.fps)+'fps')
		print('Engine :              '+self.renderingEngine.lower()\
							+'('+self.renderingDevice+')\n')
		
		# print output parameters
		print('Output : ')
		print('  output path (absolute) :                    '+str(self.outputPath))
		print('  automatique subpath (for each task) :       '+self.outputSubPath)
		print('  name :                                      '+self.outputName)
		print('  format :                                    '+self.outputFormat+'\n')
		
		
		# print Tiles parameters
		print('Tiles : ')
		print('  cycles GPU :             '+str(self.tilesCyclesGPUX)+'x'\
												+str(self.tilesCyclesGPUY))
		print('  cycles CPU :             '+str(self.tilesCyclesCPUX)+'x'+str(self.tilesCyclesCPUY))
		print('  blender internal :       '+str(self.tilesBIX)+'x'+str(self.tilesBIY))
		
		
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
		
		print('Keywords :')
		print('  background : '+' | '.join(self.backgroundLayersKeywords))
		print('  foreground : '+' | '.join(self.foregroundLayersKeywords)+'\n')
		
	
	
	
	
	
	def getClone(self):
		'''create another settings object with the same attribut values
		restart/end attributes value with start/end argument values if set'''
		
		return setting( xmlMod.fromstring( self.toXmlStr( head = True, root = True) ) )
	
	
	
	
	
	def compare(self, ref, exclude = ['blenderPath', 'outputPath', 'outputSubPath', 'outputName', 'backgroundLayersKeywords', 'foregroundLayersKeywords']):
		same = True
		excludeType = ["<class 'builtin_function_or_method'>",\
						"<class 'function'>",\
						"<class 'method-wrapper'>",\
						"<class 'method'>"]
		
		for attr in dir(self):
			if attr not in exclude\
			and str(type(getattr(self, attr))) not in excludeType:
				if getattr(self, attr) != getattr(ref, attr):
					same = False
		return same
		
	
	
	
	
	
	def see(self, log):
		'''print settings and let edit or reset it'''
		change = False
		log.menuIn('Preferences')
		while True:
			#print log and preferences
			os.system('clear')
			log.print()
			print('    Settings\n')
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
	
	
	
	
	def edit(self, log, extended = False):
		'''method to edit settings/preferences'''
		change = False
		if extended:
			log.menuIn('Customize')
			log.write('Customize task settings\n')
			menu = '''		customize task settings :
		0- Blender path
		1- Resolution
		2- Animation
		3- Cycles samples
		4- Engine
		5- Output
		6- Tiles
		7- Ligth path
		8- OPtions
		9- Keywords
		10- Renderlayer settings'''
		else:
			log.menuIn('Editing')
			menu = '''		preferences editing:
		0- Blender path
		1- Resolution
		2- Animation rate
		3- Cycles samples
		4- Engine
		5- Output
		6- Tiles
		7- Ligth path
		8- OPtions
		9- Keywords'''
		
		
		while True:
			#print log and edit preferences menu
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
				change = (self.editBlenderPath(log) or change)
			elif choice == 1:
				#edit resolution setting
				change = (self.editResolution(log) or change)
			elif choice == 2:
				#edit animation frame rate
				if extended:
					change = (self.editAnimation(log) or change)
				else:
					change = (self.editAnimationRate(log) or change)
			elif choice == 3:
				# edit Cycles samples settings
				change = (self.editSample(log) or change)
			elif choice == 4:
				#edit Engine settings
				change = (self.editEngine(log) or change)
			elif choice == 5:
				#edit Output settings
				change = (self.editOutput(log) or change)
			elif choice == 6:
				#edit Tiles settings
				change = (self.editTiles(log) or change)
			elif choice == 7:
				#edit Ligth path settings
				change = (self.editLight(log) or change)
			elif choice == 8:
				#edit OPtions settings
				change = (self.editOption(log) or change)
			elif choice == 9:
				#edit Keywords settings
				change = (self.editKeyword(log) or change)
			elif choice == 10:
				#edit renderlayer list settings
				change = (self.editRenderlayerList(log) or change)
			else:
				log.write('\033[31munknow request!\033[0m\n')
	
	
	
	
	
	
	def editBlenderPath(self, log):
		'''method to change absolute path to the Blender version to use'''
		#edit blender path
		change = False
		#print current blender path and ask a new one
		os.system('clear')
		log.menuIn('Blender Path')
		log.write('blender path editing : ')
		log.print()
		print('current path :'+self.blenderPath+'\n\n')
		
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
			
	
	
	
	
	def editOutputPath(self, log):
		'''method to change output path'''
		# edit output path
		log.write('edit main output path:')
		log.menuIn('Main Output Path')
		os.system('clear')
		log.print()
		print('current output path : '+str(self.outputPath)) 
		new = input('\nnew path (must already exist and be absolute path):').strip()
		
		# empty path
		if new in ['', "''", '""']:
			self.outputPath = None
			log.write('set to None\n')
			log.menuOut()
			return True
		
		if new[0] in ['\'', '"'] and new[0]==new[-1]:
			new  = new[1:len(new)-1]
		
		match = re.search(r'^/(.+/)$',new)
		
		if match is None:
			# check if path is a good syntaxe
			log.write('\033[31munvalid path : "'+new+'"\nThe path must be absolute (begin and end by "/")\033[0m\n')
			log.menuOut()
			return False
		
		# check if it's a good path and save it
		if os.path.exists(new) and os.path.isdir(new)\
				and os.access(new, os.W_OK):
			self.outputPath = new
			log.write(new+'\n')
			log.menuOut()
			return True
		
		log.write("\033[31munvalid path : '"+new+"'\nthe path didn't exist, is not a directories or you don't have the right to write in it\033[0m\n")
		log.menuOut()
		return False
	
	
	
	
	
	def editOutputSubpath(self, log):
		'''method to change output subpath naming convention'''
		# edit output subpath
		# write old settings
		log.write('edit output subpath :')
		log.menuIn('Output Subpath')
		os.system('clear')
		log.print()
		print('current output subpath : '+self.outputSubPath) 
		new = input('\nnew subpath (%N will be replaced by the task file name and %S by the scene name):').strip()
		
		if new in ['', "''", '""']:
			log.write('\033[31mcanceled\033[0m\n')
			log.menuOut()
			return False
		
		if new[0] in ['\'', '"'] and new[0]==new[-1]:
			new  = new[1:len(new)-1]
		
		if new.find('/') != -1:
			# check if there is a '/' caractère in the new name
			log.write('\033[31munvalid : "'+new+'"\nThe subpath must not contain "/"!\033[0m\n')
			log.menuOut()
			return False
		
		if new.find('%S') == -1 or new.find('%N') == -1:
			# check if there is a '%N' and a '%S' sequences in the new name
			log.write('\033[31munvalid : "'+new+'"\nThe subpath must contain at less one occurence of "%N" and "%S" or different render risk to overwrite themselves!\033[0m\n')
			log.menuOut()
			return False
		
		# change output SubPath if the new one is good
		self.outputSubPath = new
		log.write(new+'\n')
		log.menuOut()
		return True
	
	
	
	
	
	def editOutputName(self, log):
		'''method to change output naming convention'''
		# edit output naming
		log.write('edit output naming :')
		log.menuIn('output naming')
		os.system('clear')
		log.print()
		print('current output naming : '+self.outputName) 
		
		# get new name
		new = input('%N will be replaced by the original blender file name (optionel)\n\
%S will be replaced by the scene name (optionel)\n\
%L will be replaced by the renderlayer name\n\
%F will be replaced by the render frame number\n\
new naming :').strip()
		
		if new in ['', "''", '""']:
			log.write('\033[31mcanceled\033[0m\n')
			log.menuOut()
			return False
		
		if new[0] in ['\'', '"'] and new[0]==new[-1]:
			new  = new[1:len(new)-1]
		
		if new.find('/') != -1:
			# check if there is a '/' caractère in the new name
			log.write('\033[31munvalid : "'+new+'"\nThe name must not contain "/"!\033[0m\n')
			log.menuOut()
			return False
		
		if new.find('%L') == -1 or new.find('%F') == -1:
			# check if there is a '%F' and a '%L' sequences in the new name
			log.write('\033[31munvalid : "'+new+'"\nThe name must contain at less one occurence of "%L" and "%F" or different render risk to overwrite themselves!\033[0m\n')
			log.menuOut()
			return False
		
		# change output name if the new one is good
		self.outputName = new
		log.write(new+'\n')
		log.menuOut()
		return True
	
	
	
	
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
	
	
	
	
	def editTiles(self, log):
		'''method to change tiles size settings'''
		#edit Tiles settings
		log.menuIn('Tiles Size')
		change = False
		
		while True:
			os.system('clear')
			log.write('change tiles size : ')
			log.print()
			# print old settings
			name = ['Cycle GPU', 'Cycles CPU', 'Blender Internal']
			value = [ str(self.tilesCyclesGPUX)+'x'+str(self.tilesCyclesGPUY),
						str(self.tilesCyclesCPUX)+'x'+str(self.tilesCyclesCPUY),
						str(self.tilesBIX)+'x'+str(self.tilesBIY)]
			print('current sizes :\n'\
					+'\n    1- Cycle GPU tiles : '+value[0]+'\n'\
					+'\n    2- Cycles CPU tiles : '+value[1]+'\n'\
					+'\n    3- Blender Internal tiles : '+value[2]+'\n\n'
					)
			
			# get index of parameter to edit
			choice = input('''what's the tile size to edit?('q' to quit)''').strip().lower()
			
			try:
				if choice in ['q', 'cancel', 'quit']:
					choice = -1
				else:
					choice = int(choice)
			except ValueError:
				choice = 9999
			
			if choice == -1:
				log.write('\033[31mend\033[0m\n')
				log.menuOut()
				return change
			
			if choice < 1 or choice > 3:
				log.write('\033[31munvalid choice : "'+str(choice)+'"\033[0m\nretry\n')
				continue
			
			
			name = name[choice-1]
			value = value[choice-1]
			log.write(name+' new tiles size : ')
			
			# print current settings
			print('current '+name+' tiles size : '+value+'\n\n' )
			
			# get new size and check it
			new = input('new '+name+' tiles size ("256x256" or "256" syntax)').strip()
			match = re.search(r'^(\d{1,5})(x(\d{1,5}))?', new)
			
			if match is None:
				log.write('\033[31munvalid value : '+new+'\033[0m\n')
				continue
			
			# get new size x and y values
			match = match.groups()
			x = int(match[0])
			if match[2] is None:
				y = x
			else:
				y = int(match[2])
			
			# apply new size
			if choice == 1:
				self.tilesCyclesGPUX = x
				self.tilesCyclesGPUY = y
			elif choice == 2:
				self.tilesCyclesCPUX = x
				self.tilesCyclesCPUY = y
			elif choice == 3:
				self.tilesBIX = x
				self.tilesBIY = y
			
			log.write(str(x)+'x'+str(y)+'\n')
			change = True
	
	
	
	
	
	
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
	
	
	
	
	
	def editKeyword(self, log):
		'''method to manage renderlayer name keyword '''
		#edit Keywords settings
		change = False
		log.menuIn('Renderlayers Keywords')
		
		while True:
			os.system('clear')
			log.write('edit renderlayer keywords : ')
			log.print()
			
			# print option and current settings
			print('1- remove from current background keyword(s) :\n  '\
				+(' | '.join(self.backgroundLayersKeywords))\
				+'\n2- remove from current foreground keyword(s) :\n  '\
				+(' | '.join(self.foregroundLayersKeywords))\
				+'\n3- add background keyword\n'\
				+'4- add foreground keyword\n')
				
			
			# get index of option to run
			choice = input('''what do you want?('q' to quit)''').strip()
			
			try:
				if choice in ['q', 'cancel', 'quit']:
					choice = -1
				else:
					choice = int(choice)
			except ValueError:
				choice = -2
			
			# if user want to quit menu
			if choice == -1 :
				log.write('\033[31mend\033[0m\n')
				log.menuOut()
				return change
			
			# check if user make a valid choice
			if choice < 1 or choice > 4:
				log.write('\033[31munvalid choice : "'+str(choice)+'"\033[0m\n')
				continue
			
			# get corresponding list 
			if choice in [1, 3]:
				keys = self.backgroundLayersKeywords
				noKeys = self.foregroundLayersKeywords
			else:
				keys = self.foregroundLayersKeywords
				noKeys = self.backgroundLayersKeywords
			
			# call corresponding method
			if choice in [1, 2]:
				change = (self.removeKeyWords(log, keys, noKeys, choice) or change)
			else:
				change = (self.addKeyWords(log, keys, noKeys, choice) or change)
	
	
	
	
	
	
	def removeKeyWords(self, log, keys, noKeys, choice):
		'''method to remove renderlayer name keyword '''
		os.system('clear')
		
		if choice == 1:
			log.write('remove background keyword : ')
			log.menuIn('remove background keyword')
			log.print()
			print('current background keyword(s) :')
		else:
			log.write('remove foreground keyword : ')
			log.menuIn('remove foreground keyword')
			log.print()
			print('current foreground keyword(s) :')
		
		# print current settings
		for i, k in enumerate(keys):
			print('  '+str(i)+'- '+k)
		
		choice = input('''what is the keyword to remove? (type corresponding number or 'q' to quit)''').strip().lower()
		
		try:
			if choice in ['q', 'cancel', 'quit']:
				choice = -1
			else:
				choice = int(choice)
		except ValueError:
			choice = -2
		
		# check user choice
		if choice == -1:
			log.write('\033[31mend\033[0m\n')
			log.menuOut()
			return False
		
		
		if choice < 0 or choice >= len(keys) :
			log.write('\033[31munvalid choice : '+str(choice)+' : must be an integer between 0 and '+str(len(keys)-1)+'\033[0m\nretry\n')
			log.menuOut()
			return False
		
		# remove corresponding keyword
		log.write(keys.pop(choice)+'\n')
		log.menuOut()
		return True
	
	
	
	
	
	def addKeyWords(self, log, keys, noKeys, choice):
		'''method to add renderlayer name keywords'''
		os.system('clear')
		
		if choice == 3:
			log.write('add background keyword : ')
			log.menuIn('add background keyword')
			log.print()
			print('current background keyword(s) :')
		else:
			log.write('add foreground keyword : ')
			log.menuIn('add foreground keyword')
			log.print()
			print('current foreground keyword(s) :')
		
		# print current settings
		for k in keys:
			print('  '+k)
		
		choice = input('''what is the keyword to add? (type new keyword(s), split by a pipe (|) or empty string to pass)''').strip()
		
		# check user choice
		if choice == '':
			log.write('\033[31mcanceled\033[0m\n')
			log.menuOut()
			return False
			
		match = re.search(r'^[-0-9a-zA-Z_]{3,}( *\| *[-0-9a-zA-Z_]{3,})*$', choice)
		if match is None:
			log.write('''\033[31munvalid choice : '''+choice+''' : the keyword must only contain letters, numbers or '-' or '_', they can be split by '|' and space\033[0m\nretry\n''')
			log.menuOut()
			return False
		
		for v in choice:
			if v in noKeys:
				log.write('''\033[31munvalid choice : '''+choice+''' : some key word are already in the other keyword list\033[0m\nretry\n''')
				log.menuOut()
				return False
		
		# split and add new keywords
		log.write(choice+'\n')
		choice = choice.split('|')
		change = False
		for v in choice:
			if v not in keys:
				keys.append(v.strip())
				change = True
		log.menuOut()
		return change
	
	
	
	
	
	def editRenderlayerList(self, log):
		'''method to choose a renderlayer to edit settings'''
		change = False
		log.menuIn('Renderlayers')
		enable = { True : 'Enabled', False : 'Disabled' }
		
		while True:
			os.system('clear')
			log.write('edit renderlayer : ')
			log.print()
			print('		renderlayer list:\n')
			print('id- name => z pass => object index pass => activated')
			
			for i, layer in enumerate(self.renderLayerList):
				txt = str(i)+'- '+layer['name']
				for k in ['z', 'object index', 'use']:
					txt += ' => '+enable[layer[k]]
				print(txt)
			
			choice = input("id of renderlayer to edit?(or 'q' to quit)").strip().lower()
			
			try:
				if choice in ['q', 'cancel', 'quit']:
					choice = -1
				else:
					choice = int(choice)
			except ValueError:
				choice = -2
			
			if choice == -1:
				log.menuOut()
				log.write('quit\n')
				return change
			
			if choice < 0 or choice > i:
				log.write('unvalid choice, must be a integer between 0 and '+str(i)+' or q\n')
				continue
			
			change = (self.editRenderlayer(log, choice) or change)
	
	
	
	
	
	def editRenderlayer(self, log, index):
		'''method to edit a renderlayer settings'''
		change = False
		layer = self.renderLayerList[index]
		log.menuIn(layer['name'])
		log.write(layer['name']+'\n')
		enable = { True : 'Disable', False : 'enable' }
		settings = ['z', 'object index', 'use']
		
		while True:
			os.system('clear')
			log.print()
			
			print('		Edit «'+layer['name']+'» renderlayer settings :')
			print('1- '+enable[layer['z']]+' renderlayer Z pass')
			print('2- '+enable[layer['object index']]+' renderlayer object index pass')
			print('3- '+enable[layer['use']]+' renderlayer')
			
			choice = input("action?(corresponding integer or 'q' to quit)").strip().lower()
			
			try:
				if choice in ['q', 'cancel', 'quit']:
					choice = -1
				else:
					choice = int(choice)-1
			except ValueError:
				choice = -2
			
			if choice == -1:
				log.menuOut()
				log.write('quit\n')
				return change
			
			if choice < 0 or choice > 2:
				log.write('unknow action\n')
				continue
			
			
			log.write(enable[layer[settings[choice]]])
			if choice == 2:
				log.write(' renderlayer\n')
			else:
				log.write(' '+settings[choice]+' pass\n')
			layer[settings[choice]] = not(layer[settings[choice]])
			change = True
			
	
	
	
	
	
