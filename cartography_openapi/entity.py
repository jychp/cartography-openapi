from collections import OrderedDict
from typing import TYPE_CHECKING, Any

from jinja2 import Environment, PackageLoader
from loguru import logger

from cartography_openapi.component import Component
from cartography_openapi.path import Path

if TYPE_CHECKING:
    from cartography_openapi.module import Module


class Entity:
    """Represents an entity (a node) in the data model.

    This class is used to represent an entity in the data model.
    An entity is a node in the graph that represents a resource in the API.
    The entity is used to generate the Cartography schema and the Intel schema.

    Args:
        module (Module): The module the entity belongs to.
        name (str): The name of the entity.
        component_name (str): The name of the component in the OpenAPI specification.

    Attributes:
        _module (Module): The module the entity belongs to.
        name (str): The name of the entity.
        description (str): The description of the entity.
        component_name (str): The name of the component in the OpenAPI specification.
        _jinja_env (Environment): The Jinja environment used to render the templates.
        fields (OrderedDict[str, str]): The fields of the entity.
        parent_entity (Entity | None): The parent entity of the entity.
        children_entities (list[Entity]): The children entities of the entity.
        enumeration_path (Path | None): The enumeration path of the entity.
        path_id (str | None): The path ID of the entity.
    """

    def __init__(self, module: "Module", name: str, component_name: str) -> None:
        self._module = module
        self.name = name
        self.description: str = "#CHANGEME: Add here the description of the entity"
        self.component_name: str = component_name
        self._jinja_env = Environment(
            loader=PackageLoader("cartography_openapi", "templates"),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        # name, type, description, example, is_array
        self.fields: OrderedDict[str, dict[str, Any]] = OrderedDict()
        self.parent_entity: "Entity" | None = None
        self.children_entities: list["Entity"] = []
        self.enumeration_path: Path | None = None
        self.path_id: str | None = None
        self.related_entities: dict[str, dict[str, Any]] = {}

    @property
    def node_name(self) -> str:
        """Name of the node in the graph.

        The node name is the concatenation of the module name and the entity name.
        eg: 'KeycloakRealm'

        Returns:
            str: The node name.
        """
        return self._module.name + self.name

    @property
    def node_class(self) -> str:
        """Name of the class in the graph.

        The node class is the concatenation of the module name and the entity name followed by 'Schema'.
        eg: 'KeycloakRealmSchema'

        Returns:
            str: The node class.
        """
        return f"{self.node_name}Schema"

    @property
    def has_relationships(self) -> bool:
        """Check if the entity has relationships.

        This property returns True if the entity has relationships with other entities.

        Returns:
            bool: True if the entity has relationships, False otherwise.
        """
        if self.parent_entity is not None:
            return True
        if len(self.children_entities) > 0:
            return True
        return False

    @property
    def all_parents(self) -> list["Entity"]:
        """All parents of the entity.

        This property returns a list of all the parents of the entity.
        The list is ordered from the closest parent to the most distant parent.
        Parents are entities that have "sub-resources" link to the entity.

        Returns:
            list[Entity]: The list of all parents of the entity.
        """
        result: list["Entity"] = []
        if self.parent_entity is not None:
            result = self.parent_entity.all_parents
            result.append(self.parent_entity)
        return result

    @property
    def needed_params(self) -> dict[str, dict[str, str | None]]:
        """Returns the needed parameters to fetch the entity.

        This method returns the needed parameters to fetch the entity.
        The parameters are the path parameters of the enumeration path.
        The parameters are returned as a dictionary with the parameter name as key and a dictionary as value.
        The dictionary contains different format of the parameter name:
            - name (key): the name of the parameter in the path
            - var_name: the name of the parameter as it will be used is Cartography functions
            - dict_name: the variable used to retrieve the parameter from the parent entity

        Exemple: for a path '/groups/{group_id}/users/{user_id}' with enumeration path '/groups/{group_id}/users'
        The method will return:
        {
            'group_id': {
                'var_name': 'group_id',
                'dict_name': 'group['id']',
            },
        }

        Returns:
            dict[str, dict[str, str | None]]: The needed parameters to fetch the entity.
        """
        result: dict[str, dict[str, str | None]] = {}
        if self.enumeration_path is None:
            if self.path_id is not None:
                result[self.path_id] = {
                    "var_name": self.path_id,
                    "dict_name": None,
                    "test_value": '"CHANGEME"',
                }
            return result
        for p_name, p_data in self.enumeration_path.path_params.items():
            found_in_parent = False
            for parent in self.all_parents:
                if p_name == parent.path_id:
                    found_in_parent = True
                    test_module_path = f"cartography.tests.data.{self._module.name.lower()}.{parent.name.lower()}s"
                    test_data_dict = (
                        f"{self._module.name.upper()}_{parent.name.upper()}"
                    )

                    result[p_name] = {
                        "var_name": f"{parent.name.lower()}_id",
                        "dict_name": f"{parent.name.lower()}['id']",
                        "test_value": f"{test_module_path}.{test_data_dict}[0]['id']",
                    }
                    break
            if not found_in_parent:
                result[p_name] = {
                    "var_name": p_name,
                    "dict_name": None,
                    "test_value": '"CHANGEME"',
                }
        return result

    def build_from_component(
        self, component: Component, consolidated_entities: dict[str, "Entity"]
    ) -> None:
        """Build the entity from a component.

        This method builds the entity from a component.
        It extracts the fields from the properties and relations of the component.
        It also creates the link between the entity and its parent entity.

        Args:
            component (Component): The component to build the entity from.
            consolidated_entities (dict[str, Entity]): The list of all Entity that will be added to the module.
        """
        self.enumeration_path = component.enumeration_path
        self.path_id = component.path_id
        if component.description is not None:
            self.description = component.description.strip().replace("\n", "<br/>")

        # Build fields from properties
        for prop_name, field in component.properties.items():
            self.fields[field.clean_name] = {
                "name": prop_name,
                "type": field.type,
                "description": "",
                "example": field.example,
                "is_array": field.is_array,
            }
            if field.description is not None:
                self.fields[field.clean_name][
                    "description"
                ] = field.description.strip().replace("\n", "<br/>")

        # Build fields from relations
        for rel_name, rel in component.relations.items():
            rel_field_name = f"{rel['clean_name']}_id"
            if rel["linked_component"] in component.FIELDS:
                typed_field = component.FIELDS[rel["linked_component"]]
                self.fields[rel_name] = {
                    "name": rel_name,
                    "type": typed_field.type,
                    "description": typed_field.description,
                    "example": typed_field.example,
                    "is_array": typed_field.is_array,
                }
            elif rel["linked_component"] in consolidated_entities:
                self.related_entities[rel_name] = {
                    "entity": consolidated_entities[rel["linked_component"]],
                    "name": f"{rel_name}.id",
                    "to_many": rel["is_array"],
                }
            else:
                self.fields[rel_field_name] = {
                    "name": f"{rel_name}.id",
                    "type": "string",
                    "is_array": False,
                    "description": f"ID of the {rel['linked_component']} entity",
                }

        # Build sub_resource link
        if component.parent_component is not None:
            self.parent_entity = self._module.get_entity_by_component(
                component.parent_component.name
            )
            if self.parent_entity is None:
                logger.error(
                    f"Parent entity not found for component '{component.parent_component.name}'"
                )
            else:
                self.parent_entity.children_entities.append(self)

    def export_model(self) -> str:
        """Generate the model python file for the entity.

        This method generates the model python file for the entity.
        The file contains the node schema of the entity and the edges to other entities.

        Returns:
            str: the content of the model python file.
        """
        template = self._jinja_env.get_template("model.jinja")
        return template.render(entity=self)

    def export_intel(self) -> str:
        """Generate the intel python file for the entity.

        This method generates the intel python file for the entity.
        The file contains the required methods to fetch the entity from the API and
        to create the node in the graph.

        Returns:
            str: the content of the intel python file.
        """
        template = self._jinja_env.get_template("intel_entity.jinja")
        return template.render(
            entity=self,
        )

    def export_sync_call(
        self, recursive: bool = False, param_style: str = "dict"
    ) -> str:
        """Generate the sync call for the entity.

        This method generates the sync call for the entity.
        This call is used in the intel/__init__.py file to fetch the entity from the API.
        This method also calls the sync call of the children entities.

        Args:
            recursive (bool): enable recursive call (default: False)
            param_style (str): the style of the function params (dict, var)

        Returns:
            str: the sync call for the entity.
        """
        if param_style not in ("dict", "var"):
            raise ValueError(
                f"param_style must be one of ['dict', 'var'] not '{param_style}'"
            )
        template = self._jinja_env.get_template("intel_sync_call.jinja")
        current_call = template.render(
            entity=self, recursive=recursive, param_style=param_style
        )
        if recursive:
            current_call += "\n"
            for child in self.children_entities:
                for line in child.export_sync_call(recursive).split("\n"):
                    current_call += f"    {line}\n"
        return current_call

    def export_tests_data(self) -> str:
        """Generate the tests data for the entity.

        This method generates the tests data for the entity.
        The file contains the data to use in the tests.
        WARNING: At the time it's only build the skeleton, the data must be filled manually.

        Returns:
            str: the content of the tests data file.
        """
        template = self._jinja_env.get_template("tests_data.jinja")
        return template.render(
            entity=self,
        )

    def export_tests_integration(self) -> str:
        """Generate the tests integration for the entity.

        This method generates the tests integration for the entity.
        The file contains the tests to check the integration of the entity in the graph.

        Returns:
            str: the content of the tests integration file.
        """
        template = self._jinja_env.get_template("tests_integration.jinja")
        return template.render(
            entity=self,
        )

    def __repr__(self) -> str:
        return f"<Entity {self.name}>"
