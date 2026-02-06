import sys
import tty
import select
import termios
from typing import Final


class TerminalCtl:
    """
    A collection of utilities for terminal manipulation using ANSI sequences.
    """

    erase_line: Final[str] = "\033[K"

    @staticmethod
    def hide_cursor() -> None:
        """Hides the terminal cursor from view.

        Returns:
            None
        """
        print("\033[?25l", end="")

    @staticmethod
    def show_cursor() -> None:
        """Makes the terminal cursor visible again.

        Returns:
            None
        """
        print("\033[?25h", end="")

    @staticmethod
    def reset_cursor(row: int = 1, col: int = 1) -> None:
        """Moves the terminal cursor to a specific coordinate.

        Args:
            row: The target row number.
            col: The target column number.

        Returns:
            None
        """
        print(f"\033[{row};{col}H", end="")

    @staticmethod
    def clean_up() -> None:
        """Resets terminal formatting and shows the cursor.

        Returns:
            None
        """
        print("\033[0m")
        TerminalCtl.show_cursor()

    @staticmethod
    def clear_screen() -> None:
        """Clears the terminal screen and homes the cursor.

        Returns:
            None
        """
        print("\033[H\033[J", end="")

    @staticmethod
    def check_for_enter() -> bool:
        """Checks if the Enter key is currently pressed.

        Returns:
            bool: True if Enter key was detected in the input buffer.
        """
        if select.select([sys.stdin], [], [], 0)[0] == [sys.stdin]:
            char = sys.stdin.read(1)
            if char in ('\n', '\r'):
                return True
        return False

    @staticmethod
    def getch() -> str:
        """Reads a single character from stdin in raw mode.

        Returns:
            str: The character captured from the keyboard.
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        return ch
