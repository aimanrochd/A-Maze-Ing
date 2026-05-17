*This project has been created as part of the 42 curriculum by mzoubir, arochd.*

## Description
A-Maze-ing is a highly customizable and interactive terminal-based maze generator and solver. The primary goal of this project is to implement robust graph algorithms capable of generating perfect (single path) and imperfect (multiple paths) mazes, and to simulate their creation and solution visibly within a TUI (Text User Interface). Randomness and algorithmic complexity dictate the challenge of the mazes, while the resulting generation is verifiable and correctly formatted using hex encoding.

## Instructions
**Installation:**
You can safely install project dependencies inside a virtual environment using the Makefile:
```bash
make install
```

**Execution:**
You can run the program directly via the Makefile standard test or by invoking the python script directly with absolute paths.
```bash
make run
# Or manually
python3 a_maze_ing.py config.txt
```

**Display Controls:**
Once generated, you can use the interactive menu:
- `↑` / `↓` : Navigate the menu options
- `Enter` : Confirm selection
- Options include toggling the visibility of the shortest path, cycling wall colors, or instantly regenerating a brand new layout.

## Resources
During the development of this project, we primarily relied on the following resources:
1. "Graph Theory and Maze Generation" literature (understanding DFS vs BFS logic).
2. `curses` Python Official Documentation (for terminal rendering and state management).

**AI Usage:**
AI was utilized under strict project guidelines to accelerate development and resolve specific technical blockers:
- **Type annotations (all files):** AI was used to audit and complete `mypy`-compatible type hints across `visualizer.py`, `algorithms.py`, and `writer.py`, catching missing `Tuple`, `List`, and `Any` annotations.
- **Makefile auditing:** AI reviewed our Makefile structure to verify it matched the assignment rule-set, specifically checking target names, virtual environment handling, and the `.whl` packaging step.
- **Debugging curses crashes:** AI helped diagnose a recurring `curses.error` caused by writing to the bottom-right terminal corner during resize events, and guided the placement of `try/except` guards in `draw_board` and `draw_status`.

---

## Configuration File Format
The program reads variables from a simple `.txt` config file defined by strict `KEY=VALUE` pairs. Here is the structure:
```
WIDTH=20                     # Maze width (9 to 100)
HEIGHT=15                    # Maze height (7 to 100)
ENTRY=0,0                    # Entry coordinates
EXIT=19,14                   # Exit coordinates
OUTPUT_FILE=maze.txt         # Output encoding file location
PERFECT=true                 # true for perfect mazes, false for braided/imperfect
ALGORITHM=recursive_backtracker # The generation algorithm to trigger
```

## Maze Generation Algorithm

**Chosen Algorithms:**
1. **Recursive Backtracker** (Depth-First Search) 
2. **Prim's Algorithm**

**Why we chose them:**
We implemented the Recursive Backtracker because it naturally creates "perfect" mazes that feature long, winding, and convoluted "snake-like" corridors which are aesthetically pleasing and difficult for humans to solve quickly. It is memory-efficient and easy to implement using a stack. We secondary implemented Prim's Algorithm because it yields mazes with a more "cellular" or branching look with many short, confusing dead-ends, offering high variety in our resulting outputs.

## Reusable Code
The core algorithmic generation components of this project have been deliberately isolated from the terminal UI and converted into a standalone, pip-installable module named `mazegen`. It allows third-party scripts to import our exact logic reliably.

**How to use our package:**
```bash
make install # Installs the local .whl package
```
```python
from mazegen import MazeGenerator

gen = MazeGenerator(height=20, width=20)  # or MazeGenerator(20, 20)
gen.generate_maze(entry=(0,0), exit_pos=(19,19), algorithm="prims", seed=42)
gen.solve((0,0), (19,19))
```

## Team and Project Management

**Roles:**
- **Aiman Rochd**: Engineered the interactive menus and banner (`visualizer.py`), path animation rendering, grid encoding and output formatting (`writer.py`), and configuration file parsing.
- **Mohamed Zoubir**: Implemented the maze generation algorithms and generation animation (`algorithms.py`), pathfinding logic, project architecture and auditing, Makefile structure, and module packaging.

**Anticipated Planning vs Reality:**
Initially, we planned to build the mathematical generation and the terminal rendering simultaneously. However, this caused massive debugging delays because we couldn't tell if the bugs were in the math or the display. We evolved to build and thoroughly test the data structures (`Cell`/grid lists) completely headless first, then overlay the visualizer on top of known-working data.

**What worked well and what could be improved:**
- *Worked well:* Our decision to utilize a stateless grid of `Cell` objects made rendering trivial.
- *Needs improvement:* The visualizer currently redraws large sections of the screen each tick instead of just deltas, which was challenging to optimize for terminal bounds checking.

**Specific Tools Used:**
- `flake8`: To enforce code style.
- `mypy`: Used strictly to guarantee no type-hint leaks across the modules.
- Python `curses`: For robust TUI rendering instead of raw print statement strings.

## Advanced Features
- **Imperfect Generation:** If `PERFECT=False` in the config file, the maze undergoes a dedicated `braiding` process (after generation) that locates dead ends and destroys selective walls dynamically, allowing multiple routes to the exit.
- **Multiple Algorithms:** The user can specify `ALGORITHM=prims` to override the default DFS-based generation.
- **Dynamic Visual Colors:** We implemented a color cycling state loop attached to the keyboard interrupts, allowing the user to dynamically recolor walls.