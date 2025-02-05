from typing import TYPE_CHECKING

from loguru import logger

from cartography_openapi.checklist import Checklist

if TYPE_CHECKING:
    from src.cartography_openapi.path import Path


class Pagination:
    # DOC
    OFFSET_PARAMS = ['offset', 'first']
    LIMIT_PARAMS = ['limit', 'per_page', 'max', 'size']
    PAGE_PARAMS = ['page', 'current_page']

    def __init__(self, path: 'Path') -> None:
        self._path = path
        self._offset: str | None = None
        self._limit: str | None = None
        self._page: str | None = None

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
                f'No pagination parameters found for path {self._path.path},'
                'pagination might be missing',
            )
        elif self._offset and self._limit and self._page:
            Checklist().add_warning(
                f'Ambigous pagination parameters found for path {self._path.path},'
                'please check the parameters',
            )
        elif self._limit is None:
            Checklist().add_warning(f'Missing limit parameter for path {self._path.path}, pagination might be missing')
        elif self._offset:
            logger.debug(f'Found pagination ({self._offset},{self._limit}) for path {self._path.path}')
        else:
            logger.debug(f'Found pagination ({self._page},{self._limit}) for path {self._path.path}')

    @classmethod
    def current_params(cls) -> list[str]:
        return cls.OFFSET_PARAMS + cls.LIMIT_PARAMS + cls.PAGE_PARAMS
