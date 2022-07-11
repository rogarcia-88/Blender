import bpy
from mathutils import Matrix, Vector
import numpy as np


class PivotToolsPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Pivot Tools"
    bl_idname = "VIEW3D_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    #bl_category = 'Gold Fever Tools'
    #bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        # Pivot Tools UI
        layout.label(text="Pivot:")
        row = layout.row()
        #row.scale_y = 2.0
        row = layout.row(align=True)
        row.operator("opr.pivot_bottom", text= "Pivot Bottom")
        row.operator("opr.pivot_top", text= "Pivot Top")
        row = layout.row()
        row.operator("opr.pivot_center", text= "Pivot Center")
        row = layout.row()
        row.operator("opr.to_origin", text= "Move to Origin")
        row.scale_y = 2.0
        

class PivotBottom(bpy.types.Operator):
    bl_idname = "opr.pivot_bottom"
    bl_label = "Pivot Bottom"
    
    def execute(self, context):
       
        def origin_to_bottom(ob, matrix=Matrix()):
            me = ob.data
            mw = ob.matrix_world
            local_verts = [matrix @ Vector(v[:]) for v in ob.bound_box]
            o = sum(local_verts, Vector()) / 8
            o.z = min(v.z for v in local_verts)
            o = matrix.inverted() @ o
            me.transform(Matrix.Translation(-o))

            mw.translation = mw @ o

        for o in bpy.context.selected_objects:
            if o.type == 'MESH':
                origin_to_bottom(o)
            #origin_to_bottom(o, matrix=o.matrix_world) # global        
            
        return {'FINISHED'}

class PivotTop(bpy.types.Operator):
    bl_idname = "opr.pivot_top"
    bl_label = "Pivot Top"
    
    def execute(self, context):
       
        def origin_to_top(ob, matrix=Matrix(), use_verts=False):
            me = ob.data
            mw = ob.matrix_world
            if use_verts:
                data = (v.co for v in me.vertices)
            else:
                data = (Vector(v) for v in ob.bound_box)


            coords = np.array([matrix @ v for v in data])
            z = coords.T[2]
            mins = np.take(coords, np.where(z == z.max())[0], axis=0)

            o = Vector(np.mean(mins, axis=0))
            o = matrix.inverted() @ o
            me.transform(Matrix.Translation(-o))

            mw.translation = mw @ o    

        for o in bpy.context.selected_objects:
            if o.type == 'MESH':
                origin_to_top(o)
            #origin_to_bottom(o, matrix=o.matrix_world) # global        
            
        return {'FINISHED'}

class PivotCenter(bpy.types.Operator):
    bl_idname = "opr.pivot_center"
    bl_label = "Pivot Center"
    
    def execute(self, context):
       
        
        selected = bpy.context.selected_objects 
        
        for obj in selected:
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
            
                 
            
        return {'FINISHED'}
    
class ToOrigin(bpy.types.Operator):
    bl_idname = "opr.to_origin"
    bl_label = "Pivot Center"
    
    def execute(self, context):
       
        bpy.context.scene.cursor.location = (0, 0, 0)
        selected = bpy.context.selected_objects 
        
        for obj in selected:
            bpy.ops.object.location_clear(clear_delta=True)
            
            
                 
            
        return {'FINISHED'}



def register():
    bpy.utils.register_class(PivotToolsPanel)
    bpy.utils.register_class(PivotBottom)
    bpy.utils.register_class(PivotTop)
    bpy.utils.register_class(PivotCenter)
    bpy.utils.register_class(ToOrigin)



def unregister():
    bpy.utils.unregister_class(PivotToolsPanel)
    bpy.utils.unregister_class(PivotBottom)
    bpy.utils.unregister_class(PivotTop)
    bpy.utils.register_class(PivotCenter)
    bpy.utils.register_class(ToOrigin)


if __name__ == "__main__":
    register()

