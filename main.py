import curses
import sys
import time
import ast

TOP = 1
RIGHT = 2
BOTTOM = 4
LEFT = 8

# ================= FILE PARSER =================

def read_file(path):
    with open(path, "r") as f:
        lines = [l.strip() for l in f if l.strip()]

    maze_lines = []
    i = 0

    while i < len(lines) and all(c in "0123456789ABCDEFabcdef" for c in lines[i]):
        maze_lines.append(lines[i])
        i += 1

    maze = [[int(c, 16) for c in line] for line in maze_lines]

    entry = ast.literal_eval(lines[i]); i += 1
    exit_  = ast.literal_eval(lines[i]); i += 1
    path = lines[i]

    return maze, entry, exit_, path

# ================= SAFE DRAW =================

def safe_addch(stdscr, y, x, ch):
    H, W = stdscr.getmaxyx()
    if 0 <= y < H and 0 <= x < W:
        try:
            stdscr.addch(y, x, ch)
        except:
            pass

# ================= WALL CHARS =================

def wall_char(up, right, down, left):
    mask = (up << 0) | (right << 1) | (down << 2) | (left << 3)
    table = {
        0b0000: " ",
        0b0001: "╹",
        0b0010: "╺",
        0b0011: "┗",
        0b0100: "╻",
        0b0101: "┃",
        0b0110: "┏",
        0b0111: "┣",
        0b1000: "╸",
        0b1001: "┛",
        0b1010: "━",
        0b1011: "┻",
        0b1100: "┓",
        0b1101: "┫",
        0b1110: "┳",
        0b1111: "╋",
    }
    return table[mask]

# ================= BUILD WALL GRID =================

def build_wall_grid(maze):
    h = len(maze)
    w = len(maze[0])

    screen_h = h * 2 + 1
    screen_w = w * 2 + 1

    grid = [[0 for _ in range(screen_w)] for _ in range(screen_h)]

    for y in range(h):
        for x in range(w):
            cell = maze[y][x]
            gy = y * 2
            gx = x * 2

            if cell & TOP:
                grid[gy][gx] = grid[gy][gx+1] = grid[gy][gx+2] = 1
            if cell & BOTTOM:
                grid[gy+2][gx] = grid[gy+2][gx+1] = grid[gy+2][gx+2] = 1
            if cell & LEFT:
                grid[gy][gx] = grid[gy+1][gx] = grid[gy+2][gx] = 1
            if cell & RIGHT:
                grid[gy][gx+2] = grid[gy+1][gx+2] = grid[gy+2][gx+2] = 1

    return grid

# ================= DRAW MAZE =================

def draw_maze(stdscr, grid):
    H = len(grid)
    W = len(grid[0])

    for y in range(H):
        for x in range(W):
            if grid[y][x] == 0:
                safe_addch(stdscr, y, x, " ")
            else:
                up = y > 0 and grid[y-1][x]
                down = y < H-1 and grid[y+1][x]
                left = x > 0 and grid[y][x-1]
                right = x < W-1 and grid[y][x+1]
                ch = wall_char(up, right, down, left)
                safe_addch(stdscr, y, x, ch)

# ================= ANIMATE PATH =================

def animate_path(stdscr, grid, entry, exit_, path):
    # entry and exit are (row, col)
    sy = entry[0] * 2 + 1
    sx = entry[1] * 2 + 1

    ey = exit_[0] * 2 + 1
    ex = exit_[1] * 2 + 1

    # Draw S and E INSIDE maze
    safe_addch(stdscr, sy, sx, "E")
    safe_addch(stdscr, ey, ex, "X")
    stdscr.refresh()

    time.sleep(50)

    DIR = {
        "N": (-1, 0),
        "S": (1, 0),
        "E": (0, 1),
        "W": (0, -1),
    }

    cy, cx = sy, sx

    for move in path:
        dy, dx = DIR[move]

        # Each step is TWO moves (corridor + next cell)
        for _ in range(2):
            ny = cy + dy
            nx = cx + dx

            # Don't draw over walls
            if grid[ny][nx] == 0:
                cy, cx = ny, nx

                if (cy, cx) != (ey, ex):
                    safe_addch(stdscr, cy, cx, "█")

                stdscr.refresh()
                time.sleep(0.01)

    # Redraw end
    safe_addch(stdscr, ey, ex, "E")
    stdscr.refresh()

# ================= MAIN =================

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()

    if len(sys.argv) != 2:
        stdscr.addstr(0, 0, "Usage: python3 maze.py file.txt")
        stdscr.getch()
        return

    maze, entry, exit_, path = read_file(sys.argv[1])
    grid = build_wall_grid(maze)

    # Check terminal size
    H, W = stdscr.getmaxyx()
    if len(grid) > H or len(grid[0]) > W:
        stdscr.clear()
        stdscr.addstr(0, 0, "Terminal too small for this maze!")
        stdscr.addstr(1, 0, f"Need: {len(grid)} x {len(grid[0])}")
        stdscr.addstr(2, 0, f"Have: {H} x {W}")
        stdscr.getch()
        return

    draw_maze(stdscr, grid)
    animate_path(stdscr, grid, entry, exit_, path)

    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)