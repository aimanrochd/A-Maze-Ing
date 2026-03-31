import sys
import curses
import random
import time
from typing import Dict, List, Tuple, Any

from config_parser import parse_config, validate_config
from mazegen.algorithms import MazeGenerator
from mazegen.visualizer import Visualizer
from mazegen.writer import write_hex_output


def main() -> None:
    """Entry point of the application.

    Parses and validates the configuration file provided as a command-line
    argument, then launches the curses-based visual flow. Exits with an
    error message if arguments are missing, the config is invalid, or an
    unexpected runtime error occurs.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    try:
        config = parse_config(sys.argv[1])
        validate_config(config, sys.argv[1])
    except Exception as e:
        print(f"Config Error: {e}")
        sys.exit(1)

    try:
        curses.wrapper(lambda stdscr: run_visual_flow(stdscr, config))
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Fatal Error: {e}")
        sys.exit(1)


def _draw_entity(
    stdscr: Any, x: int, y: int, char: str,
    color_pair: int, is_rev: bool = False
) -> None:
    """Draw a single character entity on the maze screen.

    Converts maze grid coordinates to screen coordinates and renders
    the character with bold styling, optionally reversed for highlighting.
    Silently ignores curses errors caused by out-of-bounds positions.

    Args:
        stdscr: The main curses window.
        x: Maze grid column of the entity.
        y: Maze grid row of the entity.
        char: The character string to display.
        color_pair: Curses color pair index to apply.
        is_rev: If True, applies reverse video attribute for highlighting.
            Defaults to False.
    """
    if is_rev is True:
        style = (curses.color_pair(color_pair) |
                 curses.A_BOLD |
                 curses.A_REVERSE)
    else:
        style = curses.color_pair(color_pair) | curses.A_BOLD

    try:
        stdscr.addstr(y * 2 + 1, x * 4 + 2, char, style)
    except curses.error:
        pass


def play_game_mode(
    stdscr: Any, viz: Visualizer, grid: List[List[Any]],
    entry: Tuple[int, int], exit_pos: Tuple[int, int], wall_color: str
) -> None:
    """Run the interactive playable maze mode.

    Allows the user to navigate the maze using arrow keys. Redraws the
    board each frame, enforces wall collision, and displays a victory
    message when the player reaches the exit.

    Args:
        stdscr: The main curses window.
        viz: The Visualizer instance used for rendering.
        grid: 2D list of Cell objects representing the maze.
        entry: (col, row) coordinates of the maze entry point.
        exit_pos: (col, row) coordinates of the maze exit point.
        wall_color: Name of the wall color to use during rendering.
    """
    px, py = entry
    current_char = "▼"

    stdscr.timeout(-1)

    while True:
        viz.draw_board(grid, wall_color)

        _draw_entity(stdscr, entry[0], entry[1], "S", 6)
        _draw_entity(stdscr, exit_pos[0], exit_pos[1], "E", 4)
        _draw_entity(stdscr, px, py, current_char, 3)

        if (px, py) == exit_pos:
            _draw_entity(stdscr, exit_pos[0], exit_pos[1], "E", 6, is_rev=True)
            stdscr.refresh()
            curses.napms(200)
            viz.draw_status("VICTORY! You Solved The Maze! Press Any Key...")
            stdscr.getch()
            return

        viz.draw_status("ARROWS To Move, 'q' To Quit.")

        key = stdscr.getch()
        if key == ord('q'):
            break

        if not (0 <= py < len(grid) and 0 <= px < len(grid[0])):
            continue

        cell = grid[py][px]

        moves = {
            curses.KEY_UP: ("▲", 0, -1, cell.north),
            curses.KEY_DOWN: ("▼", 0, 1, cell.south),
            curses.KEY_RIGHT: ("►", 1, 0, cell.east),
            curses.KEY_LEFT: ("◄", -1, 0, cell.west)
        }

        if key in moves:
            char, dx, dy, has_wall = moves[key]
            current_char = char
            if not has_wall:
                px += dx
                py += dy


def save_maze(config: Dict[str, Any], maze_seed: int, viz: Visualizer) -> None:
    """Generate and save the maze to the configured output file.

    Runs the full generation pipeline headlessly (without animation) and
    writes the hex-encoded maze, entry, exit, and solution path to the
    output file specified in the config. Errors are silently ignored to
    avoid interrupting the visual flow.

    Args:
        config: Dictionary of validated configuration values.
        maze_seed: Integer seed for reproducible maze generation.
        viz: The Visualizer instance (unused directly, reserved
        for future use).
    """
    try:
        maze = MazeGenerator(config['HEIGHT'], config['WIDTH'])
        algo = config.get('ALGORITHM', 'recursive_backtracker').lower()
        algo_name = 'prims' if 'prims' in algo else 'recursive_backtracker'

        maze.generate_maze(config['ENTRY'], config['EXIT'],
                           algo_name, maze_seed)
        if not config.get('PERFECT', True):
            maze.braid_maze()
        write_hex_output(
            maze.grid, config['ENTRY'], config['EXIT'],
            maze.solve(config['ENTRY'], config['EXIT']),
            config['OUTPUT_FILE']
        )
    except Exception as e:
        raise Exception(e)


def generate_and_visualize(
    config: Dict[str, Any], maze_seed: int,
    viz: Visualizer, wall_color: str
) -> MazeGenerator:
    """Generate the maze with a step-by-step visual animation.

    Runs the maze generation algorithm with a callback that redraws the
    board after each step, producing a live construction animation. After
    generation, applies braiding if configured and computes the solution.

    Args:
        config: Dictionary of validated configuration values.
        maze_seed: Integer seed for reproducible maze generation.
        viz: The Visualizer instance used for rendering each step.
        wall_color: Name of the wall color to use during rendering.

    Returns:
        The fully generated and solved MazeGenerator instance.
    """
    algo = config.get('ALGORITHM', 'recursive_backtracker').lower()
    algo_name = 'prims' if 'prim' in algo else 'recursive_backtracker'

    gen = MazeGenerator(config['HEIGHT'], config['WIDTH'])

    def step_callback() -> None:
        viz.draw_board(gen.grid, wall_color)
        time.sleep(0.01)

    gen.generate_maze(
        config['ENTRY'], config['EXIT'], algo_name, maze_seed,
        step_callback
    )
    if not config.get('PERFECT', True):
        gen.braid_maze()
    gen.solve(config['ENTRY'], config['EXIT'])
    return gen


def handle_post_gen_loop(
    stdscr: Any, viz: Visualizer, config: Dict[str, Any],
    gen: MazeGenerator, wall_color: str, colors: List[str]
) -> str:
    """Manage the post-generation menu interaction loop.

    Renders the maze and handles user actions from the control menu,
    including toggling the solution path, cycling wall colors, launching
    play mode, regenerating, or quitting.

    Args:
        stdscr: The main curses window.
        viz: The Visualizer instance used for rendering.
        config: Dictionary of validated configuration values.
        gen: The fully generated and solved MazeGenerator instance.
        wall_color: The currently active wall color name.
        colors: List of available wall color names to cycle through.

    Returns:
        A string indicating the next action: 'new_maze' or 'quit'.
    """
    path_visible = False
    anim_played = False
    selected_index = 0

    while True:
        viz.draw_board(gen.grid, wall_color)

        if path_visible:
            should_anim = not anim_played
            viz.draw_path(config['ENTRY'], config['EXIT'],
                          "".join(gen.solution), animate=should_anim)
            if should_anim:
                anim_played = True

        action, selected_index = viz.show_post_gen_menu(
            path_visible, wall_color, config['WIDTH'],
            config['HEIGHT'], selected_index
        )

        if action == "play_game":
            play_game_mode(stdscr, viz, gen.grid, config['ENTRY'],
                           config['EXIT'], wall_color)
        elif action == "toggle_path":
            path_visible = not path_visible
        elif action == "cycle_color":
            idx = (colors.index(wall_color) + 1) % len(colors)
            wall_color = colors[idx]
        elif action == "new_maze":
            return "new_maze"
        elif action == "quit":
            return "quit"


def run_visual_flow(stdscr: Any, config: Dict[str, Any]) -> None:
    """Orchestrate the full visual application flow.

    Displays the main menu, initializes the maze seed and wall color,
    validates terminal size, then loops through maze generation and
    the post-generation menu until the user quits.

    Args:
        stdscr: The main curses window provided by curses.wrapper.
        config: Dictionary of validated configuration values.

    Raises:
        Exception: If the terminal is too small to display the maze.
    """
    viz = Visualizer(stdscr)
    if viz.show_menu() == 'quit':
        return

    colors = ["Cyan", "Yellow", "Red", "White"]
    wall_color = colors[random.randint(0, 3)]

    seed = config.get('SEED')
    if seed is not None:
        maze_seed = int(seed)
    else:
        maze_seed = random.randint(0, 999999)

    while True:
        sh, sw = stdscr.getmaxyx()
        maze_w = (config['WIDTH'] * 4) + 1
        maze_h = (config['HEIGHT'] * 2) + 1
        if maze_w + 25 > sw or maze_h > sh:
            raise Exception("Size of the screen is smaller than the maze size")

        save_maze(config, maze_seed, viz)

        gen = generate_and_visualize(
            config, maze_seed, viz, wall_color
        )

        result = handle_post_gen_loop(
            stdscr, viz, config, gen, wall_color, colors
        )

        if result == "quit":
            return
        elif result == "new_maze":
            if not config.get('SEED'):
                maze_seed = random.randint(0, 999999)


if __name__ == "__main__":
    main()
