import random
from typing import List, Tuple


class MazeGenerator:
    """
    Mandatory class to generate a perfect maze.
    """

    DIRECTIONS = [
        (0, -1, 1, 4),
        (0, 1, 4, 1),
        (1, 0, 2, 8),
        (-1, 0, 8, 2)
    ]

    def __init__(self, width: int, height: int, seed: int = None) -> None:
        self.width = width
        self.height = height

        self.grid = [[15 for _ in range(width)] for _ in range(height)]

        self.visited = [[False for _ in range(width)] for _ in range(height)]

        if seed is not None:
            random.seed(seed)

    def _mask_42(self) -> None:
        """
        Marks cells in the shape of '42' as visited.
        Since they are visited but we never opened their walls,
        they remain solid blocks (Value 15).
        """

        pattern = [
            # The '4'
            (0, 0), (0, 1), (0, 2), (1, 2), (2, 0), (2, 1), (2, 2),
            # The '2'
            (4, 0), (4, 1), (4, 2), (5, 0), (5, 2), (6, 0), (6, 1), (6, 2)
        ]

        start_x = (self.width // 2) - 4
        start_y = (self.height // 2) - 2

        if start_x < 0 or start_y < 0 or start_x + 7 > self.width or start_y + 3 > self.height:
            print("Warning: Maze too small for '42' pattern.")
            return

        for dx, dy in pattern:
            px, py = start_x + dx, start_y + dy
            self.visited[py][px] = True

    def generate(self, start_pos: Tuple[int, int]) -> List[List[int]]:
        """
        Generates the maze starting from start_pos.
        """

        self._mask_42()
        sx, sy = start_pos
        stack: List[Tuple[int, int]] = [(sx, sy)]
        self.visited[sy][sx] = True

        while stack:
            cx, cy = stack[-1]

            neighbors = []
            for dx, dy, wall, opp_wall in self.DIRECTIONS:
                nx, ny = cx + dx, cy + dy

                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if not self.visited[ny][nx]:
                        neighbors.append((nx, ny, wall, opp_wall))

            if neighbors:
                nx, ny, wall, opp_wall = random.choice(neighbors)

                self.grid[cy][cx] &= ~wall
                self.grid[ny][nx] &= ~opp_wall

                self.visited[ny][nx] = True
                stack.append((nx, ny))
            else:
                stack.pop()

        return self.grid
