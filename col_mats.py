import bpy
import enum

class SurfaceType(enum.IntEnum):
    DEFAULT = 0
    TARMAC = 1
    DIRT = 2
    GRASS = 3
    GRAVEL = 4
    MUD = 5
    PAVEMENT = 6
    SIDEWALK = 7
    CEMENT_STAIRS = 8
    CURBING = 9
    CERAMIC = 10
    BRICK_WALL = 11
    CONCRETE_WALL = 12
    PLASTER_WALL = 13
    CAR = 14
    GLASS = 15
    TRANSPARENT_CLOTH = 16
    GARAGE_DOOR = 17
    CAR_PANEL = 18
    THICK_METAL_PLATE = 19
    SCAFFOLD_POLE = 20
    LAMP_POST = 21
    GARBAGE_CAN = 22
    FIRE_HYDRANT = 23
    GIRDER = 24
    METAL_CHAIN_FENCE = 25
    PED = 26
    SAND = 27
    ICE = 28
    SNOW = 29
    SHALLOW_WATER = 30
    PUDDLE = 31
    WOOD_CRATES = 32
    WOOD_BENCH = 33
    WOOD_SOLID = 34
    WOOD_STAIRS = 35
    POLE = 36
    BOARD = 37
    RUBBER = 38
    PLASTIC = 39
    PLASTIC_HOLLOW = 40
    LINO = 41
    LINO_STAIRS = 42
    VEGETATION = 43
    TREE_TRUNK = 44
    STEEPHILL = 45
    CONTAINER = 46
    NEWS_VENDOR = 47
    WHEELBASE = 48
    CARDBOARDBOX = 49
    NEWSPAPER = 50
    TRASH = 51
    TRANSPARENT_STONE = 52
    METAL_GATE = 53
    SAND_NOTBEACH = 54
    CONCRETE_BEACH = 55
    METAL_STAIRS = 56
    CARPET = 57
    CARPET_STAIRS = 58
    WOOD_DOCK = 59
    BOXING_MAT = 60
    DEEP_PUDDLE = 61
    CROUCH_ON_BRANCH = 62
    CROUCH_ON_ROOF = 63
    NOT_WALL = 64
    INVISIBLE = 65
    MIRROR = 66

SURFACE_COLORS = {
    SurfaceType.DEFAULT: (1.0, 0.0, 1.0, 1.0),
    SurfaceType.TARMAC: (0.2, 0.2, 0.2, 1.0),
    SurfaceType.DIRT: (0.6, 0.4, 0.2, 1.0),
    SurfaceType.GRASS: (0.2, 0.6, 0.1, 1.0),
    SurfaceType.GRAVEL: (0.5, 0.5, 0.5, 1.0),
    SurfaceType.MUD: (0.4, 0.3, 0.1, 1.0),
    SurfaceType.PAVEMENT: (0.7, 0.7, 0.7, 1.0),
    SurfaceType.SIDEWALK: (0.75, 0.75, 0.75, 1.0),
    SurfaceType.CEMENT_STAIRS: (0.65, 0.65, 0.65, 1.0),
    SurfaceType.CURBING: (0.8, 0.8, 0.7, 1.0),
    SurfaceType.CERAMIC: (0.9, 0.9, 0.9, 1.0),
    SurfaceType.BRICK_WALL: (0.7, 0.3, 0.2, 1.0),
    SurfaceType.CONCRETE_WALL: (0.6, 0.6, 0.6, 1.0),
    SurfaceType.PLASTER_WALL: (0.85, 0.85, 0.8, 1.0),
    SurfaceType.CAR: (0.1, 0.3, 0.7, 1.0),
    SurfaceType.GLASS: (0.8, 0.95, 1.0, 1.0),
    SurfaceType.TRANSPARENT_CLOTH: (1.0, 1.0, 1.0, 1.0),
    SurfaceType.GARAGE_DOOR: (0.5, 0.5, 0.5, 1.0),
    SurfaceType.CAR_PANEL: (0.2, 0.2, 0.7, 1.0),
    SurfaceType.THICK_METAL_PLATE: (0.4, 0.4, 0.4, 1.0),
    SurfaceType.SCAFFOLD_POLE: (0.6, 0.6, 0.3, 1.0),
    SurfaceType.LAMP_POST: (0.3, 0.3, 0.3, 1.0),
    SurfaceType.GARBAGE_CAN: (0.3, 0.7, 0.3, 1.0),
    SurfaceType.FIRE_HYDRANT: (0.8, 0.1, 0.1, 1.0),
    SurfaceType.GIRDER: (0.5, 0.4, 0.3, 1.0),
    SurfaceType.METAL_CHAIN_FENCE: (0.7, 0.7, 0.7, 1.0),
    SurfaceType.PED: (0.9, 0.7, 0.5, 1.0),
    SurfaceType.SAND: (0.9, 0.8, 0.5, 1.0),
    SurfaceType.ICE: (0.8, 0.9, 1.0, 1.0),
    SurfaceType.SNOW: (1.0, 1.0, 1.0, 1.0),
    SurfaceType.SHALLOW_WATER: (0.2, 0.5, 0.8, 1.0),
    SurfaceType.PUDDLE: (0.3, 0.5, 0.7, 1.0),
    SurfaceType.WOOD_CRATES: (0.6, 0.4, 0.2, 1.0),
    SurfaceType.WOOD_BENCH: (0.5, 0.35, 0.2, 1.0),
    SurfaceType.WOOD_SOLID: (0.4, 0.3, 0.2, 1.0),
    SurfaceType.WOOD_STAIRS: (0.5, 0.4, 0.2, 1.0),
    SurfaceType.POLE: (0.3, 0.3, 0.3, 1.0),
    SurfaceType.BOARD: (0.6, 0.5, 0.3, 1.0),
    SurfaceType.RUBBER: (0.1, 0.1, 0.1, 1.0),
    SurfaceType.PLASTIC: (0.3, 0.7, 0.7, 1.0),
    SurfaceType.PLASTIC_HOLLOW: (0.4, 0.8, 0.8, 1.0),
    SurfaceType.LINO: (0.7, 0.6, 0.5, 1.0),
    SurfaceType.LINO_STAIRS: (0.7, 0.6, 0.5, 1.0),
    SurfaceType.VEGETATION: (0.1, 0.5, 0.1, 1.0),
    SurfaceType.TREE_TRUNK: (0.3, 0.2, 0.1, 1.0),
    SurfaceType.STEEPHILL: (0.5, 0.5, 0.3, 1.0),
    SurfaceType.CONTAINER: (0.3, 0.3, 0.7, 1.0),
    SurfaceType.NEWS_VENDOR: (0.9, 0.3, 0.3, 1.0),
    SurfaceType.WHEELBASE: (0.2, 0.2, 0.2, 1.0),
    SurfaceType.CARDBOARDBOX: (0.8, 0.6, 0.4, 1.0),
    SurfaceType.NEWSPAPER: (0.9, 0.9, 0.8, 1.0),
    SurfaceType.TRASH: (0.5, 0.5, 0.3, 1.0),
    SurfaceType.TRANSPARENT_STONE: (0.7, 0.7, 0.9, 1.0),
    SurfaceType.METAL_GATE: (0.6, 0.6, 0.7, 1.0),
    SurfaceType.SAND_NOTBEACH: (0.8, 0.7, 0.4, 1.0),
    SurfaceType.CONCRETE_BEACH: (0.7, 0.7, 0.6, 1.0),
    SurfaceType.METAL_STAIRS: (0.5, 0.5, 0.6, 1.0),
    SurfaceType.CARPET: (0.5, 0.2, 0.2, 1.0),
    SurfaceType.CARPET_STAIRS: (0.5, 0.2, 0.2, 1.0),
    SurfaceType.WOOD_DOCK: (0.6, 0.5, 0.3, 1.0),
    SurfaceType.BOXING_MAT: (0.2, 0.2, 0.6, 1.0),
    SurfaceType.DEEP_PUDDLE: (0.1, 0.3, 0.6, 1.0),
    SurfaceType.CROUCH_ON_BRANCH: (0.4, 0.3, 0.1, 1.0),
    SurfaceType.CROUCH_ON_ROOF: (0.4, 0.4, 0.4, 1.0),
    SurfaceType.NOT_WALL: (1.0, 0.0, 1.0, 1.0),
    SurfaceType.INVISIBLE: (1.0, 1.0, 1.0, 1.0),
    SurfaceType.MIRROR: (0.9, 0.9, 0.9, 1.0),
}

def create_material_from_surface_type(surface_type):

    surface_type = SurfaceType(surface_type)

    if bpy.data.materials.get(surface_type.name, None):
        return bpy.data.materials[surface_type.name]

    mat = bpy.data.materials.new(name=surface_type.name)
    mat.diffuse_color = SURFACE_COLORS[surface_type]
    
    return mat