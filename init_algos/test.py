import sys


def analyze_cell(c):
    if c == "\n":
        print("\n\n────────────────────────────────────\n\n")
    try:
        v = int(c, 16)
    except ValueError:
        return
    N = 1
    E = 2
    S = 4
    W = 8

    print(f"Cell '{c}'  (value : {v})")

    if v & N:
        print(" - North Wall: CLOSED 🚧")
    else:
        print(" - North Wall:  OPEN   🛤️ (You can move Left)")
    if v & E:
        print(" - East Wall: CLOSED 🚧")
    else:
        print(" - East Wall:  OPEN   🛤️ (You can move Left)")
    if v & S:
        print(" - South Wall: CLOSED 🚧")
    else:
        print(" - South Wall:  OPEN   🛤️ (You can move Left)")
    if v & W:
        print(" - West Wall: CLOSED 🚧")
    else:
        print(" - West Wall:  OPEN   🛤️ (You can move Left)")


if len(sys.argv) != 2:
    print("Messing argements")
    print("Usage: python3 script.py output.txt")
    sys.exit(1)

file = sys.argv[1]
try:
    with open(file, "r") as f:
        while True:
            c = f.read(1)
            if not c:
                break
            analyze_cell(c)
except FileNotFoundError:
    print(f"Error: File {file} not found.")
