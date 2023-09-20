import bpy
from bpy.types import Operator, Panel
import os

class UnrealEngineExport(bpy.types.Panel):
    """
    Unreal Engine Export Panel: Provides options for exporting objects to FBX with optional triangulation.
    """
    bl_idname = 'VIEW3D_PT_export_panel'
    bl_label = 'Unreal Engine Export'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Game Pipeline Tools'
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator('opr.gold_fever_export_operator', text="Export", icon="EXPORT")
        
        # CREATE A CHECKBOX FOR TRIANGULATING MESHES
        layout.prop(context.scene, "triangulate_fbx_bool", text="Triangulate Mesh")

class UnrealEngineExportOperator(bpy.types.Operator):
    """
    Unreal Engine Export Operator: Exports selected objects to FBX format, optionally triangulating them.
    """
    bl_idname = 'opr.gold_fever_export_operator'
    bl_label = 'Object Exporter'
    
    def execute(self, context):
        selected = bpy.context.selected_objects 
        
        # TRIANGULATE IF THE CHECKBOX IS ENABLED
        if context.scene.triangulate_fbx_bool:
            for obj in selected:
                target_modifier_name = 'Triangulate'
                triangulate_modifier = obj.modifiers.get(target_modifier_name)
                
                if triangulate_modifier:
                    break
                else:
                    triangulate = obj.modifiers.new("Triangulate", 'TRIANGULATE')
                    triangulate.quad_method = 'FIXED'
                    triangulate.keep_custom_normals = True
            
        bpy.ops.export_scene.fbx('INVOKE_DEFAULT',
                                use_selection=True, 
                                object_types={'MESH', 'ARMATURE'}, 
                                mesh_smooth_type='FACE', 
                                use_tspace=True,  
                                add_leaf_bones=False, 
                                )
        return {'FINISHED'}      

class FBXMeshExport(bpy.types.Panel):
    """
    FBX Mesh Export Panel: Provides options for exporting selected objects to FBX with optional triangulation.
    """
    bl_idname = 'VIEW3D_PT_mesh_export_panel'
    bl_label = 'FBX Split Export'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Game Pipeline Tools'
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator('opr.fbx_mesh_export_operator', text="Export", icon="EXPORT")
         # CREATE A CHECKBOX FOR TRIANGULATING MESHES
        layout.prop(context.scene, "triangulate_split_fbx_bool", text="Triangulate Mesh")

class FBXMeshExportOperator(bpy.types.Operator):
    """
    FBX Mesh Export Operator: Exports selected objects to FBX format, optionally triangulating them.
    """
    bl_idname = 'opr.fbx_mesh_export_operator'
    bl_label = 'Mesh Exporter'
    
    
    
    def execute(self, context):
        # CREATES THE PATH FOR THE EXPORTED FBX.
        file_path = os.path.splitext(bpy.data.filepath)[0]  
        
        #INFO MESSAGE DISPLAYED WHEN MESHES EXPORTED SUCCESFULLY
        def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

            def draw(self, context):
                self.layout.label(text=message)

            bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
        
        
        # OUTPUT ERROR IF THE FILE HASN'T BEEN SAVED
        if not os.path.exists(bpy.data.filepath):
            self.report({'ERROR'}, "Please save the scene first")

        elif not os.path.exists(file_path):
            os.mkdir(file_path)

        else:
            for obj in bpy.context.selected_objects:
                # TRIANGULATE MESHES IF THE CHECKBOX IS ENABLED
                if context.scene.triangulate_split_fbx_bool:
                    target_modifier_name = 'Triangulate'
                    triangulate_modifier = obj.modifiers.get(target_modifier_name)
                    
                    if triangulate_modifier:
                        break
                    else:
                        triangulate = obj.modifiers.new("Triangulate", 'TRIANGULATE')
                        triangulate.quad_method = 'FIXED'
                        triangulate.keep_custom_normals = True
                    
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)
                
                obj_path = os.path.join(file_path, obj.name + "." + "fbx")
                
                bpy.ops.export_scene.fbx(
                    filepath=obj_path,
                    use_selection=True, 
                    object_types={'MESH', 'ARMATURE'}, 
                    mesh_smooth_type='FACE', 
                    use_tspace=True,  
                    add_leaf_bones=False, 
                )
                #SHOWS A MESSAGE BOX WITH A MESSAGE AND CUSTOM TITLE
                ShowMessageBox(f"Assets exported to {file_path} ", "Export Succesful")
                        
        return {'FINISHED'}
