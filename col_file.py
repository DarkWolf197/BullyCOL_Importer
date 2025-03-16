import struct
from dataclasses import dataclass
from typing import List

@dataclass
class Vector3:
    x: float
    y: float
    z: float
    
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

@dataclass
class BoundingSphere:
    center: Vector3
    radius: float
    
    def __str__(self):
        return f"Center: {self.center}, Radius: {self.radius}"

@dataclass
class BoundingBox:
    min: Vector3
    max: Vector3
    a: float
    b: float
    
    def __str__(self):
        return f"Min: {self.min}, Max: {self.max}, a: {self.a}, b: {self.b}"

@dataclass
class Surface:
    material: int
    flag: int
    unknown: int
    light: int
    
    def __str__(self):
        return f"Material: {self.material}, Flag: {self.flag}, Unknown: {self.unknown}, Light: {self.light}"

@dataclass
class Sphere:
    center: Vector3
    radius: float
    surface: Surface
    
    def __str__(self):
        return f"Center: {self.center}, Radius: {self.radius}, Surface: {self.surface}"

@dataclass
class Box:
    min: Vector3
    max: Vector3
    a: float
    b: float
    surface: Surface
    
    def __str__(self):
        return f"Min: {self.min}, Max: {self.max}, a: {self.a}, b: {self.b}, Surface: {self.surface}"

@dataclass
class Vertex:
    position: Vector3
    
    def __str__(self):
        return f"Position: {self.position}"

@dataclass
class Face:
    vertices: tuple
    material: int
    light: int
    
    def __str__(self):
        return f"Vertices: {self.vertices}, Material: {self.material}, Light: {self.light}"

@dataclass
class ColBlock:
    version: str
    size: int
    type1: int
    type2: int
    model_id: int
    bounding_sphere: BoundingSphere
    bounding_box: BoundingBox
    spheres: List[Sphere]
    boxes: List[Box]
    vertices: List[Vertex]
    faces: List[Face]
    unknown_value: int
    
    def __str__(self):
        return (f"Version: {self.version}, Size: {self.size} bytes\n"
                f"Type1: {self.type1}, Type2: {self.type2}, Model ID: {self.model_id}\n"
                f"Bounding Sphere: {self.bounding_sphere}\n"
                f"Bounding Box: {self.bounding_box}\n"
                f"Spheres: {len(self.spheres)}, Boxes: {len(self.boxes)}, "
                f"Vertices: {len(self.vertices)}, Faces: {len(self.faces)}")


class ColFile:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.blocks: List[ColBlock] = []
        
    def parse(self):
        """Parse the COL file and populate the blocks list."""
        try:
            with open(self.file_path, 'rb') as f:
                offset = 0
                
                while True:
                    f.seek(offset)
                    
                    # Read block header
                    header_data = f.read(8)
                    if len(header_data) < 8:
                        break
                    
                    version = header_data[:4].decode('ascii')
                    if version != "COL3":
                        break
                    
                    file_size = struct.unpack('<I', header_data[4:8])[0]
                    
                    # Read block types
                    type_data = f.read(4)
                    type1, type2 = struct.unpack('<HH', type_data)
                    
                    # Read model name and ID
                    f.read(20)  # Skip name
                    model_id = struct.unpack('<I', f.read(4))[0]
                    
                    # Read bounding sphere
                    center_x, center_y, center_z, radius = struct.unpack('ffff', f.read(16))
                    bounding_sphere = BoundingSphere(
                        center=Vector3(center_x, center_y, center_z),
                        radius=radius
                    )
                    
                    # Read bounding box
                    min_x, min_y, min_z, a, max_x, max_y, max_z, b = struct.unpack('ffffffff', f.read(32))
                    bounding_box = BoundingBox(
                        min=Vector3(min_x, min_y, min_z),
                        max=Vector3(max_x, max_y, max_z),
                        a=a,
                        b=b
                    )
                    
                    # Read sphere count and details
                    sphere_count = struct.unpack('<I', f.read(4))[0]
                    spheres = []
                    
                    # Process all spheres
                    for _ in range(sphere_count):
                        center_x, center_y, center_z = struct.unpack('fff', f.read(12))
                        sphere_radius = struct.unpack('f', f.read(4))[0]
                        material, flag, unknown, light = struct.unpack('BBBB', f.read(4))
                        
                        spheres.append(Sphere(
                            center=Vector3(center_x, center_y, center_z),
                            radius=sphere_radius,
                            surface=Surface(material, flag, unknown, light)
                        ))
                    
                    unknown_value = struct.unpack('<I', f.read(4))[0]
                    
                    # Read box count and details
                    box_count = struct.unpack('<I', f.read(4))[0]
                    boxes = []
                    
                    # Process all boxes
                    for _ in range(box_count):
                        min_x, min_y, min_z = struct.unpack('fff', f.read(12))
                        a = struct.unpack('f', f.read(4))[0]
                        max_x, max_y, max_z = struct.unpack('fff', f.read(12))
                        b = struct.unpack('f', f.read(4))[0]
                        material, flag, unknown, light = struct.unpack('BBBB', f.read(4))
                        
                        boxes.append(Box(
                            min=Vector3(min_x, min_y, min_z),
                            max=Vector3(max_x, max_y, max_z),
                            a=a,
                            b=b,
                            surface=Surface(material, flag, unknown, light)
                        ))
                    
                    # Read vertex count and details
                    vert_count = struct.unpack('<I', f.read(4))[0]
                    vertices = []
                    
                    for _ in range(vert_count):
                        vert_x, vert_y, vert_z = struct.unpack('3h', f.read(6))
                        vertices.append(Vertex(
                            position=Vector3(vert_x, vert_y, vert_z)
                        ))
                    
                    # Handle padding if vertex count is odd
                    if vert_count % 2 != 0:
                        f.read(2)
                    
                    # Read face count and details
                    face_count = struct.unpack('<I', f.read(4))[0]
                    faces = []
                    
                    for _ in range(face_count):
                        vert1, vert2, vert3, material, light = struct.unpack('<3HBB', f.read(8))
                        faces.append(Face(
                            vertices=(vert1, vert2, vert3),
                            material=material,
                            light=light
                        ))
                    
                    # Create block and add to blocks list
                    block = ColBlock(
                        version=version,
                        size=file_size + 8,
                        type1=type1,
                        type2=type2,
                        model_id=model_id,
                        bounding_sphere=bounding_sphere,
                        bounding_box=bounding_box,
                        spheres=spheres,
                        boxes=boxes,
                        vertices=vertices,
                        faces=faces,
                        unknown_value=unknown_value
                    )
                    
                    self.blocks.append(block)
                    
                    # Update offset for next block
                    offset += file_size + 8
            
            return True
                    
        except Exception as e:
            print(f"Error: {e}")
            return False