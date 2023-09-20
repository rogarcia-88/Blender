bl_info = {
    # required
    'name': 'Game Pipeline Tools',
    'blender': (2, 93, 0),
    'category': 'Object',
    # optional
    'version': (1, 0, 1),
    'author': 'Ró García',
    'description': 'Basic Asset Management & Pipeline tools for Game Engines',
}

import bpy
from .ops import batch_renamer, pivot_tools, export_tools
    
#List of Classes
classes = [
   
    batch_renamer.Object_OT_RenameObjects,
    batch_renamer.RenamerPanel,
    pivot_tools.PivotBottom,
    pivot_tools.PivotTop,
    pivot_tools.PivotCenter,
    pivot_tools.ToOrigin,
    pivot_tools.PivotToolsPanel, 
    export_tools.UnrealEngineExportOperator,
    export_tools.UnrealEngineExport,
    export_tools.FBXMeshExport,
    export_tools.FBXMeshExportOperator,
    
]

### REGISTER CLASSES & PROPERTIES

def register():
    
    #Registering Bool Checkbox
    bpy.types.Scene.triangulate_fbx_bool = bpy.props.BoolProperty(
        name="Triangulate",
        description="Add a Triangulate modifier to assets",
        default=False
    )
    
    bpy.types.Scene.triangulate_split_fbx_bool = bpy.props.BoolProperty(
    name="Triangulate",
    description="Add a Triangulate modifier to assets",
    default=False
    )
        
    for klass in classes:
        bpy.utils.register_class(klass)
        
def unregister():
    
    del bpy.types.Scene.triangulate_fbx_bool
    del bpy.types.Scene.triangulate_split_fbx_bool
    
    for klass in classes:
        bpy.utils.unregister_class(klass)
        
    
    
    
#Register the class
if __name__ == '__main__':
   register()