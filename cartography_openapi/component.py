import re
from collections import OrderedDict
from typing import Any

from loguru import logger

from cartography_openapi.path import Path


class Component:
    """Represents a component of the OpenAPI schema.

    The component is a part of the OpenAPI schema that defines a reusable schema object.
    This class is used to store the properties of the component and the relations between components.
    Relations are guessed by looking at the paths that return the linked component.

    See: https://swagger.io/specification/#components-object

    Args:
        name (str): The name of the component.

    Attributes:
        name (str): The name of the component.
        properties (OrderedDict[str, dict[str, Any]]): The properties of the component.
        relations (OrderedDict[str, dict[str, Any]]): The relations of the component
            (properties that return an other component).
        direct_path (Path): The direct path of the component.
        enumeration_path (Path): The enumeration path of the component.
        parent_component (Component): The parent component of the component.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.properties: OrderedDict[str, dict[str, Any]] = OrderedDict()
        self.relations: OrderedDict[str, dict[str, Any]] = OrderedDict()
        self.direct_path: Path | None = None
        self.enumeration_path: Path | None = None
        self.parent_component: "Component" | None = None

    @property
    def path_id(self) -> str:
        """Returns the parameter to use in the path to identify the component.

        This method returns the parameter to use in the path to identify the component.
        The parameter is the first parameter that is in the direct path but not in the enumeration path.

        Example:
            If the direct path is '/groups/{group_id}' and the enumeration path is '/groups',
            the method will return 'group_id'.

        Raises:
            ValueError: If the direct path or the enumeration path is not set.

        Returns:
            str: The parameter to use in the path to identify the component.
        """
        if self.direct_path is None or self.enumeration_path is None:
            raise ValueError("Paths not set")
        for p in self.direct_path.path_params:
            if p not in self.enumeration_path.path_params:
                return p
        return "<UNK>"

    def from_schema(self, schema: dict[str, Any]) -> bool:
        """Parse the schema of the component.

        This method parses the schema of the component.
        The method will return False if the schema is not an object.

        Args:
            schema (dict[str, Any]): The schema of the component.

        Returns:
            bool: True if the schema has been parsed, False otherwise.
        """
        if schema.get("type", "object") != "object":
            logger.debug(
                f"Parsing of non-object components not yet implemented ({self.name})"
            )
            return False

        for prop_name, prop_details in schema.get("properties", {}).items():
            parsed_property: dict[str, Any] = {
                "name": prop_name,
                "is_array": False,
                "type": "string",
                "clean_name": self._name_to_field(prop_name),
            }
            if prop_details.get("$ref") is not None:
                linked_component = prop_details["$ref"].split("/")[-1]
                self.relations[prop_name] = {
                    "name": prop_name,
                    "linked_component": linked_component,
                    "clean_name": self._name_to_field(prop_name),
                }
            else:
                parsed_property["type"] = prop_details.get("type", "string")
                self.properties[prop_name] = parsed_property
        return True

    def _name_to_field(self, name: str) -> str:
        # Replace consecutive uppercase by a single uppercase
        local_name = re.sub(r"([A-Z]+)", lambda m: m.group(1).capitalize(), name)
        # Replace camelCase by snake_case
        local_name = local_name[0].lower() + "".join(
            ["_" + c.lower() if c.isupper() else c for c in local_name[1:]]
        )
        return local_name

    def set_enumeration_path(self, path: Path, components: list["Component"]) -> bool:
        """Set the enumeration path of the component.

        The enumeration path is the path that is used to list all the components of the same type.
        The method will set the enumeration path if the new path is better than the previous one.
        Path evaluation is based on the following criteria:
        - No previous path
        - Linkable vs non-linkable (the path is a sub-path of the direct path of another component)
        - The new path is better because it has less parameters
        - The new path is better because it is shorter (allow to prefer x/groups over x/groups-default)

        Args:
            path (Path): The path to set as the enumeration path.

        Returns:
            bool: True if the path has been set as the enumeration path, False otherwise.
        """
        # Option 1: No previous path
        if self.enumeration_path is None:
            self.enumeration_path = path
            logger.debug(
                f"Enumeration path set to '{path.path}' for {self.name} [no previous path]"
            )
            return True
        # Option 2: Linkable vs non-linkable
        is_self_linkable = False
        is_other_linkable = False
        for c in components:
            if not c.direct_path:
                continue
            if self.enumeration_path.is_sub_path_of(c.direct_path):
                is_self_linkable = True
            if path.is_sub_path_of(c.direct_path):
                is_other_linkable = True
        if is_other_linkable and not is_self_linkable:
            self.enumeration_path = path
            logger.debug(
                f"Enumeration path set to '{path.path}' for {self.name} [linkable]"
            )
            return True
        if is_self_linkable and not is_other_linkable:
            return False
        # Option 3: The new path is better than the previous one because it has less parameters
        if len(self.enumeration_path.path_params) > len(path.path_params):
            self.enumeration_path = path
            logger.debug(
                f"Enumeration path set to '{path.path}' for {self.name} [less parameters]"
            )
            return True
        # Option 4: The new path is better because it is shorted (allow to prefer x/groups over x/groups-default)
        if len(self.enumeration_path.path) > len(path.path):
            self.enumeration_path = path
            logger.debug(
                f"Enumeration path set to '{path.path}' for {self.name} [shorter path]"
            )
            return True
        return False

    def set_direct_path(self, path: Path, components: list["Component"]) -> bool:
        """Set the direct path of the component.

        The direct path is the path that is used to get a single component.
        The method will set the direct path if the new path is better than the previous one.
        Path evaluation is based on the following criteria:
        - No previous path
        - Linkable vs non-linkable (the path is a sub-path of the direct path of another component)
        - The new path is better because it has less parameters
        - The new path is better because it is shorter (allow to prefer x/groups/y over x/groups-default/y)

        Args:
            path (Path): The path to set as the direct path.

        Returns:
            bool: True if the path has been set as the direct path, False otherwise.
        """
        # Option 1: No previous path
        if self.direct_path is None:
            self.direct_path = path
            logger.debug(
                f"Direct path set to '{path.path}' for {self.name} [no previous path]"
            )
            return True
        # Option 2: Linkable vs non-linkable
        is_self_linkable = False
        is_other_linkable = False
        for c in components:
            if not c.direct_path:
                continue
            if self.direct_path.is_sub_path_of(c.direct_path, 1):
                is_self_linkable = True
            if path.is_sub_path_of(c.direct_path, 1):
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
            logger.debug(
                f"Direct path set to '{path.path}' for {self.name} [less parameters]"
            )
            return True
        # Option 4: The new path is better because it is shorted (allow to prefer x/groups over x/groups-default)
        if len(self.direct_path.path) > len(path.path):
            self.direct_path = path
            logger.debug(
                f"Direct path set to '{path.path}' for {self.name} [shorter path]"
            )
            return True
        return False

    def __repr__(self) -> str:
        return f"<Component {self.name}>"
