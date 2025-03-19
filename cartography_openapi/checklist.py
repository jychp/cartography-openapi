from loguru import logger


class SingletonMeta(type):
    _instances: dict["SingletonMeta", "SingletonMeta"] = {}

    def __call__(cls, *args, **kwargs) -> "SingletonMeta":
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Checklist(metaclass=SingletonMeta):
    """List of warnings generated during the parsing of the OpenAPI spec.

    The Checklist class is used to store the warnings generated during the parsing of the OpenAPI spec.
    The checklist is a singleton, so there is only one instance of it.

    Attributes:
        checklist (list[str]): The list of warnings.
    """

    def __init__(self) -> None:
        self.checklist: list[str] = []

    def add_warning(self, warning: str) -> None:
        """Adds a warning to the checklist.

        This method adds a warning to the checklist.
        A WARNING log is also generated.

        Args:
            warning (str): The warning to add.
        """
        self.checklist.append(warning)
        logger.warning(warning)
