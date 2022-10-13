import maya.cmds as cmds
import os
import pathlib
from functools import partial

path = ''
prefixPath = ''
folderPath = ''
filePath = ''
fileName = ''
modelName = ''
files = []
folders = []
saveMode = False
checkingFinalFolder = False
publishMode = False

# Methods to execute
# Save window methods
def nameFile(currentValue):
   print("Save File mode")
   stringList = currentValue.split("_")
   versionArray = [int(i) for i in stringList[-1].split('v') if i.isdigit()]
   if len(versionArray) != 0:
      versionNo = versionArray[0]+1
      stringList.pop(-1)
      updateNo = '_v' + f'{versionNo:03d}'
      updateVersion = '_'.join(stringList) + updateNo
   else:
      updateVersion = currentValue + '_v001'
   if cmds.textFieldGrp('fileName', exists = True):
      cmds.deleteUI('fileName')
   cmds.textFieldGrp('fileName', label = 'File Name', editable=True, text=updateVersion)

def nameFolder(currentValue):
   global folderPath
   global checkingFinalFolder
   checkingFinalFolder = True
   if cmds.textFieldGrp('folderName', exists = True):
      cmds.deleteUI('folderName')
   cmds.textFieldGrp('folderName', label = 'Model Name', editable=True, text=currentValue)

def folderButton(typeName, *args):
   global folderPath
   global files
   if(saveMode == True):
      folder = cmds.textFieldGrp('folderName', q=True, text = True)
   else:
      folder = fileName
   modelFolder = joinPath(folderPath, folder)
   folderPath = joinPath(modelFolder, typeName)
   pathlib.Path(folderPath).mkdir(parents=True, exist_ok=True)
   files = os.listdir(folderPath)
   createOptionMenu('Model', files)


# Publish window methods
def checkfileFromWIP(currentValue):
   global modelName
   global filePath
   modelName = currentValue
   dest = joinPath(folderPath, currentValue)
   if(os.path.isfile(dest)):
      filePath = dest
      cmds.text("Chosen File path: " + str(dest))
      cmds.button(label='Publish', command='publishFile()')
   else:
      cmds.text("Warning: file cannot be find in the saving directory")

def updateVersion():
   os.remove(filePath)
   stringList = fileName.split("_")
   stringList[-1] = stringList[-1].replace('.mb','')
   versionArray = [int(i) for i in stringList[-1].split('v') if i.isdigit()]
   if len(versionArray) != 0:
      versionNo = versionArray[0]+1
      stringList.pop(-1)
      print(stringList)
      updateNo = '_v' + f'{versionNo:03d}'
      updateVersion = '_'.join(stringList) + updateNo
   else:
      updateVersion = fileName + '_v001'
   customPath = joinPath(folderPath, updateVersion) 
   cmds.file(rename = customPath)
   cmds.file(s=True,f=True, type= "mayaBinary")

def cacheFormated(destPath, formate, folderName):
   cache = 'cache' + os.sep + folderName
   cacheFolder = joinPath(destPath, cache)
   pathlib.Path(cacheFolder).mkdir(parents=True, exist_ok=True)
   if(os.path.isdir(cacheFolder) == False):
      os.mkdir(cacheFolder)
   customPth = joinPath(cacheFolder, fileName)
   cmds.file(rename = customPth)
   cmds.file(s=True,f=True, type= formate)


# General functions
def createOptionMenu(name, list):
   if cmds.optionMenu(name, exists = True):
         cmds.deleteUI(name)
   if (saveMode == True):
      if (checkingFinalFolder == True):
         cmds.optionMenu(name, label= name, changeCommand=nameFile)
      else:
         cmds.optionMenu(name, label= name, changeCommand=nameFolder)
   if (publishMode == True):
      cmds.optionMenu(name, label= name, changeCommand=checkfileFromWIP) 
   if not list:
      cmds.menuItem(label = '')
   else:
      cmds.menuItem(label = '')
      for i in list:
         cmds.menuItem( label= i )

def joinPath(file, newElement):
   newPath = pathlib.PurePath(file, newElement)
   return newPath


# UI Functions
# Option menu commands
def confirm():
    global prefixPath
    prefixPath = cmds.textFieldGrp(path, q =True, text = True)
    print(prefixPath)

def openCharater():
   global folderPath
   global folders
   typeList = ['anim', 'model', 'rig', 'surfacing']
   folderPath = joinPath(folderPath,"Asset/Character")
   pathlib.Path(folderPath).mkdir(parents=True, exist_ok=True)
   folders = os.listdir(folderPath)
   createOptionMenu('Character', folders)
   for text in typeList:
      name = 'Character ' + text
      cmds.button(label = name, command=partial(folderButton,text))

def openProp():
   global folderPath
   global folders
   typeList = ['model', 'rig', 'surfacing']
   folderPath = joinPath(folderPath, "Asset/Prop")
   pathlib.Path(folderPath).mkdir(parents=True, exist_ok=True)
   folders = os.listdir(folderPath)
   createOptionMenu('Prop', folders)
   for text in typeList:
      name = 'Prop ' + text
      cmds.button(label = name, command=partial(folderButton,text))

def openSet():
   global folderPath
   global folders
   typeList = ['model']
   folderPath = joinPath(folderPath, "Asset/Set")
   pathlib.Path(folderPath).mkdir(parents=True, exist_ok=True)
   folders = os.listdir(folderPath)
   createOptionMenu('Set', folders)
   for text in typeList:
      name = 'Set ' + text
      cmds.button(label = name, command=partial(folderButton,text))

def openSetPiece():
   global folderPath
   global folders
   typeList = ['model', 'surfacing']
   folderPath = joinPath(folderPath, "Asset/SetPiece")
   pathlib.Path(folderPath).mkdir(parents=True, exist_ok=True)
   folders = os.listdir(folderPath)
   createOptionMenu('SetPiece', folders)
   for text in typeList:
      name = 'Set Piece ' + text
      cmds.button(label = name, command=partial(folderButton,text))

def openSequence():
   global folderPath
   global folders
   typeList = ['animation', 'layout', 'light']
   folderPath = joinPath(folderPath,"Sequence")
   pathlib.Path(folderPath).mkdir(parents=True, exist_ok=True)
   folders = os.listdir(folderPath)
   createOptionMenu('Sequence', folders)
   for text in typeList:
      name = 'Sequence ' + text
      cmds.button(label = name, command=partial(folderButton,text))

def select():
   global path
   path = cmds.fileDialog2(fileMode=3)[0]
   if cmds.textFieldGrp('Prefix', exists = True):
      cmds.deleteUI('Prefix')
   path = cmds.textFieldGrp('Prefix', label = 'Folder Path:', text=path,editable=True)
   

# Button commands
def saveFile():
   global folderPath
   global fileName
   global saveMode
   global checkingFinalFolder
   fileName = cmds.textFieldGrp('fileName', q=True, text = True)
   customPth = joinPath(folderPath, fileName) 
   cmds.file(rename = customPth)
   cmds.file(s=True,f=True, type= "mayaBinary")
   folderPath = ''
   fileName = ''
   saveMode = False
   checkingFinalFolder = False
   cmds.deleteUI('save_window')
   # forward slash in save cmds

def publishFile():
   # os path split / os sep
   # check index of last wip
   global fileName
   global filePath
   global folderPath
   global publishMode
   length = len(str(prefixPath).split(os.sep))
   dest = str(filePath).split(os.sep)
   dest[dest.index("wip",length)] = 'publish'
   dest = os.sep.join(dest)
   dest = pathlib.Path(dest)
   pathlib.Path(dest).mkdir(parents=True, exist_ok=True)
   fbx = cmds.checkBox('FBX', query=True, value=True)
   abc = cmds.checkBox('Alembic', query=True, value=True)
   if (fbx == True):
      cacheFormated(dest, "FBX", "fbx")
   if (abc == True):
      cacheFormated(dest, "alembic", "abc")
   customPth = joinPath(dest, fileName) 
   cmds.file(rename = customPth)
   cmds.file(s=True,f=True, type= "mayaBinary")
   updateVersion()
   fileName = ''
   filePath = ''
   folderPath = ''
   publishMode = False
   cmds.deleteUI('publish_window')

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
   cmds.text('Format')
   cmds.separator(h=10)

   cmds.checkBox("FBX", l="Fbx Format")
   cmds.checkBox("Alembic", l="Alembic Format")

   cmds.separator(h=10)

   cmds.showWindow('publish_window')


def save_publish_init():
   if cmds.window('save_publish_init', exists = True):
      cmds.deleteUI('save_publish_init')
   cmds.window('save_publish_init', resizeToFitChildren=True)
   cmds.scrollLayout()

   global path
   cmds.button(label = 'Select File', command = 'select()')
   cmds.button(label = 'Confirm', command = 'confirm()')
   cmds.button(label = 'Save', command = 'save_window()')
   cmds.button(label = 'Publish', command = 'publish_window()')

   cmds.showWindow('save_publish_init')

save_publish_init()
