R = "\033[31m"
B = "\033[34m"
RS = "\033[0m"


class ConfigError(Exception):
    def __init__(self, message: str = "Config file is incorrect") -> None:
        super().__init__(f"{R}ConfigError{RS}: {message}")


class ConfigSyntaxError(ConfigError):
    def __init__(self, message: str = "Syntax is incorrect") -> None:
        full_msg = (
            f"{R}ConfigSyntaxError{RS}: {message}\n"
            "Correct syntax:\n"
            f"{B}{ConfigSyntaxError.get_correct_syntax()}{RS}"
        )
        super().__init__(full_msg)

    @staticmethod
    def get_correct_syntax() -> str:
        try:
            with open("example.txt", "r") as file:
                return file.read()
        except (FileNotFoundError, PermissionError, IsADirectoryError):
            return "KEY=VALUE"


class ConfigKeyError(ConfigError):
    def __init__(self, key_info: str = "Key is incorrect") -> None:
        full_msg = (
            f"{R}ConfigKeyError{RS}: {key_info}\n"
            f"Required keys: {B}{ConfigKeyError.get_required_keys()}{RS}."
        )
        super().__init__(full_msg)

    @staticmethod
    def get_required_keys() -> tuple[str, ...]:
        return (
            "WIDTH", "HEIGHT",
            "OUTPUT_FILE", "PERFECT",
        )


class ConfigValueError(ConfigError):
    def __init__(self, message: str = "Value is incorrect") -> None:
        super().__init__(f"{R}ConfigValueError{RS}: {message}")


def report_error(error: Exception) -> None:
    """Print a standardized diagnostic report for any caught exception."""

    tb = error.__traceback__

    print(f"{R}{error.__class__.__name__}{RS}: {error}")

    if not tb:
        return
    while tb.tb_next:
        tb = tb.tb_next

    line_number = tb.tb_lineno
    full_path = tb.tb_frame.f_code.co_filename
    file_name = full_path.split('/')[-1]
    if file_name == full_path:
        file_name = full_path.split('\\')[-1]

    print(
        f"{B}Location{RS} - Line: {line_number} | File: {file_name}",
        end="\n\n"
    )
