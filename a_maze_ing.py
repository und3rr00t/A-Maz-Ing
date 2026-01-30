import os
import sys
# import time
from maze import Maze
from gen_maze import MazeGenerator
from error_class import report_error, RS, Y


def clear_screen():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def a_maz_ing():

    maze = Maze(sys.argv[1])
    gen_maze = MazeGenerator(maze)
    gen_maze.generate()

    if not maze.perfection:
        gen_maze.make_imperfect(chance=0.3)

    path = gen_maze.solve_maze(0)
    # path_coords = gen_maze.get_path_coords(path)
    gen_maze.write_output(path)
    gen_maze.display_maze([])

    print(f"\nMaze generated & saved to {gen_maze.get_maze().output_file}")
    print(f"Solution Path Length: {len(path)}")
    print("-" * 30)
    print("1. Show Solution Path")
    print("2. Regenerate New Maze")
    print("3. Quit")

    choice = "Invalid choice."

    while choice not in ('1', '2', '3'):

        choice = input("Choice: ")
        if choice == '1':
            maze = gen_maze.get_maze()
            if maze.d_mod == "Visualizer":
                print("Visualizer coming soon")
            else:
                path = gen_maze.solve_maze(1)
                final_path_coords = gen_maze.get_path_coords(path)
                clear_screen()
                gen_maze.display_maze(final_path_coords)
                print(f"\n{Y}EXIT REACHED! BFS explored the whole maze.{RS}")

            exit(0)
        elif choice == '2':
            return
        elif choice == '3':
            exit(0)
        else:
            print("Invalid choice.")


def main():

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
