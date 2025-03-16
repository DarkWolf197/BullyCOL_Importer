import bpy
import math

def create_sphere_mesh(radius):
    vertices = []
    faces = []
    segments=16
    rings=8

    sphere_mesh = bpy.data.meshes.new("sphere_mesh")


    # Generate vertices
    for i in range(rings + 1):
        ring_angle = math.pi * i / rings
        y = radius * math.cos(ring_angle)
        ring_radius = radius * math.sin(ring_angle)
        
        for j in range(segments):
            segment_angle = 2 * math.pi * j / segments
            x = ring_radius * math.cos(segment_angle)
            z = ring_radius * math.sin(segment_angle)
            
            vertices.append((x, y, z))
    
    # Generate faces
    for i in range(rings):
        for j in range(segments):
            v1 = i * segments + j
            v2 = i * segments + (j + 1) % segments
            v3 = (i + 1) * segments + (j + 1) % segments
            v4 = (i + 1) * segments + j
            
            faces.append((v1, v2, v3, v4))

    sphere_mesh.from_pydata(vertices, [], faces)
    sphere_mesh.update()

    return sphere_mesh


def create_box_mesh(min_point, max_point):

    box_mesh = bpy.data.meshes.new("box_mesh")
    vertices = [
        (min_point.x, min_point.y, min_point.z),
        (max_point.x, min_point.y, min_point.z),
        (max_point.x, max_point.y, min_point.z),
        (min_point.x, max_point.y, min_point.z),
        (min_point.x, min_point.y, max_point.z),
        (max_point.x, min_point.y, max_point.z),
        (max_point.x, max_point.y, max_point.z),
        (min_point.x, max_point.y, max_point.z)
    ]
    
    faces = [
        (0, 1, 2, 3),  # Bottom face
        (4, 5, 6, 7),  # Top face
        (0, 1, 5, 4),  # Front face
        (1, 2, 6, 5),  # Right face
        (2, 3, 7, 6),  # Back face
        (3, 0, 4, 7)   # Left face
    ]
    
    box_mesh.from_pydata(vertices, [], faces)
    box_mesh.update()

    return box_mesh


def create_main_mesh(vertices, faces):

    main_mesh = bpy.data.meshes.new("main_mesh")
    v = []
    for vertex in vertices:
        x = vertex.position.x
        y = vertex.position.y
        z = vertex.position.z
        v.append((x, y, z))

    # Extract face indices
    f = []
    for face in faces:
        f.append(face.vertices)

    main_mesh.from_pydata(v, [], f)
    main_mesh.flip_normals()
    main_mesh.update()

    return main_mesh


def create_obj(
    name: str,
    mesh: bpy.types.Mesh,
    parent: bpy.types.Object
) -> bpy.types.Object:

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.parent = parent
    return obj