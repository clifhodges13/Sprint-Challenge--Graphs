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
map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

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

# populate graph entry with '?' for each exit
# def pop_graph(current_room):
#     # get all exits for current room
#     exits = current_room.get_exits()
#     # initialize graph entry for room
#     traversal_graph[current_room.id] = {}
#     # loop through exits and add to room entry in graph
#     for e in exits:
#         traversal_graph[current_room.id][e] = '?'
#     print(exits)
#     return exits

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# graph to keep up with rooms and their neighboring rooms
traversal_graph = {}

s = [[player.current_room]]

# c = s.pop()
# print(c)
# exits = c[-1].get_exits()
# print(exits)

# for e in exits:
#     get_room = c[-1].get_room_in_direction(e)
#     exits_2 = get_room.get_exits()
#     output_2 = {}
#     for r in exits_2:
#         output_2[r] = '?'
#     output = {
#         e: output_2
#     }
#     s.append(output)

# print(s)








# while the stack is not empty:
while len(s) > 0:
    # pop off the current room from the stack
    path_to_current_room = s.pop() # this is a list
    
    if path_to_current_room[-1].id not in traversal_graph: # if the current room is not already in the graph
        # get all exits for current room
        exits = path_to_current_room[-1].get_exits()
        # initialize graph entry for room
        traversal_graph[path_to_current_room[-1].id] = {}
        # loop through exits and add to room entry in graph
        for e in exits:
            traversal_graph[path_to_current_room[-1].id][e] = '?'

    # print(traversal_graph)
    # pick random unexplored direction
    random.shuffle(exits)
    rand_dir = exits[0]
    # print('EXITS   ', exits)
    # save the previous room
    prev_room = path_to_current_room[-1]
    # print('PREV    ', traversal_graph[prev_room.id])

    prev_room_graph = traversal_graph[prev_room.id]

    # if the current room has no way to go, we need to do our BFS to find the nearest room with an unexplored route
    if all([e in prev_room_graph and prev_room_graph[e] != '?' for e in player.current_room.get_exits()]):
        # TODO:
        print('WEVE REACHED THE BFS CASE!')
        print('stack',s)

        unexplored = False
        for path in s[-1].reverse():
            exits = path[-1].get_exits()
            for direction in exits:
                room = traversal_graph[direction]
                print(room.id)


    # if that direction is unexplored:
    if rand_dir in prev_room_graph and prev_room_graph[rand_dir] == '?':
        # print('DIRECTION', rand_dir)
        # travel that direction and log
        traversal_graph[prev_room.id][rand_dir] = player.current_room.id

        if player.current_room.get_room_in_direction(rand_dir) is not None:
            traversal_path.append(rand_dir)
            player.travel(rand_dir)
        
        opp_dir = get_opposite(rand_dir)
        # log the prev_room room id in the current room on the graph
        # get all exits for current room
        exits = player.current_room.get_exits()
        # initialize graph entry for room
        traversal_graph[player.current_room.id] = {}
        # loop through exits and add to room entry in graph
        for e in exits:
            traversal_graph[player.current_room.id][e] = '?'
        
        traversal_graph[player.current_room.id][opp_dir] = prev_room.id
        # print('GET EXITS', exits)
        # append all adjacents rooms to stack
        for direction in exits:
            # take current path
            new_path = path_to_current_room.copy()
            # append the neighboring room to it
            new_path.append(player.current_room.get_room_in_direction(direction))
            # add the NEW path to the stack
            s.append(new_path)

print('stack',s)
print('graph',traversal_graph)
print('path ',traversal_path)

    # else: # BFS for last unexplored room
    #             # Create an empty queue and enqueue the PATH TO starting_vertex
    #     q = Queue()
    #     q.enqueue({
    #         'current_vertex': starting_vertex,
    #         'path': [starting_vertex]
    #     })
    #     # create an empty set to track visited vertices
    #     visited = set()

    #     # while the queue is not empty:
    #     while q.size() > 0:
    #         # get the current vertex PATH (dequeue from queue)
    #         current_obj = q.dequeue()
    #         current_path = current_obj['path']
    #         current_vertex = current_obj['current_vertex']
    #         # set the current vertex to the LAST element of the PATH

    #         # check if current vertex has not been visited:
    #         if current_vertex not in visited:
    #             # Check if the current vertex is destination
    #             if current_vertex == destination_vertex:
    #                 # IF IT IS, STOP AND RETURN THE PATH
    #                 return current_path

    #             # mark the current vertex as visited
    #             visited.add(current_vertex)

    #             # queue up all NEW paths with each neighbor:
    #             for p in self.get_neighbors(current_vertex):
    #                 # take current path
    #                 new_path = list(current_path)
    #                 # append the neighbor to it
    #                 new_path.append(p)
    #                 # queue up the NEW path
    #                 q.enqueue({
    #                     'current_vertex': p,
    #                     'path': new_path
    #                 })
    #     return None




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
