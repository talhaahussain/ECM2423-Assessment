"""
Some old code from a sixth form project of mine, used for maze generation and testing.
Adapted for use with current DFS and BFS implementations, as well as for generating compatible files.

(Legacy comments:)
KEY:
'|' and '#' indicate a WALL
' ' and '-' indicate a SPACE
'+' indicates an EXPOSED UNDETERMINED LOCATION
'?' indicates an UNDETERMINED LOCATION

The 'check' function determines if a cell should be a space or a wall.
If it returns True, it should become a space.
If it returns False, it should become a wall.
"""

import random # Since the generation of this maze is random, I need the random module.
from dfs import get_file, check_grid, check_entrance_exit, find_neighbours, dfs

def generate_maze(x_cells, y_cells):
#x_cells = 20 # This defines the number of cells in the x-direction.
#y_cells = 20 # This defines the number of cells in the y-direction.
    grid = [] # This allows me to build the grid from which the maze is generated. 

    for y in range(y_cells): 
        row = [] # Creates a 'row' list for all y locations (10 rows)
        for x in range(x_cells):
            row.append('?') # Sets all cells to UNDETERMINED
        grid.append(row) # Fills the grid with these rows

    exposed = [] # This is a list of EXPOSED UNDETERMINED LOCATIONS (+)

    def carve(y, x): # This function makes the cell a space.
        if (0 > (x or y)) or ((x > x_cells) or (y > y_cells)) or (type(x) != int or type(y) != int):
            return # This is for validation - 'if invalid data has been entered, ignore.'
     
        grid[y][x] = ' ' # This takes the two parameters and updates location.
        adjacent = [] # This stores any adjacent cells.

        if x > 0: # This checks if there is a cell behind the current cell (x direction).
            if grid[y][x-1] == '?': # If there is, and this adjacent cell is undetermined...
                grid[y][x-1] = '+' # ...Mark it as EXPOSED.
                adjacent.append((y,x-1)) # Add this cell to the 'adjacent'
            
        if x < x_cells - 1: # This checks if there is a cell in front of the current cell (x direction).
            if grid[y][x+1] == '?': # If there is, and this adjacent cell is undetermined...
                grid[y][x+1] = '+' # ...Mark it as EXPOSED.
                adjacent.append((y,x+1)) # Add this cell to the 'adjacent' list.
            
        if y > 0: # This checks if there is a cell behind the current cell (y direction).
            if grid[y-1][x] == '?': # If there is, and this adjacent cell is undetermined...
                grid[y-1][x] = '+' # ...Mark it as EXPOSED.
                adjacent.append((y-1,x)) # Add this cell to the 'adjacent' list.
            
        if y < y_cells - 1: # This checks if there is a cell in front of the current cell (y direction).
            if grid[y+1][x] == '?': # If there is, and this adjacent cell is undetermined...
                grid[y+1][x] = '+' # ...Mark it as EXPOSED.
                adjacent.append((y+1,x)) # Add this cell to the 'adjacent' list.
            
        random.shuffle(adjacent) # Shuffles the list of adjacent cells.
        exposed.extend(adjacent) # Adds the list of adjacent cells to the 'exposed' list.


    def wall(y, x): # This function make the cell a wall.
        if (0 > (x or y)) or ((x > x_cells) or (y > y_cells)) or (type(x) != int or type(y) != int):
            return # This is for validation - 'if invalid data has been entered, ignore.'
        grid[y][x] = '|' # This takes the two parameters and updates location.



    def check(y, x, nodiagonals = True): # Takes the 'nodiagonals' parameter...
    # ...this parameter determines if a cell has NO diagonals (when True).
        edgestate = 0 # This is a way of determining the behaviour of the edges around a  point.
    
        if x > 0: # If the cell has cells to the left...
            if grid[y][x-1] == ' ': # ...if the cell directly to the left is a space...
                edgestate += 1 # Increase edgestate by 1.
            
        if x < x_cells-1: # If the cell has cells to the right...
            if grid[y][x+1] == ' ': # ...if the cell directly to the right is a space...
                edgestate += 2 # Increase edgestate by 2.
            
        if y > 0: # If the cell has cells above...
            if grid[y-1][x] == ' ': # ...if the cell directly above is a space...
                edgestate += 4 # Increase edgestate by 4.
            
        if y < y_cells-1: # If the cell has cells below...
            if grid[y+1][x] == ' ': # ...if the cell directly below is a space...
                edgestate += 8 # Increase edgestate by 8.

        if nodiagonals: # If 'nodiagonals' is True...
            if edgestate == 1: # ...if 'edgestate' is 1...
                if x < x_cells-1: # ...if there are cells to the right...
                    if y > 0: # ...if there are cells above...
                        if grid[y-1][x+1] == ' ': # ...if the cell directly top-right is a space...
                            return False # Return False.
                    if y < y_cells-1: # ...if there are cells below...
                        if grid[y+1][x+1] == ' ': # ...if the cell directly bottom-right is a space...
                            return False # Return False.
                return True # Return True.
        
            elif edgestate == 2: # ...else, if 'edgestate' is 2...
                if x > 0: # ...if there are cells to the left...
                    if y > 0: # ...if there are cells above...
                        if grid[y-1][x-1] == ' ': # ...if the cell directly top-left is a space...
                            return False # Return False.
                    if y < y_cells-1: # ...if there are cells below...
                        if grid[y+1][x-1] == ' ': # ...if the cell directly bottom-left is a space...
                            return False # Return False.
                return True # Return True.
        
            elif edgestate == 4: # ...else, if 'edgestate' is 4...
                if y < y_cells-1: # ...if there are cells below...
                    if x > 0: # ...if there are cells to the left...
                        if grid[y+1][x-1] == ' ': # ...if the cell directly bottom-left is a space...
                            return False # Return False.
                    if x < x_cells-1: # ...if there are cells to the right...
                        if grid[y+1][x+1] == ' ': # ...if the cell directly bottom-right is a space...
                            return False # Return False.
                return True # Return True.
        
            elif edgestate == 8: # ...if 'edgestate' is 8...
                if y > 0: # ...if there are cells above...
                    if x > 0: # ...if there are cells to the left...
                        if grid[y-1][x-1] == ' ': # ...if the cell directly top-left is a space...
                            return False # Return False.
                    if x < x_cells-1: # ...if there are cells to the right...
                        if grid[y-1][x+1] == ' ': # ...if the cell directly top-right is a space...
                            return False # Return False.
                    
                return True # Return True.
            return False # Return False.
    
        else: # ...if not... (hence 'nodiagonals' is False)
            if [1, 2, 4, 8].count(edgestate): # ...count the number if times that 'edgestate' appears in that array.
                # If it does appear in the array...
                return True # Return True.
        
            return False # Return


    x_random = random.randint(0, x_cells-1) # Choose a random point in the x-axis, on the grid.
    y_random = random.randint(0, y_cells-1) # Choose a random point in the y-axis, on the grid.
    carve(x_random, y_random) # Use these random points and carve.


    def create():
        while(len(exposed)): # While there are exposed cells...
            pos = random.random() # Select a random number.
            choice = exposed[int(pos*len(exposed))] # This randomly selects an exposed cell from the list.
            if check(*choice): # If the selected cell should become a space...
                carve(*choice) # ...make this cell a space.
            else: # If not...
                wall(*choice) # ...make this cell a wall.
            exposed.remove(choice) # Remove this cell from the 'exposed' list.

    # The following changes any unexposed, unidentified cells to be walls.
        for y in range(y_cells): 
            for x in range(x_cells):
                if grid[y][x] == '?':
                    grid[y][x] = '|'

    # The following prints the entire maze.
        maze_data = []
        for y in range(y_cells):
            row = ' '
            for x in range(x_cells):
                row += grid[y][x]
            maze_data.append(row)

        return maze_data

    maze_data = create()
    return maze_data


def parse(maze_data):
    """
    Ensures compatibility between legacy format and CA spec defined format through conversion
    """
    new_maze = []
    border = ['# '] * (len(maze_data[1]) + 2) 
    border[1] = '- ' # Inserting entrance
    top_border = ''.join(border)
    new_maze.append(top_border[:-1]) # Adding top row of wall
    
    for row in maze_data:
        row = row.replace(' ', '-')
        row = row.replace('|', '#')
        row = '#' + row + "#" # Inserting left/right columns of wall
        new_maze.append(" ".join(row))
    border[1] = '# '
    border[-2] = '- ' # Inserting exit
    bottom_border = ''.join(border) 
    new_maze.append(bottom_border[:-1]) # Adding in bottom row of wall
    return new_maze

def write_to_file(maze_data, filename):
    """
    Writing maze to file.
    """
    file = open(filename, "w")
    for row in maze_data:
        file.write(row + "\n")
    file.close()

def test(filename):
    """
    Using DFS to make sure maze is solvable.
    """
    maze = get_file(filename)
    check_grid(maze)
    targets = check_entrance_exit(maze)
    result = dfs(targets[0], targets[1], maze, ["Up", "Down", "Left", "Right"])
    if result == False:
        return False
    else:
        return True

def main():
    while True:
        print("\n")
        print("Hello. This is a program for generating square mazes and writing them to a file.")
        print("Please enter a filename. Extension must be .txt.")
        print("Please note that if an existing file is used, all data will be overwritten.")
        print("Please note that generation may take a while for larger mazes.")
        filename = input()
        if filename[-4:] != ".txt" or len(filename) < 5: # Check file extension
            print("Invalid file format detected.")
            continue # Loop
        print("Because all mazes generated are square, you only need to specify one value for width/height.")
        try:
            x = int(input("Please enter a value.\n"))
        except ValueError:
            print("Invalid value. Please try again.")
            continue # Loop
        if x < 2:
            print("Invalid value. Please try again.")
            continue # Loop
        maze_data = parse(generate_maze(x, x)) # Initial maze generation
        write_to_file(maze_data, filename)
        while test(filename) == False: # If maze isn't solvable, regenerate
            maze_data = parse(generate_maze(x, x))
            write_to_file(maze_data, filename)
        print("Your maze has been generated. Please check your directory.")
        print("\n")
        print("Thank you!")
        input('Press ENTER to exit')
        return

if __name__ == '__main__':
    main()
