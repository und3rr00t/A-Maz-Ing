# import os
import sys
from maze import Maze
from gen_maze import MazeGenerator
# from error_class import report_error


def a_maz_ing():

    gen_maze = MazeGenerator(Maze(sys.argv[1]))

    action = gen_maze.run_interactive_session()

    if action == "quit":
        print("\nGoodbye!")
        sys.exit(0)
    elif action == "regenerate":
        return


def main():
    if len(sys.argv) != 2:
        print("How to use: python3 a_maze_ing.py <config_file.txt>")
        sys.exit(1)

    try:
        while True:
            a_maz_ing()
    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
else:
    print(f"This module '{__name__}' not for import")
