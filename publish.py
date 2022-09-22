import maya.cmds as cmds
import os

def openAsset():
   print("test")

def openSequence():
   print("test")

def prefixPath():
   global prefixPath
   prefixPath = cmds.textFieldGrp(path, q = True, text = True)
   if(os.path.isdir(prefixPath)):
      os.chdir(prefixPath)
      print(prefixPath)
   else:
      print("Warning: Folder Path does not exist! ")


def save_window():
   folderPath = prefixPath + "\wip"
   if(os.path.isdir(folderPath)):
      os.chdir(folderPath)
   else:
      os.mkdir(folderPath)
      os.chdir(folderPath)
   if cmds.window('save_publish_init', exists = True):
      cmds.deleteUI('save_publish_init')
   cmds.window('save_window', resizeToFitChildren=True)
   cmds.scrollLayout()
   
   cmds.showWindow('save_window')


def publish_window():
   folderPath = prefixPath + "\publish"
   if(os.path.isdir(folderPath)):
      os.chdir(folderPath)
   else:
      os.mkdir(folderPath)
      os.chdir(folderPath)
   if cmds.window('save_publish_init', exists = True):
      cmds.deleteUI('save_publish_init')
   cmds.window('publish_window', resizeToFitChildren=True)
   cmds.scrollLayout()
   
   cmds.showWindow('publish_window')


def save_publish_init():
   if cmds.window('save_publish_init', exists = True):
      cmds.deleteUI('save_publish_init')
   cmds.window('save_publish_init', resizeToFitChildren=True)
   cmds.scrollLayout()

   global path
   path = cmds.textFieldGrp(label = 'Folder Path:', text=os.getcwd(),editable=True)
   cmds.button(l = 'Confirm', command = 'prefixPath()')
   cmds.button(label = 'Save', command = 'save_window()')
   cmds.button(label = 'Publish', command = 'publish_window()')

   cmds.showWindow('save_publish_init')

save_publish_init()

