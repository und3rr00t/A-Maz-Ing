import sys
import time
from maze_generator import MazeGenerator, report_error, player_mode, getch


def clear_screen() -> None:
    """
    Clears the terminal screen using ANSI escape codes.\n

    Returns:
        None\n
    """
    print("\033[H\033[J", end="")


def a_maz_ing() -> None:
    """
    Main logic for maze generation, visualization, and user interaction menu.\n

    This function initializes the maze generator, handles the generation
    process, manages imperfect maze adjustments, and provides an interactive
    menu for the user to solve, play, or regenerate mazes.\n

    Returns:
        None\n
    """
    gen_maze = MazeGenerator(sys.argv[1])
    maze = gen_maze.get_maze()
    gen_maze.generate_maze()

    if not maze.perfection:
        gen_maze.make_imperfect(chance=1)

    path = gen_maze.solve_maze()
    path_coords = gen_maze.get_path_coords(path)
    gen_maze.write_output(path)
    gen_maze.display_maze([])

    print(f"\nMaze generated & saved to {gen_maze.get_maze().output_file}")
    print(f"Solution Path Length: {len(path)}")
    print("-" * 30)
    print("1. Show Solution Path")
    print("2. Regenerate New Maze")
    print("3. Play Mode")
    print("4. Quit")

    while True:

        choice = getch()
        while choice not in ('1', '2', '3', '4'):
            choice = getch()

        if choice == '1':
            while True:
                clear_screen()
                gen_maze.display_maze()
                print("1. Show step solving")
                print("2. Show path")
                replay = getch()
                while replay not in ('1', '2', '3', '4'):
                    replay = getch()
                if replay == '1':
                    gen_maze.solve_maze_visual()
                else:
                    clear_screen()
                    time.sleep(0.5)
                    tmp_coords = []
                    for coord in path_coords:
                        tmp_coords.append(coord)
                        gen_maze.display_maze(tmp_coords)
                        time.sleep(0.1)
                        if coord != path_coords[-1]:
                            clear_screen()

                print("1. Regenerate Solution Path")
                print("2. Regenerate New Maze")
                print("3. Play Mode")
                print("4. Quit")

                choice = getch()
                while choice not in ('1', '2', '3', '4'):
                    choice = getch()

                if choice == '1':
                    continue
                else:
                    clear_screen()
                    break
        if choice == '2':
            return
        if choice == '3':
            player_mode(gen_maze)
            print("\n1. Show Solution Path")
            print("2. Regenerate New Maze")
            print("3. Replay")
            print("4. Quit")

        if choice == '4':
            exit(0)


def main() -> None:
    """
    Entry point of the script.\n

    Handles command line arguments validation and manages the main program
    loop. It also catches and reports unexpected exceptions.\n

    Returns:
        None\n

    Raises:
        SystemExit: If the number of command line arguments is incorrect.\n
    """
    if len(sys.argv) != 2:
        print(
            "Error in use:\n\tHow to use: "
            "'python3 a_maz_ing.py <config_file.txt>"
        )
        sys.exit(1)

    try:
        while True:
            a_maz_ing()
    except Exception as error:
        report_error(error)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
