from functools import partial
from genericpath import exists
import maya.cmds as cmds
import os
from enum import Enum
import json
import glob
import pathlib

# SceneTypes are used to distinguished between types of scenes and can be easily replaced by strings
class SceneType(Enum):
    Layout = 1
    Animation = 2
    Lighting = 3

# Setting up globals to be called between functions
currentFilePath = ''
folders = []

setRef = ''
layoutRef = ''
charRigRef = ''
charAnimCacheRef = ''

# Main function for building an empty scene.
def sceneBuilder(*args):
    # Start by finding where the current scene lives in the project structure
    getCurrentScene()
    # Find the sceneType by the name of the file to determine functionality
    sceneToBuild = setSceneType()
    # Layout and Animation need to choose character(s) to add before building the scene, while Lighting immediately builds
    if sceneToBuild == SceneType.Layout:
        addCharactersWindow(sceneToBuild)
    elif sceneToBuild == SceneType.Animation:
        addCharactersWindow(sceneToBuild)
    elif sceneToBuild == SceneType.Lighting:
        buildScene(sceneToBuild)
        
# Main function for updating references.
def update(*args):
    # Start by finding where the current scene lives in the project structure
    getCurrentScene()
    # Find the sceneType by the name of the file to determine functionality
    sceneToBuild = setSceneType()
    # Find the refernces currently in the scene
    getCurrentReferences()
    # Launch window to choose updated references.
    updateSceneReferences(sceneToBuild)

# Pass a SceneType of the type that you want to build
def buildScene(sceneToBuild, *args):
    # These globals should be empty and be overwritten/assigned in this function
    global setRef
    global layoutRef
    global charRigRef
    global charAnimCacheRef
    
    # A Layout scene needs to load character rigs and a set
    if sceneToBuild == SceneType.Layout:
        # Special handling, looping for rigs since there can be multiple characters in a scene
        for ele in args:
            # Get the list of all rig version filepaths: ['path/to/charName_rig.v001.mb', 'path/to/charName_rig.v002.mb']
            charRigsList = getCharacterRigs(ele)
            # Get the last element in the list - the latest version
            charRigRef = charRigsList[len(charRigsList)-1]
            # Get only the name of the file: _ = 'path/to/', charRigNamespace = 'rig.v002.mb'
            _, charRigNamespace = os.path.split(charRigRef)
            # Check that string for the filepath isn't empty before loading it
            if charRigRef:
                # Load the file as a reference with a namespace of the same as its name: namespace = charName_rig.v002
                cmds.file(charRigRef, reference=True, namespace=str(charRigNamespace).replace('.mb', ''))
        # Get the list of all set version filepaths. See 'Layout/rigs' section above
        setsList = getSets()
        # Get the last element in the list - the latest version
        setRef = setsList[len(setsList)-1]
        # Get only the name of the file
        _, setNamespace = os.path.split(setRef)
        # Check that string for the filepath isn't empty before loading it
        if setRef:
            # Load the file as a reference with a namespace of the same as its name
            cmds.file(setRef, reference=True, gr=True, namespace=str(setNamespace).replace('.mb', ''))

    # An animation scene needs to load character rigs, a set and a layout (camera). See the above 'Layout' section for a description
    elif sceneToBuild == SceneType.Animation:
        for ele in args:
            charRigsList = getCharacterRigs(ele)
            charRigRef = charRigsList[len(charRigsList)-1]
            _, charRigNamespace = os.path.split(charRigRef)
            if charRigRef:
                cmds.file(charRigRef, reference=True, namespace=str(charRigNamespace).replace('.mb', ''))
        
        setsList = getSets()
        setRef = setsList[len(setsList)-1]
        _, setNamespace = os.path.split(setRef)
        if setRef:
            cmds.file(setRef, reference=True, gr=True, namespace=str(setNamespace).replace('.mb', ''))

        layoutsList = getLayouts()
        layoutRef = layoutsList[len(layoutRef)-1]
        _, layoutNamespace = os.path.split(layoutRef)
        if layoutRef:
            cmds.file(layoutRef, reference=True, namespace=str(layoutNamespace).replace('.abc', ''))

    # A lighting scene needs to load a set, layout (camera) and character animation cache. See the above Layout section for a description
    elif sceneToBuild == SceneType.Lighting:
        setsList = getSets()
        setRef = setsList[len(setsList)-1]
        _, setNamespace = os.path.split(setRef)
        if setRef:
            cmds.file(setRef, reference=True, gr=True, namespace=str(setNamespace).replace('.mb', ''))

        layoutsList = getLayouts()
        layoutRef = layoutsList[len(setsList)-1]
        _, layoutNamespace = os.path.split(layoutRef)
        if layoutRef:
            cmds.file(layoutRef, reference=True, namespace=str(layoutNamespace).replace('.abc', ''))

        animationCachesList = getAnimationCaches()
        charAnimCacheRef = animationCachesList[len(setsList)-1]
        _, charAnimNamespace = os.path.split(charAnimCacheRef)
        if charAnimCacheRef:
            charAnimCacheRef = cmds.file(charAnimCacheRef, reference=True, gr=True, namespace=str(charAnimNamespace).replace('abc', ''))

# Find where the working file lives in the project structure
def getCurrentScene():
    # Edit the global variable so that other functions can use it.
    global currentFilePath
    # Query the sceneName for the full filepath of the opened scene
    currentFilePath = cmds.file(q=True, sceneName=True)
    # Normalize the path so that it is safe to use. Maya commands always use and return forwards slashes '/'.
    currentFilePath = os.path.normpath(currentFilePath)

# Set the SceneType to determine functionality for other functions
def setSceneType():
    global currentFilePath
    global folders
    
    sceneToBuild = ''
    # Split the path into each folder by the separator
    folders = currentFilePath.split(os.sep)
    # Throw an error if folders returns empty
    if not folders:
        cmds.error('File is unsaved for saved in the incorrect location.')
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
        cmds.error('Builder cannot build for scene: ' + folders[-2] + '. Please check that the file is saved in the correct place and refer to the documentation.')
    
    return sceneToBuild

# Get the list of all versions of a set. This function uses the name of the current file to determine which set to retrieve.
def getSets():
    global currentFilePath
    setsList = []

    # Get only the name of the file from the full filepath: tail = 'seqName_shotName_SceneType.v???.mb
    _, tail = os.path.split(currentFilePath)
    # The name of the sequence should always be the first 3 characters like in the json file: 'lng' or 'cnr'
    shortSequenceName = tail[:3]

    # Open the sequences.json file to determine the fullname of the sequence
    f = open(str(pathlib.PurePath(cmds.workspace(q=1,rd=1), 'scripts/sceneBuilderTool/sequences.json')), 'r')
    data = json.loads(f.read())
    # 'lng' = 'loungeRoom'
    fullSequenceName = data[shortSequenceName]

    # Create a path to the sets folder based on the retrieved name of the file.
    setsFolder = pathlib.PurePath(cmds.workspace(q=1,rd=1), 'scenes/publish/assets/set/', fullSequenceName, 'model/*.mb')
    # Get a list of all the mayaBinary (.mb) files in that folder.
    setsList = glob.glob(str(setsFolder))
    # Throw an error if the folder is empty.
    if len(setsList) == 0:
        cmds.error('No sets found in folder: '+ str(setsFolder))
    else:
        return setsList

# Get the list of all versions of a layout. This is different to getSets() because it doesn't need the json file.
def getLayouts():
    global currentFilePath
    layoutsList = []

    # Get the path to the current file relative to the project root: 'scenes/wip/sequence/lng01/lng01_010/SceneType/currentFile.mb'
    relativeCurrentFilePath = os.path.normpath((cmds.workspace(projectPath=currentFilePath)))
    # Split the filepath into a list of folders: [scenes, wip, sequence, ..., currentFile.mb]
    folders = relativeCurrentFilePath.split(os.sep)
    # Find where in the list is the wip and change it to publish
    indexOfWip = folders.index('wip')
    folders[indexOfWip] = 'publish'

    # edit the folders to get retrieve the correct folder
    folders.pop() # popping 'seqName_shotNum_light.v???.mb'
    folders.pop() # popping 'light'
    folders.append('layout')
    folders.append('cache')
    folders.append('alembic')

    # Reconstruct the filepath from the list.
    layoutsFolder = pathlib.PurePath(cmds.workspace(q=1,rd=1), *folders, '*.abc')
    # Get a list of all the caches in the folder 
    layoutsList = glob.glob(str(layoutsFolder))
    # Throw an error if the folder is empty
    if len(layoutsList) == 0:
        cmds.error('No layouts found in folder: '+ str(layoutsFolder))
        return
    else:
        return layoutsList

# Get the list of all cache versions of an animation. See getLayouts() for an explanation
def getAnimationCaches():
    global currentFilePath
    animationsList = []

    relativeCurrentFilePath = os.path.normpath((cmds.workspace(projectPath=currentFilePath)))
    folders = relativeCurrentFilePath.split(os.sep)
    indexOfWip = folders.index('wip')
    folders[indexOfWip] = 'publish'

    folders.pop()
    folders.pop()
    folders.append('animation')
    folders.append('cache')
    folders.append('alembic')

    animationFolder = pathlib.PurePath(cmds.workspace(q=1,rd=1), *folders, '*.abc')
    animationsList = glob.glob(str(animationFolder))
    if len(animationsList) == 0:
        cmds.error('No animations found in folder: '+ str(animationFolder))
        return
    else:
        return animationsList

# Return a list of all versions of an rig of the characterName parameter. Same as getSets() but change the json access with the characterName
def getCharacterRigs(characterName):
    global currentFilePath
    rigsList = []

    _, tail = os.path.split(currentFilePath)

    rigsFolder = pathlib.PurePath(cmds.workspace(q=1,rd=1), 'scenes/publish/assets/character/', characterName, 'rig/*.mb')
    rigsList = glob.glob(str(rigsFolder))
    if len(rigsList) == 0:
        cmds.error('No rigs found in folder: '+ str(rigsFolder))
        return
    else:
        return rigsList

# Get the list of all cache versions of an animation. See getLayouts() for an explanation
def getCharacterNames():
    global currentFilePath
    charactersList = []

    _, tail = os.path.split(currentFilePath)

    charactersFolder = pathlib.PurePath(cmds.workspace(q=1,rd=1), 'scenes/publish/assets/character/*')
    charactersList = glob.glob(str(charactersFolder))
    if len(charactersList) == 0:
        cmds.error('No characters found in folder: '+ str(charactersFolder))
        return
    else:
        return charactersList

# Called in update() on Layout and Animation scenes to determine which character(s) to add.
def addCharactersWindow(sceneToBuild):
    # Edit this to change the name of the window
    windowName = 'AddCharacters'
    windowLayoutName = 'addCharacterWindowLayout'
    if cmds.window(windowName, exists=True):
        cmds.deleteUI(windowName)
    cmds.window(windowName, resizeToFitChildren = 1)
    cmds.rowColumnLayout(windowLayoutName, nc=2)
    
    # Both buttons call the same confirmBuild() function, but with overloads.
    cmds.button(label='Build', command = partial(confirmBuild, windowName, True, sceneToBuild, windowLayoutName))
    cmds.button(label='Cancel', command = partial(confirmBuild, windowName, False))
    
    # Get the list of characterNames
    characterNames = getCharacterNames()

    # Add buttons to allow for adding more characters to the scene.
    button = cmds.button(label='+')
    cmds.button(button, edit=True, command=partial(onPlusButton, button, characterNames))

    cmds.showWindow(windowName)

# Deletes the UI. If true, query the optionMenus and call buildScene()
def confirmBuild(windowName, confirmed, sceneToBuild, layoutName, *args):
    # If 'Build' button was pressed
    if confirmed:
        # Get the layout of the window to access the optionsMenus
        layoutChildren = cmds.layout(layoutName, q=True, childArray=True)
        menuNames = []
        # Iterate through all children of the layout and extract the optionMenus handles.
        for child in layoutChildren:
            if 'optionMenu' in child:
                menuNames.append(child)
        characterNames = []
        # Iterate through the optionsMenus and get the value attached to them which is the characterName to add.
        for menuName in menuNames:
            characterNames.append(cmds.optionMenu(menuName, q=True, value=True))

        # Call buildScene() with those characterNames
        buildScene(sceneToBuild, *characterNames)
    # Delete the UI after. Will be called on 'Cancel' button too/
    cmds.deleteUI(windowName)

# Functionality for the plus button. Adds optionMenu, plus button and minus button.
def onPlusButton(button, characterNames, *args):
    # Delete the previous plus button -- the one that called this.
    cmds.deleteUI(button, control=True)

    # Create an optionsMenu
    optionMenu = cmds.optionMenu(label = 'Character: ')
    cmds.optionMenu(optionMenu, edit=True, changeCommand=updateMenu)
    # First option is '-' to indicate that that an option hasn't been selected yet.
    cmds.menuItem(label = '-')
    # Iterate through the characterNames and create a menuItem with the filename only (not full filepath)
    for file in characterNames:
        cmds.menuItem(label = os.path.split(file)[1])

    # Add remove button
    removeButton = cmds.button(label='-')
    cmds.button(removeButton, edit=True, command=partial(removeOption, optionMenu, removeButton))

    # Add another plus button
    addButton = cmds.button(label='+')
    cmds.button(addButton, edit=True, command = partial(onPlusButton, addButton, characterNames))

# Delete the button and the option menu it is associated with so it can't be queried later.
def removeOption(option, button, *args):
    cmds.deleteUI(option, control=True)
    cmds.deleteUI(button, control=True)

# Throws a warning if the user tries to select '-' as an option to load.
def updateMenu(menuItem, *args):
    if menuItem == '-':
        cmds.warning('Do not select \"-\" as an option. If you do not want to add another character, click the subtract button.')

# Get the references already in the scene. These should only be the ones that the scipt can build otherwise it won't update properly.
def getCurrentReferences():
    # Get a list of all references in the scene
    references = cmds.ls(rf=True)
    rootRefNodes = []
    # Extract only the nodes in the root scene -- without the ':'
    for node in references:
        if ':' not in node:
            rootRefNodes.append(node)
    # Iterate through the nodes and assign them to the global variables
    for node in rootRefNodes:
        # Get the file that the reference node is attached to and get the name only, not the full filepath
        _, filename = os.path.split(cmds.referenceQuery(node, filename=True))
        # If the filename has the keywords in the name, then assign them appropriately
        if 'model' in node:
            global setRef
            setRef = filename
        elif 'layout' in node:
            global layoutRef
            layoutRef = filename
        elif 'rig' in node:
            global charRigRef
            charRigRef = filename
        elif 'anim' in node:
            global charAnimCacheRef
            charAnimCacheRef = filename

# Update window to select which file to replace the current reference.
def updateSceneReferences(sceneToBuild, *args):
    windowName = 'UpdateScene'
    windowLayoutName = 'updateSceneLayout'
    if cmds.window(windowName, exists=True):
        cmds.deleteUI(windowName)
    cmds.window(windowName, resizeToFitChildren=True)

    cmds.columnLayout(windowLayoutName)

    cmds.separator(h=10)

    # Get the list of the versions and make an optionMenu of them.
    # All SceneTypes have a set
    setsList = getSets()
    cmds.text('Current Set: ' + setRef)
    cmds.optionMenu(label = 'New Set: ', changeCommand=updateMenu)
    cmds.menuItem(label='-')
    for file in setsList:
        cmds.menuItem(label = os.path.split(file)[1])
    cmds.separator(h=10)

    # Only Layout and Animation scenes have a rig to update
    if sceneToBuild == SceneType.Layout or sceneToBuild == SceneType.Animation:
        global charRigRef
        print(charRigRef)
        characterName = charRigRef[:charRigRef.index('_')-2]
        rigsList = getCharacterRigs(characterName)
        cmds.text('Current Rig: ' + charRigRef)
        cmds.optionMenu(label = 'New Rig: ', changeCommand=updateMenu)
        cmds.menuItem(label='-')
        for file in rigsList:
            cmds.menuItem(label = os.path.split(file)[1])
        cmds.separator(h=10)

    # Only Animation and Lighting scenes have a layout to update
    if sceneToBuild == SceneType.Animation or sceneToBuild == SceneType.Lighting:
        layoutsList = getLayouts()
        cmds.text('Current Layout: ' + layoutRef)
        cmds.optionMenu(label = 'New Layout: ', changeCommand=updateMenu)
        cmds.menuItem(label='-')
        for file in layoutsList:
            cmds.menuItem(label = os.path.split(file)[1])
        cmds.separator(h=10)

    # Only Lighting scenes have an animationCache to update
    if sceneToBuild == SceneType.Lighting:
        animationCachesList = getAnimationCaches()
        cmds.text('Current Animation: ' + charAnimCacheRef)
        cmds.optionMenu(label = 'New Animation: ', changeCommand=updateMenu)
        cmds.menuItem(label='-')
        for file in animationCachesList:
            cmds.menuItem(label = os.path.split(file)[1])
        cmds.separator(h=10)

    cmds.separator(h=10)
    
    cmds.button(label = 'Update References', command=partial(updateReferences, sceneToBuild, windowName, windowLayoutName))

    cmds.showWindow(windowName)

# Update the references by quering the options menu.
def updateReferences(sceneToBuild, windowName, layoutName, *args):
    layoutChildren = cmds.layout(layoutName, q=True, childArray=True)
    menuNames = []
    for child in layoutChildren:
        if 'optionMenu' in child:
            menuNames.append(child)
    newSet = ''
    newLayout = ''
    newRig = ''
    newAnim = ''
    for menuName in menuNames:
        fileToLoad = cmds.optionMenu(menuName, q=True, value=True)
        if 'model' in fileToLoad:
            newSet = fileToLoad
        elif 'layout' in fileToLoad:
            newLayout = fileToLoad
        elif 'rig' in fileToLoad:
            newRig = fileToLoad
        elif 'anim' in fileToLoad:
            newAnim = fileToLoad
    
    # Always update Set
    global setRef
    setRefNode = cmds.file(setRef, q=True, referenceNode=True)
    setsList = getSets()
    for filepath in setsList:
        if filepath.endswith(newSet):
            newSet = filepath
            break
    if newSet:
        cmds.file(newSet, loadReference = setRefNode)
        print('Updated '+setRefNode+' to reference '+newSet)

    # Only update Rig if scene is Layout or Animation
    if sceneToBuild == SceneType.Layout or sceneToBuild == SceneType.Animation:
        global charRigRef
        rigRefNode = cmds.file(charRigRef, q=True, referenceNode=True)
        characterName = charRigRef[:charRigRef.index('_')-2]
        rigsList = getCharacterRigs(characterName)
        for filepath in rigsList:
            if filepath.endswith(newRig):
                newRig = filepath
                break
        if newRig:
            cmds.file(newRig, loadReference = rigRefNode)
            print('Updated '+rigRefNode+' to reference '+newRig)

    # Only update Layout if scene is Animation or Lighting
    if sceneToBuild == SceneType.Animation or sceneToBuild == SceneType.Lighting:
        global layoutRef
        layoutRefNode = cmds.file(layoutRef, q=True, referenceNode=True)
        layoutsList = getLayouts()
        for filepath in layoutsList:
            if filepath.endswith(newLayout):
                newLayout = filepath
                break
        if newLayout:
            cmds.file(newLayout, loadReference = layoutRefNode)
            print('Updated '+layoutRefNode+' to reference '+newLayout)

    # Only update Lighting if scene is Lighting
    if sceneToBuild == SceneType.Lighting:
        global charAnimCacheRef
        animRefNode = cmds.file(charAnimCacheRef, q=True, referenceNode=True)
        animCachesList = getAnimationCaches()
        for filepath in animCachesList:
            if filepath.endswith(newAnim):
                newAnim = filepath
                break
        if newAnim:
            cmds.file(newAnim, loadReference = animRefNode)
            print('Updated '+animRefNode+' to reference '+newAnim)

    cmds.deleteUI(windowName)

# Function won't be called if imported. In which case, call sceneBuilder() to build a scene and update() to update references
if __name__ == '__main__':
    # Create window on launch to select whether to build a scene or update references.
    # Edit this to change the name of the window
    windowName = 'SceneBuilderTool'
    if cmds.window(windowName, exists=True):
        cmds.deleteUI(windowName)
    cmds.window(windowName, resizeToFitChildren=True)
    cmds.columnLayout()
    cmds.separator(h=10)

    cmds.button(label = 'Build Scene', command=sceneBuilder)
    cmds.separator(h=10)

    cmds.button(label='Update References', command=update)

    cmds.showWindow(windowName)