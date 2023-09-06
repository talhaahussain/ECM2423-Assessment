"""
KEY:
'#' indicates a WALL
'-' indicates a SPACE
Format is (row, column), or (row, element in row).
"""
import time
from itertools import permutations

  
def get_file(filename: str) -> list:
    """
    Opens the given file and loads rows of file as maze rows.

            Parameters:
                    filename (str): The name of the file
                
            Returns:
                    maze (list): A 2d list of rows
    """
    f = open(filename)
    maze = []
    for x in f:
        maze.append(x.split())
    return maze
    
    
def check_grid(grid: list) -> bool:
    """
    Takes a 2d list and checks if all the rows are the same length.

            Parameters:
                    grid (list): The 2d list
                
            Returns:
                    bool: Success or failure
    """
    w = len(grid[0])
    for row in grid:
        if len(row) != w:
            return False
    return True;


def check_entrance_exit(grid: list):# -> tuple | bool:
    """
    Checks for and finds the entrance and exit of the maze represented as a 2d list.

            Parameters:
                    grid (list): The 2d list (maze)
                
            Returns:
                    tuple/bool: Tuple of the start/end if successful, False is failure
    """
    h = len(grid)
    try:
        if ((grid[0].count("#")) != len(grid[0]) - 1) or ((grid[h-1].count("#")) != len(grid[0]) - 1): # If entrance isn't top row/exit isn't bottom...
            return False # ...return False - invalid maze.
        return ((0, grid[0].index("-")), (h-1, grid[h-1].index("-"))) # Returns entrance and exit
    except ValueError:
        return False


def find_neighbours(node: tuple, grid: list, ordering: list) -> list:
    """
    Finds neighbours of the given node in the maze.

            Parameters:
                    node (tuple): Node for neighbours to be retrieved
                    grid (list): The maze
                    ordering (list): Order in which neighbours are retrieved
                
            Returns:
                    neighbours (list): A list of tuples (neigbouring nodes)
    """
    neighbours = []
    for direction in ordering: # Customised configuration of neighbour priority
        if direction == "Up":
            if (grid[node[0]-1][node[1]] == "-"): # up
                neighbours.append((node[0]-1, node[1]))
            
        if direction == "Down":
            if (grid[node[0]+1][node[1]] == "-"): # down
                neighbours.append((node[0]+1, node[1]))

        if direction == "Right":
            if (grid[node[0]][node[1]+1] == "-"): # right
                neighbours.append((node[0], node[1]+1))
            
        if direction == "Left":
            if (grid[node[0]][node[1]-1] == "-"): # left
                neighbours.append((node[0], node[1]-1))
                
    return neighbours

def bfs(start: tuple, end: tuple, grid: list, ordering: list):# -> tuple | bool:
    """
    Opens the given file and loads rows of file as maze rows.

            Parameters:
                    start (tuple): Starting node location
                    end (tuple): Ending node location
                    grid (list): Maze
                    Ordering (list): Order in which neighbours are discovered
                
            Returns:
                    tuple/bool: Tuple of (path, no. of explored nodes,time taken, nodes in path, config) if successful; False if fail 
    """
    start_time = time.time()
    visited, queue, solution = set(), [(start, [start])], []
    while queue:
        node, path = queue.pop(0)
        solution = path
        visited.add(node)
        for node in find_neighbours(node, grid, ordering):
            if node == end:
                solution.append(end) # Path is kept with queue/node, so solution is easier to retrieve
                result_time = time.time() - start_time
                return solution, len(visited), result_time, len(solution), ordering
            else:
                if node not in visited:
                    visited.add(node)
                    queue.append((node, path + [node]))
    return False # If no solution can be found, return False



def bfs_analysis(maze: list):# -> list | bool:
    """
    Allows analysis of BFS with different permutations by running for all 24 configs on current maze.

            Parameters:
                    maze (list): Maze 
                
            Returns:
                    list/bool: List of results if successful, False is failure
    """
    targets = check_entrance_exit(maze)
    perm = permutations(["Up", "Down", "Left", "Right"])
    results = []
    for config in list(perm): # Going through all config permutations
        result = bfs(targets[0], targets[1], maze, config) # Returns in format: (solution, no. explored, time, no. in solution, config)
        if result == False:
            return False
        print("--- %s nodes explored for BFS with configuration %s ---" % (result[1], config))
        print("--- %s seconds for BFS with configuration %s ---" % (result[2], config))
        print("--- %s nodes in solution with configuration %s ---" % (result[3], config))
        print(" %s configuration finds solution..." % str(config))
        print(result[0])
        results.append(result)
        print("\n")

    return results


def main() -> None:
    while True:
        print("\n")
        file = input("Please enter a file path for your maze.\n")
        try:
            maze = get_file(file)
        except FileNotFoundError:
            print("File not found. Please try again.")
            continue
        except OSError:
            print("Invalid input. Please try again.")
            continue
        if (not check_grid(maze)):
            print("Maze provided does not have valid dimensions. Please try again.")
            continue
        if (not check_entrance_exit(maze)):
            print("Maze provided does not have valid entrance and exit points. Please try again.")
            continue
        print("Maze accepted!\n")
        break
    while True:
        print("\n")
        print("You have 2 options. Would you like to...")
        print("Use BFS to solve the maze you've given? (Respond with 0.)")
        print("Find the optimal permutation of neighbour exploration in BFS for your maze? (Respond with 1).\n")
        print("If you are unsure and would like an explanation, respond with 2.")
        try:
            choice_1 = int(input())
        except ValueError:
            print("Invalid choice. Please try again.")
            continue
        
        if choice_1 == 0:
            print("\n")
            print("Would you like to use the default configuration for neighbour search (respond with 0), or would you like to use your own (Respond with 1)?")
            try:
                choice_2 = int(input())
            except ValueError:
                print("Invalid choice. Please try again.")
                continue
            if choice_2 == 0:
                print("\n")
                targets = check_entrance_exit(maze)
                config = ['Up', 'Down', 'Left', 'Right']
                # Optimal configuration for provided mazes happens here
                if file == "maze-Easy.txt":
                    config = ['Up', 'Down', 'Right', 'Left']
                if file == "maze-Medium.txt":
                    config = ['Up', 'Left', 'Down', 'Right']
                if file == "maze-Large.txt":
                    config = ['Up', 'Left', 'Down', 'Right']
                if file == "maze-VLarge.txt":
                    config = ['Up', 'Right', 'Left', 'Down']
                result = bfs(targets[0], targets[1], maze, config)
                if result == False:
                    print("We are sorry, a solution to your maze could not be found.")
                    input('Press ENTER to exit')
                    return
                print("Solution:")
                print(result[0])
                print("--- Number of nodes explored: " + str(result[1]) + " nodes ---")
                print("--- Execution time: " + str(result[2]) + " seconds ---")
                print("--- Number of nodes in path: " + str(result[3]) + " nodes ---")
                print("Thank you!")
                input('Press ENTER to exit')
                return

            elif choice_2 == 1:
                while True:
                    print("\n")
                    perm = permutations(["Up", "Down", "Left", "Right"])
                    print("Please enter your configuration. Make sure you use capital letters at the start of each word.")
                    print("Please ensure that your input is formatted like the following example:")
                    print("'Up', 'Down', 'Left', 'Right'")
                    try:
                        config = eval(input()) # Taking user input for configuration
                    except NameError:
                        print("Improper formatting detected. Please try again.")
                        continue
                    if config in list(perm):
                        break                        
                    else:
                        print("Configuration not recognised. Please ensure you are formatting correctly.") 
                        continue
                    except SyntaxError:
                        print("Improper formatting detected. Please try again.")
                        continue
                targets = check_entrance_exit(maze) # Find entrance and exit
                result = bfs(targets[0], targets[1], maze, config)
                if result == False:
                    print("We are sorry, a solution to your maze could not be found.")
                    input('Press ENTER to exit')
                    return
                print("Solution:")
                print(result[0])
                print("--- Number of nodes explored: " + str(result[1]) + " nodes ---")
                print("--- Execution time: " + str(result[2]) + " seconds ---")
                print("--- Number of nodes in path: " + str(result[3]) + " nodes ---")
                print("Thank you!")
                input('Press ENTER to exit')
                return

            else:
                print("Invalid choice. Please try again.\n")
                continue


            

        elif choice_1 == 1:
            print("\n")
            results = bfs_analysis(maze)
            if results == False:
                print("We are sorry, a solution to your maze could not be found.")
                input('Press ENTER to exit')
                return
            results.sort(key=lambda a:a[2]) # Sort by fastest time
            print("Configuration %s found the solution to your maze the fastest (%s seconds)." % (results[0][-1], results[0][2]))
            print("Configuration %s found the solution to your maze the slowest (%s seconds)." % (results[-1][-1], results[-1][2]))
            results.sort(key=lambda a:a[1]) # Sort by fewest nodes explored
            print("Configuration %s explored the fewest nodes in your maze (%s nodes) before reaching a solution." % (results[0][-1], results[0][1]))
            print("Configuration %s explored the most nodes in your maze (%s nodes) before reaching a solution." % (results[-1][-1], results[-1][1]))
            print("\nBFS discovers the shortest path in the maze to have " + str(results[0][3]) + " nodes.")
            print("Thank you!")
            input('Press ENTER to exit')
            return
        elif choice_1 == 2: # Help section
            print("\n")
            print("The 'configuration' refers to the order in which the neighbours of a particular node are discovered.")
            print("A configuration is always some permutation of four possible directions - up, down, left or right. There are 24 possible configurations.")
            print("For different mazes, different configurations may have different effects on the performance of the algorithm.")
            print("For example, one configuration may lead to the solution being found faster than another, or in fewer nodes, etc.")
            print("Unlike with DFS, different configurations will have no effect on optimality for BFS, since optimality is guaranteed.")
            print("This program's BFS implementation allows for the order in which nodes are discovered to be customised.")
            print("This program also includes an analysis tool for your maze, which will run all 24 configurations of BFS on your maze and report back statistics.")
            print("The default configuration is 'Up', 'Down', 'Left', 'Right'.")
            print("If the sample mazes (Easy, Medium, Large, VLarge) are entered, this program will switch to configurations designed to optimise performance for these mazes.")
        else:
            print("Invalid choice. Please try again.\n")
            continue # Loop

if __name__ == '__main__':
    main()
