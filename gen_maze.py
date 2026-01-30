import os
import sys
import time
import random
from cell import Cell
from maze import Maze
from typing import List, Tuple, Optional
from error_class import R, G, C, Y, RS


NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8
DIRECTIONS = ((0, -1, NORTH, 4), (0, 1, 4, 1), (1, 0, 2, 8), (-1, 0, 8, 2))


def clear_screen():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


class MazeGenerator:

    def __init__(self, maze: Maze) -> None:

        self.__maze = maze
        random.seed(self.__maze.seed)
        self.__cells: List[List[Cell]] = Cell.get_cells(maze)

    def get_maze(self):
        return self.__maze

    def gen_standard_maze(self) -> None:

        sx, sy = self.__maze.entry
        stack: List[Tuple[int, int]] = [(sx, sy)]
        self.__cells[sy][sx].visited = True

        while stack:

            cx, cy = stack[-1]

            neighbors = []
            for dx, dy, wall, opp_wall in DIRECTIONS:
                nx, ny = cx + dx, cy + dy

                if (
                    0 <= nx < self.__maze.width
                    and 0 <= ny < self.__maze.height
                ):
                    if not self.__cells[ny][nx].visited:
                        neighbors.append((nx, ny, wall, opp_wall))

            if neighbors:
                nx, ny, wall, opp_wall = random.choice(neighbors)

                self.__cells[cy][cx].grid &= ~wall
                self.__cells[ny][nx].grid &= ~opp_wall

                self.__cells[ny][nx].visited = True
                stack.append((nx, ny))
                self.display_maze()
                time.sleep(0.01)
                clear_screen()
            else:
                stack.pop()

    def generate(self) -> None:
        """Switchboard to choose the algorithm based on config."""
        algo = getattr(self.__maze, 'algo', 'DFS').upper()

        if algo == "SIDEWINDER":
            self.generate_sidewinder()
        else:
            self.gen_standard_maze()

    def generate_sidewinder(self):
        for y in range(self.__maze.height):
            run = []

            for x in range(self.__maze.width):
                cell = self.__cells[y][x]
                run.append(x)
                at_east_boundary = (x == self.__maze.width - 1)
                at_north_boundary = (y == 0)

                is_next_cell_pattern = False
                if not at_east_boundary:
                    is_next_cell_pattern = self.__cells[y][x+1].ft_pattern
                should_close_run = (
                    at_east_boundary or is_next_cell_pattern or
                    (not at_north_boundary and random.choice([True, False]))
                    )

                if should_close_run:
                    member_x = random.choice(run)

                    if not at_north_boundary:
                        if (
                            not self.__cells[y][member_x].ft_pattern
                            and not self.__cells[y-1][member_x].ft_pattern
                        ):
                            self.__cells[y][member_x].grid &= ~NORTH
                            self.__cells[y-1][member_x].grid &= ~SOUTH

                    run = []
                else:
                    if not cell.ft_pattern and not is_next_cell_pattern:
                        self.__cells[y][x].grid &= ~EAST
                        self.__cells[y][x+1].grid &= ~WEST

                self.display_maze()
                time.sleep(0.02)
                clear_screen()

    def make_imperfect(self, chance: float = 0.5) -> None:

        for y in range(self.__maze.height):
            for x in range(self.__maze.width):
                if self.__cells[y][x].ft_pattern is True:
                    continue

                walls = []
                if self.__cells[y][x].grid & NORTH:
                    walls.append(DIRECTIONS[0])
                if self.__cells[y][x].grid & EAST:
                    walls.append(DIRECTIONS[2])
                if self.__cells[y][x].grid & SOUTH:
                    walls.append(DIRECTIONS[1])
                if self.__cells[y][x].grid & WEST:
                    walls.append(DIRECTIONS[3])
                if len(walls) == 3 and random.random() < chance:
                    dx, dy, wall, opp_wall = random.choice(walls)
                    nx, ny = x + dx, y + dy
                    if (
                        0 <= nx < self.__maze.width
                        and 0 <= ny < self.__maze.height
                    ):
                        if self.__cells[ny][nx].ft_pattern is True:
                            continue
                        self.__cells[y][x].grid &= ~wall
                        self.__cells[ny][nx].grid &= ~opp_wall
                        self.display_maze()
                        time.sleep(0.1)
                        clear_screen()

    def solve_maze(self, dis: int) -> str:
        queue = [(self.__maze.entry, "")]
        visited = {self.__maze.entry}

        while queue:
            (cx, cy), path = queue.pop(0)

            if (cx, cy) == self.__maze.exit:
                return path

            directions = [
                (0, -1, NORTH, "N"),
                (1, 0, EAST, "E"),
                (0, 1, SOUTH, "S"),
                (-1, 0, WEST, "W")
            ]

            for dx, dy, wall, move in directions:
                nx, ny = cx + dx, cy + dy

                if (
                    0 <= nx < self.__maze.width
                    and 0 <= ny < self.__maze.height
                ):
                    if (
                        not (self.__cells[cy][cx].grid & wall)
                        and (nx, ny) not in visited
                    ):
                        visited.add((nx, ny))
                        queue.append(((nx, ny), path + move))

                        if dis == 1:
                            clear_screen()
                            self.display_maze(list(visited))
                            time.sleep(0.01)

        return ""

    def get_path_coords(self, path_str: str) -> List[Tuple[int, int]]:

        coords = [self.__maze.entry]
        x, y = self.__maze.entry
        for move in path_str:
            if move == 'N':
                y -= 1
            elif move == 'S':
                y += 1
            elif move == 'E':
                x += 1
            elif move == 'W':
                x -= 1
            coords.append((x, y))
        return coords

    def write_output(self, path: str) -> None:

        output_path = self.__maze.output_file

        try:
            with open(output_path, "w") as f:

                for row in self.__cells:
                    hex_row = "".join([f"{cell.grid:X}" for cell in row])
                    f.write(hex_row + "\n")

                f.write(f"\nSEED: {self.__maze.seed}\n")
                f.write(
                    f"ENTRY: {self.__maze.entry[0]},{self.__maze.entry[1]}\n"
                )
                f.write(f"EXIT: {self.__maze.exit[0]},{self.__maze.exit[1]}\n")
                f.write(f"SOLUTION: {path}\n")

            print(f"Maze saved to {output_path}")
        except (PermissionError, IsADirectoryError) as e:
            print(f"Error writing to file: {e}")
            sys.exit(1)

    def display_maze(
        self,
        path_coords: Optional[List[Tuple[int, int]]] = None
    ) -> None:
        if path_coords is None:
            path_coords = []

        ORANGE = "\033[38;5;208m"

        is_finished = len(path_coords) > 0 and self.__maze.exit in path_coords
        path_color = ORANGE if is_finished else Y

        cells = self.__cells
        BLOCK = "\u2588"
        V_WALL = BLOCK * 2
        CORNER = BLOCK * 2
        BODY = "  "

        H_WALL = BLOCK * 4
        H_OPEN = BODY + CORNER

        print(CORNER, end="")
        for cell in cells[0]:
            if cell.grid & NORTH:
                print(H_WALL, end="")
            else:
                print(H_OPEN, end="")
        print()

        for y, row in enumerate(cells):
            for x, cell in enumerate(row):
                if cell.grid & WEST:
                    print(V_WALL, end="")
                else:
                    if (x, y) in path_coords and (x - 1, y) in path_coords:
                        print(f"{path_color}██{RS}", end="")
                    else:
                        print("  ", end="")

                if (x, y) == self.__maze.entry:
                    print(f"{G}██{RS}", end="")
                elif (x, y) == self.__maze.exit:
                    print(f"{path_color if is_finished else R}██{RS}", end="")
                elif (x, y) in path_coords:
                    print(f"{path_color}██{RS}", end="")
                elif cell.ft_pattern is True:
                    print(f"{C}██{RS}", end="")
                else:
                    print(BODY, end="")

            if row[-1].grid & EAST:
                print(V_WALL, end="")
            print()

            print(CORNER, end="")
            for x, cell in enumerate(row):
                if cell.grid & SOUTH:
                    print(H_WALL, end="")
                else:
                    if (x, y) in path_coords and (x, y + 1) in path_coords:
                        print(f"{path_color}██{RS}██", end="")
                    else:
                        print(H_OPEN, end="")
            print()
