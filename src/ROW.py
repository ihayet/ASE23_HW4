class ROW:
    def __init__(self, t):
        self.cells = []
        for val in t:
            self.cells.append(val)

    def get_cells(self):
        return self.cells