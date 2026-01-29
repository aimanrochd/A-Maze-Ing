from typing import List, Tuple, Any
import random

# 1. Missing Cell Class
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.north = True
        self.east = True
        self.south = True
        self.west = True
        # We need a helper flag to track if we've been here.
        # You can add this to your class or use a separate "visited" matrix.
        self.visited = False 


def imprint_42(grid: List[List[Cell]], width: int, height: int) -> None:
    """
    Marks cells in the shape of '42' as visited and ensures all walls are closed.
    This forces the maze generator to work around them.
    """
    # 1. Safety Check: If maze is too small, skip it (Subject Requirement)
    if width < 15 or height < 10:
        print("Warning: Maze too small for '42' pattern.")
        return

    # 2. Calculate Center
    cx, cy = width // 2, height // 2

    # 3. Define the shape relative to the center
    # (x_offset, y_offset)
    pattern_cells = [
        # --- The Number 4 ---
        (-5, -2), (-5, -1), (-5, 0),        # Left vertical bar
        (-4, 0), (-3, 0),                   # Middle horizontal bar
        (-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2), # Right vertical bar
        
        # --- The Number 2 ---
        (1, -2), (2, -2), (3, -2), (4, -2), # Top bar
        (4, -1),                            # Top-right corner
        (1, 0), (2, 0), (3, 0), (4, 0),     # Middle bar
        (1, 1),                             # Bottom-left corner
        (1, 2), (2, 2), (3, 2), (4, 2)      # Bottom bar
    ]

    # 4. Apply the pattern
    for dx, dy in pattern_cells:
        px, py = cx + dx, cy + dy
        
        # Boundary check (just in case)
        if 0 <= px < width and 0 <= py < height:
            cell = grid[py][px]
            
            # LOCK THE CELL:
            # 1. Close all walls (visually creates the block)
            cell.north = True
            cell.east = True
            cell.south = True
            cell.west = True
            
            # 2. Mark as visited (prevents algorithm from digging here)
            cell.visited = True

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

def cell_to_hex(cell: Any) -> str:
    value = 0
    if cell.north: value += 1
    if cell.east: value += 2
    if cell.south: value += 4
    if cell.west: value += 8
    return format(value, 'X')

def write_hex_output(maze_grid, entry, exit, solution_path, output_file):
    with open(output_file, "w") as f:
        for row in maze_grid:
            hex_row = ''
            for cell in row:
                hex_row += cell_to_hex(cell)
            f.write(hex_row + '\n')
        f.write('\n')
        f.write(f"{entry[0]},{entry[1]}\n")
        f.write(f"{exit[0]},{exit[1]}\n")
        f.write(f"{solution_path}\n")

if __name__ == "__main__":
    WIDTH = 100
    HEIGHT = 100
    FILENAME = "test_maze.txt"
    
    print(f"Generating {WIDTH}x{HEIGHT} maze...")
    grid = generate_backtracking_maze(WIDTH, HEIGHT)
    
    write_hex_output(grid, (0,0), (WIDTH-1, HEIGHT-1), "NNSS", FILENAME)
    
    print(f"Saved to {FILENAME}")
    print(f"Run this command to see it: python3 viz.py {FILENAME}")