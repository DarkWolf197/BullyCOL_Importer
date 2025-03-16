bl_info = {
    "name": "COL Importer",
    "author": "DarkWolf197",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "File > Import > COL (.col)",
    "description": "Import .col files into Blender",
    "category": "Import-Export",
}

import bpy
import os
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, CollectionProperty
from bpy.types import Operator

from .col_file import ColFile
from .obj_utils import *



class ImportCOL(Operator, ImportHelper):
    """Import COL file(s)"""
    bl_idname = "import_scene.col"
    bl_label = "Import COL"
    bl_options = {"PRESET", "UNDO"}

    filename_ext = ".col"
    filter_glob: StringProperty(
        default="*.col",
        options={'HIDDEN'},
        maxlen=255,
    ) # type: ignore

    # Add multiple files support
    files: CollectionProperty(
        name="File Path",
        type=bpy.types.OperatorFileListElement,
    ) # type: ignore

    directory: StringProperty(
        subtype='DIR_PATH',
    ) # type: ignore

    def execute(self, context):
        # Check if files are selected
        if not self.files:
            self.report({'ERROR'}, "No files selected")
            return {'CANCELLED'}
        
        total_blocks = 0
        total_imported = 0
        
        # Process each selected file
        for file in self.files:
            filepath = os.path.join(self.directory, file.name)
            
            # Parse the COL file
            col_file = ColFile(filepath)
            if not col_file.parse():
                self.report({'ERROR'}, f"Failed to parse {file.name}")
                continue
            
            # Create root empty object
            col_empty = create_root_empty(os.path.basename(filepath[:-4]))
            
            # Process each block in the COL file
            imported_blocks = 0
            for block in col_file.blocks:
                
                if not any(len(l) > 0 for l in (block.boxes, block.vertices, block.spheres)):
                    continue

                block_empty = create_block_empty(str(block.model_id), col_empty)

                if block.vertices:
                    import_mesh(block, block_empty)

                if block.spheres:
                    import_spheres(block, block_empty)

                if block.boxes:
                    import_boxes(block, block_empty)
                
                imported_blocks += 1
            
            total_blocks += len(col_file.blocks)
            total_imported += imported_blocks
            
            self.report({'INFO'}, f"Imported {imported_blocks} blocks of {len(col_file.blocks)} from {file.name}")
        
        if len(self.files) > 1:
            self.report({'INFO'}, f"Total: Imported {total_imported} blocks of {total_blocks} from {len(self.files)} files")
        
        return {'FINISHED'}


# Menu function for the importer
def menu_func_import(self, context):
    self.layout.operator(ImportCOL.bl_idname, text="COL (.col)")


# Register/unregister functions
def register():
    bpy.utils.register_class(ImportCOL)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportCOL)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()