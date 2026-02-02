from typing import List, Tuple, Any
from mazgen.cell import Cell

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

def cell_to_hex(cell: Any) -> str:
    """Convert cell walls to hex character"""
    value = 0
    if cell.north:
        value += 1
    if cell.east:
        value += 2
    if cell.south:
        value += 4
    if cell.west:
        value += 8
    return format(value, 'X')


def write_hex_output(maze_grid: List[List[Any]], entry: Tuple[int, int],
                     exit: Tuple[int, int], solution_path: str,
                     output_file: str) -> None:
    """Write maze to output file in hex format"""
    with open(output_file, "w") as f:
        for row in maze_grid:
            hex_row = ''
            for cell in row:
                hex_char = cell_to_hex(cell)
                hex_row += hex_char
            f.write(hex_row + '\n')
        f.write('\n')
        f.write(f"{entry[0]},{entry[1]}\n")
        f.write(f"{exit[0]},{exit[1]}\n")
        f.write(f"{solution_path}\n")
