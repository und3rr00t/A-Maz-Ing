import sys
import tty
import time
import random
import shutil
import termios
from .cell import Cell
from .maze import Maze
from .error_class import Y, RS
from .terminal_ctl import TerminalCtl
from typing import List, Tuple, Optional, Set


NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8
DIRECTIONS = (
    (0, -1, NORTH, SOUTH),
    (0, 1, SOUTH, NORTH),
    (1, 0, EAST, WEST),
    (-1, 0, WEST, EAST)
)


class MazeGenerator:
    """
    Class responsible for generating and solving mazes.

    This class handles the core logic of creating mazes (via DFS or Wilson's),
    modifying them (making them imperfect), solving them using BFS,
    and rendering the result to the terminal or a file.

    Attributes:
        __maze (Maze): The maze configuration and properties.
        __cells (List[List[Cell]]): The 2D grid of maze cells.
        __solution (str): The solution path string.
    """

    def __init__(self, config_file: str) -> None:
        """
        Initializes the generator with a maze configuration.

        Args:
            config_file (str): Path to the configuration file.
        """
        self.__maze = Maze(config_file)
        random.seed(self.__maze.seed)
        self.__cells: List[List[Cell]] = Cell.get_cells(self.__maze)
        self.__solution: str = ""

    def get_maze(self) -> Maze:
        """
        Returns the current maze object.

        Returns:
            Maze: The internal maze instance.
        """
        return self.__maze

    def get_cells(self) -> List[List[Cell]]:
        """
        Returns the current cells object.

        Returns:
            List[List[Cell]]: The 2D grid of Cell objects.
        """
        return self.__cells

    def get_solution_path(self) -> str:
        """
        Returns the short solution path for the maze.

        Returns:
            str: A string representing the moves (N, S, E, W).
        """
        return self.__solution

    def generate_maze(self, visualizing: bool = False) -> None:
        """
        Triggers the maze generation based on the selected algorithm.

        Args:
            visualizing (bool): Whether to show the generation process.
            Defaults to False.

        Returns:
            None
        """
        def dfs_maze_generator(skip: bool) -> bool:
            """
            Generates a maze using the Randomized Depth-First Search algorithm.

            This is a recursive backtracker implementation
            that creates a perfect maze by carving paths
            until all reachable cells are visited.

            Args:
                skip (bool): Whether to skip the visualization.

            Returns:
                bool: Updated skip status.
            """
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

                    if (
                        visualizing and not skip
                        and TerminalCtl.check_for_enter()
                    ):
                        skip = True

                    if visualizing and not skip:
                        self.display_maze(visualizing=visualizing)
                        time.sleep(0.001)
                        TerminalCtl.reset_cursor()
                else:
                    stack.pop()

            return skip

        def wilson_maze_generator(skip: bool) -> bool:
            """
            Generates a maze using Wilson's algorithm.

            This algorithm produces an unbiased uniform
            spanning tree of the grid, ensuring a perfectly
            random distribution of mazes.

            Args:
                skip (bool): Whether to skip the visualization.

            Returns:
                bool: Updated skip status.
            """
            width, height = self.__maze.width, self.__maze.height
            unvisited = [(x, y) for x in range(width) for y in range(height)]

            root = self.__maze.entry
            self.__cells[root[1]][root[0]].visited = True
            unvisited.remove(root)

            while unvisited:
                current = None
                while not current and unvisited:
                    current = random.choice(unvisited)

                    if self.__cells[current[1]][current[0]].ft_pattern:
                        unvisited.remove(current)
                        current = None

                if not current:
                    break

                path = [current]

                while not self.__cells[current[1]][current[0]].visited:
                    dx, dy, wall, opp_wall = random.choice(DIRECTIONS)
                    nx, ny = current[0] + dx, current[1] + dy

                    if 0 <= nx < width and 0 <= ny < height:
                        if self.__cells[ny][nx].ft_pattern:
                            continue
                        neighbor = (nx, ny)

                        if neighbor in path:
                            path = path[:path.index(neighbor) + 1]
                        else:
                            path.append(neighbor)
                        current = neighbor

                for i in range(len(path) - 1):
                    cx1, cy1 = path[i]
                    cx2, cy2 = path[i + 1]

                    for dx, dy, wall, opp_wall in DIRECTIONS:
                        if (cx1 + dx == cx2) and (cy1 + dy == cy2):
                            self.__cells[cy1][cx1].grid &= ~wall
                            self.__cells[cy2][cx2].grid &= ~opp_wall
                            break

                    self.__cells[cy1][cx1].visited = True
                    if (cx1, cy1) in unvisited:
                        unvisited.remove((cx1, cy1))
                    if (
                        visualizing and not skip
                        and TerminalCtl.check_for_enter()
                    ):
                        skip = True
                    if visualizing and not skip:
                        self.display_maze(visualizing=visualizing)
                        time.sleep(0.001)
                        TerminalCtl.reset_cursor()

            return skip

        def make_imperfect(skip: bool, chance: float = 0.7) -> bool:
            """
            Creates an imperfect maze by randomly removing walls at dead ends.

            Args:
                skip (bool): Whether to skip the visualization.
                chance (float): Probability (0.0 to 1.0) of removing a wall.

            Returns:
                bool: Updated skip status.
            """
            for y in range(self.__maze.height):
                for x in range(self.__maze.width):
                    if self.__cells[y][x].ft_pattern is True:
                        continue

                    walls = []
                    for i, (dx, dy, wall, opp) in enumerate(DIRECTIONS):
                        if (self.__cells[y][x].grid & wall):
                            walls.append(DIRECTIONS[i])

                    if len(walls) == 3 and random.random() < chance:
                        dx, dy, wall, opp_wall = random.choice(walls)
                        nx, ny = x + dx, y + dy
                        if (
                            0 <= nx < self.__maze.width
                            and 0 <= ny < self.__maze.height
                        ):
                            if self.__cells[ny][nx].ft_pattern:
                                continue

                            self.__cells[y][x].grid &= ~wall
                            self.__cells[ny][nx].grid &= ~opp_wall

                            if (
                                visualizing and not skip
                                and TerminalCtl.check_for_enter()
                            ):
                                skip = True
                            if visualizing and not skip:
                                TerminalCtl.reset_cursor()
                                self.display_maze(visualizing=visualizing)
                                time.sleep(0.1)

            return skip

        def get_solution_path() -> str:
            """
            Finds the shortest path from entry to exit using BFS.

            Returns:
                str: A string representing the moves (N, S, E, W).
            """
            queue = [(self.__maze.entry, "")]
            visited = {self.__maze.entry}

            while queue:
                (cx, cy), path = queue.pop(0)

                if (cx, cy) == self.__maze.exit:
                    return path

                for dx, dy, wall, move in [
                    (0, -1, NORTH, "N"), (1, 0, EAST, "E"),
                    (0, 1, SOUTH, "S"), (-1, 0, WEST, "W")
                ]:
                    nx, ny = cx + dx, cy + dy
                    if (0 <= nx < self.__maze.width and
                            0 <= ny < self.__maze.height and
                            not (self.__cells[cy][cx].grid & wall) and
                            (nx, ny) not in visited):
                        visited.add((nx, ny))
                        queue.append(((nx, ny), path + move))

            return ""

        skip = False
        algo = self.__maze.algo.upper()

        TerminalCtl.clear_screen()
        TerminalCtl.hide_cursor()

        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno())
            if algo == "WILSON":
                skip = wilson_maze_generator(skip)
            else:
                skip = dfs_maze_generator(skip)
            if not self.__maze.perfection:
                skip = make_imperfect(skip)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

        if visualizing:
            if skip:
                TerminalCtl.reset_cursor()
                self.display_maze(visualizing=visualizing)
            self.__solution = get_solution_path()
            TerminalCtl.reset_cursor(row=self.__maze.height * 2 + 1)
            TerminalCtl.show_cursor()

    def solve_maze(self, visualizing: bool = False) -> None:
        """
        Finds the shortest path from entry to exit using BFS.

        Args:
            visualizing (bool): Whether to visualize the solving process.

        Returns:
            None
        """
        BLOCK = "\u2588"

        TerminalCtl.hide_cursor()
        TerminalCtl.clear_screen()
        self.display_maze(visualizing=visualizing)

        skip = False
        exp_c = self.__maze.theme.theme['EXP_C']
        reset = self.__maze.theme.reset
        queue = [(self.__maze.entry, "")]
        visited: Set[Tuple[int, int]] = {self.__maze.entry}
        old_settings = termios.tcgetattr(sys.stdin)

        try:
            tty.setcbreak(sys.stdin.fileno())

            while queue:
                (cx, cy), path = queue.pop(0)

                if (cx, cy) == self.__maze.exit:
                    coords = self.get_path_coords(self.__maze.entry, path)
                    tmp_coords: List[Tuple[int, int]] = []

                    if visualizing:
                        for coord in coords:
                            if (
                                visualizing and not skip
                                and TerminalCtl.check_for_enter()
                            ):
                                skip = True
                            if skip:
                                TerminalCtl.reset_cursor()
                                self.display_maze(visualizing, coords, visited)
                                return
                            TerminalCtl.reset_cursor()
                            tmp_coords.append(coord)
                            self.display_maze(visualizing, tmp_coords, visited)
                            time.sleep(0.001)

                    return

                for dx, dy, wall, move in [
                    (0, -1, NORTH, "N"), (1, 0, EAST, "E"),
                    (0, 1, SOUTH, "S"), (-1, 0, WEST, "W")
                ]:
                    nx, ny = cx + dx, cy + dy

                    if (
                        0 <= nx < self.__maze.width
                        and 0 <= ny < self.__maze.height
                        and not (self.__cells[cy][cx].grid & wall)
                    ):
                        if (nx, ny) not in visited:
                            visited.add((nx, ny))
                            queue.append(((nx, ny), path + move))

                        if (
                            visualizing and not skip
                            and TerminalCtl.check_for_enter()
                        ):
                            skip = True

                        if visualizing and not skip:
                            bridge_col = (cx * 4 + 3) + (dx * 2)
                            bridge_row = (cy * 2 + 2) + dy

                            TerminalCtl.reset_cursor(
                                col=bridge_col, row=bridge_row
                            )
                            print(f"{exp_c}{BLOCK * 2}{reset}")

                            if (
                                (nx, ny) != self.__maze.exit
                                and (nx, ny) != self.__maze.entry
                            ):
                                TerminalCtl.reset_cursor(
                                    col=nx * 4 + 3, row=ny * 2 + 2
                                )
                                print(f"{exp_c}{BLOCK * 2}{reset}", flush=True)
                            time.sleep(0.001)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            TerminalCtl.show_cursor()
            if visualizing:
                TerminalCtl.reset_cursor(row=self.__maze.height * 2 + 2)

    @staticmethod
    def get_path_coords(
        start: Tuple[int, int], path_str: str
    ) -> List[Tuple[int, int]]:
        """
        Translates a solution string into coordinate pairs.

        Args:
            start (Tuple[int, int]): Starting (x, y) coordinates.
            path_str (str): The string of directional moves (N, S, E, W).

        Returns:
            List[Tuple[int, int]]: A list of (x, y) tuples
            representing the path.
        """
        coords = [start]
        x, y = start
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

    def write_output(self) -> None:
        """
        Saves the generated maze grid and its solution details to a file.

        Returns:
            None

        Raises:
            SystemExit: If an error occurs during file writing.
        """
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
                f.write(f"SOLUTION: {self.__solution}\n")
        except (PermissionError, IsADirectoryError):
            print(f"Error writing to file: {output_path}")
            sys.exit(1)

    def display_maze(
        self,
        visualizing: bool = False,
        path_coords: Optional[List[Tuple[int, int]]] = None,
        visited_coords: Optional[Set[Tuple[int, int]]] = None
    ) -> None:
        """
        Renders the maze in the terminal with colored characters.

        Args:
            visualizing (bool): Whether visualization is enabled.
            path_coords (Optional[List[Tuple[int, int]]]):
            Coordinates for the path.
            visited_coords (Optional[Set[Tuple[int, int]]]):
            Coordinates for explored nodes.

        Returns:
            None
        """

        if not visualizing:
            return

        def check_terminal_size() -> bool:
            """Checks if the terminal dimensions meet the minimum requirements.

            Returns:
                bool: True if dimensions are sufficient, False otherwise.
            """
            size = shutil.get_terminal_size()

            return (
                size.columns >= self.__maze.width * 4 + 4
                and size.lines >= self.__maze.height * 2 + 2
            )

        while not check_terminal_size():
            print(
                f"{Y}WARNING{RS}: Terminal are insufficient to show the maze."
            )
            print("Please enlarge the terminal.")
            print("Press ENTER to continue | Press any key to exit.")
            ch = TerminalCtl.getch()
            if ch != '\n' and ch != '\r':
                sys.exit()

        if path_coords is None:
            path_coords = []

        if visited_coords is None:
            visited_coords = set()

        BLOCK = "\u2588"

        theme = self.__maze.theme.theme
        reset = self.__maze.theme.reset
        v_wall = f"{theme['W_C']}{BLOCK * 2}{reset}"
        corner = f"{theme['W_C']}{BLOCK * 2}{reset}"
        body = f"{theme['P_C']}{BLOCK * 2}{reset}"
        h_wall = f"{theme['W_C']}{BLOCK * 4}{reset}"

        print(f"{corner}", end="")
        for _ in self.__cells[0]:
            print(h_wall, end="")
        print(TerminalCtl.erase_line)

        for y, row in enumerate(self.__cells):
            for x, cell in enumerate(row):
                if cell.grid & WEST:
                    print(v_wall, end="")
                else:
                    if (x, y) in path_coords and (x - 1, y) in path_coords:
                        print(f"{theme['SOL_C']}██{reset}", end="")
                    elif (
                        (x, y) in visited_coords
                        and (x - 1, y) in visited_coords
                    ):
                        print(f"{theme['EXP_C']}██{reset}", end="")
                    else:
                        print(body, end="")

                if path_coords and (x, y) == path_coords[-1]:
                    print(f"{theme['PL_C']}██{reset}", end="")
                elif (x, y) == self.__maze.entry:
                    print(f"{theme['S_C']}██{reset}", end="")
                elif (x, y) == self.__maze.exit:
                    print(f"{theme['E_C']}██{reset}", end="")
                elif (x, y) in path_coords:
                    print(f"{theme['SOL_C']}██{reset}", end="")
                elif (x, y) in visited_coords:
                    print(f"{theme['EXP_C']}██{reset}", end="")
                elif cell.grid == 15:
                    print(f"{theme['CC_C']}██{reset}", end="")
                else:
                    print(body, end="")

            if row[-1].grid & EAST:
                print(v_wall, end="")
            print(TerminalCtl.erase_line)

            print(corner, end="")
            for x, cell in enumerate(row):
                if cell.grid & SOUTH:
                    print(h_wall, end="")
                else:
                    if (x, y) in path_coords and (x, y + 1) in path_coords:
                        print(f"{theme['SOL_C']}██{reset}{corner}", end="")
                    elif (
                        (x, y) in visited_coords
                        and (x, y + 1) in visited_coords
                    ):
                        print(f"{theme['EXP_C']}██{reset}{corner}", end="")
                    else:
                        print(f"{theme['P_C']}██{reset}{corner}", end="")
            print(TerminalCtl.erase_line)
