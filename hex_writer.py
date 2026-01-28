from typing import List, Tuple, Any


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
