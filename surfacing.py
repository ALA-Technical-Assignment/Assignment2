import maya.cmds as cmds
import json

#find material in object
def getMaterialFromObject(target):
    shadeEng = cmds.listConnections(target , type = "shadingEngine")
    materials = cmds.ls(mc.listConnections(shadeEng ), materials = True)
    return materials

#export selected material into Maya Binary
#select all the material you want to export first
# then export it 
cmds.file("D:/Uni/TD/asd/s.mb",op = "v=0",typ="mayaBinary",pr=True,es=True)

#set material to object
cmds.sets(e=True, forceElement="standardSurface1SG");

#create and write to json
with  open('D:/Uni/TD/new_file.json','w') as f:
    json.dump('Will be inside json',f)


#var lastImported
#var latestVersionTextBox

#def MaterialExportAllfromObject():
    #deselect all
    #select all object in scene
    #create dictionary to store object name and corresponding material
    #for each object in scene
        #select its material (get the material, and then select it with tgl on)
        #write into the dictionary "objectName  = materialName "
    #var Name = MaterialGenerateName()
    #export as mb into correct folder with Name
    #convert dictionary into json and put in same folder as exported mb with correct name
    #show dialogue box where it's located and whether to show it in explorer

    #update latestVersionTextBox using MaterialFindlatestVer();

#def ExportMaterialFromObject(Objects)
    #create dictionary to store object name and corresponding material
    #for each Objects
        #select its material (get the material, and then select it with tgl on)
        #write into the dictionary "objectName  = materialName "
    #var Name = MaterialGenerateName()
    #export as mb into correct folder with Name
    #convert dictionary into json and put in same folder as exported mb with correct name
    #show dialogue box where it's located and whether to show it in explorer

#def MaterialImportAllLatestVersion():
    #for each 
    #importFrom("fileName_material_" + MaterialFindlatestVer())

#def MaterialImportSpecificVersion()
    # var returnedFile = show dialogue box to select file (filter, only mb, open material folder)
    #MaterialImport(returnedFile)

#def MaterialGenerateName():
    #get file and folder name
    #return fileName +"_material_" + MaterialFindlatestVer()

#def MaterialImport(file)
    #var succesfulImportMaterial
    #check if JSON exist 
        #show dialogue box if no json with MB
    #import mb
    #read json
    #for each line
        #get object in line
        #if found
            #assign materialName to objectName
            #succesfulImportMaterial ++
    #if succesfulImportMaterial==number of line in Json
        #dialogue box, Successful! all material exported
    #else
        #dialogue box, Not all material succesfully imported. (differnece) fail to import. Perhaps some object renamed and/or wrong version

#def MaterialFindlatestVer():
    #go to folder of material
    #var currentVersion = 0;
    #check all file in material folder
        #materialVar = some string manipulation to find ver
        #if materialVer > currentVersion;
            #currentVersion  = materialVer
    #return currentVersion

#def main():
    #latestVersionTextBox = textbox => Latest Material Version => MaterialFindlatestVer()

    #section material export "Surfacing"
    #button =>  Publish => MaterialExportAllfromObject()

    #section material Import "Lighting"
    #textbox => Last Imported => lastimported
    #button=> Import All published material into scene (latest) => MaterialImportAllLatestVersion()
    ####button=> Import Specific Version => MaterialImportSpecificVersion()

    

#main