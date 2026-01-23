import sys


def get_walls(hex_char):
    val = int(hex_char, 16)
    return {
        'N': val & 1,
        'E': val & 2,
        'S': val & 4,
        'W': val & 8
    }


def draw_maze(lines):
    st_line = lines[0].strip()
    print(" ", end="")

    for c in st_line:
        walls = get_walls(c)
        print("___ " if walls['N'] else "    ", end="")
    print("")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        for c in line:
            walls = get_walls(c)
            print("|" if walls['W'] else " ", end="")
            print("   ", end="")
        lst_walls = get_walls(line[-1])
        print("|" if lst_walls['E'] else " ")
        print(" ", end="")

        for c in line:
            walls = get_walls(c)
            print("___ " if walls['S'] else "    ", end="")
        print("")


file = sys.argv[1]

try:
    with open(file, 'r') as f:
        lines = f.readlines()
        draw_maze(lines)


except Exception as e:
    print(f"3ndk ch Err: {e}")
