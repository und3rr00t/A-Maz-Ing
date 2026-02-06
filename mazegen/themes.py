from typing import Dict, Tuple, Callable
from .terminal_ctl import TerminalCtl


class Themes:
    """
    Manages visual themes for the maze terminal display.

    This class provides several predefined color schemes
    (Badlands, Dark Forest, Cherry Grove, Pale Garden)
    and a custom configuration option using
    ANSI true-color (24-bit RGB) codes.\n

    Attributes:
        reset (str): ANSI escape code to reset terminal formatting.\n
        theme (Dict[str, str]): The currently selected color mapping.
    """
    reset = "\033[0m"

    def __init__(self) -> None:
        """
        Initializes the Themes class and prompts the user to select a theme.\nn

        Returns:
            None
        """
        # Use Callable to be explicit about dictionary values
        theme_options: Dict[str, Callable[[], Dict[str, str]]] = {
            '1': self.get_badlands_theme,
            '2': self.get_dark_forest_theme,
            '3': self.get_cherry_grove_theme,
            '4': self.get_pale_garden_theme,
            '5': self.get_custom_theme
        }

        self.theme = self._select_theme(theme_options)

    def _select_theme(
            self,
            options: Dict[str, Callable[[], Dict[str, str]]]
    ) -> Dict[str, str]:
        """
        Displays the theme menu and captures the user's selection.\n

        Args:
            options (Dict[str, Callable]):
            A mapping of keys to theme functions.\n

        Returns:
            Dict[str, str]: The dictionary containing the chosen color theme.\n
        """
        print("Choose Maze Theme:")
        print("1. Badlands Theme.")
        print("2. Dark Forest Theme.")
        print("3. Cherry Grove Theme.")
        print("4. Pale Garden Theme.")
        print("5. Custom.")

        reply = TerminalCtl.getch().lower()
        while reply not in options:
            reply = TerminalCtl.getch().lower()

        return options[reply]()

    @staticmethod
    def get_badlands_theme() -> Dict[str, str]:
        """
        Returns the 'Badlands' theme colors (Oranges and Earth tones).\n

        Returns:
            Dict[str, str]: Mapping of maze elements to RGB escape codes.
        """
        return {
            "W_C": "\x1b[38;2;211;84;0m",
            "P_C": "\x1b[38;2;253;245;230m",
            "S_C": "\x1b[38;2;39;174;96m",
            "E_C": "\x1b[38;2;241;196;15m",
            "SOL_C": "\x1b[38;2;100;210;255m",
            "EXP_C": "\x1b[38;2;52;73;94m",
            "CC_C": "\x1b[38;2;80;80;80m",
            "PL_C": "\x1b[38;2;255;140;0m"
        }

    @staticmethod
    def get_dark_forest_theme() -> Dict[str, str]:
        """
        Returns the 'Dark Forest' theme colors (Deep greens and blues).

        Returns:
            Dict[str, str]: Mapping of maze elements to RGB escape codes.
        """
        return {
            "W_C": "\x1b[38;2;13;59;24m",
            "P_C": "\x1b[38;2;236;240;241m",
            "S_C": "\x1b[38;2;46;204;113m",
            "E_C": "\x1b[38;2;192;57;43m",
            "SOL_C": "\x1b[38;2;52;152;219m",
            "EXP_C": "\x1b[38;2;44;62;80m",
            "CC_C": "\x1b[38;2;60;60;60m",
            "PL_C": "\x1b[38;2;101;67;33m"
        }

    @staticmethod
    def get_cherry_grove_theme() -> Dict[str, str]:
        """
        Returns the 'Cherry Grove' theme colors (Pinks and soft whites).\n

        Returns:
            Dict[str, str]: Mapping of maze elements to RGB escape codes.
        """
        return {
            "W_C": "\x1b[38;2;255;182;193m",
            "P_C": "\x1b[38;2;255;255;255m",
            "S_C": "\x1b[38;2;219;112;147m",
            "E_C": "\x1b[38;2;142;68;173m",
            "SOL_C": "\x1b[38;2;135;206;235m",
            "EXP_C": "\x1b[38;2;255;105;180m",
            "CC_C": "\x1b[38;2;240;240;240m",
            "PL_C": "\x1b[38;2;186;85;211m"
        }

    @staticmethod
    def get_pale_garden_theme() -> Dict[str, str]:
        """
        Returns the 'Pale Garden' theme colors (Grays and muted tones).\n

        Returns:
            Dict[str, str]: Mapping of maze elements to RGB escape codes.
        """
        return {
            "W_C": "\x1b[38;2;189;195;199m",
            "P_C": "\x1b[38;2;245;245;245m",
            "S_C": "\x1b[38;2;127;140;141m",
            "E_C": "\x1b[38;2;95;158;160m",
            "SOL_C": "\x1b[38;2;173;216;230m",
            "EXP_C": "\x1b[38;2;149;165;166m",
            "CC_C": "\x1b[38;2;100;100;100m",
            "PL_C": "\x1b[38;2;220;220;220m"
        }

    @staticmethod
    def get_custom_theme() -> Dict[str, str]:
        """
        Allows the user to interactively define a custom theme
        by entering RGB values.\n

        Returns:
            Dict[str, str]: User-defined mapping of
            maze elements to RGB escape codes.
        """
        def get_rgb() -> Tuple[int, int, int]:
            """
            Captures Red, Green, and Blue inputs from the user.\n

            Returns:
                Tuple[int, int, int]: Validated RGB values.
            """
            while True:
                hex_val = input("Enter color code (e.g., #ffffff): #").strip()
                if len(hex_val) == 6:
                    try:
                        return (
                            int(hex_val[0:2], 16),
                            int(hex_val[2:4], 16),
                            int(hex_val[4:6], 16)
                        )
                    except ValueError:
                        pass
                print("Invalid format. Use #RRGGBB (e.g., #ffffff).")

        elements: Dict[str, str] = {
            "Wall": "W_C",
            "Plain Path": "P_C",
            "Start Cell": "S_C",
            "Exit Cell": "E_C",
            "Solution Path": "SOL_C",
            "Step Algorithm": "EXP_C",
            "Closed Cell": "CC_C",
            "Player": "PL_C",
        }

        theme: Dict[str, str] = {}
        for element, t_key in elements.items():
            print(f"\n--- Configure Color for: {element} ---")
            r, g, b = get_rgb()
            theme[t_key] = f"\x1b[38;2;{r};{g};{b}m"
        return theme
