import re
from collections import OrderedDict
from typing import Any, Iterable

from loguru import logger

from cartography_openapi.path import Path


class Field:
    """Represents a field of the OpenAPI schema.

    The field is a part of the OpenAPI schema that defines a property of a component.
    This class is used to store the properties of the field and the relations between fields.

    See: https://swagger.io/specification/#schema-object
    Args:
        name (str): The name of the field.
        clean_name (str): The clean name of the field (used as property in Cartography).

    Attributes:
        name (str): The name of the field.
        clean_name (str): The clean name of the field (used as property in Cartography).
        is_array (bool): True if the field is an array, False otherwise.
        description (str | None): The description of the field.
        example (str | None): The example of the field.
        type (str | None): The type of the field.
    """

    def __init__(self, name: str, clean_name: str) -> None:
        self.name = name
        self.clean_name = clean_name
        self.is_array: bool = False
        self.description: str | None = None
        self.example: str | None = None
        self.type: str | None = None

    def from_schema(self, schema: dict[str, Any]) -> bool:
        """Parse the schema of the field.
        This method parses the schema of the field.
        The method will return False if the schema cannot be parsed.

        Args:
            schema (dict[str, Any]): The schema of the field.
        Returns:
            bool: True if the schema has been parsed, False otherwise.
        """
        self.description = schema.get("description")
        self.example = schema.get("example", "CHANGEME")
        schema_type = schema.get("type")
        # Handle array of objects
        if schema_type == "array" and len(schema.get("items", {})) == 0:
            self.type = "string"
            self.is_array = True
            return True
        if schema.get("type") == "array":
            self.is_array = True
            schema_type = schema.get("items", {}).get("type", "unknown")
        self.type = schema_type
        # TODO: handle ref
        if schema_type == "$ref":
            return False
        # TODO: handle recursion
        if schema_type == "object":
            return False

        return True


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
        description (str | None): The description of the component.
        properties (OrderedDict[str, Field]): The properties of the component.
        relations (OrderedDict[str, dict[str, Any]]): The relations of the component
            (properties that return an other component).
        direct_path (Path): The direct path of the component.
        enumeration_path (Path): The enumeration path of the component.
        parent_component (Component): The parent component of the component.
    """

    FIELDS: dict[str, Field] = {}

    def __init__(self, name: str) -> None:
        self.name = name
        self.description: str | None = None
        self.properties: OrderedDict[str, Field] = OrderedDict()
        self.relations: OrderedDict[str, dict[str, Any]] = OrderedDict()
        self.direct_path: Path | None = None
        self.enumeration_path: Path | None = None
        self.parent_component: "Component" | None = None
        self._unresolved_ref: list[tuple[str, dict[str, Any]]] = []

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
        if self.direct_path is None:
            raise ValueError("Paths not set")
        for p in self.direct_path.path_params:
            if self.enumeration_path is None:
                return p
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
        self.description = schema.get("description")

        if "allOf" in schema:
            for sub_schema in schema["allOf"]:
                self.from_schema(sub_schema)
            return True

        if schema.get("type", "object") != "object":
            field = Field(self.name, self._name_to_field(self.name))
            if field.from_schema(schema):
                self.FIELDS[self.name] = field
                return True
            return False

        for prop_name, prop_details in schema.get("properties", {}).items():
            if prop_details.get("$ref") is not None:
                short_name = prop_details["$ref"].split("/")[-1]
                self.relations[prop_name] = {
                    "name": prop_name,
                    "linked_component": short_name,
                    "clean_name": self._name_to_field(prop_name),
                    "is_array": False,
                }
            elif (
                prop_details.get("type") == "array"
                and len(prop_details.get("items", {})) > 0
            ):
                if prop_details["items"].get("$ref") is not None:
                    short_name = prop_details["items"]["$ref"].split("/")[-1]
                    self.relations[prop_name] = {
                        "name": prop_name,
                        "linked_component": short_name,
                        "clean_name": self._name_to_field(prop_name),
                        "is_array": True,
                    }
            elif prop_details.get("type") == "object":
                for sub_prop_name, sub_prop_details in prop_details.get(
                    "properties", {}
                ).items():
                    field = Field(
                        f"{prop_name}.{sub_prop_name}",
                        f"{prop_name}_{self._name_to_field(sub_prop_name)}",
                    )
                    if field.from_schema(sub_prop_details):
                        self.properties[field.name] = field
            else:
                field = Field(prop_name, self._name_to_field(prop_name))
                if field.from_schema(prop_details):
                    self.properties[prop_name] = field

        return True

    def _name_to_field(self, name: str) -> str:
        # Replace consecutive uppercase by a single uppercase
        local_name = re.sub(r"([A-Z]+)", lambda m: m.group(1).capitalize(), name)
        # Replace camelCase by snake_case
        local_name = local_name[0].lower() + "".join(
            ["_" + c.lower() if c.isupper() else c for c in local_name[1:]]
        )
        return local_name

    def set_enumeration_path(
        self, path: Path, components: Iterable["Component"]
    ) -> bool:
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
            components (Iterable[Component]): The list of components to check against.

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

    def set_direct_path(self, path: Path, components: Iterable["Component"]) -> bool:
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
