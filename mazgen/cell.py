class Cell:
    """"""
    def __init__(self, x: int, y: int):
        """"""
        self.x = x
        self.y = y
        self.north = True
        self.east = True
        self.south = True
        self.west = True
        self.visited = False
