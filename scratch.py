'''
Created on Feb 1, 2021

@author: Asus
'''

    def scalarLocateRooms(self, room_list: list[RoomObject]):

        HubAdjacency=namedtuple("HubAdjacency", "side_id side_offset")

        hub_room=None
        hub_index=None
        room_index=0
        room_origin=[0,0]

        for room_index in range(len(room_list)):
            this_room=RoomObject(room_list[room_index])

            if hub_room==None:
                hub_index=room_index
                hub_room=this_room
                hub_origin=room_origin
                this_placement=Placement(hub_origin[0], hub_origin[1], 0)
                hub_dimensions=hub_room.getDimensions()
                hub_room.setPlacement(hub_placement)
                hub_adjacent_side=RoomObject.SIDE_ID_TOP
                hub_adjacent_offset=0

                offset_vector=vmath.Vector2()
                
                continue

            '''
            Set Adjacency of this_room to the hub room
            Allocate space in a spiral order:
              Set ajdacents to Top, then Right, then Bottom, then Left
            '''
        this_dimensions=this_room.shape.getDimensions()

        if hub_adjacent_side == RoomObject.SIDE_ID_TOP:
            this_origin_x=hub_origin[0]+hub_adjacent_offset-hub_dimensions[0]/2+this_dimensions[0]/2
            this_origin_y=hub_origin[1]+hub_dimensions[1]/2+this_dimensions[1]/2
            
            adjacent_l1=hub_dimensions[0]-hub_adjacent_offset
            adjacent_l2=this_dimensions[0]
            if adjacent_l1 > adjacent_l2:
                adj_length=adjacent_l2
            else:
                adj_length=adjacent_l1
            
            adj_end1=-this_dimensions[0]/2
            adj_end2=-this_dimensions[0]/2 + adj_length
            
            
            hub_adjacent_offset+=this_dimensions[0]
            if hub_dimensions[0]<=hub_adjacent_offset:
                hub_adjacent_side=RoomObject.SIDE_ID_RIGHT
                hub_adjacent_offset=0
                

        
        
        elif hub_adjacent_side == RoomObject.SIDE_ID_RIGHT:
            this_origin_x=hub_origin[0]-hub_adjacent_offset+hub_dimensions[0]/2+this_dimensions[0]/2
            this_origin_y=hub_origin[1]+hub_dimensions[1]/2+this_dimensions[1]/2


            hub_adjacent_offset+=this_dimensions[1]
            if hub_dimensions[1]<=hub_adjacent_offset:
                hub_adjacent_side=RoomObject.SIDE_ID_BOTTOM
                hub_adjacent_offset=hub_dimensions[1]



        
        elif hub_adjacent_side == RoomObject.SIDE_ID_BOTTOM:
            this_origin_x=hub_origin[0]-hub_adjacent_offset+hub_dimensions[0]/2+this_dimensions[0]/2
            this_origin_y=hub_origin[1]-hub_dimensions[1]/2-this_dimensions[1]/2

            adjacent_l1=-hub_dimensions[0]+hub_adjacent_offset
            adjacent_l2=this_dimensions[0]
            if adjacent_l1 > adjacent_l2:
                adj_length=adjacent_l2
            else:
                adj_length=adjacent_l1
            
            adj_end1=-this_dimensions[0]/2
            adj_end2=-this_dimensions[0]/2 + adj_length

            hub_adjacent_offset+=this_dimensions[0]
            if hub_dimensions[0]>=hub_adjacent_offset:
                hub_adjacent_side=RoomObject.SIDE_ID_RIGHT
                hub_adjacent_offset=0

            
        elif hub_adjacent_side == RoomObject.SIDE_ID_LEFT:
            this_origin_x=hub_origin[0]+hub_adjacent_offset-hub_dimensions[0]/2+this_dimensions[0]/2
            this_origin_y=hub_origin[1]-hub_dimensions[1]/2-this_dimensions[1]/2

            adjacent_l1=hub_dimensions[1]-hub_adjacent_offset
            adjacent_l2=this_dimensions[1]
            if adjacent_l1 > adjacent_l2:
                adj_length=adjacent_l2
            else:
                adj_length=adjacent_l1
            
            adj_end1=-this_dimensions[1]/2
            adj_end2=-this_dimensions[1]/2 + adj_length

            hub_adjacent_offset+=this_dimensions[1]
            if hub_dimensions[1]<=hub_adjacent_offset:
                hub_adjacent_side=RoomObject.SIDE_ID_BOTTOM
                hub_adjacent_offset=hub_dimensions[1]


        '''
        The placment has been computed, and spiral offset advanced
        '''
        this_placement=Placement(this_origin_x, this_origin_y, 0)
        this_room.setPlacement(this_placement)
        this_adjacent=RoomObject.AdjacentDescriptor(room_id=hub_index, side_id=RoomObject.SIDE_ID_BOTTOM, ccw_point=adj_end1, cw_point=adj_end2 )


        continue
    
    '''
    Rooms have been located
    '''

    def prevSideNdx(self, sidendx):
        if sidendx==RoomObject.SIDE_NDX_TOP:
            return RoomObject.SIDE_NDX_LEFT
        else:
            return sidendx-1

    def nextSideNdx(self, sidendx):
        if sidendx==RoomObject.SIDE_NDX_RIGHT:
            return RoomObject.SIDE_NDX_TOP
        else:
            return sidendx+1

    def oppositeSideNdx(self, sidendx):
        return (sidendx+2)%4
        
