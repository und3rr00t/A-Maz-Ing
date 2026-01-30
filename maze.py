import time
from typing import Dict
from error_class import (
    ConfigSyntaxError, ConfigKeyError, ConfigValueError, B, RS
)


class Maze:
    def __init__(self, config_file: str):
        config = self.MazeParseConfig.parsing_conf(config_file)
        self.width = config["WIDTH"]
        self.height = config["HEIGHT"]
        self.entry = config["ENTRY"]
        self.exit = config["EXIT"]
        self.output_file = config["OUTPUT_FILE"]
        self.perfection = config["PERFECT"]
        self.seed = config["SEED"]
        self.d_mod = config["DISPLAY_MOD"]
        self.algo = config.get("ALGORITHM", "DFS").upper()

    class MazeParseConfig:
        @staticmethod
        def parsing_value(config: Dict) -> Dict:

            if "SEED" in config:
                if config["SEED"].isdigit():
                    config["SEED"] = int(config["SEED"])
            else:
                config["SEED"] = int(time.time())
            if "ALGORITHM" in config:
                config["ALGORITHM"] = config["ALGORITHM"].upper()
                if config["ALGORITHM"] not in ("DFS", "SIDEWINDER"):
                    config["ALGORITHM"] = "DFS"
            if "DISPLAY_MOD" in config:
                d_mod = config["DISPLAY_MOD"].capitalize()
                if d_mod not in ("Terminal", "Visualizer"):
                    raise ConfigValueError(
                        f"Invalid value '{d_mod}' for {B}DISPLAY_MOD{RS}. "
                        f"Expected {B}'Terminal'{RS} or {B}'Visualizer'{RS}."
                    )
                else:
                    config["DISPLAY_MOD"] = d_mod
            else:
                config["DISPLAY_MOD"] = "Visualizer"

            try:
                config["WIDTH"] = int(config["WIDTH"])
                config["HEIGHT"] = int(config["HEIGHT"])
            except ValueError:
                raise ConfigValueError(
                    f"{B}WIDTH, HEIGHT, and SEED{RS} must be valid integers."
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

            perf = config["PERFECT"].strip().capitalize()
            if perf not in ("True", "False"):
                raise ConfigValueError(
                    f"Invalid value '{perf}' for {B}PERFECT{RS}. "
                    f"Expected {B}'True'{RS} or {B}'False'{RS}."
                )
            config["PERFECT"] = (perf == "True")

            return config

        @staticmethod
        def parsing_conf(file_path: str) -> dict:

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
                                f"Syntax Error at {B}line {i}{RS} in "
                                "config file: Expected exactly one '=' "
                                f"operator (found {line.count('=')})"
                            )

                        key, value = map(str.strip, line.split('='))
                        key = key.upper()

                        if not value:
                            raise ConfigValueError(
                                f"Empty key {B}'{key}'{RS} value  at "
                                f"{B}line {i}{RS} in config file."
                            )
                        if key not in req_keys and key not in add_keys:
                            raise ConfigKeyError(
                                f"Unknown key {B}'{key}'{RS} at "
                                f"{B}line {i}{RS} in config file."
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
