from typing import List, Tuple
import random
from cell import Cell


class MazeGen:
    def __init__(self, width: int, height: int, seed: int) -> None:
        self.width = width
        self.height = height
        self.seed = seed

    def binary_tree_maze(width: int, height: int,
                         seed: int = None) -> List[List[Cell]]:
        """Generate maze using Binary Tree algorithm"""
        if seed is not None:
            random.seed(seed)

        grid = []
        for y in range(height):
            row = []
            for x in range(width):
                new_cell = Cell(x, y)
                row.append(new_cell)
            grid.append(row)

        corner = random.choice(['top-right', 'top-left',
                                'bottom-right', 'bottom-left'])

        for y in range(height):
            for x in range(width):
                possibilities = []

                if corner == 'top-right':
                    if y > 0:
                        possibilities.append('N')
                    if x < width - 1:
                        possibilities.append('E')

                elif corner == 'top-left':
                    if y > 0:
                        possibilities.append('N')
                    if x > 0:
                        possibilities.append('W')

                elif corner == 'bottom-right':
                    if y < height - 1:
                        possibilities.append('S')
                    if x < width - 1:
                        possibilities.append('E')

                elif corner == 'bottom-left':
                    if y < height - 1:
                        possibilities.append('S')
                    if x > 0:
                        possibilities.append('W')

                if not possibilities:
                    continue

                choice = random.choice(possibilities)

                if choice == 'N':
                    grid[y][x].north = False
                    grid[y-1][x].south = False
                elif choice == 'S':
                    grid[y][x].south = False
                    grid[y+1][x].north = False
                elif choice == 'E':
                    grid[y][x].east = False
                    grid[y][x+1].west = False
                elif choice == 'W':
                    grid[y][x].west = False
                    grid[y][x-1].east = False

        return grid


def generate_backtracking_maze(width: int, height: int, seed: int = None) -> List[List[Cell]]:
    if seed is not None:
        random.seed(seed)

    grid = []
    for y in range(height):
        row = []
        for x in range(width):
            new_cell = Cell(x, y)
            row.append(new_cell)
        grid.append(row)
    

    start_x, start_y = 0, 0
    current_cell = grid[start_y][start_x]
    current_cell.visited = True
    
    stack = []
    stack.append(current_cell)

    while stack:
        current_cell = stack[-1]
        x, y = current_cell.x, current_cell.y

        neighbors = []
        
        if y > 0:
            neighbor = grid[y - 1][x]
            if not neighbor.visited:
                neighbors.append(('N', neighbor))
        
        if y < height - 1:
            neighbor = grid[y + 1][x]
            if not neighbor.visited:
                neighbors.append(('S', neighbor))

        if x < width - 1:
            neighbor = grid[y][x + 1]
            if not neighbor.visited:
                neighbors.append(('E', neighbor))

        if x > 0:
            neighbor = grid[y][x - 1]
            if not neighbor.visited:
                neighbors.append(('W', neighbor))

        if neighbors:
            direction, next_cell = random.choice(neighbors)

            if direction == 'N':
                current_cell.north = False
                next_cell.south = False
            elif direction == 'S':
                current_cell.south = False
                next_cell.north = False
            elif direction == 'E':
                current_cell.east = False
                next_cell.west = False
            elif direction == 'W':
                current_cell.west = False
                next_cell.east = False
            
            next_cell.visited = True
            stack.append(next_cell)
        else:
            stack.pop() # The BackTrack  When The neighbora liat is empty means there is no unvisited neighbors so Let's go back one step and check the previous cell
            
    return grid

def find_solution_path(grid: List[List[Cell]], entry: Tuple[int, int],
                       exit: Tuple[int, int]) -> str:
    """
    Find shortest path from entry to exit using BFS
    Returns direction string like 'EESENNWW'
    """
