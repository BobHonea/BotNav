'''
define_world.py

pre-define a world to support testing and debugging


scenario 1:
 metric 1 cm per unit
 1 room  square, 500 x 1000
 2 circular objects, [25..125] units dia., random placement
 2 rectangular objects, [25..125] units dia., random placement

'''


import random
from profile import Shape, Room, Rectangle, PortalSpec, Placement, Geometry
from profile import AdjacentDescriptor, PortalDescriptor
from collections import namedtuple
import vectormath as vmath



class doorGenerator():
    
    def __init__(self):
        pass
    

RoomGenParms=namedtuple(
      "RoomGenParms","room_count cm_length cm_width")

PerRoomGenParms=namedtuple(
      "PerRoomGenParms",
      "insider_count spanner_count cm_rectangle_length cm_rectangle_width portal_count cm_portal_width")

class World(object):
    '''
    '''



    m_default_room_genparms=RoomGenParms([3,4],[400,800],[400,800])
    m_default_per_room_genparms=PerRoomGenParms([2,6],[0,1],[20,200],[20,200],[0,4],[70,210])
    
    # define ranges for parameters to be selected at random
    # define scalars for explicit values
    m_room_genparms  : RoomGenParms = None
    m_per_room_genparms : PerRoomGenParms = None
    
    

    METRIC="CM"

    m_random=None
    m_room_count:int=None
    m_room_list:list=None
    m_spanner_list:list=None
    m_portal_list:list =None
    m_insider_list:list=None

    def __init__(self, 
                 room_genparms:RoomGenParms=None,
                 per_room_genparms:PerRoomGenParms=None):

        if room_genparms==None:
            self.m_room_genparms=self.m_default_room_genparms
            
        if per_room_genparms==None:
            self.m_per_room_genparms=self.m_default_per_room_genparms
            
        # Generate World per fixed/random generation parameters
        self.generate()

    '''
    Destructor Method
    ---nothing at the moment
    '''
    def __del__(self):
        pass

    m_reflection_transform=([-1,1],[1,1],[1,-1],[-1,-1])
    #m_side_normal=([1,0],[0,1],[1,0],[0,1])
    m_side_normal_vector=(vmath.Vector2(1,0), vmath.Vector2(0,-1), 
                          vmath.Vector2(-1,0), vmath.Vector2(0,1))
    m_hub_vertices:list=None

    def diameterVector(self, room:Room):
        dim=room.getDimensions()
        return(vmath.Vector2(dim[0], dim[1]))


    def vertexVector(self, room:Room, cw_side:int) -> vmath.Vector2:
        dim=room.getDimensions()
        return(vmath.Vector2(dim[0], dim[1])*0.5*self.m_reflection_transform[cw_side])
    
    def initHubVertices(self, hub_room:Room):
        self.m_hub_vertices=[]

        for ccw_side_ndx in range(Room.SIDE_NDX_LEFT):
            self.m_hub_vertices.append(self.vertexVector(hub_room, ccw_side_ndx))

    def getSideVector(self, room:Room, side_index):
        diameter:vmath.Vector2=self.diameterVector(room)
        normal:vmath.Vector2=self.m_side_normal_vector[side_index]
        return diameter.dot(normal)

        
    def getRoomList(self) -> list :
        return self.m_room_list
    
    def getInsiderList(self) -> list :
        return self.m_insider_list
    
    def getSpannerLlist(self) -> list :
        return self.m_insider_list
    
    def getPortalList(self) -> list :
        return self.m_portal_list
    
    def setCount(self, counts):
        if type(counts) == list :
            count=random.randint(counts[0],counts[1])
        else:
            count=counts
        return count

    def setPerRoomGenParms(self, per_room_genparms:PerRoomGenParms):
        self.m_per_room_genparms=per_room_genparms
        
    def setRoomGenParms(self, room_genparms:RoomGenParms):
        self.m_room_genparms=room_genparms

    def getRoomCountGenParm(self):
        return self.m_room_genparms.room_count
    
    def getRoomDimensionGenParms(self):
        return [self.m_room_genparms.cm_length, self.m_room_genparms.cm_width]
    
    def getInsiderCountGenParms(self):
        return self.WorldGenerator.m_per_room_genparms.insider_count
    
    
    '''
    generate_rooms()
    populate a list of rooms defined by a mix of fixed and ranged parameters
    pick parameters within ranges randomly
    '''
    def generate_rooms(self):
        if self.m_room_count==None:
            self.m_room_count=self.setCount(self.m_room_genparms.room_count)
        
        self.m_room_list=[]
        
        for room_ndx in range (self.m_room_count):
            x_length=self.setCount(self.m_room_genparms.cm_width)
            y_height=self.setCount(self.m_room_genparms.cm_length)
            room_placement=Placement(cm_x=0, cm_y=0, major_axis_inclination=0)
            room_geometry=Geometry(shape_id=Shape.SHAPE_ID_RECTANGLE,
                                    cm_major_axis_length=x_length,
                                    cm_minor_axis_length=y_height)
            
            this_room=Room(room_geometry, room_placement)
            self.m_room_list.append(this_room)

        return len(self.m_room_list)

    
    '''
    generate() a world based on generator counts/count-ranges

    generate world psuedocode

      set room adjacency

    '''
    def generate(self):

        '''
        generate room_count

          for each room
            set room size
            locate room
            populate insider_count
        '''
        
        self.m_room_count=self.setCount(self.m_default_room_genparms.room_count)

        self.generate_rooms()
        
        self.locateRooms()

        # assuming room_count > 0
        for room_id in range(1,self.m_room_count):
            self.setPerRoomGenParms(self.m_default_per_room_genparms)

        '''
          for each room
            for each portal
              identify adjacent room
              identify adjacent wall
              generate portal
              assign portal to both room_count
        '''

        '''
            for each spanner
              identify portal
              locate spanner
              assign spanner to both room_count
        '''
        '''
            for each insider
              locate insider
              assign insider to room
        '''

        pass


    '''
    locateRooms()
    Generate a list of room_count of random size and undefined locations
    Assign one room as the hub room
    Systematically construct a floor plan from the room_count
        locate successive room_count clockwise adjacent to the hub room
        until no space remains for an adjacent assignment     list of predefined rectangular room_count of varying sizes

        assign hub status to a recently located room
        continue
        
    For each located room, update the following
        list of adjacent room_count
        
    allocateInsiders()
        generate a list of Rectangles of moveable objects
        randomy
    Algorithm:
    '''


        
    def registerNeighborAdjacencies(self, room_list: list , hub_room:Room):
        

        
        '''
        Duplicate first adjacent descriptor at end of list
        Makes the test 'circular'. Last and first may be adjacent.
        TypeA Adjacency: room_count share common hub_room wall
        TypeB Adjacency: room_count share common hub_room vertex
                         among their adjacency endpoints
        '''    
        hub_adjacent_room_descriptors=hub_room.getAdjacentRooms()
        hub_adjacent_room_descriptors.append(hub_adjacent_room_descriptors[-1])
        
        # loop on all except last descriptor entry
        for ccw_rmndx in range(len(hub_adjacent_room_descriptors[:-1])):
           
            cw_rmndx=ccw_rmndx+1
            
            ccw_descriptor=hub_adjacent_room_descriptors[ccw_rmndx]
            cw_descriptor=hub_adjacent_room_descriptors[cw_rmndx]
                
            ccw_hub_adj_side=ccw_descriptor.side_ndx
            cw_hub_adj_side=cw_descriptor.side_ndx
            
            ccw_room=room_list[ccw_descriptor.room_id]
            cw_room=room_list[cw_descriptor.room_id]
            
    
            '''
            This detection works since the room_count are located adjacent to
            the hub room in clockwise order. Simpler than general algorithm.
    
            Iso-Hedral Adjacent Rooms:
                both room_count are adjacent to the same hub room side
    
            Ortho-Hedral Adjacent Rooms:
                room_count are adjacent to orthogonal hub room sides
            '''    
    
            iso_hedral=ccw_hub_adj_side==cw_hub_adj_side
            
            if iso_hedral:
                ccw_adj_side=Rectangle.nextSideCCW(ccw_hub_adj_side)
                cw_adj_side=Rectangle.oppositeSide(ccw_adj_side)
            else: # ortho-hedral
                ccw_adj_side=Rectangle.oppositeSide(ccw_hub_adj_side)
                cw_adj_side=Rectangle.nextSideCW(cw_hub_adj_side)
            # processing for iso-hedral, and ortho-hedral adjacency is the 
            # same, from this point forward
    
            '''
            the clockwise adjacent endpoint of the first room
            must match the counter-clockwise endpoint the next room. 
            '''
                
            assert(ccw_descriptor.cw_endpoint == cw_descriptor.ccw_endpoint)
    

            ccw_room_dimensions=ccw_room.getDimensions()
            ccw_room_diameter=vmath.Vector2(ccw_room_dimensions[0], ccw_room_dimensions[1])
            ccw_adj_side_length=(ccw_room_diameter*self.m_side_normal[ccw_adj_side]).length

            cw_room_dimensions=cw_room.getDimensions()
            cw_room_diameter=vmath.Vector2(cw_room_dimensions[0], cw_room_dimensions[1])
            cw_adj_side_length=(cw_room_diameter*self.m_side_normal[cw_adj_side]).length
    
    
            if ccw_adj_side_length>cw_adj_side_length:
                length_difference=ccw_adj_side_length-cw_adj_side_length
                ccw_side_short=False
            else:
                length_difference=cw_adj_side_length-ccw_adj_side_length
                ccw_side_short=True
    
    
            ccw_adj_descriptor=ccw_room.AdjacentDescriptor(ccw_rmndx, ccw_adj_side,
                                                           0 if ccw_side_short else length_difference,
                                                           ccw_adj_side_length)
            cw_adj_descriptor=cw_room.AdjacentDescriptor(cw_rmndx, cw_adj_side,
                                                           length_difference if ccw_side_short else 0,
                                                           ccw_adj_side_length)
            
            ccw_room.addAdjacentRoom(ccw_adj_descriptor)
            cw_room.addAdjacentRoom(cw_adj_descriptor)


    def locateRooms(self):

        self.m_room_list=[]
        room_list=self.m_room_list


        hub_index=None
        hub_room=None
        hub_side_ndx=None
        hub_origin=None

        for room_index in range(len(room_list)):
            room=room_list[room_index]

            if hub_room==None:
                if room_index==0:   # allocate INITIAL hub_room
                    hub_index=room_index
                    hub_room=room
                    hub_room.setPlacement( Placement(cm_x=0.0, cm_y=0.0, major_axis_inclination=0))
                    hub_side_ndx=Room.SIDE_NDX_TOP
                    self.initHubVertices(hub_room)
                    hub_origin_vector=room.getOriginVector()              
                    CCW_adj_point=self.vertexVector(hub_room, Room.SIDE_NDX_TOP)
                    continue
                else:               # allocate ANTECEDENT hub_room
                    '''
                    The hub_room has no more adjacent space to locate room_count
                    All adjacencies among the located room_count have been registered
                    
                    ASSIGN a new hub_room
                    Then continue locating room_count
    
                    Pick next hub room randomly from room_count adjacent to the present hub room
                    '''
                    hub_adjacent_room_descriptors=hub_room.getAdjacentRooms()
                    randndx=random.randint(0,len(hub_adjacent_room_descriptors)-1)
                    hub_room_descriptor=hub_adjacent_room_descriptors[randndx]
                    hub_index=hub_room_descriptor.room_id
                    hub_room=room_list[hub_index]
                    hub_index=None
                    hub_origin=room.getOriginVector()
                    continue
                

            '''
            Locate rooms adjacent to the hub_room in clockwise order
            '''
            room_side_ndx=room.oppositeSide(hub_side_ndx)

            room.setPlacement(Placement(cm_x=CCW_adj_point.x, cm_y=CCW_adj_point.y,major_axis_inclination=0))
                    
            '''
            register mutual adjacency with hub and located room
            '''

             
            room_adj_side_vector=self.getSideVector(room, hub_side_ndx)           
            room_adj_side_length=room_adj_side_vector.length
            hub_adj_side_vector=self.getSideVector(hub_room,hub_side_ndx)
            hub_adj_side_length=hub_adj_side_vector.length
            
            last_room_on_side=room_adj_side_length >= hub_adj_side_length
            CW_adj_point=CCW_adj_point+(hub_adj_side_vector if last_room_on_side else room_adj_side_vector)

            '''                            
            Note the opposing chirality of adjacent segment end points
            '''
            room.addAjacentRoom( AdjacentDescriptor(   room_id=hub_index, 
                                                       side_ndx=room.oppositeSide(hub_side_ndx), 
                                                       cw_endpoint=CW_adj_point, 
                                                       ccw_endpoint=CCW_adj_point ))
                                                   
            hub_room.addAdjacentRoom( AdjacentDescriptor(room_id=room_index, 
                                                        side_ndx=hub_side_ndx, 
                                                        cw_endpoint=CCW_adj_point, 
                                                        ccw_endpoint=CW_adj_point))
            
    
            if not last_room_on_side:
                # neighborless space on this side exists
                # continue locating rooms from CW adjacent room boundary
                CCW_adj_point=CW_adj_point
                continue
            else:
                # adjacent space on this side exhausted, continue locating on next CW side
                room.setAdjacencySideLock(room.oppositeSide(hub_side_ndx))
                hub_side_ndx=hub_room.nextSideCW(hub_side_ndx)
                if hub_side_ndx!=Rectangle.SIDE_NDX_TOP:
                    # neighborless sides remain
                    CCW_adj_point=self.vertexVector(hub_room, Room.nextSideCW(self, hub_side_ndx))
                    continue
                else:
                    '''
                    Neighborless hub-room facets are exhausted
                    Before establishing another hub-room, detect and register adjacencies
                    between rooms tangent to this hub-room.
                  
                    If 2 or more adjacent rooms have been located, scan for adjacencies
                    between them. Register those inter-room adjacencies.
                    '''
                    hub_adjacent_room_descriptors=hub_room.getAdjacentRooms()
                    if len(hub_adjacent_room_descriptors) > 1:
                        self.registerNeighborAdjacencies(self, room_list, hub_room)
                
                    continue
                
                

            continue
        
        '''
        Rooms have been located
        '''
        return True