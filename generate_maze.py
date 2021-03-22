import random

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

 
dim = int(input())
p = float(input())
 
maze = generate_maze(dim,p)
print(maze)