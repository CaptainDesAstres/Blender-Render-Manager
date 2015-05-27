import os
#on vas dans le dossier dédié a blender manager
os.chdir('/home/'+os.getlogin()+'/')
try:
	os.listdir(os.getcwd()).index('.BlenderRenderManager')
except ValueError:
	#si le dossier n'existe pas on le créer
	os.mkdir('.BlenderRenderManager')
	os.mkdir('.BlenderRenderManager/log')
	
os.chdir('/home/'+os.getlogin()+'/.BlenderRenderManager')
	
print('you said "'+os.getcwd()+'"')

