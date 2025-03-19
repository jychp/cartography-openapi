import json
from typing import Any

import requests
from loguru import logger

from cartography_openapi.checklist import Checklist
from cartography_openapi.component import Component
from cartography_openapi.entity import Entity
from cartography_openapi.module import Module
from cartography_openapi.path import Path


class OpenAPIParser:
    """Parser for OpenAPI specs.

    The OpenAPIParser class is used to parse an OpenAPI spec and generate models from it.
    The parser can load the spec from a file or download it from a URL.
    Some paths can be ignored by providing a list of paths to ignore (eg. '/health*' or '/ping').

    Args:
        name (str): The name of the API (and of the new intel Module).
        url (str): The URL of the OpenAPI spec. (default: None)
        file (str): The path to the OpenAPI spec file. (default: None)
        ignored_path (list[str]): List of paths to ignore. (default: None)

    Raises:
        ValueError: If no file or URL is provided.

    Attributes:
        name (str): The name of the API.
        module (Module): The intel Module generated from the OpenAPI spec.
        components (dict[str, Component]): The components of the OpenAPI spec.
        component_to_paths (dict[str, list[Path]]): The paths that return a given component.
        _ignore_paths (list[str]): The paths to ignore.
        _ignore_partial_paths (list[str]): The partial paths to ignore.
        _ready (bool): True if the OpenAPI spec has been parsed successfully, False otherwise.
    """

    def __init__(
        self,
        name: str,
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
        self._ready = False
        if ignored_path is not None:
            for path in ignored_path:
                if path.endswith("*"):
                    self._ignore_partial_paths.append(path[:-1])
                else:
                    self._ignore_paths.append(path)
        if file:
            self._load(file)
        elif url:
            self._download(url)
        else:
            raise ValueError(
                "You must provide a file or a URL to load the OpenAPI spec"
            )

    def _download(self, url: str) -> None:
        try:
            req = requests.get(url, timeout=30)
            req.raise_for_status()
            raw_data = req.json()
        except requests.RequestException as e:
            logger.error(f"Failed to download the OpenAPI spec from {url}: {e}")
            return
        self._parse(raw_data)

    def _load(self, file_path: str) -> None:
        try:
            with open(file_path, encoding="utf-8") as f:
                raw_data = json.load(f)
        except FileNotFoundError:
            logger.error(f"File '{file_path}' not found.")
            return
        self._parse(raw_data)

    def _parse(self, raw_data: dict[str, Any]) -> None:
        # Search for server
        servers = raw_data.get("servers")
        if not servers:
            Checklist().add_warning(
                "No servers found in the OpenAPI spec,"
                "edit the `intel/*.py` files to add the server URL.",
            )
            self.module.server_url = "https://localhost"
        else:
            if len(servers) > 1:
                Checklist().add_warning(
                    "Multiple servers found in the OpenAPI spec. Check `intel/*.py` files."
                )
            self.module.server_url = servers[0].get("url")

        # Create components
        components = raw_data.get("components", {}).get("schemas", {})
        for component_name, component_schema in components.items():
            component = Component(component_name)
            if not component.from_schema(component_schema):
                continue
            self.components[component_name] = component

        # Create paths
        paths = raw_data.get("paths", {})

        for path, methods in paths.items():
            if path in self._ignore_paths:
                logger.debug(f"Skipping path {path} (ignored)")
                continue
            ignored_pattern = False
            for pattern in self._ignore_partial_paths:
                if path.startswith(pattern):
                    ignored_pattern = True
                    break
            if ignored_pattern:
                logger.debug(f"Skipping path {path} (ignored pattern)")
                continue
            if "get" not in methods:
                logger.debug(f"Skipping, no GET method found for {path}")
                continue
            get_method = methods["get"]
            path_obj = Path(path, get_method)
            if path_obj.returned_component is not None:
                if path_obj.returned_component not in self.component_to_paths:
                    self.component_to_paths[path_obj.returned_component] = []
                self.component_to_paths[path_obj.returned_component].append(path_obj)

        if len(self.components) == 0:
            logger.error("No components imported from the OpenAPI spec.")
            return

        self._ready = True
        logger.info(
            "OpenAPI spec parsed successfully, "
            f"found {len(self.component_to_paths)} resolvable components.",
        )

    def build_module(self, **kwargs) -> bool:
        """Build the cartography module from the ingested OpenAPI spec.

        This method builds the cartography module from the ingested OpenAPI spec.
        It creates the entities from the components and the paths.

        Args:
            **kwargs: The mapping between components and entities.

        Returns:
            bool: True if the module has been built successfully, False otherwise.
        """
        if not self._ready:
            logger.error("OpenAPI spec not ready, cannot build the module.")
            return False
        consolidated_components: list[Component] = []

        for component_name, entity_name in kwargs.items():
            logger.info(f"Building model for {component_name} as {entity_name}")
            # Get the schema
            component = self.components.get(component_name)
            if not component:
                logger.error(f"No component found for {component_name}")
                continue

            # Get the paths
            paths = self.component_to_paths.get(component_name, [])
            if not paths:
                logger.error(f"No path found for {component_name}")
                continue

            logger.debug(f"Processing {component_name} paths ({entity_name})")
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
                    if component.direct_path.is_sub_path_of(c.direct_path, 1):
                        component.parent_component = c
                        logger.debug(
                            f"Parent component for {component_name}: {component.parent_component.name}"
                        )
                        break
            if component.parent_component is None:
                logger.debug(f"No parent component found for {component_name}")

            consolidated_components.append(component)

        for component in consolidated_components:
            entity = Entity(self.module, kwargs[component.name], component.name)
            entity.build_from_component(component, consolidated_components)
            self.module.add_entity(entity)

        return True

    def export(self, output_dir: str) -> None:
        """Export the module to the output directory.

        see: cartography_openapi.module.Module.export

        Args:
            output_dir (str): The output directory.
        """
        if not self._ready:
            logger.error("OpenAPI spec not ready, cannot export the module.")
            return
        self.module.export(output_dir)
