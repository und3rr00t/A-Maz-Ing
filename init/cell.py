from typing import List


Y = "\033[33m"
RS = "\033[0m"


class Cell:

    def __init__(self) -> None:

        self.grid = 15
        self.visited = False
        self.is_pattern = False

    @classmethod
    def get_cells(cls, width: int, height: int) -> List[List]:

        four = [
            (0, 0), (0, 1), (0, 2),
            (1, 2),
            (2, 2), (2, 3), (2, 4)
        ]
        tow = [
            (4, 0), (5, 0), (6, 0),
            (6, 1), (6, 2),
            (5, 2), (4, 2),
            (4, 3), (4, 4),
            (5, 4), (6, 4)
        ]
        cells: List[List[Cell]] = [
            [
                cls() for _ in range(width)
            ] for _ in range(height)
        ]

        pattern = four + tow
        ft_width, ft_height = 7, 5
        start_x, start_y = int(width // 2) - 3, int(height // 2) - 2

        if width < ft_width or height < ft_height:
            print(f"{Y}Worrning{RS}: Maze size too small for '42' pattern.")
            return cells

        for ft_x, ft_y in pattern:
            x, y = start_x + ft_x, start_y + ft_y
            cells[y][x].visited = True
            cells[y][x].is_pattern = True

        return cells
