import time
from typing import Tuple, Dict, Any
from .themes import Themes
from .error_class import (
    ConfigSyntaxError, ConfigKeyError, ConfigValueError, B, RS
)


class Maze:
    """
    Class representing the maze structure and its configuration settings.\n

    This class serves as a data container and orchestrator for the maze
    properties, including its dimensions, entry/exit points, and generation
    settings, all derived from a parsed configuration file.\n

    Attributes:\n
        width (int): The width of the maze in cells.\n
        height (int): The height of the maze in cells.\n
        entry (tuple): (x, y) coordinates of the entrance.\n
        exit (tuple): (x, y) coordinates of the exit.\n
        output_file (str): Path to the file where the maze will be saved.\n
        perfection (bool): Whether the maze is perfect (no loops) or not.\n
        seed (int): Random seed used for generation.\n
        algo (str): The algorithm name (e.g., "DFS", "WILSON").\n
        theme (Themes): Theme object for terminal rendering.
    """
    def __init__(self, config_file: str) -> None:
        """
        Initializes the maze by parsing a configuration file
        and setting attributes.\n

        Args:
            config_file (str): Path to the configuration file to be parsed.\n

        Returns:
            None\n
        """
        config = self.MazeParseConfig.parsing_conf(config_file)
        self.width: int = config["WIDTH"]
        self.height: int = config["HEIGHT"]
        self.entry: Tuple[int, int] = config["ENTRY"]
        self.exit: Tuple[int, int] = config["EXIT"]
        self.output_file: str = config["OUTPUT_FILE"]
        self.perfection: bool = config["PERFECT"]
        self.seed: int = config["SEED"]
        self.algo: str = config["ALGORITHM"].upper()
        self.theme: Themes = Themes()

    class MazeParseConfig:
        """
        Internal class to handle logic for parsing
        and validating configuration data.\n

        This class provides static methods to read the file, check for syntax
        errors, and ensure all values meet the required constraints for
        maze generation.\n
        """
        @staticmethod
        def parsing_value(config: Dict[str, Any]) -> Dict[str, Any]:
            """
            Validates and converts configuration values to their
            appropriate data types.\n

            This method performs deep validation of coordinates, dimensions,
            perfection flags, and algorithm names.\n

            Args:
                config (Dict[str, str]):
                Raw dictionary of keys and string values.\n

            Returns:
                Dict:
                Processed dictionary with validated and casted data types.\n

            Raises:
                ConfigValueError: If any value is out of bounds, incorrectly
                formatted, or logically inconsistent (e.g., ENTRY == EXIT).\n
            """

            if "SEED" in config:
                if config["SEED"].isdigit():
                    config["SEED"] = int(config["SEED"])
                else:
                    config["SEED"] = int.from_bytes(
                        bytes(config["SEED"], 'utf-8')
                    )
            else:
                config["SEED"] = int(time.time())

            if "ALGORITHM" in config:
                config["ALGORITHM"] = config["ALGORITHM"].upper()
                if config["ALGORITHM"] not in ("DFS", "WILSON"):
                    raise ConfigValueError(
                        f"{B}{config['ALGORITHM']}{RS} Algorithm not found"
                    )

            try:
                config["WIDTH"] = int(config["WIDTH"])
                config["HEIGHT"] = int(config["HEIGHT"])
            except ValueError:
                raise ConfigValueError(
                    f"{B}WIDTH{RS}, {B}HEIGHT{RS}, "
                    f"and {B}SEED{RS} must be valid integers."
                )

            if config["WIDTH"] < 0 or config["HEIGHT"] < 0:
                raise ConfigValueError(
                    f"Dimensions cannot be negative. Found {B}WIDTH: "
                    f"{config['WIDTH']}{RS}, {B}HEIGHT: "
                    f"{config['HEIGHT']}{RS}"
                )

            if config["WIDTH"] * config["HEIGHT"] < 2:
                raise ConfigValueError(
                    "Maze area is too small "
                    f"({config['WIDTH'] * config['HEIGHT']} cells). "
                    f"Minimum required is {B}2{RS} cells."
                )

            for key in ("ENTRY", "EXIT"):
                val = config[key]
                if val.count(',') != 1:
                    raise ConfigValueError(
                        f"{B}{key}{RS} has invalid format"
                        f" '{val}'. Expected format: {B}x,y{RS} (no spaces)."
                    )

                try:
                    x, y = map(int, val.split(',', 1))
                    if x < 0 or y < 0:
                        raise ConfigValueError(
                            f"{B}{key}{RS} coordinates ({x},{y}) "
                            "cannot be negative."
                        )
                    if x >= config["WIDTH"] or y >= config["HEIGHT"]:
                        raise ConfigValueError(
                            f"{B}{key}{RS} ({x},{y}) is outside "
                            f"maze boundaries ({config['WIDTH']}x"
                            f"{config['HEIGHT']})."
                        )
                    config[key] = (x, y)
                except ValueError:
                    raise ConfigValueError(
                        f"{B}{key}{RS} coordinates '{val}' "
                        f"must be integers."
                    )

            if config["ENTRY"] == config["EXIT"]:
                raise ConfigValueError(
                    "The {B}ENTRY{RS} and {B}EXIT{RS} must be different"
                )

            perf = config["PERFECT"].strip().capitalize()
            if perf not in ("True", "False"):
                raise ConfigValueError(
                    f"Invalid value '{perf}' for {B}PERFECT{RS}. "
                    f"Expected {B}'True'{RS} or {B}'False'{RS}."
                )
            config["PERFECT"] = (perf == "True")

            return config

        @staticmethod
        def parsing_conf(file_path: str) -> Dict[str, Any]:
            """
            Reads the configuration file and extracts key-value pairs.\n

            Parses the file line by line, ignoring comments and empty lines,
            while checking for mandatory keys and correct syntax.\n

            Args:
                file_path (str): The filesystem path to the config file.\n

            Returns:
                dict:
                A dictionary containing all parsed and validated config keys.\n

            Raises:
                ConfigSyntaxError: If a line is malformed (missing '=').\n
                ConfigKeyError:
                If mandatory keys are missing or unknown keys are found.\n
                FileNotFoundError:
                If the config file does not exist.\n
                PermissionError:
                If there are no read permissions for the file.\n
                IsADirectoryError:
                If the provided path points to a directory.\n
            """

            req_keys = list(ConfigKeyError.get_required_keys())
            add_keys = list(ConfigKeyError.get_additional_keys())
            config = {}

            try:
                with open(file_path, "r") as file:
                    for i, line in enumerate(file, 1):
                        line = line.strip()
                        if not line or line.startswith('#'):
                            continue

                        if line.count('=') != 1:
                            raise ConfigSyntaxError(
                                f"Syntax Error at {B}line {i}: '{line}'{RS} in"
                                " config file: Expected exactly one '=' "
                                f"operator (found {line.count('=')})"
                            )

                        key, value = map(str.strip, line.split('='))
                        key = key.upper()

                        if not value:
                            raise ConfigValueError(
                                f"Empty key {B}'{key}'{RS} value  at "
                                f"{B}line {i}: '{line}'{RS} in config file."
                            )

                        if key not in req_keys and key not in add_keys:
                            raise ConfigKeyError(
                                f"Unknown key {B}'{key}'{RS} at "
                                f"{B}line {i}: '{line}'{RS} in config file."
                            )

                        config[key] = value
                        if key in req_keys:
                            req_keys.remove(key)
                        elif key in add_keys:
                            add_keys.remove(key)

                if req_keys:
                    raise ConfigKeyError(
                        f"Missing mandatory keys in config file: "
                        f"{B}{', '.join(req_keys)}{RS}"
                    )

                return Maze.MazeParseConfig.parsing_value(config)

            except FileNotFoundError:
                raise FileNotFoundError(
                    f"The configuration file {B}'{file_path}'{RS} "
                    "was not found. Ensure the path is correct."
                )
            except PermissionError:
                raise PermissionError(
                    f"Access denied to {B}'{file_path}'{RS}."
                    " Check read permissions."
                )
            except IsADirectoryError:
                raise IsADirectoryError(
                    f"{B}'{file_path}'{RS} is a directory. "
                    "A valid configuration file path is required."
                )
