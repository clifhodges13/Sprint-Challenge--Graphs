from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# get opposite direction
def get_opposite(direction):
    if direction == 'n':
        return 's'
    if direction == 's':
        return 'n'
    if direction == 'e':
        return 'w'
    if direction == 'w':
        return 'e'

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# graph to keep up with rooms and their neighboring rooms
"""
{
    room_id: { directions_travelled_when_leaving_this_room }
}
"""
visited = {} # keep track of visited rooms


stack = [(player.current_room, None)] # (current_room, direction_travelled_from)


while len(stack) > 0: # loop while the stack is not empty

    current_room = stack[-1][0] # current room is first position of last item on stack
    travelled_direction = stack[-1][1] # direction travelled is second position of last item on stack

    if current_room.id not in visited: # if the current room not visited
        visited[current_room.id] = set() # initialize with a set

    if travelled_direction: # if the direction travelled exists
        visited[current_room.id].add(travelled_direction) # add that direction to the room set

    if len(visited) == len(room_graph): # if the number of rooms visited matches the number of rooms in the room graph
        break # break out of the loop

    exits = [e for e in current_room.get_exits() if e not in visited[current_room.id]] # get a list of exits not travelled

    rand_dir = random.choice(exits) if len(exits) > 0 else None # if there are exits to choose from, pick a random one
    opp_dir = get_opposite(rand_dir) # get the opposite of the random direction

    if rand_dir != None: # if there's a direction available
        visited[current_room.id].add(rand_dir) # add that direction to the room set
        stack.append((current_room.get_room_in_direction(rand_dir), opp_dir)) # put the next room on the stack with the direction travelled from
        traversal_path.append(rand_dir) # add the direction to the traversal path

    else: # if no directions are available
        traversal_path.append(travelled_direction) # add the direction travelled to the traversal path
        stack.pop() # take the previous room off the stack




# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
