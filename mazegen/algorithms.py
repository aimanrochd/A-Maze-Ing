import random
from typing import Tuple, List, Callable, Optional
from mazegen.cell import Cell


class MazeGenerator:
    """Generate, modify, and solve mazes on a grid of Cells."""
    def __init__(self, height: int, width: int) -> None:
        """
        Initialize a maze grid of the given dimensions.

        Args:
            height: Number of rows.
            width: Number of columns.
        """
        self.height = height
        self.width = width
        self.grid = [[Cell(x, y) for x in range(width)] for y in range(height)]
        self.solution: List[str] = []

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        """
        Return a cell if coordinates are in bounds.

        Args:
            x: Column index.
            y: Row index.

        Returns:
            The Cell at (x, y), or None if out of bounds.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def remove_wall(self, c1: Cell, c2: Cell) -> None:
        """
        Remove the wall between two adjacent cells.

        Args:
            c1: First cell.
            c2: Second cell.
        """
        dx, dy = c2.x - c1.x, c2.y - c1.y
        if dx == 1:
            c1.east = False
            c2.west = False
        elif dx == -1:
            c1.west = False
            c2.east = False
        elif dy == 1:
            c1.south = False
            c2.north = False
        elif dy == -1:
            c1.north = False
            c2.south = False

    def _get_neighbors(self, cell: Cell,
                       require_visited: bool = False) -> List[Cell]:
        """
        Get neighboring cells based on visited state.

        Args:
            cell: Reference cell.
            require_visited: If True, return only visited non-mask neighbors.
                If False, return only unvisited neighbors.

        Returns:
            List of neighboring cells matching the constraint.
        """
        neighbors = []
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            neighbor = self.get_cell(cell.x + dx, cell.y + dy)
            if neighbor:
                if require_visited:
                    if neighbor.visited and not neighbor.is_42:
                        neighbors.append(neighbor)
                elif not neighbor.visited:
                    neighbors.append(neighbor)
        return neighbors

    def generate_maze(self, entry: Tuple[int, int], exit_pos: Tuple[int, int],
                      algorithm: str, seed: int,
                      callback: Optional[Callable[[], None]] = None) -> None:
        """
        Generate the maze using the selected algorithm.

        Args:
            entry: Entry coordinates (x, y).
            exit_pos: Exit coordinates (x, y).
            algorithm: Algorithm name (e.g., 'prims' or
            'recursive_backtracker').
            seed: RNG seed.
            callback: Optional function called during generation for animation.
        """
        random.seed(seed)

        self._apply_42_mask(entry, exit_pos)
        start_cell = self.get_cell(*entry)
        if not start_cell:
            return

        if "prims" in algorithm.lower():
            self._prims_algo(start_cell, callback)
        else:
            self._recursive_backtracker(start_cell, callback)

    def _recursive_backtracker(
        self, start_cell: Cell, callback: Optional[Callable[[], None]] = None
    ) -> None:
        """
        Generate maze using recursive backtracker (DFS).

        Args:
            start_cell: Starting cell.
            callback: Optional animation callback.
        """
        stack = [start_cell]
        start_cell.visited = True

        while stack:
            current = stack[-1]
            if callback:
                callback()

            neighbors = self._get_neighbors(current, require_visited=False)
            if neighbors:
                next_cell = random.choice(neighbors)
                self.remove_wall(current, next_cell)
                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()

    def _prims_algo(
        self, start_cell: Cell, callback: Optional[Callable[[], None]] = None
    ) -> None:
        """
        Generate maze using Prim's algorithm.

        Args:
            start_cell: Starting cell.
            callback: Optional animation callback.
        """
        start_cell.visited = True
        frontier = self._get_neighbors(start_cell, require_visited=False)

        while frontier:
            current = frontier.pop(random.randint(0, len(frontier) - 1))
            if current.visited:
                continue

            neighbors = self._get_neighbors(current, require_visited=True)
            if neighbors:
                self.remove_wall(current, random.choice(neighbors))
                current.visited = True
                if callback:
                    callback()
                new_n = self._get_neighbors(current, require_visited=False)
                frontier.extend(new_n)

    def braid_maze(self) -> None:
        """
        Reduce dead-ends by randomly breaking walls (imperfect maze).
        """
        for row in self.grid:
            for cell in row:
                if cell.is_42:
                    continue

                walls = [cell.north, cell.south, cell.east, cell.west]
                if walls.count(True) != 3:
                    continue

                if random.random() > 0.5:
                    continue

                valid = []
                check_dirs = [
                    (0, -1, cell.north), (0, 1, cell.south),
                    (-1, 0, cell.west), (1, 0, cell.east)
                ]
                for dx, dy, has_wall in check_dirs:
                    if has_wall:
                        n = self.get_cell(cell.x + dx, cell.y + dy)
                        if n and n.visited and not n.is_42:
                            valid.append(n)

                if valid:
                    self.remove_wall(cell, random.choice(valid))

    def _apply_42_mask(self, start_pos: Tuple[int, int],
                       end_pos: Tuple[int, int]) -> None:
        """
        Mark a centered '42' pattern as blocked/void cells.

        Args:
            start_pos: Entry coordinates (x, y).
            end_pos: Exit coordinates (x, y).
        """
        cx, cy = (self.width - 7) // 2, (self.height - 5) // 2
        offsets = [
            (0, 0), (0, 1), (0, 2), (2, 2), (1, 2), (2, 3), (2, 4),
            (4, 0), (5, 0), (6, 0), (6, 1), (4, 2), (5, 2), (6, 2),
            (4, 3), (4, 4), (5, 4), (6, 4)
        ]
        mask_coords = [(cx + dx, cy + dy) for dx, dy in offsets]

        if start_pos in mask_coords or end_pos in mask_coords:
            raise ValueError("Warning: ENTRY or EXIT is inside the '42' mask.")

        for x, y in mask_coords:
            cell = self.get_cell(x, y)
            if cell:
                cell.visited = True
                cell.is_42 = True

    def solve(self, entry: Tuple[int, int], exit_pos: Tuple[int, int]) -> str:
        """
        Solve the maze using BFS and return the shortest path string.

        Args:
            entry: Entry coordinates (x, y).
            exit_pos: Exit coordinates (x, y).

        Returns:
            A direction string made of 'N', 'E', 'S', 'W'.
            Returns "" if no path.
        """
        start = self.get_cell(*entry)
        end = self.get_cell(*exit_pos)
        if not start or not end:
            return ""

        queue = [(start, "")]
        visited = {start}

        while queue:
            current, path = queue.pop(0)
            if current == end:
                self.solution = list(path)
                return path

            moves = [(current.north, 0, -1, "N"), (current.south, 0, 1, "S"),
                     (current.east, 1, 0, "E"), (current.west, -1, 0, "W")]

            for is_wall, dx, dy, char in moves:
                if not is_wall:
                    neighbor = self.get_cell(current.x + dx, current.y + dy)
                    if neighbor and neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, path + char))
        return ""
