import bpy
from bpy.types import Operator
import os

class UnrealEngineExport(bpy.types.Panel):
       
    bl_idname = 'VIEW3D_PT_export_panel'
    bl_label = 'Unreal Engine Export'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Gold Fever Tools'
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator('opr.gold_fever_export_operator', text="Export", icon="EXPORT")
        
class UnrealEngineExportOperator(bpy.types.Operator):
    
    bl_idname = 'opr.gold_fever_export_operator'
    bl_label = 'Object Exporter'
    
    def execute(self, context):
        
        selected = bpy.context.selected_objects   

        for obj in selected:
            
            
            triangulate = obj.modifiers.new("Triangulate", 'TRIANGULATE')
            triangulate.quad_method = 'FIXED'
            triangulate.keep_custom_normals = True
            bpy.ops.export_scene.fbx('INVOKE_DEFAULT',
                                    use_selection = True, 
                                    object_types = {'MESH', 'ARMATURE'}, 
                                    mesh_smooth_type = 'FACE', 
                                    use_tspace = True,  
                                    add_leaf_bones=False, 
                                    )
            return {'FINISHED'}      
            
class FBXMeshExport(bpy.types.Panel):
       
    bl_idname = 'VIEW3D_PT_mesh_export_panel'
    bl_label = 'FBX Split Export'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Gold Fever Tools'
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator('opr.fbx_mesh_export_operator', text="Export", icon="EXPORT")

class FBXMeshExportOperator(bpy.types.Operator):
    
    bl_idname = 'opr.fbx_mesh_export_operator'
    bl_label = 'Mesh Exporter'
    
    def execute(self, context):
        
        # Creates the path for the exported fbx.
        file_path = os.path.splitext(bpy.data.filepath)[0]  
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        
         

        for obj in bpy.context.selected_objects:
            
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            
            obj_path = os.path.join(file_path,
                                    obj.name + "." + "fbx")
            
            
            triangulate = obj.modifiers.new("Triangulate", 'TRIANGULATE')
            triangulate.quad_method = 'FIXED'
            triangulate.keep_custom_normals = True
            bpy.ops.export_scene.fbx(
                                    filepath=obj_path,
                                    use_selection = True, 
                                    object_types = {'MESH'}, 
                                    mesh_smooth_type = 'FACE', 
                                    use_tspace = True,  
                                    add_leaf_bones=False, 
                                    )
        return {'FINISHED'}  