import re
from typing import Any

from loguru import logger

from cartography_openapi.pagination import Pagination


class Path:
    """Represents a path of the OpenAPI schema.

    The path is a part of the OpenAPI schema that defines an endpoint of the API.
    This class is used to store the properties of the path and the relations between paths.

    See: https://swagger.io/specification/#paths-object

    Args:
        path (str): The path of the endpoint.
        get_method (dict[str, Any]): The GET method of the endpoint.

    Attributes:
        path (str): The path of the endpoint.
        path_params (dict[str, Any]): The path parameters of the endpoint.
        body_params (dict[str, Any]): The body parameters of the endpoint.
        query_params (dict[str, Any]): The query parameters of the endpoint.
        returns_array (bool): True if the endpoint returns an array, False otherwise.
        returned_component (str): The name of the component returned by the endpoint.
        pagination (Pagination): The pagination of the endpoint.
        indirect_ref (str): The indirect reference to the entity in the path (eg: {'result': []})
    """

    def __init__(self, path: str, get_method: dict[str, Any]) -> None:
        self.path = path
        self.path_params: dict[str, Any] = {}
        self.body_params: dict[str, Any] = {}
        self.query_params: dict[str, Any] = {}
        self.returns_array: bool = False
        self.returned_component: str | None = None
        self.pagination: Pagination | None = None
        self.indirect_ref: str | None = None
        self._from_method(get_method)

    def _from_method(self, method: dict[str, Any]) -> None:
        logger.debug(f"Parsing path {self.path}")
        if "200" not in method.get("responses", {}):
            logger.debug("Skipping, no 200 response found")
            return

        response_schema = (
            method["responses"]["200"]
            .get(
                "content",
                {},
            )
            .get("application/json", {})
            .get("schema")
        )
        if not response_schema:
            logger.debug("Skipping, no response schema found")
            return
        if not self._guess_returned_component(response_schema):
            logger.debug("Skipping, no component name found")

        for param in method.get("parameters", []):
            # TODO: handled ref
            if "$ref" in param:
                logger.debug(f"Skipping, ref found in parameters: {param['$ref']}")
                continue
            if param["in"] == "path":
                self.path_params[param["name"]] = param
            elif param["in"] == "body":
                self.body_params[param["name"]] = param
            elif param["in"] == "query":
                self.query_params[param["name"]] = param
            else:
                logger.debug(
                    f"Unknown parameter type {param['in']} for {param['name']} in {self.path}"
                )

        # Sometimes the path parameters are not in the response schema
        if len(self.path_params) == 0:
            for m in re.findall(r"{[a-zA-Z-_0-9]+}", self.path):
                self.path_params[m[1:-1]] = {}

        # Check for pagination
        if self.returns_array:
            for k in Pagination.current_params():
                if k in self.query_params:
                    self.pagination = Pagination(self)
                    break

    def set_indirect_ref(self, ref: str) -> None:
        """Set the indirect reference to the entity in the path.

        Args:
            ref (str): The indirect reference to the entity in the path (eg: {'result': []})
        """
        if self.indirect_ref is None:
            self.indirect_ref = ref
        else:
            self.indirect_ref = f"{self.indirect_ref}.{ref}"

    def _guess_returned_component(self, response_schema: dict[str, Any]) -> bool:
        # DOC
        if "allOf" in response_schema:
            # Usually, the common stuff (like pagination) is in the first schema
            # and the specific stuff is in the last schema
            for schema in reversed(response_schema["allOf"]):
                if self._guess_returned_component(schema):
                    return True
            return False
        component_name = None
        if response_schema.get("type") == "object":
            for k, v in response_schema.get("properties", {}).items():
                if v.get("$ref"):
                    component_name = v.get("$ref")
                    self.set_indirect_ref(k)
                    break
                elif v.get("type") == "array" and v.get("items", {}).get("$ref"):
                    component_name = v.get("items", {}).get("$ref")
                    self.set_indirect_ref(k)
                    self.returns_array = True
                    break
        elif "properties" in response_schema:
            # If the response schema is an object but doesn't have a type, we assume it's a component
            for k, v in response_schema.get("properties", {}).items():
                if v.get("$ref"):
                    component_name = v.get("$ref")
                    self.indirect_ref = k
                    break
                elif v.get("type") == "array":
                    self.returns_array = True
                    if v.get("items", {}).get("$ref"):
                        component_name = v.get("items", {}).get("$ref")
                        self.set_indirect_ref(k)
                        break
        else:
            component_name = response_schema.get("$ref")

        if component_name:
            self.returned_component = component_name.split("/")[-1]
            return True
        return False

    def is_sub_path_of(self, other: "Path", max_args: int = 0) -> bool:
        """Check if the path is a sub-path of another path.

        This method checks if the path is a sub-path of another path.
        A path is a sub-path of another path if it starts with the other path and has the same path parameters.
        Sub-paths can have additional path parameters (defined with max_args argument), but not missing ones.

        Args:
            other (Path): The other path to compare with.
            max_args (int): The maximum number of additional path parameters allowed.

        Returns:
            bool: True if the path is a sub-path of the other path, False otherwise.
        """

        if not self.path.startswith(other.path):
            return False
        missing_args = [p for p in self.path_params if p not in other.path_params]
        return len(missing_args) <= max_args

    def __repr__(self) -> str:
        return f"<Path {self.path}>"
