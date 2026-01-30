import random
from maze import Maze
from typing import List, Tuple
from error_class import Y, RS


class Cell:

    def __init__(self) -> None:

        self.grid = 15
        self.visited = False
        self.ft_pattern = False

    @classmethod
    def get_cells(cls, maze: Maze) -> List[List]:

        four = [
            (0, 0), (0, 1), (0, 2),
            (1, 2), (2, 2), (2, 3), (2, 4)
        ]
        two = [
            (4, 0), (5, 0), (6, 0), (6, 1), (6, 2),
            (5, 2), (4, 2), (4, 3), (4, 4), (5, 4), (6, 4)
        ]

        ft_pattern = four + two

        def get_available_starts() -> List[Tuple[int, int]]:

            ft_width, ft_height = 7, 5
            available_starts: List[Tuple[int, int]] = []

            for x in range(1, maze.width - ft_width):
                for y in range(1, maze.height - ft_height):

                    occupied = {(x + px, y + py) for px, py in ft_pattern}

                    if (
                        maze.entry not in occupied
                        and maze.exit not in occupied
                    ):
                        available_starts.append((x, y))

            return available_starts

        cells: List[List[Cell]] = [
            [
                cls() for _ in range(maze.width)
            ] for _ in range(maze.height)
        ]

        ft_width, ft_height = 7, 5

        if maze.width < ft_width or maze.height < ft_height:
            print(f"{Y}Warning{RS}: Maze size too small for '42' pattern.")
            return cells

        available_starts = get_available_starts()
        if not available_starts:
            print(
                f"{Y}Warning{RS}: No valid positions for '42' pattern "
                "(entry/exit blocking)."
            )
            return cells

        start_x, start_y = random.choice(available_starts)

        for ft_x, ft_y in ft_pattern:
            x, y = start_x + ft_x, start_y + ft_y
            cells[y][x].visited = True
            cells[y][x].ft_pattern = True

        return cells
