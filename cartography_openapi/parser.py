import json
from typing import Any

from loguru import logger

from cartography_openapi.component import Component
from cartography_openapi.entity import Entity
from cartography_openapi.module import Module
from cartography_openapi.path import Path


class OpenAPIParser:
    # DOC
    def __init__(
            self, name: str,
            url: str | None = None,
            file: str | None = None,
            ignored_path: list[str] | None = None,
    ) -> None:
        self.name = name
        self.checklist: list[str] = []
        self.module = Module(name)
        self.components: dict[str, Component] = {}
        self.component_to_paths: dict[str, list[Path]] = {}
        self._ignore_paths: list[str] = []
        self._ignore_partial_paths: list[str] = []
        if ignored_path is not None:
            for path in ignored_path:
                if path.endswith('*'):
                    self._ignore_partial_paths.append(path[:-1])
                else:
                    self._ignore_paths.append(path)
        if file:
            self._load(file)
        elif url:
            self._download(url)

    def _download(self, url: str) -> None:
        # TODO: Download the OpenAPI spec from the URL
        raise NotImplementedError('Not implemented')

    def _load(self, file_path: str) -> None:
        try:
            with open(file_path, encoding='utf-8') as f:
                raw_data = json.load(f)
        except FileNotFoundError:
            logger.error(f"File '{file_path}' not found.")
            return
        self._parse(raw_data)

    def _parse(self, raw_data: dict[str, Any]) -> None:
        # Search for server
        servers = raw_data.get('servers')
        if not servers:
            logger.warning('No servers found in the OpenAPI spec')
            self.checklist.append(
                'No servers found in the OpenAPI spec, edit the `intel/*.py` files to add the server URL.',
            )
            self.module.server_url = 'https://localhost'
        else:
            if len(servers) > 1:
                logger.warning('Multiple servers found in the OpenAPI spec. Using the first one.')
                self.checklist.append(
                    'Multiple servers found in the OpenAPI spec. Check `intel/*.py` files.',
                )
            self.module.server_url = servers[0].get('url')

        # Create components
        components = raw_data.get('components', {}).get('schemas', {})
        for component_name, component_schema in components.items():
            self.components[component_name] = Component(component_name, component_schema)

        # Create paths
        paths = raw_data.get('paths', {})

        for path, methods in paths.items():
            if path in self._ignore_paths:
                logger.debug(f'Skipping path {path} (ignored)')
                continue
            ignored_pattern = False
            for pattern in self._ignore_partial_paths:
                if path.startswith(pattern):
                    ignored_pattern = True
                    break
            if ignored_pattern:
                logger.debug(f'Skipping path {path} (ignored pattern)')
                continue
            if 'get' not in methods:
                logger.debug(f'Skipping, no GET method found for {path}')
                continue
            get_method = methods['get']
            path_obj = Path(path, get_method)
            if path_obj.returned_component is not None:
                if path_obj.returned_component not in self.component_to_paths:
                    self.component_to_paths[path_obj.returned_component] = []
                self.component_to_paths[path_obj.returned_component].append(path_obj)

        logger.info(
            'OpenAPI spec parsed successfully, found {} resolvable components.'.format(
                len(self.component_to_paths),
            ),
        )

    def build_models(self, **kwargs) -> bool:
        # DOC
        consolidated_components: list[Component] = []

        for component_name, entity_name in kwargs.items():
            logger.info(f'Building model for {component_name} as {entity_name}')
            # Get the schema
            component = self.components.get(component_name)
            if not component:
                logger.error(f'No component found for {component_name}')
                continue

            # Get the paths
            paths = self.component_to_paths.get(component_name, [])
            if not paths:
                logger.error(f'No path found for {component_name}')
                continue

            logger.debug(f'Processing {component_name} paths ({entity_name})')
            for path in paths:
                if path.returns_array:
                    component.set_enumeration_path(path, consolidated_components)
                else:
                    component.set_direct_path(path, consolidated_components)

            # Find the parent component
            if component.direct_path is not None:
                for c in consolidated_components:
                    if c.direct_path is None:
                        continue
                    if component.direct_path.is_sub_path(c.direct_path, 1):
                        component.parent_component = c
                        logger.debug(f'Parent component for {component_name}: {component.parent_component.name}')
                        break
            if component.parent_component is None:
                logger.debug(f'No parent component found for {component_name}')

            consolidated_components.append(component)

        for component in consolidated_components:
            entity = Entity(self.module, kwargs[component.name], component.name)
            entity.build_from_component(component, consolidated_components)
            self.module.add_entity(entity)

        return True

    def export(self, output_dir: str) -> None:
        # DOC
        self.module.export(output_dir)
