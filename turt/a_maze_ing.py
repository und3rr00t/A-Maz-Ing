print("--- PYTHON IS STARTING ---")
import sys
import os
import turtle
from typing import List, Tuple, Dict, Any


try:
    from mazegen import MazeGenerator
except ImportError:
    print(
        "Error: Could not import 'mazegen'. "
        "Ensure the folder exists and has __init__.py."
        )
    sys.exit(1)


CELL_SIZE = 20


def parse_config(filename: str) -> Dict[str, Any]:
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    config = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'): continue
                if '=' in line:
                    k, v = line.split('=', 1)
                    config[k.strip()] = v.strip()

        data = {
            'WIDTH': int(config['WIDTH']),
            'HEIGHT': int(config['HEIGHT']),
            'OUTPUT_FILE': config.get('OUTPUT_FILE', 'maze.txt')
        }
        data['ENTRY'] = tuple(map(int, config['ENTRY'].split(',')))
        data['EXIT'] = tuple(map(int, config['EXIT'].split(',')))
        return data
    except Exception as e:
        print(f"Config Error: {e}")
        sys.exit(1)


def solve_maze(grid: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]) -> str:
    queue = [(start, "")]
    visited = {start}
    while queue:
        (cx, cy), path = queue.pop(0)
        if (cx, cy) == end: return path

        # Directions: N(1), E(2), S(4), W(8)
        moves = [(0, -1, 1, "N"), (1, 0, 2, "E"), (0, 1, 4, "S"), (-1, 0, 8, "W")]
        for dx, dy, wall, char in moves:
            nx, ny = cx + dx, cy + dy
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
                if not (grid[cy][cx] & wall) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + char))
    return ""


def get_path_coords(start: Tuple[int, int], path_str: str) -> List[Tuple[int, int]]:
    coords = [start]
    x, y = start
    for move in path_str:
        if move == 'N': y -= 1
        elif move == 'S': y += 1
        elif move == 'E': x += 1
        elif move == 'W': x -= 1
        coords.append((x, y))
    return coords


class MazeVisualizer:
    def __init__(self, cfg):
        self.cfg = cfg
        self.width = cfg['WIDTH']
        self.height = cfg['HEIGHT']
        self.grid = []

        print("DEBUG: Setting up Turtle Screen...")
        self.screen = turtle.Screen()
        self.screen.setup(width=800, height=800)
        self.screen.bgcolor("black")
        self.screen.title("A-Maze-ing (Turtle Version)")
        self.screen.tracer(0)
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)
        self.pen.penup()

        self.regenerate()

        print("DEBUG: Listening for keys...")
        self.screen.listen()
        self.screen.onkey(self.regenerate, "r")
        self.screen.onkey(sys.exit, "Escape")

        print("Controls: [R] Regenerate | [ESC] Quit")
        try:
            self.screen.mainloop()
        except Exception:
            print("Exiting...")

    def regenerate(self):
        print("Generating new maze...")
        self.pen.clear()

        gen = MazeGenerator(self.width, self.height)
        self.grid = gen.generate(self.cfg['ENTRY'])

        path_str = solve_maze(self.grid, self.cfg['ENTRY'], self.cfg['EXIT'])
        path_coords = get_path_coords(self.cfg['ENTRY'], path_str)

        self.draw(path_coords)
        self.screen.update()

    def draw_square(self, x, y, color):
        """Helper to draw a filled square"""
        screen_x = (x * CELL_SIZE) - (self.width * CELL_SIZE // 2)
        screen_y = (self.height * CELL_SIZE // 2) - (y * CELL_SIZE)

        self.pen.goto(screen_x, screen_y)
        self.pen.color(color)
        self.pen.begin_fill()
        for _ in range(4):
            self.pen.forward(CELL_SIZE - 2)
            self.pen.right(90)
        self.pen.end_fill()

    def draw(self, path):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if (x, y) in path:
                    self.draw_square(x, y, "red")

                screen_x = (x * CELL_SIZE) - (self.width * CELL_SIZE // 2)
                screen_y = (self.height * CELL_SIZE // 2) - (y * CELL_SIZE)

                self.pen.goto(screen_x, screen_y)
                self.pen.color("white")
                self.pen.width(2)

                if cell & 1:
                    self.pen.pendown(); self.pen.forward(CELL_SIZE); self.pen.penup()
                else:
                    self.pen.forward(CELL_SIZE)
                self.pen.right(90)

                if cell & 2:
                    self.pen.pendown(); self.pen.forward(CELL_SIZE); self.pen.penup()
                else:
                    self.pen.forward(CELL_SIZE)
                self.pen.right(90)

                if cell & 4:
                    self.pen.pendown(); self.pen.forward(CELL_SIZE); self.pen.penup()
                else:
                    self.pen.forward(CELL_SIZE)
                self.pen.right(90)

                if cell & 8:
                    self.pen.pendown(); self.pen.forward(CELL_SIZE); self.pen.penup()
                else:
                    self.pen.forward(CELL_SIZE)
                self.pen.right(90)


def main():
    print("DEBUG: Inside main()")
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    cfg = parse_config(sys.argv[1])
    MazeVisualizer(cfg)


if __name__ == "__main__":
    main()
