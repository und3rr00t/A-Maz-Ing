import sys
import os
import random
from typing import Dict, List, Tuple, Any


try:
    from mazegen import MazeGenerator
except ImportError:
    print(
        "Error: Could not import 'mazegen'. "
        "Make sure the 'mazegen' folder exists and has an __init__.py."
        )
    sys.exit(1)


def parse_config(filename: str) -> Dict[str, Any]:
    config = {}
    if not os.path.exists(filename):
        print(f"Error: Configuration file '{filename}' not found.")
        sys.exit(1)

    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    except Exception as e:
        print(f"Error reading config: {e}")
        sys.exit(1)

    try:
        data = {}
        data['WIDTH'] = int(config['WIDTH'])
        data['HEIGHT'] = int(config['HEIGHT'])

        e_x, e_y = map(int, config['ENTRY'].split(','))
        data['ENTRY'] = (e_x, e_y)

        ex_x, ex_y = map(int, config['EXIT'].split(','))
        data['EXIT'] = (ex_x, ex_y)

        data['OUTPUT_FILE'] = config['OUTPUT_FILE']
        return data
    except (ValueError, KeyError) as e:
        print(f"Error: Invalid configuration format. Missing or bad key: {e}")
        sys.exit(1)


def solve_maze(grid: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]) -> str:
    """
    Finds shortest path using BFS. Returns string of directions 'NESW'.
    """
    queue = [(start, "")]
    visited = {start}

    NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8

    while queue:
        (cx, cy), path = queue.pop(0)

        if (cx, cy) == end:
            return path

        # Check all 4 directions based on walls
        # North
        if not (grid[cy][cx] & NORTH) and (cx, cy - 1) not in visited:
            visited.add((cx, cy - 1))
            queue.append(((cx, cy - 1), path + "N"))
        # East
        if not (grid[cy][cx] & EAST) and (cx + 1, cy) not in visited:
            visited.add((cx + 1, cy))
            queue.append(((cx + 1, cy), path + "E"))
        # South
        if not (grid[cy][cx] & SOUTH) and (cx, cy + 1) not in visited:
            visited.add((cx, cy + 1))
            queue.append(((cx, cy + 1), path + "S"))
        # West
        if not (grid[cy][cx] & WEST) and (cx - 1, cy) not in visited:
            visited.add((cx - 1, cy))
            queue.append(((cx - 1, cy), path + "W"))

    return ""


def get_path_coords(start: Tuple[int, int], path_str: str) -> List[Tuple[int, int]]:
    """Converts a string like 'SSEN' into a list of (x,y) coordinates."""
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


def write_output(filename: str, grid: List[List[int]], start: Tuple, end: Tuple, path: str) -> None:
    try:
        with open(filename, 'w') as f:
            for row in grid:
                # Convert each cell int to Hex char (upper case)
                hex_row = "".join([f"{cell:X}" for cell in row])
                f.write(hex_row + "\n")

            f.write("\n")
            f.write(f"{start[0]},{start[1]}\n")
            f.write(f"{end[0]},{end[1]}\n")
            f.write(path + "\n")
        print(f"Maze saved to {filename}")
    except IOError as e:
        print(f"Error writing to file: {e}")


def display_maze(grid: List[List[int]], path_coords: List[Tuple[int, int]] = None):
    """
    Renders the maze using the user's specific ASCII logic (wide format).
    Adapted to handle the integer grid and solution path.
    """
    if path_coords is None:
        path_coords = []

    print(" ", end="")
    for x in range(len(grid[0])):
        val = grid[0][x]
        print("___ " if (val & 1) else "    ", end="")
    print("")

    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            print("|" if (val & 8) else " ", end="")

            if (x, y) in path_coords:
                print(" * ", end="") 
            else:
                print("   ", end="")

        print("|" if (row[-1] & 2) else " ")

        print(" ", end="")
        for val in row:
            print("___ " if (val & 4) else "    ", end="")
        print("")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    config_file = sys.argv[1]
    cfg = parse_config(config_file)

    print(f"Generating maze {cfg['WIDTH']}x{cfg['HEIGHT']}...")

    while True:
        gen = MazeGenerator(cfg['WIDTH'], cfg['HEIGHT'])
        maze = gen.generate(cfg['ENTRY'])

        path_str = solve_maze(maze, cfg['ENTRY'], cfg['EXIT'])
        path_coords = get_path_coords(cfg['ENTRY'], path_str)

        write_output(cfg['OUTPUT_FILE'], maze, cfg['ENTRY'], cfg['EXIT'], path_str)

        display_maze(maze, path_coords=[])

        print(f"\nMaze generated & saved to {cfg['OUTPUT_FILE']}")
        print(f"Solution Path Length: {len(path_str)}")
        print("-" * 30)
        print("1. Show Solution Path")
        print("2. Regenerate New Maze")
        print("3. Quit")

        choice = input("Choice: ")

        if choice == '1':
            display_maze(maze, path_coords)
            input("\nPress Enter to continue...")
        elif choice == '2':
            continue
        elif choice == '3':
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
