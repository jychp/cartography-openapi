import re
from collections import OrderedDict
from typing import Any

from loguru import logger

from cartography_openapi.path import Path


class Component:
    # DOC
    def __init__(self, name: str, schema: dict[str, Any]) -> None:
        self.name = name
        self.properties: OrderedDict[str, dict[str, Any]] = OrderedDict()
        self.relations: OrderedDict[str, dict[str, Any]] = OrderedDict()
        self._from_schema(schema)
        self.direct_path: Path | None = None
        self.enumeration_path: Path | None = None
        self.parent_component: 'Component' | None = None

    @property
    def path_id(self) -> str:
        # DOC
        if self.direct_path is None or self.enumeration_path is None:
            raise ValueError('Paths not set')
        for p in self.direct_path.path_params:
            if p not in self.enumeration_path.path_params:
                return p
        return '<UNK>'

    def _from_schema(self, schema: dict[str, Any]) -> None:
        if schema.get('type', 'object') != 'object':
            logger.warning(f'Parsing of non-object components not yet implemented ({self.name})')
            return

        for prop_name, prop_details in schema.get('properties', {}).items():
            parsed_property: dict[str, Any] = {
                'name': prop_name,
                'is_array': False,
                'type': 'string',
                'clean_name': self._name_to_field(prop_name),
            }
            if prop_details.get('$ref') is not None:
                linked_component = prop_details['$ref'].split('/')[-1]
                self.relations[prop_name] = {
                    'name': prop_name,
                    'linked_component': linked_component,
                    'clean_name': self._name_to_field(prop_name),
                }
            else:
                parsed_property['type'] = prop_details.get('type', 'string')
                self.properties[prop_name] = parsed_property

    def _name_to_field(self, name: str) -> str:
        # DOC
        # Replace consecutive uppercase by a single uppercase
        local_name = re.sub(r'([A-Z]+)', lambda m: m.group(1).capitalize(), name)
        # Replace camelCase by snake_case
        local_name = local_name[0].lower() + ''.join(['_' + c.lower() if c.isupper() else c for c in local_name[1:]])
        return local_name

    def set_enumeration_path(self, path: Path, components: list['Component']) -> bool:
        # DOC
        # Option 1: No previous path
        if self.enumeration_path is None:
            self.enumeration_path = path
            logger.debug(f"Enumeration path set to '{path.path}' for {self.name} [no previous path]")
            return True
        # Option 2: Linkable vs non-linkable
        is_self_linkable = False
        is_other_linkable = False
        for c in components:
            if not c.direct_path:
                continue
            if self.enumeration_path.is_sub_path(c.direct_path):
                is_self_linkable = True
            if path.is_sub_path(c.direct_path):
                is_other_linkable = True
        if is_other_linkable and not is_self_linkable:
            self.enumeration_path = path
            logger.debug(f"Enumeration path set to '{path.path}' for {self.name} [linkable]")
            return True
        if is_self_linkable and not is_other_linkable:
            return False
        # Option 3: The new path is better than the previous one because it has less parameters
        if len(self.enumeration_path.path_params) > len(path.path_params):
            self.enumeration_path = path
            logger.debug(f"Enumeration path set to '{path.path}' for {self.name} [less parameters]")
            return True
        # Option 4: The new path is better because it is shorted (allow to prefer x/groups over x/groups-default)
        if len(self.enumeration_path.path) > len(path.path):
            self.enumeration_path = path
            logger.debug(f"Enumeration path set to '{path.path}' for {self.name} [shorter path]")
            return True
        return False

    def set_direct_path(self, path: Path, components: list['Component']) -> bool:
        # DOC
        # Option 1: No previous path
        if self.direct_path is None:
            self.direct_path = path
            logger.debug(f"Direct path set to '{path.path}' for {self.name} [no previous path]")
            return True
        # Option 2: Linkable vs non-linkable
        is_self_linkable = False
        is_other_linkable = False
        for c in components:
            if not c.direct_path:
                continue
            if self.direct_path.is_sub_path(c.direct_path, 1):
                is_self_linkable = True
            if path.is_sub_path(c.direct_path, 1):
                is_other_linkable = True
        if is_other_linkable and not is_self_linkable:
            self.direct_path = path
            logger.debug(f"Direct path set to '{path.path}' for {self.name} [linkable]")
            return True
        if is_self_linkable and not is_other_linkable:
            return False
        # Option 3: The new path is better than the previous one because it has less parameters
        if len(self.direct_path.path_params) > len(path.path_params):
            self.direct_path = path
            logger.debug(f"Direct path set to '{path.path}' for {self.name} [less parameters]")
            return True
        # Option 4: The new path is better because it is shorted (allow to prefer x/groups over x/groups-default)
        if len(self.direct_path.path) > len(path.path):
            self.direct_path = path
            logger.debug(f"Direct path set to '{path.path}' for {self.name} [shorter path]")
            return True
        return False
