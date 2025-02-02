from collections import OrderedDict
from typing import TYPE_CHECKING

from jinja2 import Environment
from jinja2 import PackageLoader
from loguru import logger

from cartography_openapi.component import Component
from cartography_openapi.path import Path

if TYPE_CHECKING:
    from cartography_openapi.module import Module


class Entity:
    # DOC
    def __init__(self, module: 'Module', name: str, component_name: str) -> None:
        self._module = module
        self.name = name
        self.component_name: str = component_name
        self._jinja_env = Environment(
            loader=PackageLoader('cartography_openapi', 'templates'),
        )
        self.fields: OrderedDict[str, str] = OrderedDict()
        self.parent_entity: 'Entity' | None = None
        self.children_entities: list['Entity'] = []
        self.enumeration_path: Path | None = None
        self.path_id: str | None = None

    @property
    def node_name(self) -> str:
        # DOC
        return self._module.name + self.name

    @property
    def node_class(self) -> str:
        # DOC
        return f"{self.node_name}Schema"

    @property
    def all_parents(self) -> list['Entity']:
        result: list['Entity'] = []
        if self.parent_entity is not None:
            result = self.parent_entity.all_parents
            result.append(self.parent_entity)
        return result

    @property
    def needed_kwargs(self) -> dict[str, dict[str, str]]:
        # DOC
        result: dict[str, dict[str, str]] = {}
        if self.enumeration_path is None:
            raise ValueError('Enumeration path not set')
        for p_name, p_data in self.enumeration_path.path_params.items():
            found_in_parent = False
            for parent in self.all_parents:
                if p_name == parent.path_id:
                    found_in_parent = True
                    result[p_name] = {
                        'arg_name': f"{parent.name.lower()}_id",
                        'dict_name': f"{parent.name.lower()}['id']",
                    }
                    break
            if not found_in_parent:
                raise NotImplementedError('Path with variable not implemented')
        return result

    def build_from_component(self, component: Component, consolidated_components: list[Component]) -> None:
        # DOC
        self.enumeration_path = component.enumeration_path
        self.path_id = component.path_id

        # Build fields from properties
        for prop_name, prop in component.properties.items():
            self.fields[prop['clean_name']] = prop_name

        # Build fields from relations
        for rel_name, rel in component.relations.items():
            rel_field_name = f"{rel['clean_name']}_id"
            if rel['linked_component'] in consolidated_components:
                # TODO: Create a link
                raise NotImplementedError('Not implemented')
            self.fields[rel_field_name] = f"{rel_name}.id"

        # Build sub_resource link
        if component.parent_component is not None:
            self.parent_entity = self._module.get_entity_by_component(component.parent_component.name)
            if self.parent_entity is None:
                logger.error(f"Parent entity not found for component '{component.parent_component.name}'")
            else:
                self.parent_entity.add_child_entity(self)

    def add_child_entity(self, entity: 'Entity') -> None:
        # DOC
        self.children_entities.append(entity)

    def export_model(self) -> str:
        # DOC
        template = self._jinja_env.get_template("model.jinja")
        return template.render(entity=self)

    def export_intel(self) -> str:
        # DOC
        template = self._jinja_env.get_template("intel_entity.jinja")

        return template.render(
            entity=self,
        )

    def export_sync_call(self) -> str:
        # DOC
        template = self._jinja_env.get_template("intel_sync_call.jinja")
        current_call = template.render(
            entity=self,
        )
        for child in self.children_entities:
            for line in child.export_sync_call().split('\n'):
                current_call += f'    {line}\n'
        return current_call

    def __repr__(self) -> str:
        return f'<Entity {self.name}>'
