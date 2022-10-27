bl_info = {
    # required
    'name': 'Pipeline Tools',
    'blender': (2, 93, 0),
    'category': 'Object',
    # optional
    'version': (1, 0, 1),
    'author': 'Ró García',
    'description': 'My Pipeline Tools',
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
    
    
        
    for klass in classes:
        bpy.utils.register_class(klass)
        
def unregister():
    
    
    for klass in classes:
        bpy.utils.unregister_class(klass)
        
    
    
    
#Register the class
if __name__ == '__main__':
   register()