
import bpy

# Get active object
active = bpy.context.active_object


new_material = bpy.data.materials.new(name = "Material")
active.data.materials.append(new_material)
new_material.use_nodes = True

#---------------------------- Node Creation ------------------------#

# Define Create Nodes 
nodes = new_material.node_tree.nodes #shortcut to Material's Node Tree
material_output = nodes.get("Material Output") #get Material Output node

# Create Emission Shader node
node_emission = nodes.new(type='ShaderNodeEmission')

#Create PrincipledBSDF Shader node
node_principled = nodes.new(type='ShaderNodeBsdfPrincipled')

# Create Geometry node
node_geometry = nodes.new(type="ShaderNodeNewGeometry") 

# Create Vertex Color Node Emission
node_vertex_color_emission = nodes.new(type="ShaderNodeVertexColor") 
node_vertex_color_emission.layer_name = "Emission"

# Create Vertex Color Node AO
node_vertex_color_ao = nodes.new(type="ShaderNodeVertexColor") 
node_vertex_color_ao.layer_name = "AO"

# Create Math Node 01
node_math01 = nodes.new(type="ShaderNodeVectorMath")
node_math01.inputs[1].default_value = [1,0,0]
node_math01.operation = 'MULTIPLY'

# Create Math Node 02
node_math02 = nodes.new(type="ShaderNodeVectorMath")
node_math02.inputs[1].default_value = [0,1,0]
node_math02.operation = 'MULTIPLY'

# Create Math Node 03
node_math03 = nodes.new(type="ShaderNodeVectorMath")
node_math03.operation = 'ADD'


# -------- Bake Random Per Island ---------#

# Define connections variable
connection = new_material.node_tree.links

# Connect Random Per Island to Emission Shader 
new_connection = connection.new (node_geometry.outputs[8], node_emission.inputs[0])

# Connect Emission Shader to Material Output
new_connection = connection.new (node_emission.outputs[0], material_output.inputs[0])

# Create vertex color group "Emission"
bpy.ops.mesh.vertex_color_add()
bpy.context.object.data.vertex_colors["Col"].name = "Emission"

# Bake Random Per Island
bpy.ops.object.bake(type='EMIT', target='VERTEX_COLORS') 

 
#---------- Bake Ambient Occlusion---------#

# Connect PrincipledBSDF to Material Output
new_connection = connection.new (node_geometry.outputs[8], node_emission.inputs[0])
new_connection = connection.new (node_emission.outputs[0], material_output.inputs[0])

# Create vertex color group "AO"
bpy.ops.mesh.vertex_color_add()
bpy.context.object.data.vertex_colors["Col"].name = "AO"

# Bake Ambient Occlusion
bpy.ops.object.bake(type='AO', target='VERTEX_COLORS')


#---------- Mix and Bake Output ---------#

# Connect Vertex Color to Math Nodes 
new_connection = connection.new (node_vertex_color_emission.outputs[0], node_math01.inputs[0])
new_connection = connection.new (node_vertex_color_ao.outputs[0], node_math02.inputs[0])

# Connect Math Nodes to Emission Shader
new_connection = connection.new (node_math01.outputs[0], node_math03.inputs[0])
new_connection = connection.new (node_math02.outputs[0], node_math03.inputs[1])
new_connection = connection.new (node_math03.outputs[0], node_emission.inputs[0])

# Connect Emission Shader to Material Output
new_connection = connection.new (node_emission.outputs[0], material_output.inputs[0])

# Create vertex color group "Output"
bpy.ops.mesh.vertex_color_add()
bpy.context.object.data.vertex_colors["Col"].name = "Output"

# Bake Output
bpy.ops.object.bake(type='EMIT', target='VERTEX_COLORS')

#---------- Delete Vertex Color Groups---------#

bpy.context.object.data.vertex_colors["AO"].active