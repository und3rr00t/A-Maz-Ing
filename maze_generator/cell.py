import sys
import random
from .maze import Maze
from .themes import getch
from typing import List, Tuple
from .error_class import Y, RS


class Cell:
    """
    Represents a single cell in the maze with its wall and visit status.\n

    Attributes:\n
        grid (int):
            Bitmask representing the walls of the cell (15 means all walls).\n
        visited (bool):
            Flag indicating if the cell has been visited during generation.\n
        ft_pattern (bool):
            Flag indicating if the cell is part of the '42' pattern.
    """

    def __init__(self) -> None:
        """
        Initializes a cell with all walls (15) and flags for visited/pattern.\n

        Returns:
            None
        """
        self.grid = 15
        self.visited = False
        self.ft_pattern = False

    @classmethod
    def get_cells(cls, maze: Maze) -> List[List['Cell']]:
        """
        Initializes the grid of cells and overlays the '42' pattern
        if possible or not.\n

        This method creates a 2D grid of Cell objects and attempts to place
        a visual '42' pattern in a random valid location that does not
        overlap with the entry or exit points.\n

        Args:
            maze (Maze): The maze object containing dimensions,
            entry, and exit.

        Returns:
            List[List[Cell]]: A 2D list containing the initialized Cells.\n

        Raises:
            SystemExit: If the maze is too small or no valid position is found
            and the user chooses to quit.\n
        """

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
            """
            Finds valid top-left positions for the '42' pattern.\n

            Scans the maze to find all possible starting coordinates where the
            '42' pattern can be placed without blocking entry/exit.\n

            Returns:
                List[Tuple[int, int]]: A list of (x, y)
                coordinates for valid starts.\n
            """
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
            print("1. Continue")
            print("2. Quit")
            replay = getch()
            if replay != '1':
                sys.exit(0)
            return cells

        available_starts = get_available_starts()
        if not available_starts:
            print(
                f"{Y}Warning{RS}: No valid positions for '42' pattern "
                "(entry/exit blocking)."
            )
            print("1. Continue")
            print("2. Quit")
            replay = getch()
            if replay != '1':
                sys.exit(0)
            return cells

        start_x, start_y = random.choice(available_starts)

        for ft_x, ft_y in ft_pattern:
            x, y = start_x + ft_x, start_y + ft_y
            cells[y][x].visited = True
            cells[y][x].ft_pattern = True

        return cells
