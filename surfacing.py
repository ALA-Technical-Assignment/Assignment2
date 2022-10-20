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

def GetFileInPathWithVer(path, ver):
    for fileInPath in os.listdir(path):
        if str(ver).zfill(3)+'.mb' in fileInPath:
            return fileInPath     

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

#PublishMaterial()

#-------------------------------------------------------------------------------------------------lighting-----------------------------------------------------------------------------------------


#To Do
    #write failsafe in code

# load all  material
def LoadAllMaterial():
        objects = cmds.ls(v = True, typ = 'transform')
        SurfacingPaths = set()
        for object in objects:
            path = getShaderPath(object)
            #print (path)
            if (path != None):
                #print(pathlib.PurePath(cmds.referenceQuery(object ,filename=True)).parts)
                SurfacingPaths.add(path)
        for path in SurfacingPaths:
            print('imported from: \n' + path)
            cmds.file(path,i=True)
            accompanyingJson = path [:-3] +'.json'
            for object in GetContentFromJson(accompanyingJson):
                cmds.select (object[0])
            #ask french, why the inconcistency in the set? some are based according the reference, others are not?!
#scan through all the refernce object in the scene
    #go to its directory
    #find the surfacing subdirectory of it
    #import all the material from that surfacing directory
    #then open accompanying json file .
        #go through the list of object names and material
        #apply all material accordingly
        
def SetMaterial(object, material):
    cmds.select(object, r = True )
    cmds.sets(e=True, forceElement = material);
        
def getShaderPath(object):
    if cmds.referenceQuery (object, inr = True):
        Reference = pathlib.PurePath(cmds.referenceQuery(object ,filename=True)).parts
        if ('model' in Reference):
            
            Reference = Reference [:Reference.index('model')] + ('surfacing', 'textures')
            tmpPath = os.path.join(*Reference)
            if os.path.exists(tmpPath) and (len(os.listdir(tmpPath)) > 0):
                Reference  = Reference + (GetFileInPathWithVer( tmpPath,GetlatestVerInPath(tmpPath)),) 
                return os.path.join(*Reference)
            else:
                return None      
        else:
            return None   
    return None

def GetContentFromJson(Path):
    with open(Path, 'r') as f:
          JsonTmp = json.load(f)
    listr = list(JsonTmp.items())
    return(listr)
    
LoadAllMaterial()

#GetContentFromJson(r"C:\Users\janse\OneDrive\Documents\maya\projects\Assessment2_GroupX\scenes\publish\assets\prop\truck04\surfacing\textures\truck04_shaders_v002.json")
#tmp = getSurfacingPath(cmds.ls(sl = True))
#print (cmds.ls(sl = True))
#print (tmp)
#print(tmp +' contain '+str(os.listdir(tmp)) + " latest ver in directory " + str(GetlatestVerInPath(tmp)))
#-------------------------------------------------------------------------------------------------HUD AND UI-----------------------------------------------------------------------------------------
    


#-------------------------------------------------------------------------------------------------Additional feature-----------------------------------------------------------------------------------------

#individual loading of material based on version

