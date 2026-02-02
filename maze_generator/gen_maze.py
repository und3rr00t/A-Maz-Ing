import sys
import time
import random
from .cell import Cell
from .maze import Maze
from typing import List, Tuple, Optional


NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8
DIRECTIONS = (
    (0, -1, NORTH, SOUTH),
    (0, 1, SOUTH, NORTH),
    (1, 0, EAST, WEST),
    (-1, 0, WEST, EAST)
)


def clear_screen() -> None:
    """
    Clears the terminal screen using ANSI escape codes.\n

    Returns:
        None\n
    """
    print("\033[H\033[J", end="")


class MazeGenerator:
    """
    Class responsible for generating and solving mazes.\n

    This class handles the core logic of creating mazes (via DFS or Wilson's),
    modifying them (making them imperfect), solving them using BFS,
    and rendering the result to the terminal or a file.\n

    Attributes:\n
        __maze (Maze): The maze configuration and properties.\n
        __cells (List[List[Cell]]): The 2D grid of maze cells.
    """

    def __init__(self, config_file: str) -> None:
        """
        Initializes the generator with a maze configuration
        and sets the random seed.\n

        Args:
            config_file (str): Path to the configuration file.\n

        Returns:
            None\n
        """
        self.__maze = Maze(config_file)
        random.seed(self.__maze.seed)
        self.__cells: List[List[Cell]] = Cell.get_cells(self.__maze)

    def get_maze(self) -> Maze:
        """
        Returns the current maze object.\n

        Returns:
            Maze: The internal maze instance.
        """
        return self.__maze

    def get_cells(self) -> List[List[Cell]]:
        """
        Returns the current cells object.\n

        Returns:
            List[List[Cell]]: The 2D grid of Cell objects.\n
        """
        return self.__cells

    def generate_maze(self) -> None:
        """
        Triggers the maze generation based
        on the selected algorithm in the config.\n

        Returns:
            None\n
        """
        algo = self.__maze.algo.upper()

        if algo == "WILSON":
            self.wilson_maze_generator()
        else:
            self.dfs_maze_generator()

    def dfs_maze_generator(self) -> None:
        """
        Generates a maze using the Randomized Depth-First Search algorithm.\n

        This is a recursive backtracker implementation that creates a perfect
        maze by carving paths until all reachable cells are visited.\n

        Returns:
            None\n
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
                self.display_maze()
                time.sleep(0.01)
                clear_screen()
            else:
                stack.pop()

    def wilson_maze_generator(self) -> None:
        """
        Generates a maze using Wilson's algorithm (Loop-erased random walk).\n

        This algorithm produces an unbiased uniform spanning tree of the grid,
        ensuring a perfectly random distribution of mazes.\n

        Returns:
            None\n
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

                self.display_maze()
                time.sleep(0.01)
                clear_screen()

    def make_imperfect(self, chance: float = 0.5) -> None:
        """
        Creates an imperfect maze by randomly removing walls at dead ends.\n

        Args:
            chance (float):
            Probability (0.0 to 1.0) of removing a wall at a dead end.\n

        Returns:
            None\n
        """
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

    def solve_maze(self) -> str:
        """
        Finds the shortest path from entry to exit
        using Breadth-First Search (BFS).\n

        Returns:
            str: A string representing the moves
            (N, S, E, W) to solve the maze.
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

                if (
                    0 <= nx < self.__maze.width and
                    0 <= ny < self.__maze.height and
                    not (self.__cells[cy][cx].grid & wall)
                    and (nx, ny) not in visited
                ):

                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + move))

        return ""

    def solve_maze_visual(self) -> None:
        """
        Solves the maze using BFS
        and visualizes the exploration process in real-time.\n

        Returns:
            None
        """
        queue = [(self.__maze.entry, "")]
        visited = {self.__maze.entry}

        while queue:
            (cx, cy), path = queue.pop(0)

            current_path = self.get_path_coords(path)
            clear_screen()
            self.display_maze(
                path_coords=current_path, visited_coords=visited
            )
            time.sleep(0.01)

            if (cx, cy) == self.__maze.exit:
                return

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

    def get_path_coords(self, path_str: str) -> List[Tuple[int, int]]:
        """
        Translates a solution string (e.g., 'NESE') into coordinate pairs.\n

        Args:
            path_str (str): The string of directional moves.\n

        Returns:
            List[Tuple[int, int]]: A list of (x, y) tuples
            representing the path.\n
        """
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
        """
        Saves the generated maze grid
        and its solution details to the output file.\n

        Args:
            path (str): The solution string.\n

        Returns:
            None\n

        Raises:
            SystemExit: If an error occurs during file writing.\n
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
                f.write(f"SOLUTION: {path}\n")

            print(f"Maze saved to {output_path}")
        except (PermissionError, IsADirectoryError) as e:
            print(f"Error writing to file: {e}")
            sys.exit(1)

    def display_maze(
        self,
        path_coords: Optional[List[Tuple[int, int]]] = None,
        visited_coords: Optional[set[Tuple[int, int]]] = None
    ) -> None:
        """
        Renders the maze in the terminal with colored characters.\n

        Supports visualizing the current state, solution path,
        and explored nodes using the specific theme defined in the maze.\n

        Args:
            path_coords (Optional[List[Tuple[int, int]]]):
            Coordinates to color as path\n.
            visited_coords (Optional[set]): Coordinates to color as explored.\n

        Returns:
            None
        """
        if path_coords is None:
            path_coords = []
        if visited_coords is None:
            visited_coords = set()

        BLOCK = "\u2588"

        theme = self.__maze.theme.theme
        reset = self.__maze.theme.reset

        V_WALL = f"{theme['W_C']}{BLOCK * 2}{reset}"
        CORNER = f"{theme['W_C']}{BLOCK * 2}{reset}"
        BODY = f"{theme['P_C']}{BLOCK * 2}{reset}"
        H_WALL = f"{theme['W_C']}{BLOCK * 4}{reset}"

        print(CORNER, end="")
        for _ in self.__cells[0]:
            print(H_WALL, end="")
        print()

        for y, row in enumerate(self.__cells):
            for x, cell in enumerate(row):
                if cell.grid & WEST:
                    print(V_WALL, end="")
                else:
                    if (x, y) in path_coords and (x - 1, y) in path_coords:
                        print(f"{theme['SOL_C']}██{reset}", end="")
                    elif (
                        (x, y) in visited_coords
                        and (x - 1, y) in visited_coords
                    ):
                        print(f"{theme['EXP_C']}██{reset}", end="")
                    else:
                        print(BODY, end="")

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
                        print(f"{theme['SOL_C']}██{reset}{CORNER}", end="")
                    elif (
                        (x, y) in visited_coords
                        and (x, y + 1) in visited_coords
                    ):
                        print(f"{theme['EXP_C']}██{reset}{CORNER}", end="")
                    else:
                        print(f"{theme['P_C']}██{reset}{CORNER}", end="")
            print()
