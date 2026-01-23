import random
import sys
if len(sys.argv) < 3:
    print("messing args")
    sys.exit(1)
WIDTH = int(sys.argv[1])
HEIGHT = int(sys.argv[2])

DIRECTIONS = {
    'N': (0, -1, 1, 4),
    'S': (0, 1, 4, 1),
    'E': (1, 0, 2, 8),
    'W': (-1, 0, 8, 2)
}


def remove_wall(grid, x1, y1, x2, y2):
    if x2 < x1:
        d = DIRECTIONS['W']
    elif x2 > x1:
        d = DIRECTIONS['E']
    elif y2 < y1:
        d = DIRECTIONS['N']
    elif y2 > y1:
        d = DIRECTIONS['S']
    else:
        return
    grid[y1][x1] &= ~d[2]
    grid[y2][x2] &= ~d[3]


def stamp_42(grid, visited):
    points_4 = [
        (4, 4), (4, 5), (4, 6), (4, 7), (4, 8),
        (5, 8), (6, 8), (7, 8),
        (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9), (7, 10)
    ]

    points_2 = [
        (10, 4), (11, 4), (12, 4), (13, 4),
        (13, 5), (13, 6), (13, 7),
        (12, 7), (11, 7), (10, 7),
        (10, 8), (10, 9), (10, 10),
        (11, 10), (12, 10), (13, 10)
    ]
    path_cells = points_4 + points_2

    def draw_segment(points):
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i+1]
            if abs(x1-x2) + abs(y1-y2) == 1:
                remove_wall(grid, x1, y1, x2, y2)

            visited[y1][x1] = True
            visited[y2][x2] = True

    draw_segment([(4, 4), (4, 8)])
    draw_segment([(4, 8), (7, 8)])
    draw_segment([(7, 4), (7, 10)])
    draw_segment(points_2)

    return path_cells


def gen_maze(width, height):
    grid = [[15 for _ in range(width)] for _ in range(height)]
    visited = [[False for _ in range(width)] for _ in range(height)]

    start_cells = stamp_42(grid, visited)
    stack = start_cells[:]

    while stack:
        cx, cy = stack[-1]
        neighbors = []
        possible_moves = [
            (0, -1, 1, 4),
            (0, 1, 4, 1),
            (1, 0, 2, 8),
            (-1, 0, 8, 2)
        ]

        for dx, dy, wall, opp_wall in possible_moves:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < width and 0 <= ny < height and not visited[ny][nx]:
                neighbors.append((nx, ny, wall, opp_wall))

        if neighbors:
            nx, ny, wall, opp_wall = random.choice(neighbors)
            grid[cy][cx] &= ~wall
            grid[ny][nx] &= ~opp_wall
            visited[ny][nx] = True
            stack.append((nx, ny))
        else:
            stack.pop()

    return grid


def print_hex(grid):
    for row in grid:
        line = "".join(format(cell, 'X') for cell in row)
        print(line)


maze = gen_maze(WIDTH, HEIGHT)
print_hex(maze)
