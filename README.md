# A-Maze-Ing
---

## Description
---
**A-Maze-Ing** is a robust Python-based maze generator and solver. It features custom configuration parsing, multiple generation algorithms (DFS and WILSON), and a unique "42" pattern easter egg—a nod to the **1337/42 Network** curriculum.

## Features
---
* ** Custom Maze Generation**: Supports **DFS (Depth-First Search)** and **WILSON** algorithms.
* **Intelligent Configuration**: A custom parser that handles mandatory keys, optional seeds, and error reporting.
* **"42" Pattern**: Automatically embeds a "42" shape within the maze structure using specialized cell logic.
* **Interactive Solver**: Includes a **BFS-based solver** with an animated terminal visualizer to show the solution path.
* **Imperfect Mazes**: Option to generate "imperfect" mazes by selectively removing walls, creating loops and multiple paths.
* **Diagnostic Error Handling**: Specialized error classes provide clear, color-coded feedback for syntax or value errors in config files.

## Installation
---
1. **Clone the repository:**
```Bash
git clone https://github.com/SEGV-Survivors/A-Maze-Ing.git
cd A-Maze-Ing
```
2. **Ensure you have Python 3.10+ installed**. No external dependencies are required as the project uses standard libraries.

## Usage
---
Run the program by passing a configuration file as an argument:
```Bash
python3 a_maz_ing.py config.txt
```
#### Configuration Guide
Your `config.txt` should follow this format:
* **WIDTH/HEIGHT**: Dimensions of the maze.
* **ENTRY/EXIT**: Coordinates (e.g., `0,0`).
* **PERFECT**: `True` for a mathematical maze (one path), `False` for loops.
* **ALGORITHM**: `DFS` or `WILSON`.
* **SEED**: (Optional) Use a specific integer to recreate the same maze.

## Project Structure
---
| File | Description |
| :--- | :--- |
| `a_maz_ing.py` | The main entry point and terminal UI loop. |
| `gen_maze.py` | Contains the core logic for maze generation and solving. |
| `cell.py` | Defines cell properties and the logic for the "42" pattern. |
| `maze.py` | Handles configuration parsing and maze state. |
| `error_class.py` | Custom exception classes for robust error reporting. |

## Controls
---
Once a maze is generated, you can:
1. **Show Solution Path**: Animates the path from Entry to Exit in the terminal.
2. **Regenerate**: Instantly creates a new maze using the same config.
3. **Quit**: Exit the program.

## Authors
---
This project was developed by:

| Name | 42 Login | GitHub |
| :--- | :--- | :--- |
| **OUSAMA ED-DAHBI** | `oused-da` | [@und3rr00t](https://github.com/und3rr00t) |
| **ADAM RAJI** | `adraji` | [@adraji-42](https://github.com/adraji-42) |
---
*Developed as part of the 1337/42 Network journey.*
