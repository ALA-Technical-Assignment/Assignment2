import maya.cmds as cmds
import json
import pathlib
import os

#-------------------------------------------------------------------------------------------------Surfacing-----------------------------------------------------------------------------------------
# Publish materials
def PublishMaterial():
    if ('surfacing' in cmds.file(q=True, sn=True)):
        cmds.select(clear = True) #deselect all
        RefVer = cmds.referenceQuery(cmds.ls(referencedNodes = True)[0] ,filename=True)
        JsonFile = {RefVer : {}}
        #add version number the model is based on
        materialsTMP = {}
        
        SaveNewVersion()
        
        MaterialPath = GetPublishPath(GenerateName('shader', GetlatestVerInPath(GetCurrentPath())), 'material')
        SourcePath = GetPublishPath(GenerateName('surfacing', GetlatestVerInPath(GetCurrentPath())), 'source')
        newVer = cmds.file(q=True, sn=True)
        
        objects = list(filter(lambda object: not('_grp' in object), cmds.listRelatives(cmds.ls(o = True), ad= True, typ = 'transform')))
        for object in objects:
            material = GetMaterialFromObject('*' + object)
            if (material):
                cmds.select(material, add = True)
                if not (material) in materialsTMP.values():
                    modif = (GetName()+'_'+material)
                    cmds.rename (material, modif)
                    materialsTMP.update({material : modif})
                JsonFile[RefVer].update({object [object.index('_')+1:]: modif})
        #publish material
        cmds.file(MaterialPath ,op = "v=0",typ="mayaBinary",pr=True,es=True) 
        for mat in materialsTMP:
            cmds.rename (materialsTMP[mat],mat )
        #publish the source file(i.e. surfacing)
        SaveAs(SourcePath)
        cmds.file( newVer, o=True ) #return back to WIP
        #publich Json File
        with open(MaterialPath+'.json', 'w') as outfile:
            json.dump(JsonFile, outfile, indent = 4)     
        print ('Success! published into: \n'+ MaterialPath)
    else:
        print ('Not in Surfacing')
    #update latestVersionTextBox using MaterialFindlatestVer();


def GetMaterialFromObject(target):
    
    shape = cmds.listRelatives ( target, shapes=True )
    
    shadingEngine = cmds.listConnections (shape, source=False, destination=True)
    materials = cmds.ls(cmds.listConnections(shadingEngine ), materials = True)
    #print (materials)
    if (materials[0] != 'initialShadingGroup'):
        return materials[0]
    return None

def GenerateName(sub,ver):
    Name = GetName()
    return Name + "_"+sub+".v" + str(ver).zfill(3) 


def GetName(path = cmds.file(q=True, sn=True)):
    AllParts = pathlib.PurePath(path).parts
    if ('surfacing' in AllParts):
        return AllParts[AllParts.index('surfacing')-1]
    elif ('model' in AllParts):
        return AllParts[AllParts.index('model')-1]
    else:
        return None

def GetCurrentPath():
    return os.path.join(*pathlib.PurePath(cmds.file(q=True, sn=True)).parts[:-1])

def GetCurrentName():
    return os.path.join(*pathlib.PurePath(cmds.file(q=True, sn=True)).parts[-1:])

def SaveNewVersion():
    name = cmds.file(q=True, sn=True)
    SaveAs(name[:-6]+str(GetlatestVerInPath(GetCurrentPath())+1).zfill(3)+name[-3:])
    return cmds.file(q=True, sn=True)
    
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




#PublishMaterial()
#cmds.select()
#cmds.rename ('couch01_leather_mat','leather_mat')
#print (GetMaterialFromObject('*|' + 'mRef_blocks01'))
#cmds.select(GetMaterialFromObject('*|' + 'mRef_blocks01'))
#-------------------------------------------------------------------------------------------------lighting-----------------------------------------------------------------------------------------


#To Do
    #write failsafe in code

# load all  material
def LoadAllMaterials():
        objects = cmds.ls(v = True, typ = 'transform', dag =True, leaf= False, referencedNodes = True)
        #print (objects)
        SurfacingPaths = {}
        for object in objects:
            path = getShaderPath(object)
            if (path != None):
                if not cmds.listRelatives ( object, shapes=True ): #if it's the head of the ref
                    LoadMaterial(object,path)
                    
def ManualLoadMaterial():
    selectedObject = cmds.ls(sl = True)[0]
    startingPath = getShaderPath(selectedObject)
    if startingPath == None and cmds.referenceQuery(selectedObject , inr = True):
        startingPath = pathlib.PurePath(cmds.referenceQuery(selectedObject ,filename=True)).parts
        startingPath = os.path.join(*startingPath[:startingPath.index('model')] + ('surfacing',))
    elif startingPath == None:
        startingPath = cmds.file(q=True, sn=True)
    path  = os.path.join(*cmds.fileDialog2(dir = startingPath, ff = '*.mb', dialogStyle=2, fm = 1))
    LoadMaterial(selectedObject, path)
    print ('manually loading...')
                                     

def LoadMaterial(object, path):
    print (path)
    RefChilds = cmds.listRelatives (object, c = True)
    cmds.file(path,i=True) #import the material
    Json = (GetContentFromJson(path[:-3] +'.json'))
    ##add catch when json is not found
    if Json[0] == cmds.referenceQuery(object ,filename=True):
        for RefChild in RefChilds:
            if '_' in RefChild:
                name  = RefChild [RefChild.index('_')+1:]
            elif ':' in RefChild:
                name  = RefChild [RefChild.index(':')+1:]
            for JsonName in Json[1]:
                if JsonName[0] == name:
                    SetMaterial(object+'|'+str(RefChild), JsonName[1])
                    #cmds.select(object+'|'+str(RefChild),add =True)
                    #cmds.select(JsonName[1], add = True)
                    #print (object+'|'+str(RefChild) + ' == '+  JsonName[1])
        print(object + ' Loaded')
    else:
        print('Incompatible Model Reference, please load a shader manually')
    
def SetMaterial(object, material):
    cmds.select(object)
    cmds.hyperShade(a = material)
    #cmds.sets(e=True, forceElement = material +'SG')
        
def getShaderPath(object):
    Reference = pathlib.PurePath(cmds.referenceQuery(object ,filename=True)).parts
    if ('model' in Reference):
        Reference = Reference [:Reference.index('model')] + ('surfacing', 'material')
        tmpPath = os.path.join(*Reference)
        if os.path.exists(tmpPath) and (len(os.listdir(tmpPath)) > 0):
            Reference  = Reference + (GetFileInPathWithVer( tmpPath,GetlatestVerInPath(tmpPath)),) 
            return os.path.join(*Reference)
        else:
            return None      
    else:
        return None   

def GetContentFromJson(Path):
    with open(Path, 'r') as f:
          JsonTmp = json.load(f)
    tmp = list(list(JsonTmp.items())[0])
    listr  = list(tmp[1].items())
    ModelVer = tmp[0]
    #for JsonName in listr:
    #    print(listr[JsonName])
            #SetMaterial(object+'|'+str(RefChild), JsonName[1])
    return(ModelVer,listr)
    
#LoadAllMaterial()
#GetContentFromJson(r"C:\Users\janse\OneDrive\Documents\maya\projects\Assessment2_GroupX\scenes\publish\assets\prop\truck04\surfacing\textures\truck04_shaders_v002.json")
#tmp = getSurfacingPath(cmds.ls(sl = True))
#print (cmds.ls(sl = True))
#print (tmp)
#print(tmp +' contain '+str(os.listdir(tmp)) + " latest ver in directory " + str(GetlatestVerInPath(tmp)))
#-------------------------------------------------------------------------------------------------HUD AND UI-----------------------------------------------------------------------------------------
    
def MainWindow():
    if cmds.window('ShaderPublishing', exists = True):
        cmds.deleteUI('ShaderPublishing')
    cmds.window('ShaderPublishing', resizeToFitChildren=True, width=(200))
    cmds.columnLayout( adjustableColumn=True )
    cmds.text(label='-----------------Surfacing Scene-----------------')
    cmds.button(label = 'Publish And Save Shader', command = 'PublishMaterial()')
    cmds.text(label='------------------Lighting Scene------------------')
    #cmds.text(label='Will try to get the latest shader, which is not necessarily linked to the object on the scene')
    cmds.button(label = 'Load All latest material', command = 'LoadAllMaterials()')
    cmds.button(label = 'Manually load material of selected', command = 'ManualLoadMaterial()')
    cmds.showWindow('ShaderPublishing')


MainWindow()
#-------------------------------------------------------------------------------------------------Additional feature-----------------------------------------------------------------------------------------

#individual loading of material based on version

