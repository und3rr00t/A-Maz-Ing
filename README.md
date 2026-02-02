*This project has been created as part of the 42 curriculum by ousd-da and adraji.*
# A-Maze-Ing
---

## Description
---
**A-Maze-Ing** is a terminal-based application designed to generate, solve, and play within complex mazes. Developed as part of the 1337/42 Network journey, the project’s goal is to demonstrate mastery over graph traversal algorithms, bitwise logic, and object-oriented Python design. It provides a highly customizable experience where users can define maze dimensions, choose generation algorithms, and even play through the results using a terminal-based game mode.

## Instructions
---
### Installation
1. **Clone the repository:**
```Bash
git clone https://github.com/SEGV-Survivors/A-Maze-Ing.git
cd A-Maze-Ing
```
2. **Setup Dependencies:**Ensure you have Python 3.10+ installed. Use the provided `Makefile` to install necessary linting and packaging tools:
```Bash
make install
```

### Execution
To generate a maze, provide a configuration file as a command-line argument:
```Bash
make run
# Or manually:
python3 a_maze_ing.py config.txt
```

### Development Commands
* `make lint`: `Runs` flake8 and `mypy` for strict type checking and PEP8 compliance.
* `make debug`: Starts the program in the Python debugger (`pdb`).
* `make package`: Builds a reusable `.whl` package from the project.

## Configuration Guide
---
The `config.txt` file must follow this exact structure:
| Key | Required | Value / Format | Description |
| :--- | :--- | :--- | :--- |
| **WIDTH** | Yes | Integer (e.g., `30`) | Horizontal cells in the maze. |
| **HEIGHT** | Yes | Integer (e.g., `30`) | Vertical cells in the maze. |
| **ENTRY** | Yes | `x,y` (e.g., `6,0`) | Start coordinates. |
| **EXIT** | Yes | `x,y` (e.g., `19,19`) | Target coordinates. |
| **OUTPUT_FILE** | Yes | String (e.g., `maze_output.txt`) | Filename for the saved maze. |
| **PERFECT** | Yes | `True`/`False` | If `True`, the maze has exactly one path (no loops). |
| **ALGORITHM** | Yes | `DFS` or `WILSON` | The generation strategy used to create the maze. |
| **SEED** | No | Integer | Specific seed for reproducible mazes; defaults to current time if omitted. |

## Algorithms & Technical Choices
---
### Chosen Algorithms
We implemented two distinct generation methods to provide variety in maze structure:
1. **Randomized Depth-First Search (DFS):** A recursive backtracker algorithm.
2. **Wilson’s Algorithm:** A loop-erased random walk that produces a uniform spanning tree.

### Why These Algorithms?
* **DFS** was chosen for its speed and its tendency to create long, winding corridors with fewer dead ends, making for a challenging visual experience.
* **Wilson's** was chosen because it generates mathematically "unbiased" mazes. Unlike DFS, which is biased towards certain shapes, Wilson’s ensures every possible spanning tree of the grid has an equal chance of being generated.

### Advanced Features
* **Interactive Player Mode**: A WASD-controlled game mode with real-time timers.
* **Themes Engine**: Support for 24-bit RGB terminal colors, including presets like "Badlands" and "Cherry Grove".
* **"42" Pattern**: A specialized cell logic that embeds a "42" shape within the maze.

## Reusability
---
The logic is strictly decoupled through a package structure:
* `maze_generator` **package**: This entire folder is a reusable Python package.
* `MazeGenerator` **Class**: Can be imported into any Python project to generate maze data without the terminal UI.
* `MazeParseConfig`: A standalone robust parser that can be adapted for any key-value configuration task.

## Team & Project Management
---
### C-Brothers team
#### Roles
* **OUSAMA ED-DAHBI (**`oused-da`**)**:
* **ADAM RAJI (**`adraji`**)**:

### Planning & Evolution
* **Initial Plan**: Build a simple script that prints a maze to a file.
* **Evolution**: The project expanded to include real-time terminal animation, a robust `Makefile` for CI/CD simulation, and custom themes to improve user experience.

## Resources
---
* **Jamis Buck's "The Buckblog"**: Deep dive into maze generation algorithms.
* **Python** `termios` **Documentation**: For low-level terminal I/O control.
* **ANSI Escape Codes Reference**: For 24-bit color and cursor manipulation.
