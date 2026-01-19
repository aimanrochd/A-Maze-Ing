# A-Maze-ing

## Project Guide, Implementation Roadmap & Defense Reference

---

## 1. Project Overview

### What is this project?
**A-Maze-ing** is a Python project focused on algorithmic problem solving, clean architecture, and software packaging. The goal is to build a reusable maze generator that can be installed as a Python package, generate valid mazes based on a configuration file, and visualize them interactively.

### The Problem
The program must generate a maze that:
- Has a guaranteed path between a defined **Entry** and **Exit**
- Can be **Perfect** (exactly one unique solution) when requested
- Embeds a visible **"42" pattern** using fully closed cells
- Maintains strict wall coherence between neighboring cells

### Expected Final Behavior
1. The user runs:
   ```bash
   python3 a_maze_ing.py config.txt
   ```
2. The program reads and validates the configuration
3. A maze is generated using the `mazegen` package
4. The maze is saved to a file using hexadecimal wall encoding
5. The solution path is computed and appended
6. The maze is displayed (terminal or graphical)

---

## 2. Mandatory Rules & Constraints

### Language & Tools
- **Language:** Python 3.10+
- **Style:** `flake8` compliant
- **Type Checking:** `mypy` with full type hints
- **Documentation:** All public functions and classes must have docstrings

### Error Handling
- No unhandled exceptions
- All file operations must use context managers (`with open(...)`)
- Invalid input must display a clear error and exit cleanly

### Packaging Requirement
- Core logic must be inside an installable package (`mazegen`)
- Evaluators will test the project by installing your `.whl` file

### Makefile (Required Targets)
- `install` – install dependencies / package
- `run` – execute the project
- `clean` – remove caches and build artifacts
- `lint` – run `flake8` and `mypy`

---

## 3. Required Knowledge (Before Coding)

### Algorithms
- **Maze Generation:** Recursive Backtracker (DFS-based)
- **Pathfinding:** Breadth-First Search (BFS) for shortest path

### Data Representation
- Grid-based maze
- Each cell has four walls: North, East, South, West

### Bitwise Encoding (Output Format)

| Direction | Bit | Binary | Hex |
|---------|-----|--------|-----|
| North | 1 | 0001 | 1 |
| East  | 2 | 0010 | 2 |
| South | 4 | 0100 | 4 |
| West  | 8 | 1000 | 8 |

Example: South + West = 4 + 8 = 12 = `C`

### Python Concepts
- Type hints
- Immutable vs mutable structures
- Queues (BFS)
- Stacks (DFS)
- Packaging (`pyproject.toml`, `setuptools`)

---

## 4. Step-by-Step Implementation Plan

### Phase 1: Environment & Structure
- Create repository
- Set up `mazegen/` package
- Write `pyproject.toml` and `Makefile`

### Phase 2: Config Parsing
- Read `KEY=VALUE` format
- Validate dimensions and coordinates
- Handle all errors gracefully

### Phase 3: Maze Generation
- Initialize grid with all walls closed
- Pre-place the "42" pattern as blocked cells
- Apply Recursive Backtracker to remaining cells
- Ensure wall coherence

### Phase 4: Solving the Maze
- Use BFS from Entry to Exit
- Track parents to reconstruct the path
- Output solution as N/E/S/W string

### Phase 5: Output Writing
- Convert walls to hexadecimal
- Write maze row by row
- Append solution path

### Phase 6: Visualization
- Terminal (ASCII) or MiniLibX
- Display walls, entry, exit, and solution
- Support basic interactions (regenerate, toggle path)

### Phase 7: Polish & Package
- Run `flake8` and `mypy`
- Build `.whl` file
- Test installation in a clean virtual environment

---

## 5. Project Architecture

```
root/
├── a_maze_ing.py        # Main entry point
├── config.txt           # Example configuration
├── Makefile
├── README.md
├── pyproject.toml
├── mazegen/
│   ├── __init__.py
│   ├── generator.py     # MazeGenerator class
│   ├── solver.py        # BFS pathfinding
│   ├── visualizer.py    # Rendering logic
│   └── utils.py         # Helpers
└── output_validator.py  # Provided validator
```

---

## 6. Algorithms Explained

### Recursive Backtracker (Generation)
1. Start from a random cell
2. Mark it as visited
3. Choose a random unvisited neighbor
4. Remove the wall between them
5. Move to the neighbor
6. Backtrack when no neighbors are available

This guarantees a **perfect maze** (spanning tree).

### Breadth-First Search (Solving)
1. Push Entry into a queue
2. Visit neighbors level by level
3. Store parent directions
4. Stop when Exit is reached
5. Reconstruct shortest path

---

## 7. Common Mistakes

- Wall incoherence between neighboring cells
- Forgetting to handle small maze sizes ("42" does not fit)
- Using recursive DFS causing recursion limit crashes
- Importing local files instead of the installed package
- Adding code you cannot explain during defense

---

## 8. Testing Strategy

- Always run the provided validator
- Test edge sizes (1x1, 2x2, very large mazes)
- Run `make lint` frequently
- Test package installation in a fresh virtual environment

---

## 9. Evaluation Checklist

Before submission:
- [ ] Project runs without crashing
- [ ] `make install`, `make run`, `make clean`, `make lint` work
- [ ] No `flake8` or `mypy` errors
- [ ] Output passes `output_validator.py`
- [ ] Solution path is correct
- [ ] "42" pattern is visible when applicable

---

## 10. AI Usage Declaration

AI tools were used for:
- Documentation structuring
- Algorithm explanations
- Debugging assistance

All code was reviewed, fully understood, and adapted by the team.

---

## Final Advice

- Understand every line of code you submit
- Keep generator logic independent from visualization
- Be ready to modify your code live during defense
- Simple, clean, and correct beats complex and fragile

Good luck, and build it step by step like a true 42 student 🚀