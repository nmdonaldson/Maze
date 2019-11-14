# Arrow class, acts as the vertices for the graph
class Arrow:
    # Constructor
    def __init__(self, row, column, color, circle, direction):
        super().__init__()
        self.row = row
        self.column = column
        self.color = color
        self.circle = circle
        self.direction = direction

# Graph class, contains a list of the arrows 
class Graph:
    # Constructor, defines the size of the graph
    def __init__(self, rows, columns):
        super().__init__()
        self.rows = rows
        self.columns = columns
        self.graph = {}
        self.invertedGraph = {}
    
# Creates list of arrows that can be moved to from the perspective of each arrow
# Also does this for the graph when the directions are inverted
def build_graph(rows, columns, maze):
    graph = {}
    # Adds each opposite colored arrow the current arrow points to to the vertex list
    # For each arrow
    for i in range(rows):
        for j in range(columns):
            arrowTargets = []
            invertedTargets = []
            currentArrow = maze[i][j]

            # If the arrow points east
            if currentArrow.direction == 'E':
                # Check each arrow in the row
                for arrow in maze[i]:
                    # If the colors don't match, add to that arrow's pointing list
                    if arrow.color != currentArrow.color and arrow.column > currentArrow.column:
                        arrowTargets.append(arrow)
                graph[currentArrow] = arrowTargets
            
            # If the arrow points west
            elif currentArrow.direction == 'W':
                # Check each arrow in the row
                for arrow in maze[i]:
                    # If the colors don't match, add to that arrow's pointing list
                    if arrow.color != currentArrow.color and arrow.column < currentArrow.column:
                        arrowTargets.append(arrow)
                graph[currentArrow] = arrowTargets

            # If the arrow points north
            elif currentArrow.direction == 'N':
                # Check each arrow in the column
                for z in range(columns):
                    arrow = maze[z][j]
                    # If the colors don't match, add to that arrow's pointing list
                    if arrow.color != currentArrow.color and arrow.row < currentArrow.row:
                        arrowTargets.append(arrow)
                graph[currentArrow] = arrowTargets

            # If the current arrow points south
            elif currentArrow.direction == 'S':
                # Check each arrow in the column
                for z in range(columns):
                    arrow = maze[z][j]
                    # If the colors don't match, add to that arrow's pointing list
                    if arrow.color != currentArrow.color and arrow.row > currentArrow.row:
                        arrowTargets.append(arrow)
                graph[currentArrow] = arrowTargets

            # If the current arrow points northeast
            elif currentArrow.direction == 'NE':
                # Check each arrow in the diagonal it points to
                k = j
                for z in range(i,-1,-1):
                    if k >= columns:
                        continue
                    arrow = maze[z][k]
                    k += 1
                    # If the colors don't match, add to that arrow's pointing
                    if arrow.color != currentArrow.color and arrow.row < currentArrow.row and arrow.column > currentArrow.column:
                        arrowTargets.append(arrow)
                graph[currentArrow] = arrowTargets

            # If the current arrow points northwest
            elif currentArrow.direction == 'NW':
                # Check each arrow in the diagonal it points to
                k = j
                for z in range(i,-1,-1):
                    if k >= columns:
                        continue
                    arrow = maze[z][k]
                    k += -1
                    # If the colors don't match, add to that arrow's pointing list
                    if arrow.color != currentArrow.color and arrow.row < currentArrow.row and arrow.column < currentArrow.column:
                        arrowTargets.append(arrow)
                graph[currentArrow] = arrowTargets

            # If the current arrow points southwest
            elif currentArrow.direction == 'SW':
                # Check each arrow in the diagonal it points to
                z = i
                for k in range(j,-1,-1):
                    if z >= rows:
                        continue
                    arrow = maze[z][k]
                    z += 1
                    # If the colors don't match, add to that arrow's pointing list
                    if arrow.color != currentArrow.color and arrow.row > currentArrow.row and arrow.column < currentArrow.column:
                        arrowTargets.append(arrow)
                graph[currentArrow] = arrowTargets

            # If the current arrow points southeast
            elif currentArrow.direction == 'SE':
                # Check each arrow in the diagonal it points to
                z = i
                for k in range(j,columns):
                    if z >= rows:
                        continue
                    arrow = maze[z][k]
                    z += 1
                    # If the colors don't match, add to that arrow's pointing list
                    if arrow.color != currentArrow.color and arrow.row > currentArrow.row and arrow.column > currentArrow.column:
                        arrowTargets.append(arrow)
                graph[currentArrow] = arrowTargets
    return graph

# Function that reads in contents of the maze file
def initialize_maze():
    rows = 0
    columns = 0

    fMaze = open("maze.txt")

    # Reads in first line of the file to define size of the graph
    firstLine = fMaze.readline()
    firstLineInfo = firstLine.split(" ")

    rows = int(firstLineInfo[0])
    columns = int(firstLineInfo[1])
    graph = Graph(rows, columns)

    # 2D list that contains each arrow node
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
    graph.graph = build_graph(rows, columns, mazeLayout)
    return graph

def invertDirection(direction):
    invert = ""

    # Inverts the input direction
    if direction == 'E':
        invert = 'W'
    elif direction == 'N':
        invert = 'S'
    elif direction == 'S':
        invert = 'N'
    elif direction == 'W':
        invert = 'E'
    elif direction == 'NE':
        invert = 'SW'
    elif direction == 'NW':
        invert = 'SE'
    elif direction == 'SE':
        invert = 'NW'
    elif direction == 'SW':
        invert = 'NE'
    
    return invert

maze = initialize_maze()
for f in maze.graph:
    for g in maze.graph[f]:
        print(g.row,g.column)