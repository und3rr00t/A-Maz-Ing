import random

WIDTH = 20
HEIGHT = 20

DIRECTIONS = [
    (0, -1, 1, 4),
    (0, 1, 4, 1),
    (1, 0, 2, 8),
    (-1, 0, 8, 2)
]


def gen_maze(width, height):
    grid = [[15 for _ in range(width)] for _ in range(height)]
    visited = [[False for _ in range(width)] for _ in range(height)]
    stack = [(0, 0)]
    visited[0][0] = True

    while stack:
        cx, cy = stack[-1]

        neigbors = []
        for dx, dy, wall, opp_wall in DIRECTIONS:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < width and 0 <= ny < height and not visited[ny][nx]:
                neigbors.append((nx, ny, wall, opp_wall))

        if neigbors:
            nx, ny, wall, opp_wall = random.choice(neigbors)

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
