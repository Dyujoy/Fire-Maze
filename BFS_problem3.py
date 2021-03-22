import random

# Class to keep the parent position and current position of the cell. Thus, we can find the path as we move backwards from the end cell.
class pathMaker:
    def __init__(self, parent, current ):
        self.parent = parent
        self.current = current
    
    def parent(self):
        return self.parent
    def current(self):
        return self.current

# Generate the maze where the blocked cells are placed.
def generate_maze(dim, p):
    # 2-D Array for the maze. Put 0 in all the cells. 0 for all cells which are not occupied.
    maze = [[0 for i in range (dim)] for i in range(dim) ]
    for x in range(len(maze)):
        for y in range(dim):
            
            r = random.uniform(0,1)
            # If r is less than the input obstacle density then fill the maze cell.
            if r < p:
                # If filled then put 1 in that cell.
                maze[x][y] = 1
    maze[0][0] = 0
    maze[dim-1][dim-1] = 0
    return maze

# Breadth First Search for the maze.
def BFS(maze, path_setter ):
    fringe = [(0,0)]
    visited_set = [(0,0)]

    # Goal position of the path.
    goal = (len(maze)-1, len(maze)-1)

    # The only positions the cell can move from the current position.
    move_pos = [(0,1),(1,0),(0,-1),(-1,0)]

    while len(fringe) != 0:
        # Current cell from the fringe.
        current = fringe.pop(0)

        # If we reach the goal position then return True.
        if current[0] == goal[0] and current[1] == goal[1]:
            return True

        # If the current position is not in fringe.
        if current not in fringe:
            # for lopp for every possible position the agent can move.
            for i in move_pos:

                # We do not consider if the agent has been to a previous visited cell.
                if (i[0] + current[0],i[1] + current[1]) not in visited_set:
                    
                    # If the move to the next position is illegal or not i.e the agen does not go out of the maze.
                    if (i[0] + current[0]) > len(maze)-1 or (i[1] + current[1]) > len(maze)-1 or (i[0] + current[0]) < 0 or (i[1] + current[1]) < 0:
                        continue
                    
                    # Check if the position moved to is not occupied.
                    if maze[i[0] + current[0]][i[1] + current[1]] != 1 and (i[0] + current[0],i[1] + current[1]) not in fringe:
                        fringe.append((current[0] + i[0],current[1]+i[1]))
                        # Keep a track of all the cells visited. Put the parent cell and the current cell together.
                        path_setter.append(pathMaker(current,(i[0] + current[0], i[1] + current[1] )))
        # Keep a track of all the cells visited by agent.
        visited_set.append(current)
    
    # Return false if no path.
    return False


# To get the actual path from start to end.
def get_path_BFS_problem_3(dim,p):

    #First entry of the path_setter.
    entry1 = pathMaker((-1,-1),(0,0))
    # Keep tracks of the all the cells the agent has visited. Keep the parent cell and visited cell together.
    path_setter = [entry1]

    maze = generate_maze(dim,p)

    find_BFS_path = BFS(maze, path_setter)

    path = [(dim-1,dim-1)]

    # No path then return 0 i.e length of the path is 0.
    if find_BFS_path == False:
        return 0


    if find_BFS_path == True:
        # While the parent at the end position of the path_setter is not the starting position and path_setter is not empty.
        while path_setter[-1].parent != (0,0) and len(path_setter)!=0:

            # Initiate the parent of end position of the path_setter.
            parent = path_setter[-1].parent

            # while the end position's current of the class path_setter is not equal to the parent. 
            while parent != path_setter[-1].current and len(path_setter)!=0:
                # Keep removing the end position of path_setter.
                path_setter = path_setter[:-1]

            # Add the end position's current of path_setter to the actual path the agent follows.
            path.append(path_setter[-1].current)

    path.append((0,0))
    path = path[::-1]

    return path


dim = 100
p = 0.5
print('dim',dim)
print('p',p)

path_length = []
failure = 0
for i in range(20):
    path_BFS_problem_3 = get_path_BFS_problem_3(dim,p)
    if path_BFS_problem_3 == False:
        failure += 1
        continue
    # print(path_BFS_problem_3)
    path_length.append(len(path_BFS_problem_3))
while path_BFS_problem_3 != True:
    path_BFS_problem_3 = get_path_BFS_problem_3(dim,p)
    print('show')
    if path_BFS_problem_3 == False:
        failure += 1
        continue
    path_length.append(len(path_BFS_problem_3))

print('success',path_length)
print('fail',failure)