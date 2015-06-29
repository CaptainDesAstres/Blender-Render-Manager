 #!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''A script to be executed by Blender Python API to return Blender version'''

import bpy
print('<?xml version="1.0" encoding="UTF-8"?>\n')
print('<root>\n')
version = bpy.app.version_string
print('<version version="'+str(version[0])+'.'+str(version[1])+'-'\
					+str(bpy.app.build_branch)+'" />\n')
print('</root>')
