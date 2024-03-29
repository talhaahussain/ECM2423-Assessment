# maze-solving-algorithms

Continuous Assessment for ECM2423 - Artificial Intelligence and Applications, set by Prof. Ayah Helal (Year 2, Semester 2). Involves the use of several search algorithms for the problem of solving mazes, as well as comparing performance and an independent extra program for generating new mazes.

This work received a final mark of 85/100.

Please see `specification.pdf` for specification.

## Prerequisites

Python 3.x. Requires the libraries _time_, _itertools_ and _random_. All of these should be installed by default.

## Usage

In order to supply a maze to any maze solving algorithm provided, a valid .txt file must be used. '#' indicates a wall, and '-' indicates a space. The supplied maze must have a perimeter wall, as well as an entrance and exit (in the first and last line of the text file). bfs.py and dfs.py will reject any files with invalid formatting. maze_generator.py may be used to generate and save a valid maze. I have included some valid mazes as examples.

bfs.py, dfs.py and maze_generator.py all contain an interactive main program, from which instructions on usage and options are provided. bfs.py and dfs.py also contain analysis options, which analyse the performance of the algorithms based on direction biases, which can be used to determine the biases of a given maze.

## Limitations

maze_generation.py can only be used to generate square mazes, where the width of the maze is equal to the height.

## Footnote
a-star.py is not entirely my code, and is sourced and adapted from https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2. All credits go to the respective owners. Comments in a-star.py provide further detail.

maze_generator.py is code from a legacy project of mine, adapted to work with the formatting of this project. Comments in maze_generator.py provide further detail.
