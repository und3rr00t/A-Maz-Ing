from error_class import ConfigSyntaxError, ConfigKeyError, ConfigValueError
import random

B = "\033[34m"
RS = "\033[0m"


class Maze:
    def __init__(self, config_file: str):
        config = self.MazeConfig.parsing_conf(config_file)
        self.width = config["WIDTH"]
        self.height = config["HEIGHT"]
        self.output_file = config["OUTPUT_FILE"]
        self.perfection = config["PERFECT"]
##############################################
        if "SEED" in config:
            self.seed = config["SEED"]
            explicit_seed = True
        else:
            self.seed = random.randint(0, 10**20)
            explicit_seed = False
        random.seed(self.seed)
        if explicit_seed or ("ENTRY" not in config or "EXIT" not in config):
            self.entry = self._generate_random_gate()
            self.exit = self._generate_random_gate(exclude=self.entry)
        else:
            self.entry = config["ENTRY"]
            self.exit = config["EXIT"]

    def _generate_random_gate(self, exclude=None):
        """Pick a random coordinate on the maze border."""
        w, h = self.width, self.height

        border_cells = []

        for x in range(w):
            border_cells.append((x, 0))
            border_cells.append((x, h - 1))

        for y in range(1, h - 1):
            border_cells.append((0, y))
            border_cells.append((w - 1, y))

        if exclude and exclude in border_cells:
            border_cells.remove(exclude)

        return random.choice(border_cells)
#######################################

    class MazeConfig:
        @staticmethod
        def parsing_value(config: dict) -> dict:
            # parse seed
            if "SEED" in config:
                try:
                    config["SEED"] = int(config["SEED"])
                except ValueError:
                    raise ConfigValueError(f"{B}SEED{RS} must be an integer")

            try:
                config["WIDTH"] = int(config["WIDTH"])
                config["HEIGHT"] = int(config["HEIGHT"])
                if config["WIDTH"] < 0 or config["HEIGHT"] < 0:
                    raise ConfigValueError(
                        f"{B}WIDTH{RS} and {B}HEIGHT{RS} cannot be negative"
                    )
                if config["WIDTH"] * config["HEIGHT"] < 2:
                    raise ConfigValueError(
                        "Maze connot be less 2 cells"
                    )
            except (ValueError):
                raise ConfigValueError(
                    f"{B}WIDTH & HEIGHT & SEED{RS} must be integers"
                )

            for key in ("ENTRY", "EXIT"):
                if key in config:
                    val = config[key]
                    if ',' not in val or ',,' in val:
                        raise ConfigValueError(
                            f"{B}{key}{RS} should be x,y' and without spaces."
                        )

                    try:
                        x, y = map(int, val.split(',', 1))
                        if x < 0 or y < 0:
                            raise ConfigValueError(
                                f"{B}{key}{RS} coordinates cannot be negative"
                            )
                        if x >= config["WIDTH"] or y >= config["HEIGHT"]:
                            raise ConfigValueError(
                                f"{B}{key}{RS} coordinates "
                                "cannot be larger than the "
                                "dimensions of the maze"
                            )
                        config[key] = (x, y)
                    except ValueError:
                        raise ConfigValueError(
                            f"{B}{key}{RS} coordinates must be integers"
                        )

            perf = config["PERFECT"].strip().capitalize()
            if perf not in ("True", "False"):
                raise ConfigValueError(
                        f"{B}PERFECT{RS} must be 'True' or 'False'"
                )
            config["PERFECT"] = (perf == "True")

            return config

        @staticmethod
        def parsing_conf(file_path: str) -> dict:
            req_keys = list(ConfigKeyError.get_required_keys())
            valid_keys = req_keys + ["SEED", "ENTRY", "EXIT"]
            config = {}

            try:
                with open(file_path, "r") as file:
                    for i, line in enumerate(file, 1):
                        line = line.strip()
                        if not line or line.startswith('#'):
                            continue

                        if line.count('=') != 1:
                            raise ConfigSyntaxError(
                                f"{B}In line {i}{RS} invalid format"
                            )

                        key, value = map(str.strip, line.split('='))

                        if key not in valid_keys:
                            raise ConfigKeyError(
                                f"{B}Key '{key}'{RS} at {B}line {i}{RS}"
                            )

                        config[key] = value
                        if key in req_keys:
                            req_keys.remove(key)

                if req_keys:
                    raise ConfigKeyError(f"Missing keys: {B}{req_keys}{RS}")

                return Maze.MazeConfig.parsing_value(config)

            except FileNotFoundError:
                raise FileNotFoundError(
                    f"Config {B}'{file_path}'{RS} not found"
                )
            except PermissionError:
                raise PermissionError(
                    f"The Config file {B}'{file_path}'{RS} "
                    "does not have read permissions."
                )
            except IsADirectoryError:
                raise IsADirectoryError(
                    f"{B}'{file_path}'{RS} is a directory not file to read"
                )
