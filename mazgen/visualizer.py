import curses
import random
import locale
from typing import List, Tuple, Any

# Ensure Unicode characters work in the terminal
locale.setlocale(locale.LC_ALL, '')

# ==========================================
# 1. YOUR CLASSES (Pasted & Fixed for import)
# ==========================================

class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.north = True
        self.east = True
        self.south = True
        self.west = True

class MazeGen:
    def __init__(self, width: int, height: int, seed: int) -> None:
        self.width = width
        self.height = height
        self.seed = seed


    # Added @staticmethod because this function doesn't use 'self'
    @staticmethod
    def binary_tree_maze(width: int, height: int, seed: int = None) -> List[List[Cell]]:
        if seed is not None:
            random.seed(seed)

        grid = []
        for y in range(height):
            row = []
            for x in range(width):
                new_cell = Cell(x, y)
                row.append(new_cell)
            grid.append(row)

        # Randomize the bias corner
        corner = random.choice(['top-right', 'top-left', 'bottom-right', 'bottom-left'])

        for y in range(height):
            for x in range(width):
                possibilities = []

                if corner == 'top-right':
                    if y > 0: possibilities.append('N')
                    if x < width - 1: possibilities.append('E')

                elif corner == 'top-left':
                    if y > 0: possibilities.append('N')
                    if x > 0: possibilities.append('W')

                elif corner == 'bottom-right':
                    if y < height - 1: possibilities.append('S')
                    if x < width - 1: possibilities.append('E')

                elif corner == 'bottom-left':
                    if y < height - 1: possibilities.append('S')
                    if x > 0: possibilities.append('W')

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

# ==========================================
# 2. THE VISUALIZER LOGIC
# ==========================================

# The "Heavy" Box Drawing Character Set for smooth lines
BOX_CHARS = {
    # (Up, Down, Left, Right)
    (False, False, False, False): ' ',
    (False, False, False, True):  '╺',
    (False, False, True,  False): '╸',
    (False, False, True,  True):  '━',
    (False, True,  False, False): '╻',
    (True,  False, False, False): '╹',
    (True,  True,  False, False): '┃',
    (False, True,  False, True):  '┏',
    (False, True,  True,  False): '┓',
    (True,  False, False, True):  '┗',
    (True,  False, True,  False): '┛',
    (False, True,  True,  True):  '┳',
    (True,  False, True,  True):  '┻',
    (True,  True,  False, True):  '┣',
    (True,  True,  True,  False): '┫',
    (True,  True,  True,  True):  '╋',
}

def draw_smart_maze(stdscr, grid, width, height):
    # Setup Colors
    if curses.has_colors():
        curses.start_color()
        curses.use_default_colors()
        # Pair 1: Blue/Cyan walls
        curses.init_pair(1, curses.COLOR_WHITE, -1)
    
    wall_attr = curses.color_pair(1) | curses.A_BOLD

    # 1. Create a map of "Edges" to determine connection types
    # Size is (2x + 1)
    max_h = height * 2 + 1
    max_w = width * 2 + 1
    edge_map = [[False for _ in range(max_w)] for _ in range(max_h)]

    for y in range(height):
        for x in range(width):
            cell = grid[y][x]
            cy, cx = y * 2 + 1, x * 2 + 1 # Center of cell

            # If wall exists, mark it on the edge map
            if cell.north: edge_map[cy - 1][cx] = True
            if cell.south: edge_map[cy + 1][cx] = True
            if cell.west:  edge_map[cy][cx - 1] = True
            if cell.east:  edge_map[cy][cx + 1] = True

    # 2. Render Loop
    for y in range(max_h):
        for x in range(max_w):
            
            # If it's a "Room" (odd, odd), skip or draw floor
            if y % 2 == 1 and x % 2 == 1:
                stdscr.addch(y, x, ' ') 
                continue

            # If it's a wall/junction (even coordinates involved)
            # Check neighbors to pick the right Unicode character
            has_up    = edge_map[y-1][x] if y > 0 else False
            has_down  = edge_map[y+1][x] if y < max_h - 1 else False
            has_left  = edge_map[y][x-1] if x > 0 else False
            has_right = edge_map[y][x+1] if x < max_w - 1 else False

            # If it's a vertex (intersection), draw it based on connections
            if y % 2 == 0 and x % 2 == 0:
                if not (has_up or has_down or has_left or has_right):
                    char = ' ' # Isolated vertex
                else:
                    char = BOX_CHARS.get((has_up, has_down, has_left, has_right), '?')
                stdscr.addch(y, x, char, wall_attr)
            
            # If it's a straight wall piece
            elif edge_map[y][x]:
                char = '┃' if y % 2 == 1 else '━'
                stdscr.addch(y, x, char, wall_attr)

def main(stdscr):
    # Initial Curses Setup
    curses.curs_set(0) # Hide cursor
    stdscr.clear()

    # Define Maze Size
    WIDTH = 70
    HEIGHT = 45
    SEED = None

    # Check terminal size
    sh, sw = stdscr.getmaxyx()
    if sh < HEIGHT * 2 + 1 or sw < WIDTH * 2 + 1:
        stdscr.addstr(0, 0, "Terminal too small! Zoom out.")
        stdscr.getch()
        return

    # Generate First Maze
    grid = MazeGen.binary_tree_maze(WIDTH, HEIGHT, SEED)

    while True:
        stdscr.clear()

        # Instructions
        stdscr.addstr(0, 0, f"Maze Size: {WIDTH}x{HEIGHT} | Press 'r' to Regenerate | 'q' to Quit")
        
        # Draw the Maze (shifted down by 2 lines)
        # Create a sub-window or just write to stdscr
        draw_smart_maze(stdscr, grid, WIDTH, HEIGHT)

        stdscr.refresh()

        # Input Handling
        try:
            key = stdscr.getkey()
        except:
            continue

        if key.lower() == 'q':
            break
        elif key.lower() == 'r':
            # Regenerate with a random seed
            SEED = random.randint(0, 9999)
            grid = MazeGen.binary_tree_maze(WIDTH, HEIGHT, SEED)

if __name__ == "__main__":
    curses.wrapper(main)