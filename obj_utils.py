import bpy
from .mesh_utils import *
from .col_mats import *

def create_root_empty(name):
    """Create the root empty object for the COL file"""
    col_empty = bpy.data.objects.new(name, None)
    col_empty.empty_display_type = 'PLAIN_AXES'
    col_empty.empty_display_size = 0.0001
    bpy.context.collection.objects.link(col_empty)
    return col_empty


def create_block_empty(block_id, parent):
    """Create an empty object for a COL block"""
    block_empty = bpy.data.objects.new(block_id, None)
    block_empty.empty_display_type = 'PLAIN_AXES'
    block_empty.empty_display_size = 0.0001
    bpy.context.collection.objects.link(block_empty)
    block_empty.parent = parent
    return block_empty


def import_mesh(block, parent):
    """Import mesh from a COL block"""
    
    # Create mesh
    main_mesh = create_main_mesh(block.vertices, block.faces)
    main_obj = create_obj(f"{block.model_id}_Mesh", main_mesh, parent)
    main_obj.scale = (0.01, 0.01, 0.01)
    
    # Assign materials to faces
    for i, face in enumerate(block.faces):
        mat = create_material_from_surface_type(face.material)
        if mat.name not in main_obj.data.materials:
            main_obj.data.materials.append(mat)
        main_mesh.polygons[i].material_index = main_obj.data.materials.find(mat.name)


def import_spheres(block, parent):
    """Import spheres from a COL block"""
    
    for j, sphere in enumerate(block.spheres):
        # Create sphere
        sphere_mesh = create_sphere_mesh(sphere.radius)
        sphere_obj = create_obj(f"{block.model_id}_Sphere_{j}", sphere_mesh, parent) 
        sphere_obj.location = (sphere.center.x, sphere.center.y, sphere.center.z)

        # Apply material
        mat = create_material_from_surface_type(sphere.surface.material)
        sphere_obj.data.materials.append(mat)


def import_boxes(block, parent):
    """Import boxes from a COL block"""
    
    for j, box in enumerate(block.boxes):
        # Create box
        box_mesh = create_box_mesh(box.min, box.max)
        box_obj = create_obj(f"{block.model_id}_Box_{j}", box_mesh, parent)       
        
        # Apply material
        mat = create_material_from_surface_type(box.surface.material)
        box_obj.data.materials.append(mat)