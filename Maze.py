# Acts as the vertices for the graph
class Arrow:
    # Constructor
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
    graph = {}
    # Looks through the maze layout and creates the graph
    for currentRow in range(rows):
        for currentCol in range(cols):
            # node = tuple describing the location of each arrow
            node = (currentRow+1,currentCol+1)
            y, x = currentRow,currentCol
            graph[node] = []
            # dx and dy represent translations of x and y depending on
            # the arrow's head direction
            translateX, translateY = directions[maze[currentRow][currentCol].direction]
            # Creates the graph, adding the nodes in the path of the current arrow
            # To that node's adjacency list (If they are the opposite color)
            while 0 <= y + translateY < rows and 0 <= x + translateX < cols:
                x += translateX
                y += translateY
                if maze[y][x].color != maze[currentRow][currentCol].color:
                    graph[node].add((y+1, x+1))
            # Resets x and y
            y, x = currentRow,currentCol
            # Does the same, but for the nodes in the path of the arrow's tail
            while 0 <= y - translateY < rows and 0 <= x - translateX < cols:
                x -= translateX
                y -= translateY
                if maze[y][x].color != maze[currentRow][currentCol].color:
                    graph[node].add((y+1, x+1))
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


# Setup and maze search
graph = initialize_graph()
print("Widow is a 'fun' hero")