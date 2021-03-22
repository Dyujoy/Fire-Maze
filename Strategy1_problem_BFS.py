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

# Generate the maze where the blocked cells and first fire are placed.
def generate_fire_maze(dim, p):
    
    # 2-D Array for the maze. Put 0 in all the cells. 0 for all cells which are not occupied.
    maze = [[0 for i in range (dim)] for i in range(dim) ]
    for x in range(len(maze)):
        for y in range(dim):
            r = random.uniform(0,1)
            if r < p:
                maze[x][y] = 1

    # get the random position of the cell where the fire should start.
    x1 = random.randrange(0,dim-1)
    y1 = random.randrange(0,dim-1)
    
    # while the fire is not in either the top left corner nor the bottom corner cell.
    while (x1 == 0 and y1 == 0) or (x1 == dim-1 and y1 == dim-1):
        x1 = random.randrange(0,dim-1)
        y1 = random.randrange(0,dim-1)


    maze[x1][y1] = 2
    maze[0][0] = 0
    maze[dim-1][dim-1] = 0
    return maze


# Breadth First Search for the Strategy 1
def strat1_BFS(maze, path_setter ):
    fringe = [(0,0)]
    visited_set = [(0,0)]

    # Goal position of the path.
    goal = (len(maze)-1, len(maze)-1)
    
    # The only positions the cell can move from the current position.
    move_pos = [(0,1),(1,0),(0,-1),(-1,0)]
    
    while len(fringe) != 0:
        # Current cell from the fringe.        
        current = fringe.pop(0)
        
        # If we reach the goal position then return True
        if current[0] == goal[0] and current[1] == goal[1]:
            return True
        
        if current not in fringe:
            for i in move_pos:
                if (i[0] + current[0],i[1] + current[1]) not in visited_set:
                    
                    if (i[0] + current[0]) > len(maze)-1 or (i[1] + current[1]) > len(maze)-1 or (i[0] + current[0]) < 0 or (i[1] + current[1]) < 0:
                        continue
                    if maze[i[0] + current[0]][i[1] + current[1]] != 1 and (i[0] + current[0],i[1] + current[1]) not in fringe and maze[i[0] + current[0]][i[1] + current[1]] != 2:
                        fringe.append((current[0] + i[0],current[1]+i[1]))
                        path_setter.append(pathMaker(current,(i[0] + current[0], i[1] + current[1] )))
                        
        visited_set.append(current)
        
    return False


# To advance the fire after each step
def advance_fire_one_step(maze, q):
    
    new_maze = maze
    move_pos = [(0,1),(1,0),(0,-1),(-1,0)]
    for i in range(len(maze)):
        for j in range(len(maze)):
            if maze[i][j] !=2 and maze[i][j]!=1:
                k=0
                for a in move_pos:
                    if (a[0] + i) > len(maze)-1 or (a[1] + j) > len(maze)-1 or (a[0] + i) < 0 or (a[1] + j) < 0:
                        continue
                    if maze[a[0]+i][a[1]+j] == 2:
                        k+=1
                prob = 1- (1-q)**k
                r = random.uniform(0,1)
                if r <= prob:
                    # new_maze cell is on fire hence is 2
                    new_maze[i][j] = 2
    
    return new_maze           

def strat1(dim,p,q):

    entry1 = pathMaker((-1,-1),(0,0))
    path_setter = [entry1]

    fire_maze = generate_fire_maze(dim,p)

    print(fire_maze)

    find_BFS_path = strat1_BFS(fire_maze, path_setter)
    path = [(dim-1,dim-1)]

    if find_BFS_path == False:
        return -1

    # Get the initial path of agent from the start to end.
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
            path_setter[-1].current
            path.append(path_setter[-1].current)
    path.append((0,0))
    path = path[::-1]

    # for each position of the initial path we move, we also call advance_fire_one_step. 
    for i in path:
        # If the initial path meets a fire we return 0 i.e failed.
        if fire_maze[i[0]][i[1]] == 2:
            return 0
        # Call the next fire step.
        fire_maze = advance_fire_one_step(fire_maze,q)
    return 1


dim = 5
p = 0.3
q = 0.1
n=5

success = 0
failure = 0
print('dim',dim)
print('p',p)
print('q',q)
for i in range(n):

    path_strat1 = strat1(dim,p,q)
    if path_strat1 == 0:
        failure += 1
        continue
    elif path_strat1 == 1:
        success+=1

print('n =',n)
print('success',success)
print('failure', failure)