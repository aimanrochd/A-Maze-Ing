class Cell:
    """Represent a single maze cell with wall and state information."""
    def __init__(self, x: int, y: int):
        """
        Initialize a cell at the given coordinates.

        Args:
            x: Column index of the cell.
            y: Row index of the cell.
        """
        self.x = x
        self.y = y
        self.visited = False
        self.north = True
        self.south = True
        self.east = True
        self.west = True
        self.is_42 = False
