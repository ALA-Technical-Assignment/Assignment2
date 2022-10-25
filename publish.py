import maya.cmds as cmds
import os
import pathlib
from functools import partial

# Methods to execute
# Save window methods
def nameFile(currentValue):
   print("Save File mode")
   if cmds.textFieldGrp('fileName', exists = True):
      cmds.deleteUI('fileName')
   cmds.textFieldGrp('fileName', label = 'File Name', editable=True, text=versionUpdate(currentValue))

def nameFolder(currentValue):
   global folderPath
   global checkingFinalFolder
   checkingFinalFolder = True
   if (currentValue == ''):
      currentValue = 'NewDocument'
   if cmds.textFieldGrp('folderName', exists = True):
      cmds.deleteUI('folderName')
   cmds.textFieldGrp('folderName', label = 'Model Folder Name', editable=True, text=currentValue)


# Publish window methods
def checkfileFromWIP(currentValue):
   global folderPath
   global filePath
   global fileName
   if(os.path.exists(folderPath)):
      if('.mb' in currentValue):
         fileName = currentValue
         filePath = joinPath(folderPath, currentValue)
         cmds.text("Chosen Folder path: " + str(folderPath))
      else:
         folderPath = joinPath(folderPath, currentValue)
         cmds.text("Chosen File path: " + str(folderPath))
   else:
      cmds.text("Warning: file cannot be find in the saving directory")

def cacheFormated(destPath, folderName):
   cache = 'cache' + os.sep + folderName
   cacheFolder = joinPath(destPath, cache)
   pathlib.Path(cacheFolder).mkdir(parents=True, exist_ok=True)
   if(os.path.exists(cacheFolder) == False):
      os.mkdir(cacheFolder)
   customPth = joinPath(cacheFolder, fileName)
   if (folderName == 'fbx'):
      cmds.file(rename = customPth)
      cmds.file(s=True, f=True, type= "FBX export")
   if (folderName == 'abc'):
      start = 0
      end = 120
      command = "-frameRange " + str(start) + " " + str(end) + " -file " + str(customPth)
      cmds.AbcExport ( j = command )

def updateAfterPublish():
   os.remove(filePath)
   customPath = joinPath(folderPath, versionUpdate(fileName)) 
   cmds.file(rename = customPath)
   cmds.file(s=True,f=True, type= "mayaBinary")


# General functions
def can_convert_to_int(string):
    try:
        int(string)

        return True
    except ValueError:
        return False

def versionUpdate(currentValue):
   stringList = currentValue.split("_")
   stringList[-1] = stringList[-1].replace('.mb','')
   stringList = stringList[-1].split('.v')
   versionArray = [int(i) for i in stringList if can_convert_to_int(i)]
   if len(versionArray) != 0:
      versionNo = versionArray[0]+1
      stringList.pop(-1)
      updateNo = '.v' + f'{versionNo:03d}'
      updateVersion = '_'.join(stringList) + updateNo
   else:
      updateVersion = currentValue + '.v001'
   return updateVersion

def createOptionMenu(name, list):
   if cmds.optionMenu(name, exists = True):
         cmds.deleteUI(name)
   if (saveMode == True):
      if (checkingFinalFolder == True):
         cmds.optionMenu(name, label= name, changeCommand=nameFile)
      else:
         cmds.separator(h=10)
         cmds.text('Please choose model folder from option menu first before pressing buttons below')
         cmds.separator(h=10)
         cmds.optionMenu(name, label= name, changeCommand=nameFolder)
   if (publishMode == True):
      cmds.separator(h=10)
      cmds.text('Please choose model folder from option menu first before pressing buttons below')
      cmds.separator(h=10)
      cmds.optionMenu(name, label= name, changeCommand=checkfileFromWIP) 
   if not list:
      cmds.menuItem(label = '')
   else:
      cmds.menuItem(label = '')
      for i in list:
         cmds.menuItem( label= i )

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
   if (publishMode == True):
      cmds.button(label='Publish', command='publishFile()')

def joinPath(file, newElement):
   newPath = pathlib.PurePath(file, newElement)
   return newPath

# UI Functions
# Option menu commands
def confirm():
    global prefixPath
    prefixPath = cmds.textFieldGrp(path, q =True, text = True)

def openCharater():
   global folderPath
   global folders
   typeList = ['anim', 'model', 'rig', 'surfacing']
   folderPath = joinPath(prefixPath,"Asset/Character")
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
   folderPath = joinPath(prefixPath, "Asset/Prop")
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
   folderPath = joinPath(prefixPath, "Asset/Set")
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
   folderPath = joinPath(prefixPath, "Asset/SetPiece")
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
   folderPath = joinPath(prefixPath,"Sequence")
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
   cmds.separator(h = 10)
   cmds.text("Path Selected")
   path = cmds.textFieldGrp('Prefix', label = 'Folder Path:', text=path,editable=True)
   

# Button commands
def saveFile():
   fileName = cmds.textFieldGrp('fileName', q=True, text = True)
   customPth = joinPath(folderPath, fileName) 
   cmds.file(rename = customPth)
   cmds.file(s=True,f=True, type= "mayaBinary")
   cmds.deleteUI('save_window')
   save_publish_init()

def publishFile():
   length = len(str(prefixPath).split(os.sep))-1
   dest = str(filePath).split(os.sep)
   dest[dest.index("wip",length)] = 'publish'
   dest = os.sep.join(dest)
   dest = pathlib.Path(dest)
   pathlib.Path(dest).mkdir(parents=True, exist_ok=True)
   fbx = cmds.checkBox('FBX', query=True, value=True)
   abc = cmds.checkBox('Alembic', query=True, value=True)
   if (fbx):
      cacheFormated(dest, 'fbx')
   if (abc):
      cacheFormated(dest, 'abc')
   customPth = joinPath(dest, fileName) 
   cmds.file(rename = customPth)
   cmds.file(s=True,f=True, type= "mayaBinary")
   updateAfterPublish()
   cmds.deleteUI('publish_window')
   save_publish_init()

def saveWindowCancel():
   if cmds.window('save_window', exists = True):
      cmds.deleteUI('save_window')
   save_publish_init()

def publishWindowCancel():
   if cmds.window('publish_window', exists = True):
      cmds.deleteUI('publish_window')
   save_publish_init()
   

def exitButton():
   if cmds.window('save_publish_init', exists = True):
      cmds.deleteUI('save_publish_init')

# Windows
def save_window():
   global saveMode
   global prefixPath
   saveMode = True
   prefixPath = joinPath(prefixPath, "wip")
   if(os.path.exists(prefixPath) == False):
      os.mkdir(prefixPath)
   if cmds.window('save_publish_init', exists = True):
      cmds.deleteUI('save_publish_init')
   if cmds.window('save_window', exists = True, ):
      cmds.deleteUI('save_window')
   cmds.window('save_window', resizeToFitChildren=True, t= 'Save Windows')
   cmds.columnLayout( adjustableColumn=True )

   cmds.separator(h=10)
   cmds.text(label = 'Asset', fn = 'boldLabelFont')
   cmds.separator(h=10)

   cmds.button( label='Character', command='openCharater()')
   cmds.button( label='Prop', command='openProp()')
   cmds.button( label='Set', command='openSet()')
   cmds.button( label='SetPiece', command='openSetPiece()')

   cmds.separator(h=10)
   cmds.text(label = 'Sequence', fn = 'boldLabelFont')
   cmds.separator(h=10)

   cmds.button( label='Sequence', command='openSequence()')

   cmds.separator(h=30)

   cmds.button( label='Save', command='saveFile()')
   cmds.button( label='Cancel', command='saveWindowCancel()')

   cmds.separator(h=20)
   
   cmds.showWindow('save_window')


def publish_window():
   global prefixPath
   global publishMode
   publishMode = True
   prefixPath = joinPath(prefixPath, "wip")
   if cmds.window('save_publish_init', exists = True):
      cmds.deleteUI('save_publish_init')
   if cmds.window('publish_window', exists = True):
      cmds.deleteUI('publish_window')
   destPath = joinPath(prefixPath, "publish")
   if(os.path.exists(destPath) == False):
      os.mkdir(destPath)
   cmds.window('publish_window', resizeToFitChildren=True, t= 'Publish Windows')
   cmds.columnLayout( adjustableColumn=True )

   cmds.separator(h=10)
   cmds.text(label = 'Asset', fn = 'boldLabelFont')
   cmds.separator(h=10)

   cmds.button( label='Character', command='openCharater()')
   cmds.button( label='Prop', command='openProp()')
   cmds.button( label='Set', command='openSet()')
   cmds.button( label='SetPiece', command='openSetPiece()')

   cmds.separator(h=10)
   cmds.text(label = 'Sequence', fn = 'boldLabelFont')
   cmds.separator(h=10)

   cmds.button( label='Sequence', command='openSequence()')

   cmds.separator(h=30)
   cmds.text(label = 'Format', fn = 'boldLabelFont')
   cmds.separator(h=10)

   cmds.checkBox("FBX", l="Fbx Format")
   cmds.checkBox("Alembic", l="Alembic Format")

   cmds.separator(h=10)

   cmds.button( label='Cancel', command='publishWindowCancel()')

   cmds.separator(h=20)

   cmds.showWindow('publish_window')


def save_publish_init():
   global path
   global prefixPath
   global folderPath
   global filePath
   global fileName
   global files
   global folders
   global saveMode
   global checkingFinalFolder
   global publishMode
   path = ''
   prefixPath = ''
   folderPath = ''
   filePath = ''
   fileName = ''
   files = []
   folders = []
   saveMode = False
   checkingFinalFolder = False
   publishMode = False
   
   if cmds.window('save_publish_init', exists = True):
      cmds.deleteUI('save_publish_init')
   cmds.window('save_publish_init', resizeToFitChildren=True, t= 'Start Up Windows')
   cmds.columnLayout( adjustableColumn=True )

   cmds.separator(h=30)
   cmds.text(label = 'Set Folder', fn = 'boldLabelFont')
   cmds.separator(h=10)

   cmds.button(label = 'Select Folder', command = 'select()')
   cmds.button(label = 'Confirm', command = 'confirm()')

   cmds.separator(h=10)
   cmds.text(label = 'Save and Publish Functions', fn = 'boldLabelFont')
   cmds.separator(h=10)

   cmds.button(label = 'Save', command = 'save_window()')
   cmds.button(label = 'Publish', command = 'publish_window()')

   cmds.separator(h=10)
   cmds.button(label = 'Exit', command = 'exitButton()')

   cmds.showWindow('save_publish_init')

save_publish_init()
