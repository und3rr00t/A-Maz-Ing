import os


R = "\033[31m"
G = "\033[32m"
Y = "\033[33m"
B = "\033[34m"
C = "\033[36m"
RS = "\033[0m"


class ConfigError(Exception):
    """
    Base class for all configuration-related exceptions.\n

    Args:
        message (str):
            The error message to display.
            Defaults to "Config file incorrect".\n
    """
    def __init__(self, message: str = "Config file incorrect") -> None:
        super().__init__(message)


class ConfigSyntaxError(ConfigError):
    """
    Raised when the format of the configuration file is invalid.\n

    This exception provides a syntax guide to help the user format the
    configuration file correctly.\n

    Args:
        message (str): The error message. Defaults to "Syntax is incorrect".\n
    """
    def __init__(self, message: str = "Syntax is incorrect") -> None:
        syntax_guide = ConfigSyntaxError.get_correct_syntax()
        full_msg = (
            f"{message}\n"
            f"{B}Correct syntax guide:{RS}\n{syntax_guide}"
        )
        super().__init__(full_msg)

    @staticmethod
    def get_correct_syntax() -> str:
        """
        Retrieves syntax rules from a default string.\n

        Returns:
            str: A string describing the expected KEY=VALUE syntax.\n
        """
        return f"{B}KEY=VALUE{RS} (one pair per line)"


class ConfigKeyError(ConfigError):
    """
    Raised when mandatory keys are missing or invalid keys are provided.\n

    Args:
        key_info (str):
            Details about the specific key error. Defaults to "Invalid key".
    """
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
        """
        Returns the list of keys that must be present in the config.\n

        Returns:
            tuple[str, ...]: Mandatory configuration keys.\n
        """
        return ("WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT")

    @staticmethod
    def get_additional_keys() -> tuple[str, ...]:
        """
        Returns the list of optional configuration keys.\n

        Returns:
            tuple[str, ...]: Optional configuration keys.\n
        """
        return ("SEED", "ALGORITHM")


class ConfigValueError(ConfigError):
    """
    Raised when a configuration value is of wrong type or out of bounds.\n

    Args:
        message (str):
            The error message. Defaults to "Value out of range or invalid".\n
    """
    def __init__(self, message: str = "Value out of range or invalid") -> None:
        super().__init__(message)


def report_error(error: Exception) -> None:
    """
    Prints a standardized diagnostic report including error type
    and location.\n

    This function extracts traceback information to point the user to the
    exact file and line number where the exception occurred.\n

    Args:
        error (Exception): The caught exception to be reported.\n

    Returns:
        None\n
    """
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
