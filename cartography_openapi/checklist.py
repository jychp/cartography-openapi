from loguru import logger


class SingletonMeta(type):
    _instances: dict['SingletonMeta', 'SingletonMeta'] = {}

    def __call__(cls, *args, **kwargs) -> 'SingletonMeta':
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Checklist(metaclass=SingletonMeta):
    # DOC
    def __init__(self) -> None:
        self.checklist: list[str] = []

    def add_warning(self, warning: str) -> None:
        # DOC
        self.checklist.append(warning)
        logger.warning(warning)
