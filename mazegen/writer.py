from typing import List, Tuple
from mazegen.cell import Cell


def cell_to_hex(cell: Cell) -> str:
    """Convert a cell's wall configuration to a hexadecimal character.

    Encodes the presence of walls as a 4-bit value where each bit
    represents a cardinal direction: north=1, east=2, south=4, west=8.
    The resulting integer is returned as an uppercase hex character.

    Args:
        cell: The Cell object whose wall configuration is to be encoded.

    Returns:
        A single uppercase hexadecimal character (e.g. '0' to 'F')
        representing the cell's wall state.
    """
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


def write_hex_output(maze_grid: List[List[Cell]], entry: Tuple[int, int],
                     exit_pos: Tuple[int, int], solution_path: str,
                     output_file: str) -> None:
    """Write the maze grid and metadata to a file in hex-encoded format.

    Each row of the maze is written as a string of uppercase hexadecimal
    characters, one character per cell, encoding its wall configuration.
    After the grid, a blank line separates the metadata block containing
    the entry coordinates, exit coordinates, and the solution path string.

    Args:
        maze_grid: 2D list of Cell objects representing the maze.
        entry: (col, row) coordinates of the maze entry point.
        exit_pos: (col, row) coordinates of the maze exit point.
        solution_path: String of direction characters ('N', 'S', 'E', 'W')
            describing the shortest path from entry to exit.
        output_file: Path to the output file to write to.
    """
    with open(output_file, "w") as f:
        for row in maze_grid:
            hex_row = ""
            for cell in row:
                hex_row += cell_to_hex(cell)
            f.write(hex_row + "\n")

        f.write("\n")
        f.write(f"{entry[0]},{entry[1]}\n")
        f.write(f"{exit_pos[0]},{exit_pos[1]}\n")
        f.write(f"{solution_path}\n")
