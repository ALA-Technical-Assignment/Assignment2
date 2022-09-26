import maya.cmds as cmds
import json

#find material in object
def getMaterialFromObject(target):
    shadeEng = cmds.listConnections(target , type = "shadingEngine")
    materials = cmds.ls(mc.listConnections(shadeEng ), materials = True)
    return materials

#export selected material into Maya Binary
cmds.file("D:/Uni/TD/asd/s.mb",op = "v=0",typ="mayaBinary",pr=True,es=True)

#set material to object
cmds.sets(e=True, forceElement="standardSurface1SG");

#create and write to json
with  open('D:/Uni/TD/new_file.json','w') as f:
    json.dump('Will be inside json',f)