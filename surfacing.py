import maya.cmds as cmds
import json
import pathlib
import os

#-------------------------------------------------------------------------------------------------Surfacing-----------------------------------------------------------------------------------------
# Publish materials
def PublishMaterial():
    if ('wip' in cmds.file(q=True, sn=True)):
        JsonFile = {}
        materialsTMP = {}
        
        SaveNewVersion()
        
        MaterialPath = GetPublishPath(GenerateName('shader', GetlatestVerInPath(GetCurrentPath())), 'material')
        SourcePath = GetPublishPath(GenerateName('surfacing', GetlatestVerInPath(GetCurrentPath())), 'source')
        newVer = cmds.file(q=True, sn=True)
        
        objects = list(filter(lambda object: not('_grp' in object), cmds.listRelatives(cmds.ls(o = True), ad= True, typ = 'transform')))
        for object in objects:
            material = GetMaterialFromObject(object)
            if (material):
                cmds.select(material, add = True)
                modif = (GetName()+'_'+material)
                cmds.rename (material, modif )
                materialsTMP.update({material : modif})
                JsonFile.update ({object : modif})
        cmds.file(MaterialPath ,op = "v=0",typ="mayaBinary",pr=True,es=True) #publish only material
        for mat in materialsTMP:
            cmds.rename (materialsTMP[mat],mat )
            
        SaveAs(SourcePath) #publish the surfacing file
        cmds.file( newVer, o=True ) #return back to WIP
        with open(MaterialPath+'.json', 'w') as outfile: #publich Json File
            json.dump(JsonFile, outfile, indent = 4)   
            
        print ('Success! published into: \n'+ MaterialPath)
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

def GenerateName(sub,ver):
    Name = GetName()
    return Name + "_"+sub+".v" + str(ver).zfill(3) 

def GetName():
    AllParts = pathlib.PurePath(cmds.file(q=True, sn=True)).parts
    return AllParts[AllParts.index('surfacing')-1]

def GetCurrentPath():
    return os.path.join(*pathlib.PurePath(cmds.file(q=True, sn=True)).parts[:-1])

def GetCurrentName():
    return os.path.join(*pathlib.PurePath(cmds.file(q=True, sn=True)).parts[-1:])

def SaveNewVersion():
    name = cmds.file(q=True, sn=True)
    SaveAs(name[:-4]+str(GetlatestVerInPath(GetCurrentPath())+1)+name[-3:])
    return name[:-4]+str(GetlatestVerInPath(GetCurrentPath()))+name[-3:]
    
def SaveAs(path):
    cmds.file(rename = path)
    cmds.file(save = True, type ='mayaBinary')

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

def GetPublishPath(Name, sub):
    AllParts = pathlib.PurePath(cmds.file(q=True, sn=True)).parts
    if not 'wip' in AllParts:
        return None
    else:
        Path = AllParts[:AllParts.index('surfacing')+1]
        #print (os.path.join(*Path))
        Path = Path[:AllParts.index('wip')]+('publish',)+Path[AllParts.index('wip')+1:] #replace wip to publish
        if not os.path.exists(os.path.join(*Path+(sub,))):
            os.makedirs(os.path.join(*Path+(sub,)))
        return (os.path.join(*Path + (sub,Name)))


PublishMaterial()

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
    
#LoadAllMaterial()

#GetContentFromJson(r"C:\Users\janse\OneDrive\Documents\maya\projects\Assessment2_GroupX\scenes\publish\assets\prop\truck04\surfacing\textures\truck04_shaders_v002.json")
#tmp = getSurfacingPath(cmds.ls(sl = True))
#print (cmds.ls(sl = True))
#print (tmp)
#print(tmp +' contain '+str(os.listdir(tmp)) + " latest ver in directory " + str(GetlatestVerInPath(tmp)))
#-------------------------------------------------------------------------------------------------HUD AND UI-----------------------------------------------------------------------------------------
    


#-------------------------------------------------------------------------------------------------Additional feature-----------------------------------------------------------------------------------------

#individual loading of material based on version

