import maya.cmds as cmds
import os

def openCharater():
   folderPath = folderPath + "\Asset"
   if(os.path.isdir(folderPath)):
      destPath = folderPath + "\Character"
      if(os.path.isdir(destPath)):
         os.chdir(destPath)
      else:
         os.mkdir(destPath)
         os.chdir(destPath)
   else:
      os.mkdir(folderPath)
      os.chdir(folderPath)

def openProp():
   folderPath = folderPath + "\Asset"
   if(os.path.isdir(folderPath)):
      destPath = folderPath + "\Prop"
      if(os.path.isdir(destPath)):
         os.chdir(destPath)
      else:
         os.mkdir(destPath)
         os.chdir(destPath)
   else:
      os.mkdir(folderPath)
      os.chdir(folderPath)

def openSet():
   folderPath = folderPath + "\Asset"
   if(os.path.isdir(folderPath)):
      destPath = folderPath + "\Set"
      if(os.path.isdir(destPath)):
         os.chdir(destPath)
      else:
         os.mkdir(destPath)
         os.chdir(destPath)
   else:
      os.mkdir(folderPath)
      os.chdir(folderPath)

def openSetPiece():
   folderPath = folderPath + "\Asset"
   if(os.path.isdir(folderPath)):
      destPath = folderPath + "\SetPiece"
      if(os.path.isdir(destPath)):
         os.chdir(destPath)
      else:
         os.mkdir(destPath)
         os.chdir(destPath)
   else:
      os.mkdir(folderPath)
      os.chdir(folderPath)

def openSequence():
   global folderPath 
   folderPath = prefixPath + "\Sequence"
   if(os.path.isdir(folderPath)):
      os.chdir(folderPath)
   else:
      os.mkdir(folderPath)
      os.chdir(folderPath)

def nameFile():
   print("test")

def saveFile():
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
   global folderPath 
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
   global folderPath
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
