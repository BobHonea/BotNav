'''
Created on Jan 26, 2021

@author: Asus
'''
from pickle import TRUE
from pip._internal.cli import status_codes







'''
profile.py generates and maintains a database of sonar profiles
for a room.

simplifiying design rules:

Sonar readings are taken as an angular sweep at a single elevation,
from a single location. (Ignore z-dimension complexity)


A room is an un-closed rectangular shape with an empty interior.

Openings in a room are openings into an adjacent room.

An adjacent room may be 'permitted' or 'forbidden' with regard
physical navigation.

A shape located in a room that is not in the room database is
"novel".

A room and may have openings, which lead into contiguous rooms

A hallway is a room shape having two sides only.

A world is a collection of contiguous rooms. Rooms can be fully
enclosed, or open into other rooms.

a room has a shape, dictated by walls, and contains a set of
non-overlapping interior shapes.

a profile is a function with binary, integer, or real values
over an interval (0,2*pi)

rationale: a live sonar scan from a position within the room through
2*pi degrees will yield a function. At a location within a shaped
room, containing non-overlapping primitive shapes, a sonar scan will
return a function on interval (0,2*pi) that cam be compared with
a database of pre-computed profiles for that same room.

The profiles with the nearest correlation to the live sonar scan
are candidates for identifying the position of the scanner.

The live sonar scan location can be extrapolated from the set
of correlating object profiles.

'''

'''
LIST OF Nav Database Supporting Classes

class Placement(object):
class Shape(object):
class Room(object):
class ObjectProfile(object):
class RoomProfile(object):
class World(object):

A World is a collection of Rooms
A Room has is a Shape with a hollow interior and Portals
A Shape is a geometric cylinder that is hollow or solid
A Portal


'''

from collections import namedtuple
from database import terrainFile
import math
import vectormath as vmath


AdjacentRoom=namedtuple("AdjacentRoom", "room_id shared_side ccw_offset cw_offset")
PortalSpec=namedtuple("PortalSpec","room_id shared_side ccw_offset cw_offset")


class NavError(BaseException):
    """Base class for other exceptions"""
    pass


class ShapeOutOfBounds(NavError):
    """A Shape Crosses Straddles A Boundary"""
    pass





class MeasurementUnits(object):
    

    UNITS_DISTANCE_MM=0
    UNITS_DISTANCE_CM=1
    UNITS_DISTANCE_DM=2
    UNITS_DISTANCE_BC=3
    UNITS_DISTANCE_IN=4
    UNITS_DISTANCE_FT=5

    UNITS_ANGLE_GRAD=0
    UNITS_ANGLE_DEGREE=1
    UNITS_ANGLE_RADIAN=2

    UNITS_TIME_SECONDS=0
    
    def __init__(self, distance_units, angle_units, time_units):
        pass




'''
Placement(), Geometry()
 fundamental shap location and type information
'''

Placement=namedtuple("Placement", "cm_x cm_y major_axis_inclination")
Geometry=namedtuple("Geometry", "shape_id cm_major_axis_length cm_minor_axis_length")


class Shape(object):

    '''
    This class cannot support all regular shapes
    Squares, Rectangles, and Circles (eccentricity=1) only
    '''
    
    
    # LIMITED SET OF SHAPES SUPPORTED
    SHAPE_ID_RECTANGLE=1
    SHAPE_ID_ELLIPSE=2
    SHAPE_ID_CYLINDER_ARRAY=3
    
    # CAN DEFINE RECTANGLE, OR ELLIPSE
    CMDIM_MAJORAXIS_INDEX=0
    CMDIM_MINORAXIS_INDEX=1

    m_shape_id=None
    m_major_axis_length_cm=None
    m_minor_axis_length_cm=None
    m_major_axis_inclination=None
    m_origin_x_cm=None
    m_origin_y_cm=None

    def __init__(self,  geometry:Geometry, placement:Placement):
        self.m_shape_id=geometry.shape_id
        self.m_major_axis_length_cm=geometry.cm_major_axis_length
        self.m_minor_axis_length_cm=geometry.cm_minor_axis_length
        self.m_origin_x_cm=placement.cm_x
        self.m_origin_y_cm=placement.cm_y
        self.m_major_axis_inclination=placement.major_axis_inclination

    def getShapeID(self):
        return self.m_geometery

    def getDimensions(self):
        return [self.m_major_axis_length_cm, self.m_minor_axis_length_cm]

    def getInclination(self):
        return self.m_major_axis_inclination
    
    def setInclination(self, major_axis_inclination):
        self.m_major_axis_inclination=major_axis_inclination

    def setPlacement(self, place: [Placement]):
        self.m_origin_x_cm=place.cm_x
        self.m_origin_y_cm=place.cm_y
        self.m_major_axis_inclination=place.major_axis_inclination


    def getPlacement(self) -> Placement:
        return Placement(self.m_origin_x_cm, self.m_origin_y_cm, self.m_major_axis_inclination)
    
    
    def getOriginVector(self) -> vmath.Vector2:
        origin=vmath.Vector2(self.m_origin_x_cm, self.m_origin_y_cm)
        return origin
                             
    def setGeometry(self, geometry:[Geometry]):
        self.m_major_axis_length_cm=geometry.cm_x if geometry.cm_x > geometry.cm_y else geometry.cm_y
        self.m_minor_axis_length_cm=geometry.cm_x if geometry.cm_x < geometry.cm_y else geometry.cm_y
        self.m_major_axis_inclination=geometry.major_axis_inclination

    def getGeometry(self):
        return Geometry(shape_id=self.m_shape_id, 
                        cm_major_axis_length=self.m_cm_major_axis, 
                        cm_minor_axis_length=self.m_cm_minor_axis)        

    pass



class Rectangle(Shape):
    
    # FOR N-GONS, WITH FINITE N
    SIDE_NDX_TOP=0
    SIDE_NDX_RIGHT=1
    SIDE_NDX_BOTTOM=2
    SIDE_NDX_LEFT=3
    SIDE_MODULUS=4
   
    def __init__(self, geometry:Geometry, place:Placement):
        assert(geometry.shape_id==Shape.SHAPE_ID_RECTANGLE)
        super(Shape,self).__init__(geometry, place)
        pass


    def oppositeSide(self, side_index):
        return side_index+2 % self.SIDE_MODULUS

    def nextSideCW(self, side_index):
        if side_index<self.SIDE_NDX_LEFT:
            return side_index+1
        else:
            return self.SIDE_NDX_TOP
        
    def nextSideCCW(self, side_index):
        if side_index>self.SIDE_NDX_TOP:
            return side_index-1
        else:
            return self.SIDE_NDX_LEFT



class Ellipse(Shape):
    def __init__(self, geometry:Geometry, place:Placement):
        assert (geometry.shape_id==Shape.SHAPE_ID_ELLIPSE)
        super(Shape,self).__init__(geometry, place)
    pass




AdjacentDescriptor=namedtuple("AdjacentDescriptor", "room_id side_ndx ccw_endpoint cw_endpoint")
PortalDescriptor=namedtuple("PortalDescriptor", "room_id side_ndx ccw_endpoint cw_endpoint")


class Room(Rectangle):
    '''
    SIDE_NDX_ are sequenced enumerations intended to identify a box side
    and to inentify a sequence for processing (clockwise)
    '''


    m_insider_list=None
    m_adjacent_room_list=None
    m_spanner_list=None
    m_portal_list=None
    m_adjacent_list=None

    def __init__(self,
                 geometry:Geometry,
                 place:Placement,
                 insider_list=[],
                 adjacent_room_list=[],
                 portal_list=[],
                 spanner_list=[]):
        '''
        Constructor
        '''
        
        super(Rectangle,self).__init__(geometry, place)
        self.m_insider_list=insider_list
        self.m_adjacent_room_list=adjacent_room_list
        self.m_portal_list=portal_list
        self.m_spanner_list=spanner_list
        self.initAdjacencyLocks()


    def getAdjacentRooms(self) -> list:
        return self.m_adjacent_room_list

    def setAdjacentRooms(self, adjacent_rooms: list):
        self.m_adjacent_room_list=adjacent_rooms
        
    def getAdjacentRoomCount(self):
        return len(self.m_adjacent_room_list)
        

    '''
    Adjacency Change Control
    The Room may control whether other rooms may be located adjacent.
    The design of the control criteria is external to this class.
    The enforcement, however, is intrinsic.
    '''
    m_adjacency_side_locks=None

    def initAdjacencyLocks(self):
        self.m_adjacency_side_locks=[False, False, False, False]
    
    def adjacencyLocked(self) -> bool:
        if not True in self.m_adjacent_side_locks:
            return True

    def setAdjacencySideLock(self, side_index:int, status:bool):
        self.m_adjacency_side_lock[side_index]=status

    def adjacencySideLocked(self, side_index) -> bool:
        return self.m_adjacency_side_lock[side_index]

    def addAjacentRoom(self, adjacent_room: [AdjacentDescriptor]):
        assert(self.adjacencySideLocked(adjacent_room.side_ndx)==False)
            
        if self.m_adjacent_list==None:
            self.m_adjacent_room_list=[adjacent_room]
        else:
            self.m_adjacent_room_list.append(adjacent_room)

        
        
    def addInsider(self, shape:Shape, place:Placement):

        try:
            self.checkInsider(self.m_shape, place)
        except ShapeOutOfBounds:
            return False
        finally:
            pass
        
        if self.m_insider_list==None:
            self.m_insider_list=[]
            
        self.m_insider_list.append([shape,place])
        return True

    def addSpanner(self, shape:Shape, place:Placement):
        pass
        
    def addPortal(self, place):
        pass



    '''
    checkInsider()
    verify the inside object is 'inside'
    '''

    def checkInsider(self, shape:Shape, place:Placement):

        # verify shape center is inside room
        # verify shape does not cross room boundaries
        shape_location=[place.x, place.y]
        shape_x=shape_location[0]
        shape_y=shape_location[1]
        shape_theta=place.theta
        shape_geometry=shape.getShape()

        shape_dimensions=self.m_shape.getDimensions()
        shape_x_length=shape_dimensions[0]
        shape_y_length=shape_dimensions[1]

        if ( shape_x<0 or shape_x>self.m_x_length ) \
          or (shape_y<0 or shape_y>self.m_y_length):
            raise ShapeOutOfBounds

        if shape_geometry == Shape.SHAPE_ID_SQUARE:
            '''
            from height and lenght, compute the extension in x and y
            axes from the center of the Shape.
            '''
            x_extension=(shape_x_length/2)*math.sin(shape_theta) \
                      + (shape_y_length/2) * math.cos(shape_theta)

            left_x=shape_x-x_extension
            right_x=shape_x+x_extension
            if (left_x<0 or right_x>self.m_x_length):
                raise ShapeOutOfBounds


            y_extension=((shape_x_length/2)*math.sin(shape_theta)) \
                      + (shape_y_length/2)*math.cos(shape_theta)

            top_y=shape_y+y_extension
            bottom_y=shape_y-y_extension

            if (bottom_y<0 or top_y>self.m_y_length):
                raise ShapeOutOfBounds

            return True
        
    def checkSpanner(self, shape:Shape, place:Placement):
        pass
    

class ObjectProfile(object):

    m_room_object=None
    m_detector_place=None

    def __init__(self ):
        pass

    def computeProfile(self, detector_place:Placement):
        '''
        compute the profile binary function on interval 0, 2*pi
        '''
        self.m_detector_place=detector_place


class RoomProfile(object):
    '''
    classdocs
    '''

    m_detector_place=None

    def __init__(self, detector_place:Placement):
        self.m_detector_place=detector_place





class World(object):
    '''
    classdocs
    '''
    EOLIST=-1
    m_room_list=None        # room handles
    m_shape_lists=None      # room shape lists
    m_profile_lists=None    # room scanned/computed profiles

    m_terrain_filename=None

    def __init__(self, terrain_filename):
        self.m_terrain_filename=terrain_filename
        self.worldTerrain=terrainFile(self.m_world_filename)
        # open the world file
        # parse room list
        # parse shape list, associate to a room
        # parse profile list, associate to a room

        self.m_room_ndx=None


    def roomCount(self):
        if self.m_room_list==None:
            return 0
        else:
            return len(self.m_room_list)


    def roomHandle(self, index):
        return self.m_room_list[index]


    def firstRoomHandle(self):
        if self.m_room_list==None:
            return None
        else:
            self.m_room_ndx=0
            return self.roomHandle(0)

    def nextRoomHandle(self):
        if self.m_room_ndx==None:
            return None
        else:
            self.m_room_ndx+=1
            if self.m_room_index<len(self.m_room_list):
                return self.roomHandle(self.m_room_ndx)
            else:
                return self.EOLIST



class Locate(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        constructor
        '''



    pass
