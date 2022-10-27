import maya.cmds as cmds
import json
import pathlib
import os

#-------------------------------------------------------------------------------------------------Surfacing-----------------------------------------------------------------------------------------
# Publish materials
def PublishMaterial():
    if ('surfacing' in cmds.file(q=True, sn=True) and 'wip' in cmds.file(q=True, sn=True)): #only triggers when in a surfacing scene
        cmds.select(clear = True) #deselect all
        RefVer = cmds.referenceQuery(cmds.ls(referencedNodes = True)[0] ,filename=True) #the model reference
        JsonFile = {RefVer : {}}  #stored to check compability of shader and object in scene
        materialsTMP = {}  #temporary for renaming materials 
        #whenever a shader is published, a new version of the object is also saved
        SaveNewVersion() 
        MaterialPath = GetPublishPath(GenerateName('shader', GetlatestVerInPath(GetCurrentPath())), 'material')#path for the material (i.e. shader) in publishing
        SourcePath = GetPublishPath(GenerateName('surfacing', GetlatestVerInPath(GetCurrentPath())), 'source')#path for the source (i.e. surfacing scene) in publishing
        newVer = cmds.file(q=True, sn=True)#path for self
        #scan through all objects in scene (ignoring group)
        objects = list(filter(lambda object: not('_grp' in object), cmds.listRelatives(cmds.ls(o = True), ad= True, typ = 'transform')))
        for object in objects:
            material = GetMaterialFromObject('*' + object) #get material
            if (material):
                cmds.select(material, add = True)
                if not (material) in materialsTMP.values():#get the reference mainnode (i.e. the 'head')
                    modif = (GetName()+'_'+material) 
                    cmds.rename (material, modif)#modify the stored name to distint materials between references 
                    materialsTMP.update({material : modif}) #store it temporarily
                JsonFile[RefVer].update({object [object.index('_')+1:]: modif})
        #publishing 
        cmds.file(MaterialPath ,op = "v=0",typ="mayaBinary",pr=True,es=True) #publish material
        for mat in materialsTMP: #rename it all back to original name
            cmds.rename (materialsTMP[mat],mat)
        SaveAs(SourcePath)#publish the source file(i.e. surfacing)
        cmds.file( newVer, o=True ) #return back to WIP
        with open(MaterialPath+'.json', 'w') as outfile:#publish Json File
            json.dump(JsonFile, outfile, indent = 4)     
        print ('Success! published into: \n'+ MaterialPath)
    else:
        cmds.warning ('Either Not in Surfacing or not in WIP')


def GetMaterialFromObject(target): #helper method to get material from Object
    shape = cmds.listRelatives ( target, shapes=True )
    shadingEngine = cmds.listConnections (shape, source=False, destination=True)
    materials = cmds.ls(cmds.listConnections(shadingEngine ), materials = True)
    if (materials[0] != 'initialShadingGroup'):
        return materials[0]
    return None

def GenerateName(sub,ver):#Generate a name of a file, combination of 'Name + Subcategory + Version'
    return GetName() + "_"+sub+".v" + str(ver).zfill(3) 


def GetName(path = cmds.file(q=True, sn=True)):#Get the Name, generated by finding its subfolder in the directory
    AllParts = pathlib.PurePath(path).parts
    if ('surfacing' in AllParts):
        return AllParts[AllParts.index('surfacing')-1]
    elif ('model' in AllParts):
        return AllParts[AllParts.index('model')-1]
    else:
        return None

def GetCurrentPath():#get current path without the file itself (i.e. just the folders)
    return os.path.join(*pathlib.PurePath(cmds.file(q=True, sn=True)).parts[:-1])

def SaveNewVersion():#save a new version of current (in WIP)
    name = cmds.file(q=True, sn=True)
    SaveAs(name[:-6]+str(GetlatestVerInPath(GetCurrentPath())+1).zfill(3)+name[-3:])
    return cmds.file(q=True, sn=True)
    
def SaveAs(path):#save current into
    cmds.file(rename = path)
    cmds.file(save = True, type ='mayaBinary')

def GetlatestVerInPath(path):#self explain
    filesInPath = [f for f in os.listdir(path) if os.path.join(path, f)[-3:] == '.mb']
    currentVersion = 0
    for fil in filesInPath:
        ver = int(fil[-6:-3])
        if ver > currentVersion:
           currentVersion  = ver
    return currentVersion

def GetFileInPathWithVer(path, ver): #self explain
    for fileInPath in os.listdir(path):
        if str(ver).zfill(3)+'.mb' in fileInPath:
            return fileInPath     

def GetPublishPath(Name, sub): #create publishing path from the file name (generated by other method) and the subdirectory it'll be going
    AllParts = pathlib.PurePath(cmds.file(q=True, sn=True)).parts
    if not 'wip' in AllParts:
        return None
    else:
        Path = AllParts[:AllParts.index('surfacing')+1]
        Path = Path[:AllParts.index('wip')]+('publish',)+Path[AllParts.index('wip')+1:] #replace wip to publish
        if not os.path.exists(os.path.join(*Path+(sub,))):#if the path doesn't exist yet, create it
            os.makedirs(os.path.join(*Path+(sub,)))
        return (os.path.join(*Path + (sub,Name)))

#-------------------------------------------------------------------------------------------------lighting-----------------------------------------------------------------------------------------


#load all  material for all reference in scene 
def LoadAllMaterials():
        objects = cmds.ls(v = True, typ = 'transform', dag =True, leaf= False, referencedNodes = True)
        for object in objects:#scan through all reference nodes
            path = GetShaderPath(object)
            if (path != None):
                if not cmds.listRelatives ( object, shapes=True ): #if it's the head of the ref
                    LoadMaterial(object,path)#load it from there
            else:
                cmds.warning(object + ' doesn\'t have a published material')

#load specific material for a psecific object                 
def ManualLoadMaterial():
    selectedObject = cmds.ls(sl = True)[0]
    if cmds.listRelatives ( selectedObject, shapes=True ): #if it's not the head reference node, 
        selectedObject = '|' + str(cmds.listRelatives(selectedObject, p =True)[0])#it's functionally a fail safe so if either the head reference node or the leaf is selected it would work
    #determine where the starting point of the filebrowser is, not important 
    startingPath = GetShaderPath(selectedObject)
    if startingPath == None and cmds.referenceQuery(selectedObject , inr = True):
        startingPath = pathlib.PurePath(cmds.referenceQuery(selectedObject ,filename=True)).parts
        startingPath = os.path.join(*startingPath[:startingPath.index('model')] + ('surfacing',))
    elif startingPath == None:
        startingPath = cmds.file(q=True, sn=True)
    #file dialogue
    path  = os.path.join(*cmds.fileDialog2(dir = startingPath, ff = '*.mb', dialogStyle=2, fm = 1))
    print ('manually loading...')
    LoadMaterial(selectedObject, path)
    
                                     
#load the material
def LoadMaterial(object, path):
    RefChilds = cmds.listRelatives (object, c = True) #the refernce child (i.e. the leafs)
    Json = (GetContentFromJson(path[:-3] +'.json'))
    if Json:  #incase Json doesn't exist
        if Json[0] == cmds.referenceQuery(object ,filename=True): #object ref compatibility check
            for JsonName in Json[1]: #delete the materials already existing in the scene before importing the new ones
                if (cmds.ls(JsonName[1])):
                    cmds.select(JsonName[1])
                    cmds.delete()
            cmds.file(path,i=True) #import the material
            for RefChild in RefChilds:#iterate through all the child of reference
                if '_' in RefChild: 
                    name  = RefChild [RefChild.index('_')+1:]
                elif ':' in RefChild: #same purpose above, essentially split the chidl name into the prefix and actual name in refernce, split can either happen in ':' or '_'
                    name  = RefChild [RefChild.index(':')+1:]
                for JsonName in Json[1]:#find the equivalent object and connected material in the companian Json
                    if JsonName[0] == name:
                        SetMaterial(object+'|'+str(RefChild), JsonName[1])
            print(object + ' Loaded')
        else:
            cmds.warning('Problem with "'+object+'"\nIncompatible Model Reference, please load a shader manually')
    else:
        cmds.warning('Companian Json doesn\'t exist, can\'t continue')
    
def SetMaterial(object, material):
    print (object + material)
    cmds.select(object)
    cmds.hyperShade(a = material) #hypershade is suprisingly realiable 
        
def GetShaderPath(object): #get the shader path of the object
    Reference = pathlib.PurePath(cmds.referenceQuery(object ,filename=True)).parts #get the object reference path
    if ('model' in Reference):
        Reference = Reference [:Reference.index('model')] + ('surfacing', 'material')#change into the surfacing directory
        tmpPath = os.path.join(*Reference)
        if os.path.exists(tmpPath) and (len(os.listdir(tmpPath)) > 0):#fail safe it the path doesn't exist
            Reference  = Reference + (GetFileInPathWithVer( tmpPath,GetlatestVerInPath(tmpPath)),) 
            return os.path.join(*Reference)
        else:
            return None      
    else:
        return None   

def GetContentFromJson(Path):#self explain
    with open(Path, 'r') as f:
        try:
            JsonTmp = json.load(f)
        except:
            return None
    tmp = list(list(JsonTmp.items())[0])
    listr  = list(tmp[1].items())
    ModelVer = tmp[0]
    return(ModelVer,listr)#return the path of object ref for compability check and 
    
#-------------------------------------------------------------------------------------------------HUD AND UI-----------------------------------------------------------------------------------------
currentSelectedVersion = None
    
def MainWindow():
    if cmds.window('ShaderPublishing', exists = True):
        cmds.deleteUI('ShaderPublishing')
    cmds.window('ShaderPublishing', resizeToFitChildren=True)
    cmds.columnLayout( adjustableColumn=True )
    cmds.text(label='-----------------Surfacing Scene-----------------')
    cmds.button(label = 'Publish and Save Shader', command = 'PublishMaterial()')
    cmds.text(label='------------------Lighting Scene------------------')
    cmds.button(label = 'Load All Latest Material', command = 'LoadAllMaterials()')
    cmds.button(label = 'Manually Load Material of Selected', command = 'ManualLoadMaterial()')
    cmds.showWindow('ShaderPublishing')


MainWindow()

