import bpy
from bpy.types import Operator
from mathutils import Matrix, Vector
import numpy as np

## PIVOT PANEL
class PivotToolsPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor for Pivot Tools."""
    bl_label = "Pivot Tools"
    bl_idname = "VIEW3D_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Game Pipeline Tools'

    def draw(self, context):
        layout = self.layout

        # PIVOT TOOLS UI
        row = layout.row()
        row.operator("opr.apply_transforms", text="Apply Transforms", icon="TRANSFORM_ORIGINS")
        
        row = layout.row()
        row = layout.row(align=True)
        row.operator("opr.pivot_bottom", text="Pivot Bottom", icon="PIVOT_BOUNDBOX")
        row.operator("opr.pivot_top", text="Pivot Top", icon="PIVOT_BOUNDBOX")
        row = layout.row()
        row.operator("opr.pivot_center", text="Pivot Center", icon="PIVOT_BOUNDBOX")
        row = layout.row()
        row.operator("opr.to_origin", text="Move to Origin", icon="PIVOT_CURSOR")
        row.scale_y = 2.0

class ApplyTransforms(bpy.types.Operator):
    """
    Apply Transforms Operator: Bake the transforms of the selected objects.
    """
    bl_idname = "opr.apply_transforms"
    bl_label = "Apply Transforms"
    
    def execute(self, context):
        
        selected = bpy.context.selected_objects 
        
        for obj in selected:
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            
        return {'FINISHED'}

class PivotBottom(bpy.types.Operator):
    """
    Pivot Bottom Operator: Moves the pivot point of selected objects to the bottom of their bounding box.
    """
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
            
        return {'FINISHED'}

class PivotTop(bpy.types.Operator):
    """
    Pivot Top Operator: Moves the pivot point of selected objects to the top of their bounding box.
    """
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
            
        return {'FINISHED'}

class PivotCenter(bpy.types.Operator):
    """
    Pivot Center Operator: Moves the pivot point of selected objects to their geometrical center.
    """
    bl_idname = "opr.pivot_center"
    bl_label = "Pivot Center"
    
    def execute(self, context):
        selected = bpy.context.selected_objects 
        
        for obj in selected:
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
            
        return {'FINISHED'}
    
class ToOrigin(bpy.types.Operator):
    """
    To Origin Operator: Moves the selected objects to the global origin.
    """
    bl_idname = "opr.to_origin"
    bl_label = "Move to Origin"
    
    def execute(self, context):
        bpy.context.scene.cursor.location = (0, 0, 0)
        selected = bpy.context.selected_objects 
        
        for obj in selected:
            bpy.ops.object.location_clear(clear_delta=True)
            
        return {'FINISHED'}
