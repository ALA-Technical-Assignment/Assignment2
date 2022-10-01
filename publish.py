import maya.cmds as cmds
import os
import pathlib

path = r"{}".format(cmds.file(q=True, sceneName=True))
prefixPath = ''
folderPath = ''
files = []
fileName = ''

# Methods to execute
def nameFile(currentValue):
   global fileName
   if not files:
      name = cmds.textFieldGrp(label = 'File Name', editable=True)
      fileName = name + "v_001"
   else:
      stringList = currentValue.split("_")
      versionArray = [int(i) for i in stringList[-1].split() if i.isdigit()]
      versionNo = versionArray[0]
      stringList.pop(-1)
      updateNo = '_' + f'{versionNo:03d}'
      updateVersion = '_'.join(stringList) + updateNo
      fileName = cmds.textFieldGrp(label = 'File Name', editable=True, text=updateVersion)

def createOptionMenu(name):
   cmds.optionMenu( label= name, changeCommand=nameFile )
   if not files:
      cmds.menuItem(label = '')
   else:
      cmds.menuItem(label = '')
      for i in files:
         cmds.menuItem( label= i )

def joinPath(filePath, newElement):
   newPath = pathlib.PurePath(filePath, newElement)
   return newPath

# UI Functions

def confirm():
    global prefixPath
    prefixPath = cmds.textFieldGrp(path, q =True, text = True)
    print(prefixPath)

def openCharater():
   global folderPath
   global files
   assetPath = joinPath(prefixPath,"Asset")
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
   assetPath = joinPath(prefixPath, "Asset")
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
   assetPath = joinPath(prefixPath, "Asset")
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
   assetPath = joinPath(prefixPath, "Asset")
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
   folderPath = joinPath(prefixPath,"Sequence")
   if(os.path.isdir(folderPath) == False):
      os.mkdir(folderPath)
      files = os.listdir(folderPath)
   createOptionMenu('Sequence')   

def saveFile():
   customPth = joinPath(folderPath, fileName) 
   cmds.file(rename = customPth)
   cmds.file(s=True,f=True, typ= "mayaBinary")

def publishFile():
   print("test")

def saveWindowCancel():
   print("test")

def publishWindowCancel():
   print("test")


def save_window():
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
   folderPath = joinPath(prefixPath, "publish")
   if(os.path.isdir(folderPath) == False):
      os.mkdir(folderPath)
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
   path = cmds.textFieldGrp(label = 'Folder Path:', text=path,editable=True)
   cmds.button(label = 'Confirm', command = 'confirm()')
   cmds.button(label = 'Save', command = 'save_window()')
   cmds.button(label = 'Publish', command = 'publish_window()')

   cmds.showWindow('save_publish_init')

save_publish_init()
