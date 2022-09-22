import maya.cmds as cmds
import os
from enum import Enum

class SceneType(Enum):
    Layout = 1
    Animation = 2
    Lighting = 3

currentFilePath = ''
sceneToBuild = ''

def sceneBuilder():
    if cmds.window('sceneBuilder', exists=True):
        cmds.deleteUI('sceneBuilder')

    cmds.window('sceneBuilder', resizeToFitChildren=True)

    cmds.columnLayout()

    cmds.separator(h=10)
    cmds.text('Select current file')
    cmds.separator(h=10)

    cmds.button(label='Open File', command='selectCurrentFile()')

    cmds.separator(h=10)
    global currentFilePath
    cmds.text('The current file is: ' + currentFilePath)
    cmds.separator(h=10)
    
    # -----------TO-DO-------------
    # make invisible until select file throws an error
    # -----------------------------
    cmds.separator(h=10)
    cmds.text('Error, the selected file is not compatible.')
    cmds.separator(h=10)

    cmds.button(label='Check for Updates', command='checkForUpdates()')

    cmds.separator(h=10)
    cmds.text('Set: ')
    # add dropdown menu to select version
    # hide this until new version is found with checkForUpdates()
    cmds.button(label='Update', command='updateAsset()')
    cmds.separator(h=10)
    
    # -----------TO-DO-------------
    # gray out when no changes made
    # -----------------------------
    cmds.button(label='Load', command='buildScene()')

    cmds.showWindow('sceneBuilder')

def selectCurrentFile():
    print('selectCurrentFile')
    print(currentFilePath)

def checkForUpdates():
    print('checkForUpdates')

def updateAsset():
    print('updateAsset')

def buildScene():
    print('buildScene')

def getCurrentScene():
    global currentFilePath
    currentFilePath = cmds.file(q=True, sn=True)
    print(currentFilePath)
    setSceneType()

def setSceneType():
    global currentFilePath
    global sceneToBuild
    # normalise the path so that os.sep is safe to use
    path = os.path.normpath(currentFilePath)
    # split the path into each folder
    folders = path.split(os.sep)
    # folders = ['C:', 'path', 'to', 'file.txt']
    # get the second last element, which is the folder the file lives in = 'layout/animation/lighting'
    parentFolder = folders[-2]
    if parentFolder == 'layout':
        sceneToBuild = SceneType.Layout
    elif parentFolder == 'animation':
        sceneToBuild = SceneType.Animation
    elif parentFolder == 'lightning':
        sceneToBuild = SceneType.Lighting
    else:
        print('Builder cannot build for scene: ' + folders[-2])
    
getCurrentScene()
sceneBuilder()