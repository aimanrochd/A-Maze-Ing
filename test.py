import curses
import random
import time
from typing import List

# ==========================================
# 1.HADCHI GHA KANTESTI BIIIH MACHI DYALI
# ==========================================
TOP = 1
RIGHT = 2
BOTTOM = 4
LEFT = 8

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.north = True
        self.east = True
        self.south = True
        self.west = True
        self.visited = False 

# ==========================================
# 2. DRAWING LOGIC (Adapted for Live Animation)
# ==========================================

def wall_char(up, right, down, left):
    mask = (up << 0) | (right << 1) | (down << 2) | (left << 3)
    table = {
        0b0000: " ", 0b0001: "╹", 0b0010: "╺", 0b0011: "┗",
        0b0100: "╻", 0b0101: "┃", 0b0110: "┏", 0b0111: "┣",
        0b1000: "╸", 0b1001: "┛", 0b1010: "━", 0b1011: "┻",
        0b1100: "┓", 0b1101: "┫", 0b1110: "┳", 0b1111: "╋",
    }
    return table.get(mask, " ")

def draw_frame(stdscr, grid_cells, width, height, current_x=None, current_y=None):
    """
    Draws the current state of the maze.
    This is called INSIDE the generation loop.
    """
    stdscr.clear() # Clear screen for next frame
    
    screen_h = height * 2 + 1
    screen_w = width * 2 + 1
    
    # 1. Build the wall grid (0=Empty, 1=Wall)
    wall_map = [[0 for _ in range(screen_w)] for _ in range(screen_h)]
    
    for y in range(height):
        for x in range(width):
            cell = grid_cells[y][x]
            gy = y * 2
            gx = x * 2
            
            # Translate Cell boolean (True=Wall) to Integer Bitmask
            cell_mask = 0
            if cell.north: cell_mask |= TOP
            if cell.east:  cell_mask |= RIGHT
            if cell.south: cell_mask |= BOTTOM
            if cell.west:  cell_mask |= LEFT

            # Fill wall_map based on bitmask (Same logic as your Viz)
            if cell_mask & TOP:
                wall_map[gy][gx] = 1; wall_map[gy][gx + 1] = 1; wall_map[gy][gx + 2] = 1
            if cell_mask & BOTTOM:
                wall_map[gy + 2][gx] = 1; wall_map[gy + 2][gx + 1] = 1; wall_map[gy + 2][gx + 2] = 1
            if cell_mask & LEFT:
                wall_map[gy][gx] = 1; wall_map[gy + 1][gx] = 1; wall_map[gy + 2][gx] = 1
            if cell_mask & RIGHT:
                wall_map[gy][gx + 2] = 1; wall_map[gy + 1][gx + 2] = 1; wall_map[gy + 2][gx + 2] = 1

    # 2. Render characters
    for y in range(screen_h):
        for x in range(screen_w):
            if wall_map[y][x] == 0:
                # OPTIONAL: Draw the "digger" (current position)
                if current_x is not None and y == current_y * 2 + 1 and x == current_x * 2 + 1:
                    stdscr.addch(y, x, "█", curses.color_pair(2)) # Green block for head
                else:
                    stdscr.addch(y, x, " ")
                continue
                
            up = y > 0 and wall_map[y - 1][x]
            down = y < screen_h - 1 and wall_map[y + 1][x]
            left = x > 0 and wall_map[y][x - 1]
            right = x < screen_w - 1 and wall_map[y][x + 1]
            
            ch = wall_char(up, right, down, left)
            
            # Use color pair 1 (Walls)
            stdscr.addch(y, x, ch, curses.color_pair(1))

    stdscr.refresh()

# ==========================================
# 3. ANIMATED GENERATOR
# ==========================================

def animate_backtracking(stdscr, width: int, height: int, seed: int = None):
    if seed is not None:
        random.seed(seed)

    # Initialize Grid
    grid = [[Cell(x, y) for x in range(width)] for y in range(height)]
    
    start_x, start_y = 0, 0
    current_cell = grid[start_y][start_x]
    current_cell.visited = True
    
    stack = []
    stack.append(current_cell)

    # --- ANIMATION LOOP ---
    while stack:
        current_cell = stack[-1]
        cx, cy = current_cell.x, current_cell.y

    
        draw_frame(stdscr, grid, width, height, cx, cy)
        curses.napms(20) # 20ms delay (Adjust this to speed up/slow down)

        neighbors = []
        if cy > 0:
            neighbor = grid[cy - 1][cx]
            if not neighbor.visited: neighbors.append(('N', neighbor))
        if cy < height - 1:
            neighbor = grid[cy + 1][cx]
            if not neighbor.visited: neighbors.append(('S', neighbor))
        if cx < width - 1:
            neighbor = grid[cy][cx + 1]
            if not neighbor.visited: neighbors.append(('E', neighbor))
        if cx > 0:
            neighbor = grid[cy][cx - 1]
            if not neighbor.visited: neighbors.append(('W', neighbor))

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
            stack.pop()

    # Final Draw (Show completed maze)
    draw_frame(stdscr, grid, width, height)
    return grid

def main(stdscr):
    # Setup Colors
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1) # Walls
    curses.init_pair(2, curses.COLOR_CYAN, -1)   # Digger Head

    # Check Terminal Size
    WIDTH, HEIGHT = 15, 15 # Start small for animation
    sh, sw = stdscr.getmaxyx()
    if sh < HEIGHT * 2 + 1 or sw < WIDTH * 2 + 1:
        stdscr.addstr(0,0, "Terminal too small! Zoom out.")
        stdscr.getch()
        return

    # Run Animation
    stdscr.addstr(0, 0, "Generating Maze... (Watch it grow!)")
    grid = animate_backtracking(stdscr, WIDTH, HEIGHT)
    
    stdscr.addstr(0, 0, "Generation Complete! Press any key to exit.")
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)