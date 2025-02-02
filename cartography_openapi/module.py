import os
from collections import OrderedDict

from jinja2 import Environment
from jinja2 import PackageLoader

from cartography_openapi.entity import Entity


class Module:
    # DOC
    def __init__(self, name: str) -> None:
        self.name = name
        self.server_url: str | None = None
        self.entities: OrderedDict[str, Entity] = OrderedDict()
        self.components_to_entities: dict[str, str] = {}
        self._jinja_env = Environment(
            loader=PackageLoader('cartography_openapi', 'templates'),
        )

    def add_entity(self, entity: Entity) -> None:
        # DOC
        self.entities[entity.name] = entity
        self.components_to_entities[entity.component_name] = entity.name

    def get_entity_by_component(self, component_name: str) -> Entity | None:
        # DOC
        entity_name = self.components_to_entities.get(component_name)
        if entity_name:
            return self.entities[entity_name]
        return None

    def export(self, output_dir: str) -> None:
        # DOC
        module_dir = os.path.join(output_dir, f"{self.name.lower()}_module")
        os.makedirs(module_dir, exist_ok=True)

        # Create models
        models_dir = os.path.join(module_dir, 'models')
        os.makedirs(models_dir, exist_ok=True)
        with open(os.path.join(models_dir, '__init__.py'), 'w', encoding='utf-8') as f:
            f.write('')
        for entity in self.entities.values():
            with open(os.path.join(models_dir, f"{entity.name.lower()}.py"), 'w', encoding='utf-8') as f:
                f.write(entity.export_model())

        # Create intel
        intel_dir = os.path.join(module_dir, 'intel')
        os.makedirs(intel_dir, exist_ok=True)
        # Create __init__.py
        with open(os.path.join(intel_dir, '__init__.py'), 'w', encoding='utf-8') as f:
            content = self.export_intel()
            for entity in self.entities.values():
                # Skip entities that are not the root of the tree
                if entity.parent_entity is not None:
                    continue
                content += entity.export_intel() + '\n'
            f.write(content)
        # Create entity files
        for entity in self.entities.values():
            with open(os.path.join(intel_dir, f"{entity.name.lower()}.py"), 'w', encoding='utf-8') as f:
                f.write(entity.export_intel())

    # TODO: Create tests

    # TODO: Create doc

    # TODO: Create PR message

    def export_intel(self) -> str:
        template = self._jinja_env.get_template("intel.jinja")
        return template.render(
            module=self,
        )
