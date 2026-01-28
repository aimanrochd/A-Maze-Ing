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


def find_solution_path(grid: List[List[Cell]], entry: Tuple[int, int],
                       exit: Tuple[int, int]) -> str:
    """
    Find shortest path from entry to exit using BFS
    Returns direction string like 'EESENNWW'
    """
