from typing import List, Tuple
from cell import Cell

def find_solution_path(grid: List[List[Cell]], entry: Tuple[int, int],
                       exit: Tuple[int, int]) -> str:
    """
    Find shortest path from entry to exit using BFS
    Returns direction string like 'EESENNWW'
    """