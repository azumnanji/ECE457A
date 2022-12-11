from queue import PriorityQueue
maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]]

goals = [[21, 2], [19, 23]]
start_pos = [11,2]

class Node:
    def __init__(self, pos, g):
        self.pos = pos
        
        # calculate min manhattan distance to goal
        min_dist = min((abs(pos[0] - goals[0][0]) + abs(pos[1] - goals[0][1])), (abs(pos[0] - goals[1][0]) + abs(pos[1] - goals[1][1])))
        self.h = min_dist
        self.g = g
        self.f = self.h + g

start = Node(start_pos, 0)

def printPath(curr_node, start_pos, cost, visited_nodes, maze):
    print('Goal Node: ' + str(curr_node))
    print('Cost: ' + str(cost))
    print('Num nodes visited: ' + str(len(visited_nodes)))

    visited_nodes = [visited.pos for visited in visited_nodes]
    #print path
    for i in range(len(maze)):
        path = ''
        for j in range(len(maze[i])):
            if [i,j] == start_pos:
                path += 'S'
            elif [i,j] == curr_node:
                path += 'G'
            elif [i,j] in visited_nodes:
                path += 'x'
            else:
                path += str(maze[i][j])
        print(path)

def checkSmallerNodeInVisited(node, visited):
    for n in visited:
        if n.pos == node.pos and n.f <= node.f:
            return True

def checkSmallerNodeInOpen(node, open_list):
    for _,_,_,n in open_list.queue:
        if n.pos == node.pos and n.f <= node.f:
            return True

# start search
print('A* Search')

visited = []
open_list = PriorityQueue()

# break ties based on y coordinate then x coordinate
open_list.put((start.f, start.pos[1], start.pos[0], start))
cost = 1

while not open_list.empty():
    current = open_list.get()[3]
    visited.append(current)

    if current.pos in goals:
        printPath(current.pos, start_pos, current.g, visited, maze)
        break

    new = []

    # check left, down, right, up
    if current.pos[1] - 1 >= 0:
        new.append([current.pos[0], current.pos[1] - 1])
    if current.pos[0] + 1 < 25:
        new.append([current.pos[0] + 1, current.pos[1]])
    if current.pos[1] + 1 < 25:
        new.append([current.pos[0], current.pos[1] + 1])
    if current.pos[0] - 1 >= 0:
        new.append([current.pos[0] - 1, current.pos[1]])
    
    for cell in new:
        if maze[cell[0]][cell[1]] == 1:
            continue
        node = Node(cell, current.g + 1)
        # check in visited list if there exists same node with smaller f
        # check in open list if there exists same node with smaller f
        if not checkSmallerNodeInVisited(node, visited) and not checkSmallerNodeInOpen(node, open_list):
            open_list.put((node.f, node.pos[1], node.pos[0], node))
    cost += 1

