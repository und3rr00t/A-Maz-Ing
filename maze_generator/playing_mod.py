import sys
import tty
import time
import termios
from typing import List, Tuple
from .error_class import R, G, RS
from .gen_maze import MazeGenerator, clear_screen, NORTH, SOUTH, WEST, EAST


def getch() -> str:
    """
    Reads a single character from the standard input.\n

    This function changes the terminal settings to raw mode to capture
    keystrokes immediately without requiring the user to press Enter.
    It restores the original terminal settings after reading.\n

    Returns:
        str: The character read from the input.
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return ch


def player_mode(gen_maze: MazeGenerator) -> None:
    """
    An interactive gaming session begins where the user can solve the maze.\n

    The player uses WASD keys to move through the grid. The function tracks
    the time elapsed since the first move and detects when the player
    reaches the target exit. It also provides an option to replay the
    player's movement path.\n

    Args:
        gen_maze (MazeGenerator): The generator instance providing the maze
        structure and display methods.\n

    Returns:
        None
    """
    maze = gen_maze.get_maze()
    cells = gen_maze.get_cells()
    px, py = maze.entry
    target = maze.exit
    player_path = [(px, py)]
    while (px, py) != target:
        clear_screen()

        if (px, py) == maze.entry:
            start_time = time.time()
        current_duration = time.time() - start_time

        print("--- PLAY MODE ---")
        print(f"Time: {current_duration:.1f}s")
        print("Use W, A, S, D | Press Q to Quit")
        gen_maze.display_maze(path_coords=[(px, py)])

        move = getch().lower()

        if move == 'q':
            print(f"{R}You failed to solve the maze!{RS}")
            return

        if move == 'w' and not (cells[py][px].grid & NORTH):
            py -= 1
        elif move == 's' and not (cells[py][px].grid & SOUTH):
            py += 1
        elif move == 'a' and not (cells[py][px].grid & WEST):
            px -= 1
        elif move == 'd' and not (cells[py][px].grid & EAST):
            px += 1
        else:
            continue
        player_path.append((px, py))
    else:
        clear_screen()
        gen_maze.display_maze(path_coords=[(px, py)])
        end_time = time.time()
        duration = end_time - start_time

        print(
            f"\n{G}CONGRATULATIONS! You reached the exit! "
            f"in {duration:.2f}s{RS}"
        )
        print(
            "Press E to Exit\n"
            "Press F to Show Your Path"
        )

        replay = getch()

        while replay not in ('e', 'f'):
            replay = getch()

        if replay == 'f':
            tmp_path: List[Tuple[int, int]] = []

            for coord in player_path:
                tmp_path.append(coord)
                clear_screen()
                gen_maze.display_maze(tmp_path)
                time.sleep(0.1)
        return
