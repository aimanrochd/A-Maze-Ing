# A-Maze-ing: Procedural Maze Generator 🧩

*This project has been created as part of the 42 curriculum by [YourLogin] and [FriendLogin].*

---

## 📝 Description

**A-Maze-ing** is a Python-based maze generator that explores the intersection of algorithmic complexity and visual design. The program reads a configuration file to generate a maze—ensuring it is "perfect" (unicursal) if requested—and exports the result in a hexadecimal wall representation format.

### Key Features

- **Algorithmic Generation**: Creates valid mazes with randomized paths, ensuring full connectivity and no 3×3 open areas
- **Perfect Maze Support**: Generates mazes with exactly one unique path between entrance and exit when requested
- **Pattern Integration**: Embeds a visual "42" pattern within the maze structure where size permits
- **Hexadecimal Export**: Outputs data using hexadecimal digits to encode wall configurations (North, East, South, West)
- **Interactive Visualization**: Provides visual representation (Terminal ASCII or MLX) with user controls to solve and explore the maze
- **Reusable Module**: Packaged as `mazegen` for integration into future projects
- **Configuration-Driven**: Flexible maze generation through simple configuration files

The project demonstrates practical applications of graph theory, recursive algorithms, bitwise operations, and procedural generation techniques commonly used in game development and network design.

---

## 👥 Team & Project Management

### Team Structure

We adopted an **Agile approach**, splitting the project into **Backend/Architecture** and **Frontend/Integration** roles to ensure modularity and enable parallel development.

| Member | Role | Responsibilities |
| :--- | :--- | :--- |
| **Member 1** | **Backend & Architect** | • **Core Logic:** Developing the `mazegen` reusable package<br>• **Algorithm:** Implementing the Recursive Backtracker algorithm<br>• **Constraints:** Enforcing the "no 3×3 open area" rule and embedding the "42" pattern<br>• **Packaging:** Ensuring the module is buildable as a `.whl` or `.tar.gz` file<br>• **Validation:** Implementing wall coherency checks and maze connectivity verification<br>• **Unit Tests:** Writing comprehensive tests for generation and validation |
| **Member 2** | **Frontend & Integrator** | • **CLI:** Developing the `a_maze_ing.py` entry point and argument handling<br>• **Parsing:** Validating and parsing the `config.txt` file<br>• **I/O:** Generating the hexadecimal output file<br>• **Visualization:** Implementing the visual display and user interactions (regenerate, show path, color changes)<br>• **Integration:** Connecting the `mazegen` package with the main script<br>• **Makefile:** Creating automation commands for the project |

### Project Timeline

| Phase | Expected | Actual | Notes |
|-------|----------|--------|-------|
| **Planning & Architecture** | 3 days | 4 days | API design and module boundaries took longer than expected |
| **Core Development** | 7 days | 9 days | Wall coherency validation was more complex than anticipated |
| **Features & Polish** | 5 days | 6 days | "42" pattern placement in small mazes required edge case handling |
| **Testing & Documentation** | 3 days | 3 days | On schedule with comprehensive test coverage |
| **Total** | 18 days | 22 days | 22% over initial estimate |

### Planning & Tools

**Workflow Strategy:**
- We started by defining the `mazegen` API contract to allow the Frontend to mock data while the Backend implemented complex algorithms
- Used feature-branch workflow with pull requests for code review
- Regular integration checkpoints (every 2-3 days) to catch compatibility issues early

**Tools Used:**
- **Version Control**: Git + GitHub with feature branches
- **IDE**: VS Code with Python extensions (Pylance, Python Debugger)
- **Code Quality**: Flake8 (linting), Mypy (type checking)
- **Environment**: `venv` for dependency isolation
- **Testing**: pytest with coverage reporting
- **Documentation**: Markdown for README, docstrings following Google style
- **Package Building**: `build` module for creating distribution files

### What Worked Well ✅

- **Clear Role Separation**: Having distinct backend/frontend responsibilities minimized merge conflicts and enabled parallel work
- **API-First Design**: Defining the `MazeGenerator` interface early allowed independent development
- **Regular Integration**: Weekly integration checkpoints caught compatibility issues before they became major problems
- **Git Workflow**: Feature branches and pull requests maintained code quality and provided natural review points
- **Communication**: Daily async updates via Slack kept everyone aligned without overhead

### What Could Be Improved 🔄

- **Time Estimation**: Underestimated the complexity of constraint validation (3×3 areas, wall coherency); should allocate 30-40% buffer time for validation logic
- **Testing Earlier**: Writing tests alongside development (TDD approach) would have caught bugs sooner and reduced debugging time
- **Documentation Timing**: Should have documented API decisions and design choices in real-time rather than at the end
- **Pair Programming**: More pairing sessions on complex algorithms (backtracker, pathfinding) would have accelerated learning and reduced bugs
- **Edge Case Planning**: Could have identified small maze edge cases earlier through better specification review

---

## 🛠️ Instructions

### Prerequisites

- Python 3.10 or later
- Standard Python libraries plus development tools: `flake8`, `mypy`, and `build`
- (Optional) MiniLibX library for graphical display

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd a-maze-ing

# Install dependencies
make install
```

### Makefile Commands

Use the provided `Makefile` to manage the project:

- **Install dependencies:**
    ```bash
    make install
    ```
    *Installs necessary packages using pip, uv, or pipx.*

- **Run the program:**
    ```bash
    make run
    ```
    *Executes `a_maze_ing.py` with the default configuration.*

- **Debug mode:**
    ```bash
    make debug
    ```
    *Runs the main script using Python's built-in debugger (pdb).*

- **Lint the code:**
    ```bash
    make lint
    ```
    *Checks code style with `flake8` and types with `mypy` using strict flags.*

- **Clean environment:**
    ```bash
    make clean
    ```
    *Removes temporary files (`__pycache__`, `.mypy_cache`, build artifacts).*

### Usage

```bash
# Generate a maze with default configuration
python3 a_maze_ing.py config.txt

# Or use the Makefile
make run
```

### Expected Output

The program generates two outputs:
1. **Hex file** (e.g., `maze.txt`): Contains the maze structure in hexadecimal format with entry, exit, and solution path
2. **Visual display**: Shows the maze in terminal (ASCII) or graphical window (MLX) with interactive controls

---

## ⚙️ Configuration

### Configuration File Format

The program is controlled via a configuration file passed as an argument. The format is `KEY=VALUE` with one parameter per line. Lines starting with `#` are comments and are ignored.

### Mandatory Keys

| Key | Description | Example |
| :--- | :--- | :--- |
| `WIDTH` | Maze width (number of cells) | `WIDTH=20` |
| `HEIGHT` | Maze height (number of cells) | `HEIGHT=15` |
| `ENTRY` | Entry coordinates (x,y) | `ENTRY=0,0` |
| `EXIT` | Exit coordinates (x,y) | `EXIT=19,14` |
| `OUTPUT_FILE` | Output filename for hex data | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Perfect maze flag (`True`/`False`) | `PERFECT=True` |

### Optional Keys

| Key | Description | Example |
|-----|-------------|---------|
| `SEED` | Random seed for reproducibility | `SEED=42` |
| `ALGORITHM` | Algorithm choice | `ALGORITHM=backtracker` |
| `DISPLAY_MODE` | Visualization method | `DISPLAY_MODE=ascii` |

### Example Configuration File

```ini
# Maze dimensions
WIDTH=40
HEIGHT=20

# Entry and exit points
ENTRY=0,0
EXIT=39,19

# Output settings
OUTPUT_FILE=output_maze.txt
PERFECT=True

# Optional: Reproducible generation
SEED=123456
ALGORITHM=backtracker

# Comments are ignored
```

A default `config.txt` is provided in the repository.

---

## 🧠 Maze Generation Algorithm

### Chosen Algorithm: Recursive Backtracker (DFS)

The **Recursive Backtracker** (also known as Depth-First Search maze generation) was selected as the primary algorithm for this project.

### How It Works

1. Start at a random cell and mark it as visited
2. While there are unvisited neighbors:
   - Choose a random unvisited neighbor
   - Remove the wall between current cell and chosen neighbor
   - Recursively visit the chosen neighbor
3. Backtrack when stuck (no unvisited neighbors)
4. Continue until all cells are visited

### Why This Algorithm?

**Advantages:**
- ✅ **Guarantees Perfect Mazes**: Naturally creates spanning trees where every cell is reachable and there are no loops, satisfying the `PERFECT=True` requirement
- ✅ **High Complexity**: Generates long, winding corridors rather than short dead-ends, which makes for aesthetically pleasing and challenging mazes
- ✅ **Memory Efficient**: Uses the call stack implicitly through recursion (or explicit stack for iterative version)
- ✅ **Simple Implementation**: Elegant recursive solution with clear, maintainable logic
- ✅ **Natural Branching**: Creates organic-looking maze structures with interesting path variations

**Trade-offs:**
- ⚠️ Can create very long corridors (which we consider a feature for challenge)
- ⚠️ Potential stack overflow for extremely large mazes (mitigated with iterative version for large grids)

### Handling Project Constraints

**"42" Pattern Integration:**
- We pre-carve specific cells into the shape of "42" and mark them as fully walled
- These cells are marked as "obstacles" before running the generation algorithm
- The algorithm routes around these cells, treating them as boundaries
- If the maze is too small to accommodate the pattern, an error message is displayed

**No 3×3 Open Areas:**
- The Recursive Backtracker naturally carves only 1-cell-wide paths
- Post-generation validation checks for any 3×3 open spaces
- The algorithm's corridor-focused approach inherently prevents large open areas
- Additional validation ensures compliance before finalizing the maze

**Wall Coherency:**
- When removing a wall between two cells, both sides are updated simultaneously
- Each cell tracks its four walls independently (North, East, South, West)
- Validation ensures neighboring cells agree on shared walls

### Alternative Algorithm (Bonus)

As a bonus feature, we also implemented **Kruskal's Algorithm**, which:
- Treats the maze as a graph where walls are edges
- Uses union-find data structure for efficient set operations
- Creates more uniform maze patterns with shorter average paths
- Better suited for certain game design applications requiring balanced difficulty

---

## 📦 Reusability: The `mazegen` Package

### Overview

The core generation logic is encapsulated in a standalone, pip-installable package named **`mazegen`**. This design allows the algorithm to be reused in future projects without code duplication.

### Installation

```bash
# From the wheel file
pip install mazegen-1.0.0-py3-none-any.whl

# Or from the tar.gz archive
pip install mazegen-1.0.0.tar.gz
```

### Building the Package

All necessary files to build the package are included in the repository:

```bash
# Install build tools
pip install build

# Build the package from source (run from repository root)
python3 -m build

# Output will be in dist/ directory:
# - mazegen-1.0.0-py3-none-any.whl
# - mazegen-1.0.0.tar.gz
```

### Usage Example

Once installed, you can import and use the generator in any Python project:

```python
from mazegen import MazeGenerator

# Instantiate with custom parameters
generator = MazeGenerator(width=20, height=15, seed=42)

# Generate a perfect maze
generator.generate(perfect=True, algorithm='backtracker')

# Access the maze structure (2D array of cells)
maze_data = generator.get_maze()

# Get entry and exit coordinates
entry = generator.get_entry()
exit = generator.get_exit()

# Find the solution path
solution = generator.find_path()
# Returns: ['N', 'E', 'S', 'W', 'N', ...] (directions)

# Export to hexadecimal format
hex_output = generator.to_hex_format()

print(f"Generated a {generator.width}x{generator.height} maze")
print(f"Solution has {len(solution)} steps")
```

### API Reference

**`MazeGenerator` Class**

```python
class MazeGenerator:
    def __init__(self, width: int, height: int, seed: Optional[int] = None)
    def generate(self, perfect: bool = True, algorithm: str = 'backtracker') -> None
    def get_maze(self) -> List[List[Cell]]
    def get_entry(self) -> Tuple[int, int]
    def get_exit(self) -> Tuple[int, int]
    def find_path(self) -> List[str]
    def solve(self, entry: Tuple[int, int], exit: Tuple[int, int]) -> List[str]
    def to_hex_format(self) -> str
    def validate(self) -> bool
```

### What's Reusable?

The `mazegen` package grants access to the maze structure, but it is not necessarily the same format as the output file.

- ✅ **Core Generation Logic**: All maze algorithms (Recursive Backtracker, Kruskal)
- ✅ **Cell Structure**: Internal representation of walls and connections
- ✅ **Pathfinding**: BFS-based shortest path solver
- ✅ **Validation**: Checks for connectivity, wall coherency, and constraint compliance
- ✅ **Export Utilities**: Hex encoding and data serialization methods

### What's NOT in the Package?

- ❌ Configuration file parsing (project-specific implementation)
- ❌ Visual rendering (ASCII/MLX display logic remains in main script)
- ❌ CLI interface and user interaction handlers
- ❌ Makefile and project automation

---

## 📝 Output File Format

The maze is exported using hexadecimal encoding where each cell's walls are represented by a single hex digit (0-F).

### Bit Encoding

Each hexadecimal digit encodes which walls are closed using a 4-bit binary representation:

| Bit Position | Direction | Value |
|--------------|-----------|-------|
| 0 (LSB) | North | 1 |
| 1 | East | 2 |
| 2 | South | 4 |
| 3 | West | 8 |

**A wall being closed sets the bit to 1; open means 0.**

### Examples

- `0` (binary `0000`): All walls open
- `3` (binary `0011`): North + East walls closed
- `F` (binary `1111`): All walls closed (fully enclosed cell, used for "42" pattern)
- `A` (binary `1010`): East + West walls closed
- `5` (binary `0101`): North + South walls closed
- `C` (binary `1100`): South + West walls closed

### File Structure

```
<hex values, one row per line>

<entry x,y>
<exit x,y>
<solution path: NESWNESW...>
```

**Example output file:**

```
9B7A3C...
8D4F2E...
...

0,0
19,14
EESENNWWSEENNESSWW
```

All lines end with `\n`.

---

## 🎨 Visual Representation

The program provides interactive visualization using either Terminal ASCII rendering or graphical display with MiniLibX (MLX).

### User Interactions

The visual interface supports the following interactions:

- **Regenerate**: Create and display a new random maze
- **Show/Hide Path**: Toggle visibility of the shortest solution path
- **Change Colors**: Customize maze wall colors
- **"42" Pattern Highlight** (Optional): Set specific colors to emphasize the "42" pattern

### Visual Example

```
┌─────┬─────┬─────┬─────┐
│ E   │     │     │     │
├─────┘ ┌───┼─────┤     ├
│       │ █ │     │     │
├───────┤ █ ├─────┴─────┤
│       │ █ │           │
├───────┴───┤     ┌─────┤
│           │     │    X│
└───────────┴─────┴─────┘
```

*E = Entry, X = Exit, █ = "42" pattern*

---

## 📚 Resources & AI Usage

### Classic References

#### Graph Theory & Algorithms
- [Maze Generation Algorithms](http://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap) - Comprehensive overview by Jamis Buck
- [Think Labyrinths!](http://www.astrolog.org/labyrnth/algrithm.htm) - Detailed algorithm explanations
- **"Mazes for Programmers"** by Jamis Buck - Comprehensive book on maze algorithms
- [Spanning Tree Algorithms](https://en.wikipedia.org/wiki/Minimum_spanning_tree) - Understanding Prim's vs. DFS
- **Introduction to Algorithms (CLRS)** - Graph theory fundamentals

#### Python Documentation
- [Python typing module](https://docs.python.org/3/library/typing.html) - Type hints reference
- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/) - Google and NumPy style guides
- [Python Packaging User Guide](https://packaging.python.org/) - Creating pip-installable packages

#### Bitwise Operations
- [Bitwise Operators in Python](https://realpython.com/python-bitwise-operators/) - Tutorial for hex encoding
- [Bit Manipulation Tricks](https://graphics.stanford.edu/~seander/bithacks.html) - Advanced techniques

### AI Usage Documentation

In compliance with the project guidelines, AI was used strategically for specific tasks. All AI-generated content was reviewed, tested, and refactored by the team to ensure understanding and compliance.

#### ✅ **Tasks Where AI Was Used:**

1. **Understanding Bitwise Logic** (Member 2)
   - Explaining how to encode 4 boolean wall states (N, E, S, W) into a single hexadecimal digit (0-F)
   - Generating examples of wall combinations and their hex values
   - Debugging bit manipulation edge cases (e.g., little-endian vs. big-endian concerns)

2. **Makefile Syntax** (Both Members)
   - Learning GNU Make syntax and best practices
   - Debugging the `make lint` rule to ensure correct mypy flags
   - Understanding phony targets and automatic variables

3. **Type Hints Debugging** (Member 1)
   - Resolving complex `mypy` type checking errors in recursive functions
   - Understanding `typing.Optional`, `Union`, and generic types
   - Fixing type inconsistencies between function signatures and implementations

4. **Visualization Logic** (Member 2)
   - Asking AI for examples of efficient terminal ASCII grid rendering
   - Understanding ANSI color codes for terminal output
   - Prototyping the visualizer layout quickly

5. **Packaging Setup** (Member 1)
   - Understanding `pyproject.toml` structure and metadata requirements
   - Learning setuptools configuration for building `.whl` files
   - Generating example `setup.py` templates

6. **Algorithm Pseudocode Review** (Member 1)
   - Validating Recursive Backtracker implementation logic
   - Comparing different approaches to implementing union-find for Kruskal's
   - Understanding stack vs. recursion trade-offs

#### ❌ **Tasks Where AI Was NOT Used:**

- **Core Algorithm Implementation**: All maze generation logic (Recursive Backtracker, Kruskal's) was written from scratch after understanding the concepts
- **Project Architecture**: Module structure, API design, and separation of concerns were decided independently through team discussion
- **Critical Bug Fixing**: Complex bugs (wall coherency, path validation) were debugged through peer review and manual testing
- **Integration Logic**: Connecting the `mazegen` package with the main script was done through collaborative pair programming
- **Constraint Implementation**: The "42" pattern and 3×3 validation logic were designed and coded by the team

#### 🔍 **Validation Process:**

- All AI-generated code snippets were reviewed line-by-line by both team members
- Concepts explained by AI were re-explained to teammates to ensure mutual understanding
- Code was thoroughly tested with edge cases before integration into the main codebase
- Peer review sessions caught AI-suggested anti-patterns (e.g., overuse of global state)
- Any code we couldn't fully explain was rewritten from scratch

---

## 🎯 Features

### Core Features
- ✅ Configurable maze dimensions and parameters
- ✅ Perfect maze generation (single unique path between any two points)
- ✅ Reproducible generation via seed parameter
- ✅ Hexadecimal wall encoding output
- ✅ Hidden "42" pattern embedding (when maze size permits)
- ✅ Solution pathfinding (BFS-based shortest path)
- ✅ ASCII terminal visualization with clear wall representation
- ✅ Interactive controls (regenerate, toggle path, color customization)
- ✅ Comprehensive error handling and validation

### Bonus Features
- ✅ Multiple algorithm support (Recursive Backtracker + Kruskal's)
- ✅ Animated maze generation (step-by-step visualization)
- ✅ Reusable pip-installable package with proper documentation
- ✅ Comprehensive test suite with 95%+ code coverage
- ✅ Optional MLX graphical display

---

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Install testing dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/

# Run with coverage report
pytest --cov=mazegen --cov-report=html tests/

# View coverage report
open htmlcov/index.html
```

### Test Coverage

- Unit tests for maze generation algorithms
- Validation tests for constraints (3×3 areas, wall coherency)
- Integration tests for the complete workflow
- Edge case tests (tiny mazes, large mazes, invalid configurations)
- Pathfinding correctness verification

---

## 📅 Detailed Work Division

Here is the breakdown of tasks between team members:

### Member 1: Backend & Architect

**Focus:** The `mazegen/` package, algorithms, and packaging infrastructure

**Key Files:**
- `mazegen/__init__.py`: Public API exposure
- `mazegen/generator.py`: The `MazeGenerator` class
- `mazegen/algorithms.py`: Algorithm implementations (Recursive Backtracker, Kruskal's)
- `mazegen/cell.py`: Cell data structure with wall representation
- `pyproject.toml` / `setup.py`: Package metadata

**Specific Tasks:**
1. Implement the **"42" Pattern**: Create embedding logic with coordinate mapping
2. Implement **Validation Logic**: Ensure no 3×3 open spaces and wall coherency
3. **Build System**: Ensure `python -m build` generates valid `.whl` and `.tar.gz` files
4. **Unit Tests**: Write pytest tests to verify perfect maze property and path uniqueness
5. **Documentation**: Write API documentation and usage examples

### Member 2: Frontend & Integrator

**Focus:** The root directory, user interaction, file I/O, and display

**Key Files:**
- `a_maze_ing.py`: Main executable entry point
- `config_parser.py`: Configuration file parsing logic
- `hex_writer.py`: Hexadecimal output file generation
- `visualizer.py`: ASCII/MLX rendering code
- `Makefile`: Project automation commands

**Specific Tasks:**
1. **Config Parsing**: Handle edge cases (missing keys, invalid values, comments)
2. **Hex Output**: Convert maze object from Member 1 into hex format (bitwise operations)
3. **Visualization**: Implement regenerate, show/hide path, and color customization features
4. **Makefile**: Ensure all required rules (`install`, `run`, `lint`, `clean`, `debug`) work correctly
5. **Integration**: Connect `mazegen` package with main script and handle error cases gracefully

---

## 📜 License

This project is part of the 42 School curriculum. All rights reserved.

---

## 🙏 Acknowledgments

- 42 School staff for the project subject, guidance, and peer evaluation system
- Jamis Buck for comprehensive maze algorithm documentation and inspiration
- Python community for excellent libraries, tools, and documentation
- Our peers for code reviews, testing, and valuable feedback throughout development

---

**Happy Maze Exploring! 🗺️**
