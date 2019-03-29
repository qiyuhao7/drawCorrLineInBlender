"""
author:YuhaoQI
blender脚本用与两个模型对应Vertex之间连线
使用之前请把model1Idx.txt和model2Idx.txt存放在.blender工作目录之内
里面存放的是model1和model2的Vertex的Index,每行一个
请先依次选择两个模型之后执行此脚本
"""

import os
import bpy
import random
from operator import add
filepath = bpy.data.filepath
directory = os.path.dirname(filepath)
print(directory)


def get_index_from_file(filename, model_idx):
    f = open(model1_filename,'r')
    line = f.readline()
    while line:
        model_idx.append(int(line))
        line = f.readline()
    f.close()


def getLines(object1, object2, indices1, indices2):
    assert(len(indices1) == len(indices2)) 
    lines = []
    vertices1 = [object1.data.vertices[index] for index in indices1]
    vertices2 = [object2.data.vertices[index] for index in indices2]
    for vertex1,vertex2 in zip(vertices1, vertices2):
        lines.append([tuple(object1.matrix_world * vertex1.co), tuple(object2.matrix_world * vertex2.co)])
    return lines

def setLineMaterial(n=10):
    """
    设置全局材质
    """
    for i in range(n):
        lmat = bpy.data.materials.new('Linematerial' + str(i))
        r = random.random()
        g = random.random()
        b = random.random()
        lmat.diffuse_color = (r,g,b)

def drawLine(lines, material_number=10, thickness=0.02):

    for line in lines:
        theLineData = bpy.data.curves.new(name="MyLine", type='CURVE')
        theLineData.dimensions = '3D'
        theLineData.fill_mode = 'FULL'
        theLineData.bevel_depth = thickness
    
        polyline = theLineData.splines.new('POLY')
        polyline.points.add(1)
        
        polyline.points[0].co = (line[0])+(1.0,)
        polyline.points[1].co = (line[1])+(1.0,)

        theLine = bpy.data.objects.new('LineOne',theLineData)
        bpy.context.scene.objects.link(theLine)
        theLine.location = (0.0,0.0,0.0)
        material_index = random.randint(0, material_number-1)
        
        theLine.data.materials.append(bpy.data.materials["Linematerial" + str(material_index)])



model1_filename = os.path.join(directory, "model1Idx.txt")
model2_filename = os.path.join(directory, "model2Idx.txt")
model1_idx = []
model2_idx = []
get_index_from_file(model1_filename, model1_idx)
get_index_from_file(model2_filename, model2_idx)

object1, object2 = bpy.context.selected_objects[:]

lines = getLines(object1, object2, model1_idx, model2_idx)

num_materials = 20

setLineMaterial(num_materials)

drawLine(lines, num_materials)