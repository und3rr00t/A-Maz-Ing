import sys
import tty
import time
import termios
from typing import List, Tuple
from .error_class import R, G, RS
from .terminal_ctl import TerminalCtl
from .gen_maze import MazeGenerator, NORTH, SOUTH, WEST, EAST


def player_mode(gen_maze: MazeGenerator) -> None:
    """Starts an interactive gaming session where the user can solve the maze.

    The player uses WASD keys to move through the grid. The function tracks
    the time elapsed since the first move and detects when the player
    reaches the target exit. It also provides an option to replay the
    player's movement path.

    Args:
        gen_maze (MazeGenerator): The generator instance providing the maze
            structure and display methods.

    Returns:
        None
    """
    TerminalCtl.hide_cursor()
    TerminalCtl.clear_screen()

    BLOCK = "\u2588"

    maze = gen_maze.get_maze()
    cells = gen_maze.get_cells()
    theme = maze.theme.theme
    reset = maze.theme.reset
    px, py = maze.entry
    target = maze.exit
    player_path = [(px, py)]
    start_time = time.time()

    print("--- PLAY MODE ---", TerminalCtl.erase_line)
    print("Use W, A, S, D | Press Q to Quit", TerminalCtl.erase_line)
    gen_maze.display_maze(True, player_path)

    while (px, py) != target:
        move = TerminalCtl.getch().lower()

        if move == 'q':
            print(
                f"{R}You failed to solve the maze!{RS}", TerminalCtl.erase_line
            )
            TerminalCtl.reset_cursor(row=maze.height * 2 + 5)
            TerminalCtl.show_cursor()
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

        if (px, py) != maze.entry:
            TerminalCtl.reset_cursor(
                col=player_path[0][0] * 4 + 3,
                row=player_path[0][1] * 2 + 4
            )
            print(f"{theme['S_C']}{2 * BLOCK}{reset}")

        if player_path[-1] != maze.entry:
            TerminalCtl.reset_cursor(
                col=player_path[-1][0] * 4 + 3,
                row=player_path[-1][1] * 2 + 4
            )
            print(f"{theme['P_C']}{2 * BLOCK}{reset}")

        TerminalCtl.reset_cursor(col=px * 4 + 3, row=py * 2 + 4)
        print(f"{theme['PL_C']}{2 * BLOCK}{reset}")
        player_path.append((px, py))

    TerminalCtl.clear_screen()
    gen_maze.display_maze(True, path_coords=[(px, py)])
    end_time = time.time()
    duration = end_time - start_time

    print(f"\n{G}CONGRATULATIONS! Reached exit in {duration:.2f}s{RS}")
    print("Press E to Exit | Press F to Show Your Path")

    replay = TerminalCtl.getch().lower()

    while replay not in ('e', 'f'):
        replay = TerminalCtl.getch().lower()

    if replay == 'f':
        TerminalCtl.clear_screen()
        tmp_path: List[Tuple[int, int]] = []
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno())
            for coord in player_path:
                if TerminalCtl.check_for_enter():
                    TerminalCtl.reset_cursor()
                    gen_maze.display_maze(True, player_path)
                    break
                tmp_path.append(coord)
                TerminalCtl.reset_cursor()
                gen_maze.display_maze(True, tmp_path)
                time.sleep(0.01)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

    TerminalCtl.show_cursor()
