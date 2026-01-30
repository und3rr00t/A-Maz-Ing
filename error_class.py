import os


R = "\033[31m"
G = "\033[32m"
Y = "\033[33m"
B = "\033[34m"
C = "\033[36m"
RS = "\033[0m"


class ConfigError(Exception):
    """Base class for configuration errors."""
    def __init__(self, message: str = "Config file incorrect") -> None:
        super().__init__(message)


class ConfigSyntaxError(ConfigError):
    def __init__(self, message: str = "Syntax is incorrect") -> None:
        syntax_guide = ConfigSyntaxError.get_correct_syntax()
        full_msg = (
            f"{message}\n"
            f"{B}Correct syntax guide:{RS}\n{syntax_guide}"
        )
        super().__init__(full_msg)

    @staticmethod
    def get_correct_syntax() -> str:
        try:
            with open("example.txt", "r") as file:
                return file.read()
        except (FileNotFoundError, PermissionError, IsADirectoryError):
            return f"{B}KEY=VALUE{RS} (one pair per line)"


class ConfigKeyError(ConfigError):
    def __init__(self, key_info: str = "Invalid key") -> None:
        req = ", ".join(ConfigKeyError.get_required_keys())
        add = ", ".join(ConfigKeyError.get_additional_keys())
        full_msg = (
            f"{key_info}\n"
            f"{B}Mandatory keys:{RS} {req}\n"
            f"{B}Optional keys: {RS} {add}"
        )
        super().__init__(full_msg)

    @staticmethod
    def get_required_keys() -> tuple[str, ...]:
        return ("WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT")

    @staticmethod
    def get_additional_keys() -> tuple[str, ...]:
        return ("SEED", "DISPLAY_MOD", "ALGORITHM")


class ConfigValueError(ConfigError):
    def __init__(self, message: str = "Value out of range or invalid") -> None:
        super().__init__(message)


def report_error(error: Exception) -> None:
    """Print a standardized diagnostic report for any caught exception."""
    tb = error.__traceback__

    error_name = f"{R}{error.__class__.__name__}{RS}"
    print(f"\n{error_name}: {error}")

    if not tb:
        return

    while tb.tb_next:
        tb = tb.tb_next

    line_number = tb.tb_lineno
    file_path = tb.tb_frame.f_code.co_filename
    file_name = os.path.basename(file_path)

    print(
        f"{B}Location{RS} -> [File: {file_name} | Line: {line_number}]"
    )
    print("-" * 50)
