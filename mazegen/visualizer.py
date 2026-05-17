import curses
from typing import List, Tuple, Any
from .cell import Cell
import time


class Visualizer:
    """Render the maze and UI using curses.

    Attributes:
        stdscr: The main curses window provided by curses.wrapper.
    """

    def __init__(self, stdscr: Any) -> None:
        """Initialize curses rendering settings and color pairs.

        Args:
            stdscr: The main curses window provided by curses.wrapper.
        """
        self.stdscr = stdscr
        curses.curs_set(0)
        colors = [
            (1, curses.COLOR_WHITE, curses.COLOR_BLACK),
            (2, curses.COLOR_CYAN, curses.COLOR_BLACK),
            (3, curses.COLOR_YELLOW, curses.COLOR_BLACK),
            (4, curses.COLOR_RED, curses.COLOR_BLACK),
            (5, curses.COLOR_MAGENTA, curses.COLOR_BLACK),
            (6, curses.COLOR_GREEN, curses.COLOR_BLACK),
            (7, curses.COLOR_WHITE, curses.COLOR_BLACK),
            (8, curses.COLOR_BLACK, curses.COLOR_CYAN),
        ]
        for color_data in colors:
            curses.init_pair(*color_data)
        self.stdscr.bkgd(' ', curses.color_pair(1))

    def _get_wall_char(self, u: bool, r: bool, d: bool, wall_l: bool) -> str:
        """Choose a box-drawing character for a wall intersection.

        Args:
            u: Wall exists above.
            r: Wall exists to the right.
            d: Wall exists below.
            wall_l: Wall exists to the left.

        Returns:
            A single Unicode box-drawing character.
        """
        mask = (
            (int(u) << 0) | (int(r) << 1) | (int(d) << 2) | (int(wall_l) << 3)
        )
        chars = {
            0: " ", 1: "╹", 2: "╺", 3: "┗", 4: "╻", 5: "┃", 6: "┏", 7: "┣",
            8: "╸", 9: "┛", 10: "━", 11: "┻", 12: "┓", 13: "┫", 14: "┳",
            15: "╋"
        }
        return chars.get(mask, " ")

    def draw_status(self, msg: str) -> None:
        """Draw a centered status bar on the last row of the terminal.

        Silently ignores curses errors caused by terminal resize or
        writing near the bottom-right corner.

        Args:
            msg: The status message to display.
        """
        screen_height, screen_width = self.stdscr.getmaxyx()
        try:
            self.stdscr.move(screen_height - 1, 0)
            self.stdscr.clrtoeol()
            x_pos = max(0, (screen_width - len(msg)) // 2)
            self.stdscr.addstr(
                screen_height - 1,
                x_pos,
                msg,
                curses.color_pair(2) | curses.A_REVERSE
            )
            self.stdscr.refresh()
        except curses.error:
            pass

    def _build_view_map(
        self, grid: List[List[Cell]], rows: int, cols: int
    ) -> List[List[int]]:
        """Build a 2D integer map of the maze for rendering.

        Each cell in the map is encoded as:
            0 - open passage,
            1 - wall,
            2 - special cell (is_42).

        Args:
            grid: 2D list of Cell objects representing the maze.
            rows: Number of rows in the maze grid.
            cols: Number of columns in the maze grid.

        Returns:
            A 2D list of integers with screen dimensions (rows*2+1, cols*4+1).
        """
        screen_h, screen_w = rows * 2 + 1, cols * 4 + 1
        v_map = [[1] * screen_w for _ in range(screen_h)]

        for row in range(rows):
            for col in range(cols):
                cell = grid[row][col]
                vr, vc = row * 2 + 1, col * 4 + 2
                val = 2 if cell.is_42 else 0
                for dx in (-1, 0, 1):
                    v_map[vr][vc + dx] = val
                    if not cell.north:
                        v_map[vr - 1][vc + dx] = val
                    if not cell.south:
                        v_map[vr + 1][vc + dx] = val
                if not cell.west:
                    v_map[vr][vc - 2] = val
                if not cell.east:
                    v_map[vr][vc + 2] = val
        return v_map

    def draw_board(
        self, grid: List[List[Cell]],
        wall_color_name: str = "Cyan"
    ) -> None:
        """Render the maze walls and special cells to the screen.

        Iterates over the view map and draws each tile using box-drawing
        characters for walls and block characters for passages. Silently
        aborts the current frame on curses errors caused by terminal resize.

        Args:
            grid: 2D list of Cell objects representing the maze.
            wall_color_name: Name of the wall color to use. One of
                "Cyan", "Yellow", "Red", or "White". Defaults to "Cyan".
        """
        self.stdscr.erase()
        rows, cols = len(grid), len(grid[0])
        screen_h, screen_w = rows * 2 + 1, cols * 4 + 1

        color_map = {"Cyan": 2, "Yellow": 3, "Red": 4, "White": 1}
        attr = curses.color_pair(color_map.get(wall_color_name, 2))

        v_map = self._build_view_map(grid, rows, cols)

        try:
            for y in range(screen_h):
                for x in range(screen_w):
                    tile = v_map[y][x]
                    if tile in (0, 2):
                        char = "█" if tile == 2 else " "
                        self.stdscr.addstr(y, x, char, curses.color_pair(1))
                    else:
                        u = (y > 0 and v_map[y - 1][x] == 1)
                        d = (y < screen_h - 1 and v_map[y + 1][x] == 1)
                        wall_l = (x > 0 and v_map[y][x - 1] == 1)
                        r = (x < screen_w - 1 and v_map[y][x + 1] == 1)
                        char = self._get_wall_char(u, r, d, wall_l)
                        self.stdscr.addstr(y, x, char, attr)
        except curses.error:
            pass
        self.stdscr.refresh()

    def _draw_cell(self, x: int, y: int, color_pair: int) -> None:
        """Draw a two-character colored block at the given screen position.

        Args:
            x: Screen x-coordinate (column).
            y: Screen y-coordinate (row).
            color_pair: Curses color pair index to use for the block.
        """
        style = curses.color_pair(color_pair)
        self.stdscr.addstr(y, x, "██", style)

    def draw_path(
        self,
        entry: Tuple[int, int],
        exit_pos: Tuple[int, int],
        path_str: str,
        animate: bool = False,
    ) -> None:
        """Draw the solution path from entry to exit on the maze.

        Marks the entry cell in magenta, the exit cell in red, and
        all intermediate path cells in green. Optionally animates
        the path step by step.

        Args:
            entry: (col, row) grid coordinates of the maze entry point.
            exit_pos: (col, row) grid coordinates of the maze exit point.
            path_str: String of direction characters ('N', 'S', 'E', 'W')
                describing the path from entry to exit.
            animate: If True, render each step with a short delay.
                Defaults to False.
        """
        cx, cy = entry[0] * 4 + 2, entry[1] * 2 + 1
        ex, ey = exit_pos[0] * 4 + 2, exit_pos[1] * 2 + 1

        moves = {'N': (0, -1), 'S': (0, 1), 'E': (2, 0), 'W': (-2, 0)}

        self._draw_cell(cx, cy, 5)
        self._draw_cell(ex, ey, 4)

        if animate:
            self.stdscr.refresh()
            time.sleep(0.6)

        for d in path_str:
            dx, dy = moves[d]

            cx += dx
            cy += dy
            self._draw_cell(cx, cy, 6)

            cx += dx
            cy += dy
            if (cx, cy) != (ex, ey):
                self._draw_cell(cx, cy, 6)

            if animate:
                self.stdscr.refresh()
                time.sleep(0.065)

        self._draw_cell(ex, ey, 4)
        self.stdscr.refresh()

    def show_menu(self) -> str:
        """Display the main menu and return the user's selection.

        Renders the ASCII title, navigation options, and footer.
        Raises a RuntimeError if the terminal is too small to display
        the menu.

        Returns:
            'generate' if the user selects "GENERATE MAZE",
            'quit' if the user selects "QUIT GAME".

        Raises:
            RuntimeError: If the terminal dimensions are too small.
        """
        title = [
            "  ▄       ▗▄ ▄▖  ▄  ▗▄▄▄▖▗▄▄▄▖      ▄▄▄ ▗▄ ▗▖  ▄▄ ",
            " ▐█▌      ▐█ █▌ ▐█▌ ▝▀▀█▌▐▛▀▀▘      ▀█▀ ▐█ ▐▌ █▀▀▌",
            " ▐█▌      ▐███▌ ▐█▌   ▐▛ ▐▌          █  ▐▛▌▐▌▐▌   ",
            " █ █      ▐▌█▐▌ █ █  ▗█▘ ▐███        █  ▐▌█▐▌▐▌▗▄▖",
            " ███  ██▌ ▐▌▀▐▌ ███  ▟▌  ▐▌    ██▌   █  ▐▌▐▟▌▐▌▝▜▌",
            "▗█ █▖     ▐▌ ▐▌▗█ █▖▐█▄▄▖▐▙▄▄▖      ▄█▄ ▐▌ █▌ █▄▟▌",
            "▝▘ ▝▘     ▝▘ ▝▘▝▘ ▝▘▝▀▀▀▘▝▀▀▀▘      ▀▀▀ ▝▘ ▀▘  ▀▀ ",
        ]
        options = ["GENERATE MAZE", "QUIT GAME"]
        selection = 0

        while True:
            self.stdscr.erase()
            screen_height, screen_width = self.stdscr.getmaxyx()

            min_w = len(title[0])
            min_h = len(title) + 12
            if screen_width < min_w or screen_height < min_h:
                raise RuntimeError(
                    "Terminal too small to display the menu."
                )

            start_y = (screen_height - (len(title) + 9)) // 2

            for index, line in enumerate(title):
                x_pos = (screen_width - len(line)) // 2
                self.stdscr.addstr(
                    start_y + index, x_pos, line, curses.color_pair(2)
                )

            box_y, box_x = start_y + len(title) + 2, screen_width // 2
            self.stdscr.addstr(
                box_y, box_x - 20, "=" * 40, curses.color_pair(2)
            )
            self.stdscr.addstr(
                box_y + 1, box_x - 13, "===      MAZE CONTROL      ===",
                curses.color_pair(2)
            )
            self.stdscr.addstr(
                box_y + 6, box_x - 20, "=" * 40, curses.color_pair(2)
            )

            for index, option in enumerate(options):
                if selection == index:
                    style = curses.color_pair(8)
                    display_text = f"> {option} <"
                else:
                    style = curses.color_pair(2)
                    display_text = f"   {option}   "

                x_off = box_x - len(display_text) // 2
                self.stdscr.addstr(
                    box_y + 3 + index, x_off, display_text, style
                )

            made_by_text = "Made by Aiman Rochd && Mohamed Zoubir"
            x_pos = (screen_width - len(made_by_text)) // 2
            self.stdscr.addstr(
                screen_height - 2, x_pos, made_by_text,
                curses.color_pair(1)
            )

            key_pressed = self.stdscr.getch()
            if key_pressed == curses.KEY_UP:
                selection = 0
            elif key_pressed == curses.KEY_DOWN:
                selection = 1
            elif key_pressed in [10, 13]:
                return 'generate' if selection == 0 else 'quit'

    def show_post_gen_menu(
        self,
        path_visible: bool,
        current_color: str,
        maze_columns: int,
        maze_height: int,
        selected_index: int,
    ) -> Tuple[str, int]:
        """Display the post-generation control menu and handle navigation.

        Renders the maze control options to the right of the maze and
        returns the selected action when the user presses Enter. Raises
        an exception if the terminal is too small for the maze and menu.

        Args:
            path_visible: Whether the solution path is currently shown.
                Determines the label of the toggle option.
            current_color: The currently active wall color name, displayed
                in the color cycle option.
            maze_columns: Number of columns in the maze, used to position
                the menu to the right of the maze.
            maze_height: Number of rows in the maze, used to validate
                terminal height.
            selected_index: The index of the currently highlighted menu item.

        Returns:
            A tuple of (action, selected_index) where action is one of:
                'play_game', 'toggle_path', 'cycle_color', 'new_maze', 'quit'.

        Raises:
            Exception: If the terminal is too small to display the maze
            and menu.
        """
        NORMAL_STYLE = curses.color_pair(2)
        SELECTED_STYLE = curses.color_pair(8)

        menu_actions = [
            "play_game", "toggle_path", "cycle_color", "new_maze", "quit"
        ]

        while True:
            menu_labels = [
                "PLAY MAZE",
                "HIDE PATH" if path_visible else "SHOW PATH",
                f"COLOR: {current_color}",
                "RE-GENERATE A NEW MAZE",
                "QUIT GAME",
            ]

            screen_height, screen_width = self.stdscr.getmaxyx()

            maze_width = (maze_columns * 4) + 1

            menu_x = min(maze_width + 4, screen_width - 22)

            if menu_x + 25 > screen_width or maze_height * 2 > screen_height:
                raise Exception(
                    "Size of the screen is smaller than the maze size"
                )

            self.stdscr.addstr(1, menu_x,
                               "===== MAZE CONTROL =====", NORMAL_STYLE)

            for idx, label in enumerate(menu_labels):
                is_selected = idx == selected_index
                style = SELECTED_STYLE if is_selected else NORMAL_STYLE
                self.stdscr.addstr(3 + idx, menu_x, label, style)

            self.stdscr.addstr(9, menu_x, "=" * 24, NORMAL_STYLE)

            key = self.stdscr.getch()
            if key == curses.KEY_UP:
                selected_index = max(0, selected_index - 1)
            elif key == curses.KEY_DOWN:
                selected_index = min(len(menu_labels) - 1, selected_index + 1)
            elif key in (10, 13):
                return menu_actions[selected_index], selected_index
