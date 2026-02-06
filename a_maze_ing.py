import sys
from mazegen import (
    TerminalCtl, MazeGenerator, report_error, player_mode
)


def a_maz_ing() -> None:
    """
    Main logic for maze generation, visualization, and user interaction menu.\n

    This function initializes the maze generator, handles the generation
    process, manages imperfect maze adjustments, and provides an interactive
    menu for the user to solve, play, or regenerate mazes.\n

    Returns:
        None\n
    """
    TerminalCtl.clear_screen()
    gen_maze = MazeGenerator(sys.argv[1])
    gen_maze.generate_maze(True)
    gen_maze.write_output()

    print(f"\nMaze generated & saved to {gen_maze.get_maze().output_file}")
    print(f"Solution Path Length: {len(gen_maze.get_solution_path())}")
    print("-" * 30)
    print("1. Show Solution Path")
    print("2. Regenerate New Maze")
    print("3. Play Mode")
    print("4. Quit")

    while True:

        choice = TerminalCtl.getch().lower()
        while choice not in ('1', '2', '3', '4'):
            choice = TerminalCtl.getch().lower()

        if choice == '1':
            while True:
                gen_maze.solve_maze(True)

                print("1. Regenerate Solution Path")
                print("2. Regenerate New Maze")
                print("3. Play Mode")
                print("4. Quit")

                choice = TerminalCtl.getch().lower()
                while choice not in ('1', '2', '3', '4'):
                    choice = TerminalCtl.getch().lower()

                if choice == '1':
                    continue
                else:
                    TerminalCtl.clear_screen()
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
    except BaseException:
        pass
    finally:
        TerminalCtl.clean_up()
