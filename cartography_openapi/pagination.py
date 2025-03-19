from typing import TYPE_CHECKING

from loguru import logger

from cartography_openapi.checklist import Checklist

if TYPE_CHECKING:
    from src.cartography_openapi.path import Path


class Pagination:
    """Handles the pagination of a path.

    The Pagination class is used to handle the pagination of a path.
    It looks for the pagination parameters in the path and generates the parameters to use in the request.

    Args:
        path (Path): The path to handle the pagination.

    Attributes:
        path (Path): The path to handle the pagination.
        _offset (str): The offset parameter.
        _limit (str): The limit parameter.
        _page (str): The page parameter.
        _configured (bool): True if the pagination is configured, False otherwise

    Constants:
        OFFSET_PARAMS (list[str]): The list of offset parameters to look for.
        LIMIT_PARAMS (list[str]): The list of limit parameters to look for.
        PAGE_PARAMS (list[str]): The list of page parameters to look for.
        DEFAULT_OFFSET (int): The default offset value (0).
        DEFAULT_PAGE (int): The default page value (1).
        DEFAULT_LIMIT (int): The default limit value (25).
    """

    OFFSET_PARAMS = ["offset", "first"]
    LIMIT_PARAMS = ["limit", "per_page", "max", "size"]
    PAGE_PARAMS = ["page", "current_page"]
    DEFAULT_OFFSET = 0
    DEFAULT_PAGE = 1
    DEFAULT_LIMIT = 25

    def __init__(self, path: "Path") -> None:
        self._path = path
        self._offset: str | None = None
        self._limit: str | None = None
        self._page: str | None = None
        self._configured: bool = False

        for k in self.OFFSET_PARAMS:
            if k in path.query_params:
                self._offset = k
                break

        for k in self.LIMIT_PARAMS:
            if k in path.query_params:
                self._limit = k
                break

        for k in self.PAGE_PARAMS:
            if k in path.query_params:
                self._page = k
                break

        if not self._offset and not self._limit:
            Checklist().add_warning(
                f"No pagination parameters found for path {self._path.path},"
                "pagination might be missing",
            )
        elif self._offset and self._limit and self._page:
            Checklist().add_warning(
                f"Ambigous pagination parameters found for path {self._path.path},"
                "please check the parameters",
            )
        elif self._limit is None:
            Checklist().add_warning(
                f"Missing limit parameter for path {self._path.path}, pagination might be missing"
            )
        elif self._offset:
            logger.debug(
                f"Found pagination ({self._offset},{self._limit}) for path {self._path.path}"
            )
            self._configured = True
        else:
            logger.debug(
                f"Found pagination ({self._page},{self._limit}) for path {self._path.path}"
            )
            self._configured = True

    @property
    def params(self) -> dict[str, int]:
        """Returns the parameters to use in the request.

        This method returns the parameters to use in the request.
        If the pagination is not configured, an empty dictionary is returned.
        else, the dictionary contains the offset, page or limit parameter with their default value.

        Example:
            {'offset': 0, 'limit': 25}

        Returns:
            dict[str, int]: The parameters to use in the request.
        """
        params: dict[str, int] = {}
        if not self._configured:
            return params
        if self._offset:
            params[self._offset] = self.DEFAULT_OFFSET
        elif self._page:
            params[self._page] = self.DEFAULT_PAGE
        if self._limit:
            params[self._limit] = self.DEFAULT_LIMIT
        return params

    @property
    def increment_instruction(self) -> str:
        """Returns the instruction to increment the pagination.

        This method returns the python instruction to increment the pagination.
        If the pagination is not configured, the instruction is 'break' to avoid infinite loops.

        Example:
        If the offset parameter is set, the instruction is 'params['offset'] += 25'.

        Returns:
            str: The instruction to increment the pagination.
        """
        instruction: str = (
            "break"  # For safety reasons we return break to avoid infinite loops
        )
        if not self._configured:
            return instruction
        if self._offset:
            instruction = f"params['{self._offset}'] += len(sub_results)"
        elif self._page:
            instruction = f"params['{self._page}'] += 1"
        return instruction

    @classmethod
    def current_params(cls) -> list[str]:
        """Returns the list of current parameters to look for.

        This method returns the list of current parameters to look for in the path.

        Returns:
            list[str]: The list of current parameters to look for
        """
        return cls.OFFSET_PARAMS + cls.LIMIT_PARAMS + cls.PAGE_PARAMS
