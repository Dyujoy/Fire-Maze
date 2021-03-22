import random

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
                    new_maze[i][j] = 2
    
    return new_maze           



def strat2_BFS(maze, path_setter, fringe, visited_set):

    goal = (len(maze)-1, len(maze)-1)
    move_pos = [(0,1),(1,0),(0,-1),(-1,0)]

    while len(fringe) != 0:
        current = fringe.pop(0)

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

# To get the actual path the agent takes.
def get_path(path_setter, path, first, dim):
    while path_setter[-1].parent != first and len(path_setter)!=0 :
            parent = path_setter[-1].parent
            while parent != path_setter[-1].current and len(path_setter)!=0:
                path_setter = path_setter[:-1]
            path_setter[-1].current
            path.append(path_setter[-1].current)
    path.append(first)
        
# To implement strategy 2 where for each step we re-run bfs.
def strat2(dim, p , q):
    entry1 = pathMaker((-1,-1),(0,0))
    path_setter = [entry1]

    fire_maze = generate_fire_maze(dim,p)
    print(fire_maze)

    fringe = [(0,0)]
    visited_set = [(0,0)]

    find_BFS_path = strat2_BFS(fire_maze, path_setter, fringe , visited_set )
    path = [(dim-1,dim-1)]

    if find_BFS_path == False:
        return -1

    if find_BFS_path == True:
        get_path(path_setter,path, (0,0), dim)
    path = path[::-1]
    
    # Till the second item in the path array is not the goal cell.
    while (path[1] != (dim-1,dim-1)):
        if fire_maze[path[0][0]][path[0][1]] == 2:
            return 0
        
        advance_fire_one_step(fire_maze,q)
               
        fringe = [path[1]]
        visited_set =[path[1]]
        entry1 = pathMaker((-1,-1),path[1])
        path_setter = [entry1] 
        path = [(dim-1,dim-1)]

        find_BFS_path = strat2_BFS(fire_maze, path_setter, fringe , visited_set )
        if find_BFS_path == False:
            return 0
        

        get_path(path_setter, path, visited_set[0] , dim)

        path = path[::-1]

    return 1

dim = 5
p = 0.3
q = 0.5
n=50

success = 0
failure = 0
not_count = 0
print('dim',dim)
print('p',p)
print('q',q)
for i in range(10):
    path_strat1 = strat2(dim,p,q)
    print(i,'ii')
    # while path_strat1 != -1:
    if path_strat1 == 0:
        failure += 1
        continue
    elif path_strat1 == 1:
        success +=1
        continue
    elif path_strat1 == -1:
        not_count +=1
        continue
        
    # path_strat1 = strat2(dim,p,q)


print('strat2',strat2(dim,p,q))
print('n =',n)
print('success',success)
print('failure', failure)
print('not counted', not_count)