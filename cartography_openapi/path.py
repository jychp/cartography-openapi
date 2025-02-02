import re
from typing import Any

from loguru import logger


class Path:
    # DOC
    def __init__(self, path: str, get_method: dict[str, Any]) -> None:
        self.path = path
        self.path_params: dict[str, Any] = {}
        self.body_params: dict[str, Any] = {}
        self.query_params: dict[str, Any] = {}
        self.returns_array: bool = False
        self.returned_component: str | None = None
        self._from_method(get_method)

    def _from_method(self, method: dict[str, Any]) -> None:
        if '200' not in method.get('responses', {}):
            logger.debug(f'Skipping, no 200 response found for {self.path}')
            return

        response_schema = method['responses']['200'].get(
            'content', {},
        ).get('application/json', {}).get('schema')
        if not response_schema:
            logger.debug(f'Skipping, no response schema found for {self.path}')
            return

        if response_schema.get('type') == 'array':
            self.returns_array = True
            component_name = response_schema.get('items').get('$ref')
        else:
            component_name = response_schema.get('$ref')

        if not component_name:
            logger.debug(f'Skipping, no component name found for {self.path}')
            return
        self.returned_component = component_name.split('/')[-1]

        for param in method.get('parameters', []):
            if param['in'] == 'path':
                self.path_params[param['name']] = param
            elif param['in'] == 'body':
                self.body_params[param['name']] = param
            elif param['in'] == 'query':
                self.query_params[param['name']] = param
            else:
                logger.warning(f"Unknown parameter type {param['in']} for {param['name']} in {self.path}")

        # Sometimes the path parameters are not in the response schema
        if len(self.path_params) == 0:
            for m in re.findall(r'{[a-zA-Z-_0-9]+}', self.path):
                self.path_params[m[1:-1]] = {}

    def is_sub_path(self, other: 'Path', max_args: int = 0) -> bool:
        # DOC
        if not self.path.startswith(other.path):
            return False
        missing_args = [p for p in self.path_params if p not in other.path_params]
        return len(missing_args) <= max_args
