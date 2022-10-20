from functools import partial
import maya.cmds as cmds
import os
from enum import Enum
import json
import glob
import pathlib

class SceneType(Enum):
    Layout = 1
    Animation = 2
    Lighting = 3

currentFilePath = ''
sceneToBuild = ''
folders = []

setRef = 'No file selected'
layoutRef = 'No file selected'
charRigRef = 'No file selected'
propRigRef = 'No file selected'
charAnimCacheRef = 'No file selected'
propCacheRef = 'No file selected'

def sceneBuilder():
    if cmds.window('sceneBuilder', exists=True):
        cmds.deleteUI('sceneBuilder')

    cmds.window('sceneBuilder', resizeToFitChildren=True)

    cmds.columnLayout()

    # cmds.separator(h=10)
    # cmds.text('Select current file')
    # cmds.separator(h=10)

    cmds.separator(h=10)
    global currentFilePath
    cmds.text('The current file is: '+currentFilePath)
    cmds.separator(h=10)
    
    # -----------TO-DO-------------
    # make invisible until select file throws an error
    # -----------------------------
    # cmds.separator(h=10)
    # cmds.text('Error, the selected file is not compatible.')
    # cmds.separator(h=10)

    cmds.button(label='Check for Updates', command='checkForUpdates()')

    cmds.separator(h=10)
    global setRef
    cmds.text('setRefText', label='Set: '+setRef)
    cmds.button(label='Open', command='setSetReference()')
    # cmds.button('testButton', command='printFoo(setToRef)')

    # add dropdown menu to select version
    # hide this until new version is found with checkForUpdates()
    # cmds.button(label='Update', command='updateAsset()')
    cmds.separator(h=10)

    cmds.separator(h=10)
    global layoutRef
    cmds.text('layoutRefText', label='Layout: '+layoutRef)
    cmds.button(label='Open', command='setLayoutReference()')
    # add dropdown menu to select version
    # hide this until new version is found with checkForUpdates()
    # cmds.button(label='Update', command='updateAsset()')
    cmds.separator(h=10)

    cmds.separator(h=10)
    global charAnimCacheRef
    cmds.text('charAnimCacheRefText', label='Character Animation Cache: '+charAnimCacheRef)
    cmds.button(label='Open', command='setCharAnimCacheReference()')
    # add dropdown menu to select version
    # hide this until new version is found with checkForUpdates()
    # cmds.button(label='Update', command='updateAsset()')
    cmds.separator(h=10)
    
    # -----------TO-DO-------------
    # gray out when no changes made
    # -----------------------------
    cmds.button(label='Load', command='buildScene()')

    cmds.button('my_button', label='Debug', command='debugFunction()')

    cmds.showWindow('sceneBuilder')
    
def lightingSceneBuilder():
    if cmds.window('lightingSceneBuilder', exists=True):
        cmds.deleteUI('lightingSceneBuilder')

    cmds.window('lightingSceneBuilder', resizeToFitChildren=True)

    cmds.columnLayout()

    cmds.separator(h=10)

    setsList = getSets()
    cmds.optionMenu(label = 'Set: ', changeCommand=partial(setReferenceToAdd, setsList, 'Set'))
    cmds.menuItem(label=' ')
    for file in setsList:
        cmds.menuItem(label = os.path.split(file)[1])
    
    cmds.separator(h=10)

    layoutsList = getLayouts()
    cmds.optionMenu(label = 'Layout: ', changeCommand=partial(setReferenceToAdd, layoutsList, 'Layout'))
    cmds.menuItem(label=' ')
    for file in layoutsList:
        cmds.menuItem(label = os.path.split(file)[1])

    cmds.separator(h=10)

    animationCachesList = getAnimationCaches()
    cmds.optionMenu(label = 'Animation: ', changeCommand=partial(setReferenceToAdd, animationCachesList, 'Animation'))
    cmds.menuItem(label=' ')
    for file in animationCachesList:
        cmds.menuItem(label = os.path.split(file)[1])

    cmds.button(label = 'Build Scene', command = 'buildLightingScene()')

    cmds.showWindow('lightingSceneBuilder')

def checkForUpdates():
    print('checkForUpdates')

def updateAsset():
    print('updateAsset')

def buildScene():
    global setRef
    # cmds.file(setRef, reference=True)
    print(setRef)
    print('buildScene')

def getCurrentScene():
    global currentFilePath
    currentFilePath = cmds.file(q=True, sn=True)
    currentFilePath = os.path.normpath(currentFilePath)
    print('currentFilePath: ' + currentFilePath)
    setSceneType()

def setSceneType():
    global currentFilePath
    global sceneToBuild
    global folders
    # split the path into each folder
    folders = currentFilePath.split(os.sep)
    # folders = ['C:', 'path', 'to', 'file.txt']
    # get the second last element, which is the folder the file lives in = 'layout/animation/lighting'
    parentFolder = folders[-2]
    if parentFolder == 'layout':
        sceneToBuild = SceneType.Layout
    elif parentFolder == 'animation':
        sceneToBuild = SceneType.Animation
    elif parentFolder == 'light':
        sceneToBuild = SceneType.Lighting
    else:
        print('Builder cannot build for scene: ' + folders[-2])

# def setSetReference():
#     global currentFilePath
#     global setRef
#     dir = os.path.dirname(currentFilePath)
#     setRef = cmds.fileDialog2(dialogStyle=1, fileMode=1, dir=dir)[0]
#     cmds.text('setRefText', edit=True, label='Set: '+setRef)

def getSets():
    global currentFilePath

    _, tail = os.path.split(currentFilePath)
    shortSequenceName = tail[:3]

    f = open(str(pathlib.PurePath(cmds.workspace(q=1,rd=1), 'scripts/sequences.json')), 'r')

    data = json.loads(f.read())
    fullSequenceName = data[shortSequenceName]

    setsFolder = pathlib.PurePath(cmds.workspace(q=1,rd=1), 'scenes/publish/assets/set/', fullSequenceName, 'model/*.mb')
    setsList = glob.glob(str(setsFolder))
    if len(setsList) == 0:
        print('No layouts found in folder: ' + str(setsFolder))
        return
    else:
        return setsList
    
def getLayouts():
    global currentFilePath

    relativeCurrentFilePath = os.path.normpath((cmds.workspace(projectPath=currentFilePath)))
    folders = relativeCurrentFilePath.split(os.sep)
    indexOfWip = folders.index('wip')
    folders[indexOfWip] = 'publish'

    folders.pop() # popping 'seqName_shotNum_light.v???.mb'
    folders.pop() # popping 'light'
    folders.append('layout')
    folders.append('cache')
    folders.append('alembic')

    layoutsFolder = pathlib.PurePath(cmds.workspace(q=1,rd=1), *folders, '*.abc')
    layoutsList = glob.glob(str(layoutsFolder))
    if len(layoutsList) == 0:
        print('No layouts found in folder: ' + str(layoutsFolder))
        return
    else:
        return layoutsList

def getAnimationCaches():
    global currentFilePath

    relativeCurrentFilePath = os.path.normpath((cmds.workspace(projectPath=currentFilePath)))
    folders = relativeCurrentFilePath.split(os.sep)
    indexOfWip = folders.index('wip')
    folders[indexOfWip] = 'publish'

    folders.pop() # popping 'seqName_shotNum_light.v???.mb'
    folders.pop() # popping 'light'
    folders.append('animation')
    folders.append('cache')
    folders.append('alembic')

    animationFolder = pathlib.PurePath(cmds.workspace(q=1,rd=1), *folders, '*.abc')
    animationsList = glob.glob(str(animationFolder))
    if len(animationsList) == 0:
        print('No animations found in folder: ' + str(animationFolder))
        return
    else:
        return animationsList

def setReferenceToAdd(fileFolder, fileType, filename, *args):
    fileToRef = ''
    if filename == '':
        print('No Ref')

    for file in fileFolder:
        if file.endswith(filename):
            fileToRef = file
            break
    
    if fileType == 'Set':
        global setRef
        setRef = fileToRef
        print('Set: ' + setRef)
    elif fileType == 'Layout':
        global layoutRef
        layoutRef = fileToRef
        print('Layout: ' + layoutRef)
    elif fileType == 'Animation':
        global charAnimCacheRef
        charAnimCacheRef = fileToRef
        print('Animation: ' + charAnimCacheRef)

def buildLightingScene():
    global setRef
    global layoutRef
    global charAnimCacheRef

    cmds.group(name = 'animGroup', world=True, empty=True)

    # cmds.file('setReference', setRef, reference=True)
    # cmds.file(layoutRef, reference=True)
    animRef = cmds.file(charAnimCacheRef, reference=True)
    cmds.parent(animRef, 'animGroup')
    
    return

def debugFunction():
    global folders
    global currentFilePath
    
    workingPath = 'C:/Users/Shiva/Desktop/Uni/2022 Spring (Current)/41801 Technical Direction for 3D Animation and Graphics Projects/projects'

    assFolder = os.path.split(currentFilePath)[0]
    assFolder = os.path.normpath(assFolder).split(os.sep)
    
    # add or remove directories
    assFolder.append('Assignment2')

    assFolder = os.path.join(*assFolder)
    assFolder = os.path.splitdrive(assFolder)
    assFolder = assFolder[0] + os.sep + assFolder[1]
    assFolder = assFolder.replace('\\', '/')
    cmds.fileDialog2(dialogStyle=1, fileMode=1, dir=assFolder)

def printFoo():
    references = cmds.ls(rf=True)
    rootRefNodes = []
    for node in references:
        if ':' not in node:
            rootRefNodes.append(node)
    print(rootRefNodes)



getCurrentScene()
# sceneBuilder()
# lightingSceneBuilder()
printFoo()