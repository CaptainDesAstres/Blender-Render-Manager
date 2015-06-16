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
		self.x = 1920
		self.y = 1080
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
		self.outputFormat = 'EXR'
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
		self.transparencyMaxBounces = 6
		self.transparencyMinBounces = 4
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
		self.x = int(node.get('x'))
		self.y = int(node.get('y'))
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
		self.filmExposure = node.get('exposure') in ['true', 'True']
		self.filmTransparentEnable = node.get('transparent') in ['true', 'True']
		
		# get cycles Ligth Path parameters
		node = xml.find('cycles').find('bouncesSet')
		self.transparencyMaxBounces = int(node.find('transparency').get('max'))
		self.transparencyMinBounces = int(node.find('transparency').get('min'))
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
		txt += '\t<resolution x="'+str(self.x)+'" y="'+str(self.y)+'" percent="'+str(int(self.percent*100))+'" />\n'
		
		# export animation parameters depending of settings type
		if self.start is None or self.end is None:
			txt+= '\t<animation fps="'+str(self.fps)+'" />\n'
		else:
			txt+= '\t<animation start="'+str(self.start)+'" end="'+str(self.end)+'" fps="'+str(self.fps)+'" />\n'
		
		# export engine parameter
		txt += '\t<engine value="'+self.renderingEngine+'"/>\n'
		
		# export Cycles specific  parameters
		txt += '\t<cycles>\n'
		txt += '\t\t<cpu x="'+str(self.tilesCyclesCPUX)+'" y="'+str(self.tilesCyclesCPUY)+'"/>\n'
		txt += '\t\t<gpu x="'+str(self.tilesCyclesGPUX)+'" y="'+str(self.tilesCyclesGPUY)+'"/>\n'
		txt += '\t\t<device value="'+self.renderingDevice+'"/>\n'
		txt += '\t\t<film exposure="'+str(self.filmExposure)+'" transparent="'+str(self.filmTransparentEnable)+'" />\n'
		
		# export light path Cycles specific  parameters
		txt += '\t\t<bouncesSet>\n'
		txt += '\t\t\t<transparency max="'+str(self.transparencyMaxBounces)+'" min="'+str(self.transparencyMinBounces)+'" />\n'
		txt += '\t\t\t<bounces max="'+str(self.bouncesMax)+'" min="'+str(self.bouncesMin)+'" />\n'
		txt += '\t\t\t<diffuse bounces="'+str(self.diffuseBounces)+'" />\n'
		txt += '\t\t\t<glossy bounces="'+str(self.glossyBounces)+'" />\n'
		txt += '\t\t\t<transmission bounces="'+str(self.transmissionBounces)+'" />\n'
		txt += '\t\t\t<volume bounces="'+str(self.volumeBounces)+'" />\n'
		txt += '\t\t</bouncesSet>\n'
		
		
		
		txt += '\t</cycles>\n'
		
		# export Blender Internal engine specific  parameters
		txt += '\t<blenderInternal x="'+str(self.tilesBIX)+'" y="'+str(self.tilesBIY)+'" />\n'

		# export rendering options
		txt += '\t<compositing enable="'+str(self.compositingEnable)+'" />\n'
		if self.simplify is not None:
			txt += '\t<simplify subdiv="'+str(self.simplify)+'" />\n'
		
		
		# export renderlayer list and parameters
		if len(self.renderLayerList)>0:
			txt += '\t<renderLayerList>\n'
			for layer in self.renderLayerList:
				txt += '\t\t<layer name="'+layer['name']+'" z="'+str(layer['z'])+'" objIndex="'+str(layer['object index'])+'" render="'+str(layer['use'])+'"/>\n'
			txt += '\t</renderLayerList>\n'
		
		
		txt += '\t<renderLayerPreferences>\n'
		
		# export background render layers specific parameters
		txt += '\t\t<background sample="'+str(self.backgroundCyclesSamples)+'" frame="'+str(self.backgroundAnimation)+'" >\n'
		for key in self.backgroundLayersKeywords:
			txt += '\t\t\t<keywords value="'+key+'" />\n'
		txt += '\t\t</background>\n'
		
		# export foreground render layers specific parameters
		txt += '\t\t<foreground sample="'+str(self.foregroundCyclesSamples)+'" frame="'+str(self.foregroundAnimation)+'" >\n'
		for key in self.foregroundLayersKeywords:
			txt += '\t\t\t<keywords value="'+key+'" />\n'
		txt += '\t\t</foreground>\n'
		
		# export animation render layers specific parameters
		txt += '\t\t<main sample="'+str(self.mainAnimationCyclesSamples)+'" zPass="'+str(self.zPass)+'" objectIndexPass="'+str(self.objectIndexPass)+'" />\n'
		
		txt += '\t</renderLayerPreferences>\n'
		
		
		# export rendering output parameters
		txt += '\t<output format="'+self.outputFormat+'" '
		if self.outputPath is not None:
			txt += 'mainpath="'+self.outputPath+'" '
		txt += 'subpath="'+self.outputSubPath+'" name="'+self.outputName+'" />\n'
		
		txt += '\t<blender path="'+self.blenderPath+'" />\n'
		
		if root:
			txt += '</settings>'
		return txt
	
	
	
	
	
	def print(self):
		'''print settings like preferences settings'''
		enable = {True:'enabled', False:'Disabled'}
		
		print('Blender path : '+self.blenderPath+'\n')
		
		# print resolution parameters
		print('Résolution : '+str(self.x)+'x'+str(self.y)+' (@'+str(int(self.percent*100))+'%)\n')
		
		# print Cycles sampling parameters
		print('Cycles samples :')
		print('\tmain : '+str(self.mainAnimationCyclesSamples))
		print('\tbackground : '+str(self.backgroundCyclesSamples))
		print('\tforeground : '+str(self.foregroundCyclesSamples)+'\n')
		
		# print animation and engine parameters
		print('Animation : '+str(self.fps)+'fps')
		print('Engine : '+self.renderingEngine.lower()+'('+self.renderingDevice+')\n')
		
		# print output parameters
		print('Output : ')
		print('\toutput path (absolute) : '+str(self.outputPath))
		print('\tautomatique subpath (for each task) : '+self.outputSubPath)
		print('\tname : '+self.outputName)
		print('\tformat : '+self.outputFormat+'\n')
		
		
		# print Tiles parameters
		print('Tiles : ')
		print('\tcycles GPU : '+str(self.tilesCyclesGPUX)+'x'+str(self.tilesCyclesGPUY))
		print('\tcycles CPU : '+str(self.tilesCyclesCPUX)+'x'+str(self.tilesCyclesCPUY))
		print('\tblender internal : '+str(self.tilesBIX)+'x'+str(self.tilesBIY)+'\n')
		
		
		# print Ligth path parameters
		print('Ligth path : ')
		print('\tbounces : '+str(self.bouncesMin)+' to '+str(self.bouncesMax))
		print('\ttransparency : '+str(self.transparencyMinBounces)+' to '+str(self.transparencyMaxBounces))
		print('\tdiffuse : '+str(self.diffuseBounces))
		print('\tglossy : '+str(self.glossyBounces))
		print('\ttransmission : '+str(self.transmissionBounces))
		print('\tvolume : '+str(self.volumeBounces)+'\n')
		
		
		# print others parameters
		print('OPtions :')
		print('\tz pass : '+enable[self.zPass])
		print('\tobject index pass : '+enable[self.objectIndexPass])
		print('\tcompositing : '+enable[self.compositingEnable])
		print('\texposure (cycles) : '+str(self.filmExposure))
		print('\ttransparent background : '+enable[self.filmTransparentEnable])
		if self.simplify is None:
			print('\tsimplify : Disabled\n')
		else:
			print('\tsimplify : '+str(self.simplify)+'\n')
		
		print('Keywords :')
		print('\tbackground : '+' | '.join(self.backgroundLayersKeywords))
		print('\tforeground : '+' | '.join(self.foregroundLayersKeywords)+'\n')
		
	
	
	
	
	
	def getClone(self):
		'''create another settings object with the same attribut values
		restart/end attributes value with start/end argument values if set'''
		
		return setting( xmlMod.fromstring( self.toXmlStr( head = True, root = True) ) )
	
	
	
	
	
	def see(self, log):
		'''print settings and let edit or reset it'''
		change = False
		while True:
			#print log and preferences
			os.system('clear')
			log.print()
			print('\t\tSettings\n')
			self.print()
		
			#treat available actions
			choice= input('(e)dit, (r)eset or (q)uit (and save): ')
			if choice in ['Q','q']:
				log.write('quit settings\n')
				return change
			elif choice in ['e','E']:
				log.write('edit settings\n')
				change = (self.edit(log) or change)
			elif choice in ['R','r']:
				#reset default settings
				confirm = input('this action will reset to factory settings. confirm (y):')
				if confirm in ['y','Y']:
					self.__init__()
					change = True
					log.write('reset factory settings\n')
				else:
					log.write('abort settings reset\n')
			else:
				log.write('unknow request\n')
	
	
	
	
	def edit(self, log):
		'''method to edit settings/preferences'''
		change = False
		
		while True:
			#print log and edit preferences menu
			os.system('clear')
			log.print()
			print('''		preferences editing:
		0- Blender path
		1- Resolution
		2- Animation rate
		3- Cycles samples
		4- Engine
		5- Output
		6- Tiles
		7- Ligth path
		8- OPtions
		9- Keywords''')
		
			#treat available actions
			choice = input('what\'s the parameter to edit ?(or \'q\' or \'cancel\')')
			if choice in ['cancel','CANCEL','QUIT','quit','Q','q']:
				log.write('quit\n')
				return change
			elif choice in ['0','b','B']:
				#edit blender path
				change = (self.editBlenderPath(log) or change)
			elif choice in ['1','r','R']:
				#edit resolution setting
				change = (self.editResolution(log) or change)
			elif choice in ['2','a','A']:
				#edit animation frame rate
				change = (self.editAnimationRate(log) or change)
			elif choice in ['3','c','C']:
				# edit Cycles samples settings
				change = (self.editSample(log) or change)
			elif choice in ['4','e','E']:
				#edit Engine settings
				change = (self.editEngine(log) or change)
			elif choice in ['5','o','O']:
				#edit Output settings
				change = (self.editOutput(log) or change)
			elif choice in ['6','t','T']:
				#edit Tiles settings
				change = (self.editTiles(log) or change)
			elif choice in ['7','l','L']:
				#edit Ligth path settings
				change = (self.editLight(log) or change)
			elif choice in ['8','op','OP']:
				#edit OPtions settings
				change = (self.editOption(log) or change)
			elif choice in ['9','k','K']:
				#edit Keywords settings
				change = (self.editKeyword(log) or change)
			else:
				log.write('unknow request!\n')
	
	
	
	
	
	
	def editBlenderPath(self, log):
		'''method to change absolute path to the Blender version to use'''
		#edit blender path
		change = False
		#print current blender path and ask a new one
		os.system('clear')
		log.write('blender path editing: ')
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
				log.write('blender path change canceled\n')
			else:
				log.write("error, the path must be an absolute path(beginng by '/' and ending by 'blender') or the 'blender' command\n blender path change canceled, retry!\n")
			return change
		elif choice == 'blender':
			#apply new settings and save it
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
				log.write("error: the file didn't exist or is not a file or is not executable\n blender path change canceled, retry\n")
		return change
	
	
	
	
	
	
	def editResolution(self, log):
		'''method to edit the render resolution to use'''
		#edit resolution setting
		#print current resolution settings and ask new settings
		os.system('clear')
		log.write('resolution editing: ')
		log.print()
		print('current resolution :'+str(self.x)+'x'+str(self.y)+'@'+str(int(self.percent*100))+'\n\n')
		choice = input('new resolution ? (1920x1080@100 for example or \'cancel\')')
		
		
		#parse new settings and check it
		match = re.search(r'^(\d{3,5})x(\d{3,5})@(\d{2,3})$',choice)
		if match is None:
			if choice in ['cancel','CANCEL','QUIT','quit','Q','q']:
				log.write('quit resolution editing \n')
			else:
				log.write('error, resolution change unvalid, retry\n')
			return False
		
		
		#apply new settings and save it
		self.x = int(match.group(1))
		self.y = int(match.group(2))
		self.percent = int(match.group(3))/100
		log.write(choice+'\n')
		return True
	
	
	
	
	
	def editAnimationRate(self, log):
		'''method to use to change the animation rate of the render'''
		#edit animation frame rate
		#print log and current animation settings and ask new settings
		os.system('clear')
		log.write('edit animation rate : ')
		log.print()
		print('current animation rate: '+str(self.fps)+'fps\n\n')
		choice = input('new animation rate? ( 30 for example or \'cancel\')')
	
		#parse new settings and check it
		match = re.search(r'^(\d{1,})(fps)?$',choice)
		if match is None:
			if choice in ['cancel','CANCEL','QUIT','quit','Q','q']:
				log.write('animation frame rate change canceled\n')
			else:
				log.write('error, animation frame rate change canceled, retry\n')
			return False
	
		#apply new settings and save it
		self.fps = int(match.group(1))
		log.write(match.group(1)+'fps\n')
		return True
	
	
	
	
	
	def editSample(self, log):
		'''method to change the sample settings of Cycles renders'''
		# edit Cycles samples settings
		change = False
		# print current settings
		while True:
			os.system('clear')
			log.write('edit Cycles sample settings : ')
			log.print()
			print('current Cycles sample settings: '\
					+'\n\t1- Main sample : '+str(self.mainAnimationCyclesSamples)\
					+'\n\t2- Background sample : '+str(self.backgroundCyclesSamples)\
					+'\n\t3- Foreground sample : '+str(self.foregroundCyclesSamples)\
					+'\n\n')
			
			# choice of the parameters to edit
			choice = input('what\'s the parameter to edit? ( \'1\', \'2\' \'3\' or \'q\'):').strip()
		
			if choice in ['q', 'quit', 'cancel', 'Q', 'QUIT', 'CANCEL']:
				# quit Cycles sample settings edition
				log.write('quit sample editing\n')
				return change
			
			if choice not in ['1', '2', '3']:
				print('unvalid choice : '+choice)
				continue
			
			# edit sample settings
			
			choice = int(choice)
			name = ['main animation', 'background', 'foreground'][choice-1]
			value = [str(self.mainAnimationCyclesSamples), 
					str(self.backgroundCyclesSamples), 
					str(self.foregroundCyclesSamples)][choice-1]
			
			# print current setting
			os.system('clear')
			log.write(name+' : ')
			log.print()
			print('current '+name+' sample settings : '\
					+value+'\n\n')
			
			# get user choice
			new = input('new '+name+' sample? (an integer or \'q\')').strip()
			match = re.search(r'^(\d{1,})?$',new)
			
			# if user input is not an integer, quit cycle sample setting edition
			if match is None:
				if new not in ['q', 'quit', 'cancel', 'Q', 'QUIT', 'CANCEL']:
					log.write('unvalid settings :'+new\
							+'\nretry\n')
					return change
				log.write('canceled\n')
				continue
			
			# apply a good new setting
			log.write(new+'\n')
			new = int(new)
			if choice == 1:
				self.mainAnimationCyclesSamples = new
			elif choice == 2:
				self.backgroundCyclesSamples = new
			elif choice == 3:
				self.foregroundCyclesSamples = new
			change = True
	
	
	
	
	
	def editEngine(self, log):
		'''method to change the default rendering engine '''
		#edit Engine settings
		change = False
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
	3- Quit
''')
			if choice in ['q', 'Q', 'quit', 'QUIT', 'cancel', 'CANCEL', '3']:
				log.write('end\n')
				return change
			elif choice in ['1', 'e', 'E']:
				if self.renderingEngine == 'CYCLES':
					self.renderingEngine = 'BLENDER_RENDER'
				else:
					self.renderingEngine = 'CYCLES'
				change = True
				log.write('engine switch to '+self.renderingEngine+'\n')
			elif choice in ['2', 'd', 'D']:
				if self.renderingDevice == 'GPU':
					self.renderingDevice = 'CPU'
				else:
					self.renderingDevice = 'GPU'
				change = True
				log.write('device switch to '+self.renderingDevice+'\n')
			else:
				log.write('unvalid choice :'+choice+'\nretry\n')
			
	
	
	
	
	
	def editOutput(self, log):
		'''method to change all the output settings'''
		#edit Output settings
		change = False
		while True:
			os.system('clear')
			log.write('change output Settings : ')
			log.print()
			
			# print old settings
			print('current output settings : '\
					+'\n\t1- Output path (absolute) : '+str(self.outputPath)\
					+'\n\t2- Subpath : '+self.outputSubPath\
					+'\n\t3- Name : '+self.outputName\
					+'\n\t4- Format : '+self.outputFormat\
					+'\n\t5- Quit\n\n')
			choice = input('''What's the setting to edit?''')
			
			if choice in ['q', 'Q', 'quit', 'QUIT', 'cancel', 'CANCEL', '5']:
				# quit edition
				log.write('end\n')
				return change
			elif choice in ['1', 'o', 'O']:
				# edit output path
				change = (self.editOutputPath(log) or change)
			elif choice in ['2', 's', 'S']:
				# edit subpath
				change = (self.editOutputSubpath(log) or change)
			elif choice in ['3', 'n', 'N']:
				# edit output naming
				change = (self.editOutputName(log) or change)
			elif choice in ['4', 'f', 'F']:
				# edit output format
				change = (self.editOutputFormat(log) or change)
			else:
				log.write('unvalid choice :'+choice+'\nretry\n')
			
	
	
	
	
	def editOutputPath(self, log):
		'''method to change output path'''
		# edit output path
		log.write('edit main output path:')
		print('current output path : '+str(self.outputPath)) 
		new = input('\nnew path (must already exist and be absolute path):').strip()
		
		# empty path
		if new in ['', "''", '""']:
			self.outputPath = None
			log.write('set to None\n')
			return True
		
		if new[0] in ['\'', '"'] and new[0]==new[-1]:
			new  = new[1:len(new)-1]
		
		match = re.search(r'^/(.+/)$',new)
		
		if match is None:
			# check if path is a good syntaxe
			log.write('unvalid path : "'+new+'"\nThe path must be absolute (begin and end by "/")')
			return False
		
		# check if it's a good path and save it
		if os.path.exists(new) and os.path.isdir(new)\
				and os.access(new, os.W_OK):
			self.outputPath = new
			log.write(new+'\n')
			return True
		
		log.write("unvalid path : '"+new+"'\nthe path didn't exist, is not a directories or you don't have the right to write in it\n")
		return False
	
	
	
	
	
	def editOutputSubpath(self, log):
		'''method to change output subpath naming convention'''
		# edit output subpath
		# write old settings
		log.write('edit output subpath :')
		print('current output subpath : '+self.outputSubPath) 
		new = input('\nnew subpath (%N will be replaced by the task file name and %S by the scene name):').strip()
		
		if new in ['', "''", '""']:
			log.write('canceled\n')
			return False
		
		if new[0] in ['\'', '"'] and new[0]==new[-1]:
			new  = new[1:len(new)-1]
		
		if new.find('/') != -1:
			# check if there is a '/' caractère in the new name
			log.write('unvalid : "'+new+'"\nThe subpath must not contain "/"!\n')
			return False
		
		if new.find('%S') == -1 or new.find('%N') == -1:
			# check if there is a '%N' and a '%S' sequences in the new name
			log.write('unvalid : "'+new+'"\nThe subpath must contain at less one occurence of "%N" and "%S" or different render risk to overwrite themselves!\n')
			return False
		
		# change output SubPath if the new one is good
		self.outputSubPath = new
		log.write(new+'\n')
		return True
	
	
	
	
	
	def editOutputName(self, log):
		'''method to change output naming convention'''
		# edit output naming
		log.write('edit output naming :')
		print('current output naming : '+self.outputName) 
		
		# get new name
		new = input('%N will be replaced by the original blender file name (optionel)\n\
%S will be replaced by the scene name (optionel)\n\
%L will be replaced by the renderlayer name\n\
%F will be replaced by the render frame number\n\
new naming :').strip()
		
		if new in ['', "''", '""']:
			log.write('canceled\n')
			return False
		
		if new[0] in ['\'', '"'] and new[0]==new[-1]:
			new  = new[1:len(new)-1]
		
		if new.find('/') != -1:
			# check if there is a '/' caractère in the new name
			log.write('unvalid : "'+new+'"\nThe name must not contain "/"!\n')
			return False
		
		if new.find('%L') == -1 or new.find('%F') == -1:
			# check if there is a '%F' and a '%L' sequences in the new name
			log.write('unvalid : "'+new+'"\nThe name must contain at less one occurence of "%L" and "%F" or different render risk to overwrite themselves!\n')
			return False
		
		# change output name if the new one is good
		self.outputName = new
		log.write(new+'\n')
		return True
	
	
	
	
	def editOutputFormat(self, log):
		'''method to change output format'''
		# edit output format
		# print old setting
		log.write('edit output format :')
		print('current output format : '+self.outputFormat) 
		new = input('new format (available: png / jpeg / open_exr / open_exr_multilayer):').strip().upper()
		
		if new in ['PNG', 'JPEG', 'OPEN_EXR', 'OPEN_EXR_MULTILAYER']:
			# change format if the one is one of the available
			self.outputFormat = new
			log.write(new+'\n')
			return True
		
		log.write('unvalid format : "'+new+'"\n')
		return False
	
	
	
	
	def editTiles(self, log):
		'''method to change tiles size settings'''
		#edit Tiles settings
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
					+'\n\t\t1- Cycle GPU tiles : '+value[0]+'\n'\
					+'\n\t\t2- Cycles CPU tiles : '+value[1]+'\n'\
					+'\n\t\t3- Blender Internal tiles : '+value[2]+'\n\n'
					)
			
			# get index of parameter to edit
			choice = input('''what's the tile size to edit?('q' to quit)''')
			
			if choice in ['q', 'Q', 'quit', 'QUIT', 'cancel', 'CANCEL']:
				log.write('end\n')
				return change
			
			if choice not in ['1', '2', '3']:
				log.write('unvalid choice : "'+choice+'"\nretry\n')
				continue
			
			choice = int(choice)
			name = name[choice-1]
			value = value[choice-1]
			log.write(name+' new tiles size : ')
			
			# print current settings
			print('current '+name+' tiles size : '+value+'\n\n' )
			
			# get new size and check it
			new = input('new '+name+' tiles size ("256x256" or "256" syntax)').strip()
			match = re.search(r'^(\d{1,5})(x(\d{1,5}))?', new)
			
			if match is None:
				log.write('unvalid value : '+new+'\n')
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
		
		while True:
			os.system('clear')
			log.write('change Light path settings : ')
			log.print()
			# get current settings
			name = ['bounces', 'transparency', 'diffuse', 'glossy', 'transmission', 'volume']
			value = [ str(self.bouncesMin)+' to '+str(self.bouncesMax),
						str(self.transparencyMinBounces)+' to '+str(self.transparencyMaxBounces),
						str(self.diffuseBounces),
						str(self.glossyBounces),
						str(self.transmissionBounces),
						str(self.volumeBounces)
						]
			
			# print current light path settings
			print('current light path settings :')
			i=0
			while i < 6:
				print('\t\t'+str(i+1)+'- '+name[i]+' : '+value[i])
				i += 1
			
			# get index of parameter to edit
			choice = input('''what's the parameter to edit?('q' to quit)''').strip()
			
			# if user want to quit menu
			if choice in ['q', 'Q', 'quit', 'QUIT', 'cancel', 'CANCEL']:
				log.write('end\n')
				return change
			
			# if user don't make a valid choice
			if choice not in['1', '2', '3', '4', '5', '6']:
				log.write('unvalid choice : "'+choice+'"\n')
				continue
			
			# get choice corresponding value
			choice = int(choice)-1
			name = name[choice]
			value = value[choice]
			log.write(name+' : ')
			if choice < 2:
				syntax = '3to15'
			else:
				syntax = '8'
			
			# get new value
			print(name+' current value : '+value+'\n')
			new = input('new setting( respect "'+syntax+'" syntax)').strip()
			
			if choice >= 2:
				# treat value that represent only one number
				match = re.search(r'^(\d{1,})$',new)
				if match is None:
					log.write('unvalid value : "'+new+'"\nretry\n')
					continue
				
				# change corresponding settings
				new = int(new)
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
				match = re.search(r'^(\d{1,}) to (\d{1,})$',new)
				if match is None:
					log.write('unvalid value : "'+new+'"\nretry\n')
					continue
				
				# get value and check it
				mini = match.group(1)
				maxi = match.group(2)
				if maxi < mini:
					log.write('unvalid value : "'+new+'" : second value must be greater or equal to first\nretry\n')
					continue
				
				# change corresponding settings
				if choice == 0:
					self.bouncesMin = mini
					self.bouncesMax = maxi
				elif choice == 1:
					self.transparencyMinBounces = mini
					self.transparencyMaxBounces = maxi
				
				# confirm change
				log.write(new+'\n')
				change = True
				
	
	
	
	
	
	def editOption(self, log):
		'''method to enable/disable rendering options'''
		#edit OPtions settings
		change = False
		enable = { True : 'Enabled' , False : 'Disabled' }
		
		while True:
			os.system('clear')
			log.write('change rendering option : ')
			log.print()
			
			# print current rendering options settings
			print('current rendering option settings :'\
				+'\n\t1- z pass : '+enable[self.zPass]\
				+'\n\t2- object index pass : '+enable[self.objectIndexPass]\
				+'\n\t3- compositing : '+enable[self.compositingEnable]\
				+'\n\t4- transparent background : '+enable[self.filmTransparentEnable])
			if self.simplify is None:
				print('\t5- simplify : Disabled')
			else:
				print('\t5- simplify : '+str(self.simplify))
			print('\t6- exposure (Cycles) : '+str(self.filmExposure))
			
			# get index of parameter to edit
			choice = input('''what's the option to switch/edit?('q' to quit)''').strip()
			
			# if user want to quit menu
			if choice in ['q', 'Q', 'quit', 'QUIT', 'cancel', 'CANCEL']:
				log.write('end\n')
				return change
			
			# check if user make a valid choice
			if choice not in ['1', '2', '3', '4', '5', '6']:
				log.write('unvalid choice : "'+choice+'"\n')
				continue
			
			choice = int(choice)
			
			if choice == 1:
				# switch corresponding settings
				self.zPass = not(self.zPass)
				log.write('z pass set to : "'+enable[self.zPass]+'"\n')
				change = True
			elif choice == 2:
				# switch corresponding settings
				self.objectIndexPass = not(self.objectIndexPass)
				log.write('object index pass set to : "'+enable[self.objectIndexPass]+'"\n')
				change = True
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
				
				# check value
				if re.search(r'^(\d{1,})$',choice) is None:
					log.write('unvalid value : "'+choice+'" : must be an integer\nretry\n')
					continue
				
				# apply new value
				choice = int(choice)
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
				
				# check value
				if re.search(r'^(\d{1,}(\.\d{1,})?)$',choice) is None:
					log.write('unvalid value : "'+choice+'" : must be a number\nretry\n')
					continue
				
				# apply new value
				self.filmExposure = float(choice)
				log.write(choice+'\n')
				change = True
	
	
	
	
	
	def editKeyword(self, log):
		'''method to manage renderlayer name keyword '''
		#edit Keywords settings
		change = False
		
		while True:
			os.system('clear')
			log.write('edit renderlayer keywords : ')
			log.print()
			
			# print option and current settings
			print('1- remove from current background keyword(s) :\n\t'\
				+(' | '.join(self.backgroundLayersKeywords))\
				+'\n2- remove from current foreground keyword(s) :\n\t'\
				+(' | '.join(self.foregroundLayersKeywords))\
				+'\n3- add background keyword\n'\
				+'4- add foreground keyword\n')
				
			
			# get index of option to run
			choice = input('''what do you want?('q' to quit)''').strip()
			
			# if user want to quit menu
			if choice in ['q', 'Q', 'quit', 'QUIT', 'cancel', 'CANCEL']:
				log.write('end\n')
				return change
			
			# check if user make a valid choice
			if choice not in ['1', '2', '3', '4']:
				log.write('unvalid choice : "'+choice+'"\n')
				continue
			
			# get corresponding list 
			if choice in ['1', '3']:
				keys = self.backgroundLayersKeywords
				noKeys = self.foregroundLayersKeywords
			else:
				keys = self.foregroundLayersKeywords
				noKeys = self.backgroundLayersKeywords
			
			# call corresponding method
			if choice in ['1', '2']:
				change = (self.removeKeyWords(log, keys, noKeys, choice) or change)
			else:
				change = (self.addKeyWords(log, keys, noKeys, choice) or change)
	
	
	
	
	
	
	def removeKeyWords(self, log, keys, noKeys, choice):
		'''method to remove renderlayer name keyword '''
		if choice=='1':
			log.write('remove background keyword : ')
			print('current background keyword(s) :')
		else:
			log.write('remove foreground keyword : ')
			print('current foreground keyword(s) :')
		
		# print current settings
		for i, k in enumerate(keys):
			print('\t'+str(i)+'- '+k)
		
		choice = input('''what is the keyword to remove? (type corresponding number or 'q' to quit)''').strip()
		match = re.search(r'^\d{1,}$', choice)
		
		# check user choice
		if match is None:
			if choice in ['q', 'Q', 'quit', 'QUIT', 'cancel', 'CANCEL']:
				log.write('end\n')
				return False
			log.write('unvalid choice : '+choice+' : must be an integer\nretry\n')
			return False
		
		choice = int(choice)
		if choice >= len(keys) :
			log.write('unvalid choice : '+str(choice)+' : the greater keyword index is '+str(len(keys))+'\nretry\n')
			return False
		
		# remove corresponding keyword
		log.write(keys.pop(choice)+'\n')
		return True
	
	
	
	
	
	def addKeyWords(self, log, keys, noKeys, choice):
		'''method to add renderlayer name keywords'''
		
		if choice=='3':
			log.write('add background keyword : ')
			print('current background keyword(s) :')
		else:
			log.write('add foreground keyword : ')
			print('current foreground keyword(s) :')
		
		# print current settings
		for k in keys:
			print('\t'+k)
		
		choice = input('''what is the keyword to add? (type new keyword(s), split by a pipe (|) or empty string to pass)''').strip()
		
		# check user choice
		if choice == '':
			log.write('canceled\n')
			return False
		match = re.search(r'^[-0-9a-zA-Z_]{3,}( *\| *[-0-9a-zA-Z_]{3,})*$', choice)
		if match is None:
			log.write('''unvalid choice : '''+choice+''' : the keyword must only contain letters, numbers or '-' or '_', they can be split by '|' and space\nretry\n''')
			return False
		
		for v in choice:
			if v in noKeys:
				log.write('''unvalid choice : '''+choice+''' : some key word are already in the other keyword list\nretry\n''')
				return False
		
		# split and add new keywords
		log.write(choice+'\n')
		choice = choice.split('|')
		change = False
		for v in choice:
			if v not in keys:
				keys.append(v.strip())
				change = True
		return change
	
	
	
	
	
	
	
	
