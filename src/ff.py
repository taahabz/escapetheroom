from resources import RESOURCES

class FF:
    def __init__(self, start_pos, size):
        """
        Initialize a flood fill (FF) solver.

        :param start_pos: Tuple (x, y) for the starting position.
        :param size: Tuple (width, height) for grid bounds.
        """
        self.q = []  # Queue for flood fill algorithm
        self.mat = {}  # Dictionary to store weights
        self.weight = 0
        self.start_pos = start_pos
        self.grid_bounds = size

    def update_q(self, pos):
        """
        Add a position to the queue if it meets all constraints.

        :param pos: Tuple (x, y) of the position to check.
        """
        x, y = pos

        # Check if position is already in queue, out of bounds, or invalid
        if pos in self.q:
            return

        if x >= self.grid_bounds[0] or y >= self.grid_bounds[1]:
            return

        if RESOURCES is None:
            raise RuntimeError("RESOURCES is not initialized. Please call init_resources() before using FF.")

        # Safely access RESOURCES
        resources = RESOURCES.get()
        tile = resources.lvl_map.get_tile("LAYER_WALLS", x, y)
        if tile is not None:
            return

        if pos in self.mat:
            return

        self.q.append(pos)

    def process(self):
        """
        Process the flood fill queue, updating weights for each accessible tile.
        """
        while self.q:
            x, y = self.q.pop(0)  # Dequeue

            self.weight += 1
            self.mat[(x, y)] = self.weight

            self.update_q((x + 1, y))
            self.update_q((x - 1, y))
            self.update_q((x, y + 1))
            self.update_q((x, y - 1))

    def solve(self):
        """
        Perform flood fill and return the resulting weight matrix.

        :return: Dictionary of positions to weights.
        """
        self.q.append(self.start_pos)
        self.process()
        return self.mat.copy()

# Example usage
# Initialize with starting position and grid size
# ff = FF((0, 0), (10, 10))
# result = ff.solve()
# print(result)
