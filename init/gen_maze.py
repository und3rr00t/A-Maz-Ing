import os
import sys
import random
import curses
import time
from cell import Cell
from maze import Maze
from typing import List, Tuple, Optional


Y = "\033[33m"
RS = "\033[0m"


class MazeGenerator:
    """
    Mandatory class to generate a perfect maze.
    """

    DIRECTIONS = (
        (0, -1, 1, 4),
        (0, 1, 4, 1),
        (1, 0, 2, 8),
        (-1, 0, 8, 2)
    )

    def __init__(self, maze: Maze, seed: Optional[int] = None) -> None:

        self.__maze = maze
        self.__cells: List[List[Cell]] = Cell.get_cells(
            self.__maze.width, self.__maze.height
        )

        if seed is not None:
            random.seed(seed)

    def get_maze(self):
        return self.__maze

    def _create_loops(self) -> None:
        """
        Randomly remove walls to create loops if PERFECT=False.
        """
        total_cells = self.__maze.width * self.__maze.height
        limit = total_cells // 20
        count = 0
        while count < limit:
            cx = random.randint(0, self.__maze.width - 1)
            cy = random.randint(0, self.__maze.height - 1)
            neighbors = list(self.DIRECTIONS)
            random.shuffle(neighbors)
            for dx, dy, wall, opp_wall in neighbors:
                nx, ny = cx + dx, cy + dy
                if (
                    0 <= nx < self.__maze.width
                    and 0 <= ny < self.__maze.height
                ):
                    if self.__cells[cy][cx].grid & wall:
                        self.__cells[cy][cx].grid &= ~wall
                        self.__cells[ny][nx].grid &= ~opp_wall
                        count += 1
                        break

    def gen_standard_maze(self) -> None:
        """Standard recursive backtracking generation (Non-Visual)."""
        sx, sy = self.__maze.entry
        stack: List[Tuple[int, int]] = [(sx, sy)]
        self.__cells[sy][sx].visited = True

        while stack:
            cx, cy = stack[-1]

            neighbors = []
            for dx, dy, wall, opp_wall in self.DIRECTIONS:
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
            else:
                stack.pop()

        if not self.__maze.perfection:
            self._create_loops()

    def animate_generation(self) -> None:
        """Run the generation algorithm with Curses visualization."""
        self.__cells = Cell.get_cells(self.__maze.width, self.__maze.height)
        curses.wrapper(self._run_generation_animation)
        if not self.__maze.perfection:
            self._create_loops()

    def _run_generation_animation(self, stdscr):
        """The generation logic wrapped in Curses drawing."""
        curses.curs_set(0)
        stdscr.clear()
        stdscr.nodelay(True)

        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

        self._draw_full_grid(stdscr)

        sx, sy = self.__maze.entry
        stack: List[Tuple[int, int]] = [(sx, sy)]
        self.__cells[sy][sx].visited = True

        DIRS = self.DIRECTIONS

        while stack:
            cx, cy = stack[-1]

            self._draw_cell(stdscr, cx, cy, color_pair=2)
            stdscr.refresh()
            time.sleep(0.01)

            neighbors = []
            for dx, dy, wall, opp_wall in DIRS:
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

                self._draw_cell(stdscr, cx, cy, color_pair=3)

                stack.append((nx, ny))
            else:
                self._draw_cell(stdscr, cx, cy, color_pair=3)
                stack.pop()

    def _draw_full_grid(self, stdscr):
        """Draw the initial state of the maze."""
        for y in range(self.__maze.height):
            for x in range(self.__maze.width):
                self._draw_cell(stdscr, x, y, 1)
        stdscr.refresh()

    def _draw_cell(self, stdscr, x, y, color_pair):
        """Helper to draw a single cell using 2-block wide walls."""
        scr_x = x * 4
        scr_y = y * 2

        cell = self.__cells[y][x]
        NORTH, WEST = 1, 8
        BLOCK = "\u2588"
        V_WALL = BLOCK * 2
        CORNER = BLOCK * 2
        BODY = "  "
        H_WALL = BLOCK * 4
        H_OPEN = BODY + CORNER

        try:

            stdscr.attron(curses.color_pair(color_pair))
            stdscr.move(scr_y, scr_x)
            if cell.grid & NORTH:
                stdscr.addstr(H_WALL)
            else:
                stdscr.addstr(H_OPEN)

            stdscr.move(scr_y + 1, scr_x)
            if cell.grid & WEST:
                stdscr.addstr(V_WALL + BODY)
            else:
                stdscr.addstr("  " + BODY)

            stdscr.attroff(curses.color_pair(color_pair))
        except curses.error:
            pass

    def solve_maze(self) -> str:
        queue = [(self.__maze.entry, "")]
        visited = {self.__maze.entry}
        NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8

        while queue:
            (cx, cy), path = queue.pop(0)

            if (cx, cy) == self.__maze.exit:
                return path

            if (
                not self.__cells[cy][cx].grid & NORTH
                and (cx, cy - 1) not in visited
            ):
                visited.add((cx, cy - 1))
                queue.append(((cx, cy - 1), path + "N"))
            if (
                not self.__cells[cy][cx].grid & EAST
                and (cx + 1, cy) not in visited
            ):
                visited.add((cx + 1, cy))
                queue.append(((cx + 1, cy), path + "E"))
            if (
                not self.__cells[cy][cx].grid & SOUTH
                and (cx, cy + 1) not in visited
            ):
                visited.add((cx, cy + 1))
                queue.append(((cx, cy + 1), path + "S"))
            if (
                not self.__cells[cy][cx].grid & WEST
                and (cx - 1, cy) not in visited
            ):
                visited.add((cx - 1, cy))
                queue.append(((cx - 1, cy), path + "W"))

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

    def animate_curses(self) -> None:
        """Entry point to run the solution animation."""
        path_str = self.solve_maze()
        path_coords = self.get_path_coords(path_str)
        curses.wrapper(self._run_curses_animation, path_coords)

    def _run_curses_animation(self, stdscr, path_coords):
        """The actual drawing logic using curses with 2-block wide walls."""
        curses.curs_set(0)
        stdscr.clear()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

        NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8

        BLOCK = "\u2588"
        V_WALL = BLOCK * 2
        CORNER = BLOCK * 2
        BODY = "  "
        H_WALL = BLOCK * 4
        H_OPEN = BODY + CORNER

        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(0, 0, CORNER)
        for cell in self.__cells[0]:
            if cell.grid & NORTH:
                stdscr.addstr(H_WALL)
            else:
                stdscr.addstr(H_OPEN)

        for y, row in enumerate(self.__cells):
            screen_y = y * 2 + 1
            stdscr.move(screen_y, 0)

            for x, cell in enumerate(row):

                if cell.grid & WEST:
                    stdscr.addstr(V_WALL, curses.color_pair(1))
                else:
                    stdscr.addstr("  ")

                stdscr.addstr(BODY)

            if row[-1].grid & EAST:
                stdscr.addstr(V_WALL, curses.color_pair(1))

            screen_y_south = y * 2 + 2
            stdscr.move(screen_y_south, 0)
            stdscr.addstr(CORNER, curses.color_pair(1))

            for cell in row:
                if cell.grid & SOUTH:
                    stdscr.addstr(H_WALL, curses.color_pair(1))
                else:
                    stdscr.addstr(H_OPEN, curses.color_pair(1))

        stdscr.refresh()
        time.sleep(0.5)

        for i, (px, py) in enumerate(path_coords):
            scr_y = py * 2 + 1
            scr_x = px * 4 + 2

            color = curses.color_pair(2)
            if i == 0 or i == len(path_coords) - 1:
                color = curses.color_pair(3) | curses.A_BOLD

            try:
                stdscr.addstr(scr_y, scr_x, "**", color)
                stdscr.refresh()
                time.sleep(0.05)
            except curses.error:
                pass

        max_y, _ = stdscr.getmaxyx()
        msg_y = min(max_y - 1, self.__maze.height * 2 + 3)
        try:
            stdscr.addstr(msg_y, 0, "Path Complete! Press any key to exit...")
        except curses.error:
            pass
        stdscr.getch()

    def write_output(self, path: str) -> None:
        try:
            file = open(self.__maze.output_file, "w+")
        except PermissionError:
            reply = None
            while reply != "no" and reply != "yes":
                reply = input(
                    f"This file '{self.__maze.output_file}' already exists. "
                    "Do you want to delete it and recreate it? (yes/no): "
                ).lower()
            if reply == "yes":
                os.remove(self.__maze.output_file)
                self.__maze.output_file = open(self.__maze.output_file, "w+")
            else:
                sys.exit(1)
        except IsADirectoryError:
            reply = None
            while reply != "no" and reply != "yes":
                reply = input(
                    f"This '{self.__maze.output_file}' "
                    "is directory not file. "
                    "Do you want to delete it and recreate it? (yes/no): "
                ).lower()
            if reply == "yes":
                os.rmdir(self.__maze.output_file)
                self.__maze.output_file = open(self.__maze.output_file, "w+")
            else:
                sys.exit(1)

        for row in self.__cells:
            hex_row = "".join([f"{cell.grid:X}" for cell in row])
            file.write(hex_row + "\n")

        file.write("\n")
        file.write(f"{self.__maze.entry[0]},{self.__maze.entry[1]}\n")
        file.write(f"{self.__maze.exit[0]},{self.__maze.exit[1]}\n")
        file.write(path + "\n")
        file.write(f"Seed={self.__maze.seed}\n")
        file.close()
        print(f"Maze saved to {self.__maze.output_file}")

    def display_maze(
            self, path_coords: Optional[List[Tuple[int, int]]] = None
    ) -> None:

        if path_coords is None:
            path_coords = []

        cells = self.__cells
        NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8

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
                    print("  ", end="")

                if (x, y) in path_coords:
                    print(f"{Y}**{RS}", end="")
                else:
                    print(BODY, end="")

            if row[-1].grid & EAST:
                print(V_WALL, end="")
            print()

            print(CORNER, end="")
            for cell in row:
                if cell.grid & SOUTH:
                    print(H_WALL, end="")
                else:
                    print(H_OPEN, end="")
            print()
