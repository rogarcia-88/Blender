import bpy
class GoldFeverExport(bpy.types.Panel):
       
    bl_idname = 'VIEW3D_PT_gold_fever_export_panel'
    bl_label = 'Gold Fever Export'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Gold Fever Tools'
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator('opr.gold_fever_export_operator', text="Export")
        
        
class GoldFeverExportOperator(bpy.types.Operator):
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
                                    object_types = {'MESH'}, 
                                    mesh_smooth_type = 'FACE', 
                                    use_tspace = True,  
                                    add_leaf_bones=False, 
                                    )
            
        return {'FINISHED'}

if __name__ == '__main__':
    bpy.utils.register_class(GoldFeverExport)
    bpy.utils.register_class(GoldFeverExportOperator)