import maya.cmds as cmds
import json
import pathlib
import os

#-------------------------------------------------------------------------------------------------Surfacing-----------------------------------------------------------------------------------------
# Publish materials
def PublishMaterial():
    objects = list(filter(lambda object: not('_grp' in object), cmds.listRelatives(cmds.ls(o = True), ad= True, typ = 'transform')))
    JsonFile = {}
    for object in objects:
        material = GetMaterialFromObject(object)
        if (material):
            cmds.select(material, add = True)
        JsonFile.update ({object : material})
    Path = GetPublishPath(GenerateShaderName())
    if (Path):
        cmds.file(Path ,op = "v=0",typ="mayaBinary",pr=True,es=True)
        with open(Path+'.json', 'w') as outfile:
            json.dump(JsonFile, outfile, indent = 4)
        print ('Success! published into: \n'+ Path)
    else:
        print ('Not in WIP')
    #update latestVersionTextBox using MaterialFindlatestVer();

def GetMaterialFromObject(target):
    shape = cmds.listRelatives ( target, shapes=True )
    shadingEngine = cmds.listConnections (shape, source=False, destination=True)
    materials = cmds.ls(cmds.listConnections(shadingEngine ), materials = True)
    if (materials[0] != 'initialShadingGroup'):
        return materials[0]
    return None

def GenerateShaderName():
    AllParts = pathlib.PurePath(cmds.file(q=True, sn=True)).parts
    Name = AllParts[AllParts.index('surfacing')-1]
    return Name + "_shaders_v" + str(GetlatestVerInPath(GetCurrentPath())).zfill(3) 

def GetCurrentPath():
    path  =  pathlib.PurePath(cmds.file(q=True, sn=True))
    return os.path.join(*path.parts [:-1])


def GetlatestVerInPath(path):
    filesInPath = [f for f in os.listdir(path) if os.path.join(path, f)[-3:] == '.mb']
    currentVersion = 0;
    for fil in filesInPath:
        ver = int(fil[-6:-3])
        if ver > currentVersion:
           currentVersion  = ver
    return currentVersion

def GetPublishPath(Name):
    AllParts = pathlib.PurePath(cmds.file(q=True, sn=True)).parts
    if not 'wip' in AllParts:
        return None
    else:
        Path = AllParts[:AllParts.index('surfacing')+1]
        print (os.path.join(*Path))
        Path = Path[:AllParts.index('wip')]+('publish',)+Path[AllParts.index('wip')+1:] #this is big brain as hell, wow
        if not os.path.exists(os.path.join(*Path+('textures',))):
            os.makedirs(os.path.join(*Path+('textures',)))
        return (os.path.join(*Path + ('textures',Name)))



#-------------------------------------------------------------------------------------------------lighting-----------------------------------------------------------------------------------------


def setMaterial(object, material):
    cmds.select(object, r = True )
    cmds.sets(e=True, forceElement = material);
# load all  material


#HUD AND UI


# Additional feature

# individual loading of material based on version

