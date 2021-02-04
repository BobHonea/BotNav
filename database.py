'''
database.py

navigation database file object

simplifying design rules:

geometric shapes are:
  circular or rectangular only
  hollow or solid
  closed or ported

geometric coordinates are:
  cartesian or polar


Rooms:
  are hollow shapes
  may be ported to forbidden space
  may be ported to adjacent rooms
  have shapes within their interiors

Portals:
  Linear Segment of zero width
  located on boundary of rooms
  Identifies Room boundary segment from each room's perspective



Terraine File Manifesto

Everything is a 'Shape', it is a physical world, everything
has extension along the x,y,z axis.

There is only one list of things: the Shape Inventory.
In it are all items, all shapes: Rooms, Insiders, Spanners, and Portals.

Room: a bounded space
Insider: an object inside a Room
Spanner: an object within more than one Room's boundaries
Portal: a boundary segment identifying an opening between Rooms.
World: the totality of Rooms, Insiders, Spanners, and Portals.

The World is the only notion that is not contained in the ShapeInventory.
The ShapeInventory enumerates all objects, real and notional, within the World.

The Terrain/World file contains the essential ShapeInventory in csv format.
Also in csv format, and for redundancy and integrity checking are the lists of
Names and IDs for Rooms, Portals, Insiders, and Spanners.

1. List of all Shapes/ShapedItems
2. List of all Room Names
3. List of all Portal Names
4. List of all Insider Names
5. List of all Spanner Names


'''



from collections import namedtuple
shape_interior=["solid","ported"]
shape_types=["round","rectangle","square"]
CartCoordinate=namedtuple("CartCoordinate", "x y")
PolarCoordinate=namedtuple("PolarCoordinate","radius theta")
Coordinate=namedtuple("Coordinate","is_cartesian coordinate")
NameAssignment=namedtuple("NameAssignment", "ordinal classification name")

ShapeID=namedtuple("ShapeID","shape_ordinal subclass_ordinal shape_name")
PortalInfo=namedtuple("Portal","this_room ccw_coordinate cw_coordinate far_room" )
RoomInfo=namedtuple("RoomInfo", "ordinal shape portals interior_shapes")
ShapeInfo=namedtuple("ShapeInfo","room_ordinal geometry is_hollow major_axis_diameter minor_axis_diameter major_axis_angle coordinate")
World=namedtuple("World", "room_count shape_count portal_count shape_inventory")
ShapeInventory=namedtuple("ShapeInventory", "shape_count shape_info_list")

class terrainFile(object):

    m_terrain_handle=None

    def __init__(self, terrain_filename):
        self.m_terrain_handle=open(terrain_filename,"r")
        if self.m_terrain_handle > 0:
            self.loadTerrain()

    '''
    Loading the World
    -----------------


    '''
    def load(self):
        pass

    def store(self):
        pass

    def loadList(self):
        pass
