from unicodedata import name
import bpy, os

selection = bpy.context.selected_objects

verts, edges, polys, tris, uv_channels = 0,0,0,0,0

dg = bpy.context.evaluated_depsgraph_get()

for obj in bpy.context.selected_objects:
    
    obj = obj.evaluated_get(dg)
    # This gives the evaluated version of the object.  (With all modifiers and deformations applied)
    mesh = obj.to_mesh()  # Turn it into mesh data block
    
    obj_name = obj.name
    verts += len(mesh.vertices)
    edges += len(mesh.edges)
    polys += len(mesh.polygons)
    tris += (sum(len(polygon.vertices) - 2 for polygon in obj.data.polygons))
    uv_channels +=  len(mesh.uv_layers)
    
    print(f" {obj_name} \n   Total : {verts} Verts, {edges} Edges, {polys} Polys, {tris} Triangles, {uv_channels} UV Channels")

    