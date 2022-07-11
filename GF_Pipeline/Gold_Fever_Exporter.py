bl_info = {
    # required
    'name': 'GF Pipeline Tools',
    'blender': (2, 93, 0),
    'category': 'Object',
    # optional
    'version': (1, 0, 0),
    'author': 'Ró García',
    'description': 'Gold Fever Team Pipeline Tools',
}


import bpy
import re

### MAKE GLOBAL VARIABLES

Properties = [
     ('prefix', bpy.props.StringProperty(name='Prefix', default='Pref')),
     ('suffix', bpy.props.StringProperty(name='Suffix', default='Suff')),
     ('add_version', bpy.props.BoolProperty(name='Add Version', default=False)),
     ('version', bpy.props.IntProperty(name='Version', default=1)),
     
 ]


### UTILS & FUNCTIONS

def rename_object(obj, params):
    (prefix, suffix, version, add_version) = params
    
    version_str = '-v{}'.format(version) if add_version else ''
    
    format_regex = r'(?P<prefix>.*)_(?P<main>.*)_(?P<suffix>[^-\n]*)(-v(?P<version>\d+))?'
    match = re.search(format_regex, obj.name)
    # if the object has already been renamed previously,
    # extract the initial name
    if match is not None:
        current_name = match.group('main')
    # else, if it has a "default" name
    else:
        current_name = obj.name
        
    obj.name = '{}_{}_{}{}'.format(prefix, current_name, suffix, version_str)


### PANELS
       
# Object Renamer Panel 
class ObjectRenamerPanel(bpy.types.Panel):
   
    bl_idname = 'VIEW3D_PT_object_renamer'
    bl_label = 'Object Renamer'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Gold Fever Tools'
    
    def draw(self, context):
        col = self.layout.column()
        for (prop_name, _) in Properties:
            row = col.row()
            if prop_name == 'version':
                row = row.row()
                row.enabled = context.scene.add_version
            row.prop(context.scene, prop_name)
        col.operator('opr.object_renamer_operator', text="Rename")
            
# Object Renamer Operator 
class ObjectRenamerOperator(bpy.types.Operator):
    bl_idname = 'opr.object_renamer_operator'
    bl_label = 'Object Renamer'
    
    def execute(self, context):
        params = (
            context.scene.prefix,
            context.scene.suffix,
            context.scene.version,
            context.scene.add_version
        )
        
        for obj in bpy.context.selected_objects:
            rename_object(obj, params)
            
        return {'FINISHED'}

class UnrealEngineExport(bpy.types.Panel):
       
    bl_idname = 'VIEW3D_PT_gold_fever_export_panel'
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
   
    ObjectRenamerPanel,
    ObjectRenamerOperator,
    UnrealEngineExport,
    UnrealEngineExportOperator,
    
]

### REGISTER CLASSES & PROPERTIES

def register():
    
    for (prop_name, prop_value) in Properties:
        setattr(bpy.types.Scene, prop_name, prop_value)
        
    for klass in classes:
        bpy.utils.register_class(klass)
        
def unregister():
    for (prop_name, _) in Properties:
        delattr(bpy.types.Scene, prop_name)
    
    for klass in classes:
        bpy.utils.unregister_class(klass)
        
    
    
    
#Register the class
if __name__ == '__main__':
   register()
   
   
    
    