# Author: Nolan Donaldson
# Maze project

# Used to store extra information during BFS search
class vertex:
    def __init__(self, color, parent):
        self.color = color
        self.parent = parent


# Acts as the 'vertices' for the maze layout
class Arrow:
    def __init__(self, row, column, color, circle, direction):
        super().__init__()
        self.row = row
        self.column = column
        self.color = color
        self.circle = circle
        self.direction = direction

# Creates adjacency list for each arrow
def build_graph(rows,cols,maze):
    # Tells the program how to translate depending on the direction of the arrow
    directions = {
        'N' : (0,-1),
        'E' : (1,0),
        'S' : (0,1),
        'W' : (-1,0),
        'NE': (1,-1),
        'SE': (1,1),
        'SW': (-1,1),
        'NW': (-1,-1),
        'X' : (rows,cols)
    }

    # Key: Each arrow | Value: list of the valid moves in the arrow's path
    # Graph consists of two distinct halves: the normal half and the transpose half
    # These are connected by the circle arrow nodes
    graph = {}

    # Looks through the maze layout and creates the graph
    for currentRow in range(rows):
        for currentCol in range(cols):
            # Represents coordinates used to find each node's targets
            y,x = currentRow,currentCol

            # translateX, Y represent translations of x and y depending on the arrow's head direction
            translateX,translateY = directions[maze[currentRow][currentCol].direction]

            # node = tuple describing the location of each arrow
            # Coordinates are negative if it's a circle arrow, positive otherwise
            # This allows the circle arrows to have adjacency lists of nodes inverse to themselves
            if maze[currentRow][currentCol].circle == 'C':
                node = (-(currentRow+1),-(currentCol+1))
            else:
                node = (currentRow+1,currentCol+1)
            
            # Creates key for node in the graph dictionary
            graph[node] = set()

            # Creates the graph, adding the nodes in the path of the current arrow
            # to that node's adjacency list (if they are the opposite color)
            while 0 <= y + translateY < rows and 0 <= x + translateX < cols:
                x += translateX
                y += translateY
                if maze[y][x].color != maze[currentRow][currentCol].color:
                    graph[node].add((y+1,x+1))
            
            # Reverses the node's direction (for the inverse nodes)
            if maze[currentRow][currentCol].circle == 'C':
                node = (currentRow+1,currentCol+1)
            else:
                node = (-(currentRow+1),-(currentCol+1))
            
            # Resets x and y
            y, x = currentRow,currentCol
            graph[node] = set()

            # Does the same as before, but for the nodes in the path of the arrow's tail
            # Adds the nodes as negatives (to separate them from the normal ones)
            while 0 <= y - translateY < rows and 0 <= x - translateX < cols:
                x -= translateX
                y -= translateY
                if maze[y][x].color != maze[currentRow][currentCol].color:
                    graph[node].add((-(y+1),-(x+1)))
    return graph

# Function that reads in contents of the maze file
def initialize_graph():
    rows = 0
    columns = 0

    fMaze = open("maze.txt")

    # Reads in first line of the file to define size of the graph
    firstLine = fMaze.readline()
    firstLineInfo = firstLine.split(" ")

    rows = int(firstLineInfo[0])
    columns = int(firstLineInfo[1])

    # 2D lists that contains each arrow node
    # Used for creating adjacency lists for the actual graph (a dictionary)
    mazeLayout = [[0 for i in range(columns)] for j in range(rows)]

    # Reads in the rest of the file into 2D list
    for i in range(rows):
        for j in range(columns):
            line = fMaze.readline()
            aspects = line.rstrip('\n').split(" ")
            arrow = Arrow(int(aspects[0]), int(aspects[1]), aspects[2], aspects[3], aspects[4])
            mazeLayout[i][j] = arrow

    fMaze.close()
    return build_graph(rows, columns, mazeLayout)



# BFS for the maze
def BFS(graph):
    queue = []
    vertStore = {}

    # Initializes vertex attributes
    for arrow in graph:
        vertStore[arrow] = vertex('W', None)
    
    # Adds start space to queue, defines end space
    queue.append(list(graph.keys())[0])
    antiEnd = list(graph.keys())[-1]
    end = (-antiEnd[0],-antiEnd[1])

    # Main BFS loop
    while len(queue) > 0:
        # Pops node from the queue
        u = queue.pop()
        # Checks each target of the node u
        for target in graph[u]:
            # Checks if the target node is undiscovered ('W')
            # If it is, add it to the queue and mark it as discovered ('G')
            # Also marks u as its parent node
            if vertStore[target].color == 'W':
                vertStore[target].color = 'G'
                vertStore[target].parent = u
                # If the target being looked at is the end, you're done
                if target == end or target == antiEnd:
                    return vertStore
                # Otherwise, 
                queue.append(target)
        # Marks u as finished ('B')
        vertStore[u].color = 'B'



# Setup and maze search
graph = initialize_graph()
path = BFS(graph)

pathTaken = []

# Gets finish space
traveled = sorted(path.keys())[-1]

# Gets the path taken by the maze algorithm
while traveled != None:
    pathTaken.append(traveled)
    traveled = path[traveled].parent

# Follows the parent of each node starting from the end to get the path taken
for i in range(len(pathTaken)-1,-1,-1):
    print('(', abs(pathTaken[i][0]), ',', abs(pathTaken[i][1]), ')',sep='',end=' ')