import maya.cmds as cmds

def sceneBuilder() :
    if cmds.window('sceneBuilder', exists=1):
        cmds.deleteUI('sceneBuilder')

    cmds.window('sceneBuilder', resizeToFitChildren=1)

    cmds.columnLayout()

    cmds.separator(h=10)
    cmds.text('Select current file')
    cmds.separator(h=10)

    cmds.button(label='Open File', command='selectCurrentFile()')

    cmds.separator(h=10)
    cmds.text('The current file is: ')
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

def checkForUpdates():
    print('checkForUpdates')

def updateAsset():
    print('updateAsset')

def buildScene():
    print('buildScene')

sceneBuilder()