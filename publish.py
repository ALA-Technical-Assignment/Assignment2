import maya.cmds as cmds
import os
import pathlib

path = r"{}".format(cmds.file(q=True, sceneName=True))
prefixPath = ''
folderPath = ''
filePath = ''
files = []
fileName = ''
saveMode = False
publishMode = False

# Methods to execute
# Save window methods
def nameFile(currentValue):
   global fileName
   print("Save File mode")
   if not files:
      if cmds.textFieldGrp('name', exists = True):
         cmds.deleteUI('name')
      name = cmds.textFieldGrp('name', label = 'File Name', editable=True)
      fileName = name + "v_001"
   else:
      stringList = currentValue.split("_")
      versionArray = [int(i) for i in stringList[-1].split('v') if i.isdigit()]
      if len(versionArray) != 0:
         versionNo = versionArray[0]+1
         stringList.pop(-1)
         updateNo = '_v' + f'{versionNo:03d}'
         updateVersion = '_'.join(stringList) + updateNo
      else:
         updateVersion = currentValue + '_v001'
      if cmds.textFieldGrp(fileName, exists = True):
         cmds.deleteUI(fileName)
      fileName = cmds.textFieldGrp(label = 'File Name', editable=True, text=updateVersion)


# Publish window methods
def checkfileFromWIP(currentValue):
   global fileName
   global filePath
   fileName = currentValue
   dest = joinPath(folderPath, currentValue)
   if(os.path.isfile(dest)):
      filePath = dest
      cmds.text("Chosen File path: " + dest)
      cmds.button('Publish',enable = True)
   else:
      cmds.text("Warning: file cannot be find in the saving directory")
      cmds.button('Publish',enable = False)

def updateVersion():
   os.remove(filePath)
   stringList = fileName.split("_")
   versionArray = [int(i) for i in stringList[-1].split('v') if i.isdigit()]
   if len(versionArray) != 0:
      versionNo = versionArray[0]+1
      stringList.pop(-1)
      updateNo = '_v' + f'{versionNo:03d}'
      updateVersion = '_'.join(stringList) + updateNo
   else:
      updateVersion = fileName + '_v001'
   customPath = joinPath(folderPath, updateVersion) 
   cmds.file(rename = customPath)
   cmds.file(s=True,f=True, typ= "mayaBinary")

def cacheFormated(text):
   cacheFolder = joinPath(folderPath, 'cache')
   if(os.path.isdir(cacheFolder) == False):
      os.mkdir(cacheFolder)
   customPth = joinPath(cacheFolder, fileName)
   cmds.file(rename = customPth)
   cmds.file(s=True,f=True, typ= text)


# General functions
def createOptionMenu(name):
   if cmds.optionMenu(name, exists = True):
         cmds.deleteUI(name)
   if (saveMode == True):
      cmds.optionMenu(name, label= name, changeCommand=nameFile )
   if (publishMode == True):
      cmds.optionMenu(name, label= name, changeCommand=checkfileFromWIP) 
   if not files:
      cmds.menuItem(label = '')
   else:
      cmds.menuItem(label = '')
      for i in files:
         cmds.menuItem( label= i )

def joinPath(file, newElement):
   newPath = pathlib.PurePath(file, newElement)
   return newPath

def confirm():
    global prefixPath
    prefixPath = cmds.textFieldGrp(path, q =True, text = True)
    print(prefixPath)


# UI Functions
# Option menu commands
def openCharater():
   global folderPath
   global files
   assetPath = joinPath(folderPath,"Asset")
   folderPath = joinPath(assetPath,"Character")
   if(os.path.isdir(assetPath)):
      if(os.path.isdir(folderPath)):
         files = os.listdir(folderPath)
      else:
         os.mkdir(folderPath)
   else:
      os.mkdir(assetPath)
      os.mkdir(folderPath)
   createOptionMenu('Character')

def openProp():
   global folderPath
   global files
   assetPath = joinPath(folderPath, "Asset")
   folderPath = joinPath(assetPath, "Prop")
   if(os.path.isdir(assetPath)):
      if(os.path.isdir(folderPath)):
         files = os.listdir(folderPath)
      else:
         os.mkdir(folderPath)
   else:
      os.mkdir(assetPath)
      os.mkdir(folderPath)
   createOptionMenu('Prop')

def openSet():
   global folderPath
   global files
   assetPath = joinPath(folderPath, "Asset")
   folderPath = joinPath(assetPath, "Set")
   if(os.path.isdir(assetPath)):
      if(os.path.isdir(folderPath) == False):
         os.mkdir(folderPath)
      else:
         files = os.listdir(folderPath)
   else:
      os.mkdir(assetPath)
      os.mkdir(folderPath)
   createOptionMenu('Set')

def openSetPiece():
   global folderPath
   global files
   assetPath = joinPath(folderPath, "Asset")
   folderPath = joinPath(assetPath, "SetPiece")
   if(os.path.isdir(assetPath)):
      if(os.path.isdir(folderPath) == False):
         os.mkdir(folderPath)
      else:
         files = os.listdir(folderPath)
   else:
      os.mkdir(assetPath)
      os.mkdir(folderPath)
   createOptionMenu('SetPiece')

def openSequence():
   global folderPath
   global files
   folderPath = joinPath(folderPath,"Sequence")
   if(os.path.isdir(folderPath) == False):
      os.mkdir(folderPath)
      files = os.listdir(folderPath)
   createOptionMenu('Sequence')   


# Button commands
def saveFile():
   global folderPath
   global fileName
   global saveMode
   customPth = joinPath(folderPath, fileName) 
   cmds.file(rename = customPth)
   cmds.file(s=True,f=True, typ= "mayaBinary")
   folderPath = ''
   fileName = ''
   saveMode = False
   cmds.deleteUI('save_window')

def publishFile():
   if filePath.contains('/'):
      paths = filePath.split('/')
      paths = list(map(lambda x: x.replace('wip', 'publish'), paths))
      dest = '/'.join(paths)
   elif filePath.contains('\\'):
      paths = filePath.split('\\')
      paths = list(map(lambda x: x.replace('wip', 'publish'), paths))
      dest = '\\'.join(paths)

def saveWindowCancel():
   print("test")

def publishWindowCancel():
   print("test")

# Windows
def save_window():
   global saveMode
   global folderPath
   saveMode = True
   folderPath = joinPath(prefixPath, "wip")
   if(os.path.isdir(folderPath) == False):
      os.mkdir(folderPath)
   if cmds.window('save_publish_init', exists = True):
      cmds.deleteUI('save_publish_init')
   if cmds.window('save_window', exists = True):
      cmds.deleteUI('save_window')
   cmds.window('save_window', resizeToFitChildren=True)

   cmds.scrollLayout()

   cmds.separator(h=10)
   cmds.text('Asset')
   cmds.separator(h=10)

   cmds.button( label='Character', command='openCharater()')
   cmds.button( label='Prop', command='openProp()')
   cmds.button( label='Set', command='openSet()')
   cmds.button( label='SetPiece', command='openSetPiece()')

   cmds.separator(h=10)
   cmds.text('Sequence')
   cmds.separator(h=10)

   cmds.button( label='Sequence', command='openSequence()')

   cmds.separator(h=30)

   cmds.button( label='Save', command='saveFile()')

   
   cmds.showWindow('save_window')


def publish_window():
   global folderPath
   global publishMode
   publishMode = True
   folderPath = joinPath(prefixPath, "wip")
   destPath = joinPath(prefixPath, "publish")
   if(os.path.isdir(destPath) == False):
      os.mkdir(destPath)
   if cmds.window('save_publish_init', exists = True):
      cmds.deleteUI('save_publish_init')
   cmds.window('publish_window', resizeToFitChildren=True)
   cmds.scrollLayout()
   
   cmds.button('Publish', label='Character', enable = False)#, command='openCharater()')

   cmds.showWindow('publish_window')


def save_publish_init():
   if cmds.window('save_publish_init', exists = True):
      cmds.deleteUI('save_publish_init')
   cmds.window('save_publish_init', resizeToFitChildren=True)
   cmds.scrollLayout()

   global path
   path = cmds.textFieldGrp(label = 'Folder Path:', text=path,editable=True)
   cmds.button(label = 'Confirm', command = 'confirm()')
   cmds.button(label = 'Save', command = 'save_window()')
   cmds.button(label = 'Publish', command = 'publish_window()')

   cmds.showWindow('save_publish_init')

save_publish_init()
