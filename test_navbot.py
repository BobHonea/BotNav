'''
test_navbot.py

generate worlds
test navbot modules
'''

import define_world as defworld

'''
create a world
save it to a file
'''


def main():

    # use default world generator parameters
    
    RoomWorld=defworld.World()
    RoomWorld.generate()
    pass


main()