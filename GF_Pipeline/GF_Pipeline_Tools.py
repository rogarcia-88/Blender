bl_info = {
    # required
    'name': 'GF Pipeline Tools',
    'blender': (2, 93, 0),
    'category': 'Object',
    # optional
    'version': (1, 0, 1),
    'author': 'Ró García',
    'description': 'Gold Fever Team Pipeline Tools',
}

import bpy
from bpy.types import Operator
from mathutils import Matrix, Vector
import numpy as np

class RenamerPanel(bpy.types.Panel):
       
    bl_idname = 'VIEW3D_PT_Renamer_panel'
    bl_label = 'Batch Renamer'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Gold Fever Tools'
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator('object.renameobjects', text="Rename")



class Object_OT_RenameObjects(Operator):
    bl_idname = "object.renameobjects"
    bl_label = "Rename Object(s)"

    # Multi Object rename UI
    BNameCB   : bpy.props.BoolProperty(name = "Base Name:")
    BaseName  : bpy.props.StringProperty(name = "")
    PreFixCB  : bpy.props.BoolProperty(name = "Prefix:")
    PreFix    : bpy.props.StringProperty(name = "")
    RemFrst   : bpy.props.BoolProperty(name = "Remove First")
    DgtFrst   : bpy.props.IntProperty(name = "Digits")
    SuffixCB  : bpy.props.BoolProperty(name = "Suffix")
    Suffix    : bpy.props.StringProperty(name = "")
    RemLast   : bpy.props.BoolProperty(name = "Remove Last")
    DgtLast   : bpy.props.IntProperty(name = "Digits")
    NumbredCB : bpy.props.BoolProperty(name = "Numbered")
    BaseNum   : bpy.props.IntProperty(name = "Base Number")
    Step      : bpy.props.IntProperty(name = "Step", default = 1)
    findCB    : bpy.props.BoolProperty(name = "Replace")
    find      : bpy.props.StringProperty(name = "")
    replace   : bpy.props.StringProperty(name = "")
    # Single rename UI
    Name : bpy.props.StringProperty(name="Name")

    def draw(self, ctx):
        SelCount = len(bpy.context.selected_objects)
        if SelCount > 1:
            box = self.layout.box()
            row = box.row()
            row.prop(self, "BNameCB")
            row.prop(self, "BaseName")
            row = box.row()
            row.prop(self, "PreFixCB")
            row.prop(self, "PreFix")
            row = box.row()
            row.prop(self, "RemFrst")
            row.prop(self, "DgtFrst")
            row = box.row()
            row.prop(self, "SuffixCB")
            row.prop(self, "Suffix")
            row = box.row()
            row.prop(self, "RemLast")
            row.prop(self, "DgtLast")
            row = box.row(align=True)
            row.prop(self, "NumbredCB")
            row.prop(self, "BaseNum")
            row.prop(self, "Step")
            row = box.row(align=True)
            row.prop(self, "findCB")
            row.prop(self, "find")
            row.prop(self, "replace")
        if SelCount == 1:
            box = self.layout.box()
            row = box.row()
            row.prop(self, "Name")
        if SelCount == 0:
            box = self.layout.box()
            row = box.row()
            row.label("No Selected Object")

    def __init__(self):
        if len(bpy.context.selected_objects) == 1:
            self.Name = bpy.context.selected_objects[0].name

    def execute(self, context):
        SelCount = len(bpy.context.selected_objects)
        if SelCount > 1:
            SelObj = bpy.context.selected_objects
            Index = self.BaseNum
            for i in range(0,SelCount):
                # Get Object Original Name #
                NewName = SelObj[i].name
                # Set the Base name #
                if self.BNameCB:
                    NewName = self.BaseName
                # Remove First characters #
                if self.RemFrst:
                    NewName = NewName[self.DgtFrst : self.DgtFrst + len(NewName)]
                # Remove Last Characters #
                if self.RemLast:
                    NewName = NewName[1 : len(NewName) - self.DgtLast]
                # Add Prefix to the new name #
                if self.PreFixCB:
                    NewName = self.PreFix + NewName
                # Add Suffix to the new name #
                if self.SuffixCB:
                    NewName = NewName + self.Suffix
                # Add Digits to end of new name #
                if self.NumbredCB:
                        NewName += str(Index)
                        Index += self.Step
                # Find and Replace #
                if self.findCB:
                    NewName = NewName.replace(self.find, self.replace)
                # Set the new name to the object #
                SelObj[i].name = NewName
        elif SelCount == 1:
            bpy.context.selected_objects[0].name = self.Name
        return {'FINISHED'}
       
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
## PIVOT PANEL
class PivotToolsPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Pivot Tools"
    bl_idname = "VIEW3D_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Gold Fever Tools'
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


    

class UnrealEngineExport(bpy.types.Panel):
       
    bl_idname = 'VIEW3D_PT_export_panel'
    bl_label = 'Unreal Engine Export'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Gold Fever Tools'
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator('opr.gold_fever_export_operator', text="Export")
        
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
                                    object_types = {'MESH'}, 
                                    mesh_smooth_type = 'FACE', 
                                    use_tspace = True,  
                                    add_leaf_bones=False, 
                                    )
            
        return {'FINISHED'}    
        




#List of Classes
classes = [
   
    Object_OT_RenameObjects,
    RenamerPanel,
    PivotToolsPanel,
    PivotBottom,
    PivotTop,
    PivotCenter,
    UnrealEngineExport,
    UnrealEngineExportOperator,
    
]

### REGISTER CLASSES & PROPERTIES

def register():
    
    
        
    for klass in classes:
        bpy.utils.register_class(klass)
        
def unregister():
    
    
    for klass in classes:
        bpy.utils.unregister_class(klass)
        
    
    
    
#Register the class
if __name__ == '__main__':
   register()
