import os
from collections import OrderedDict

from jinja2 import Environment
from jinja2 import PackageLoader

from cartography_openapi.entity import Entity


class Module:
    """ Represents an intel Module for Cartography.

    This class is used as a builder to create a module for Cartography.
    The module is a collection of entities that represent the data model of an API.
    The module can be exported to a directory to be used in Cartography.

    Args:
        name (str): The name of the module.

    Attributes:
        name (str): The name of the module.
        server_url (str): The BASE URL of the API.
        entities (OrderedDict[str, Entity]): The entities of the module.
        components_to_entities (dict[str, str]): The mapping between components (OpenAPI side)
            and entities (Cartography side).
        _jinja_env (Environment): The Jinja environment used to render the templates.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.server_url: str | None = None
        self.entities: OrderedDict[str, Entity] = OrderedDict()
        self.components_to_entities: dict[str, str] = {}
        self._jinja_env = Environment(
            loader=PackageLoader('cartography_openapi', 'templates'),
        )

    def add_entity(self, entity: Entity) -> None:
        """ Add an entity to the module.

        This method adds an entity to the module.
        The entity is stored in the entities attribute and the mapping between components and entities is updated.

        Args:
            entity (Entity): The entity to add to the module.
        """
        self.entities[entity.name] = entity
        self.components_to_entities[entity.component_name] = entity.name

    def get_entity_by_component(self, component_name: str) -> Entity | None:
        """ Get an entity by its component name.

        Args:
            component_name (str): The name of the component to search.

        Returns:
            Entity | None: The entity if found, None otherwise.
        """
        entity_name = self.components_to_entities.get(component_name)
        if entity_name:
            return self.entities[entity_name]
        return None

    def export(self, output_dir: str) -> None:
        """ Export the module to the output directory.

        This method exports the intel module to the output directory:
        - {output_dir}/models contains the data models of the module
        - {output_dir}/intel contains the intel module of the module

        Args:
            output_dir (str): The output directory.
        """
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
            f.write(content)
        # Create entity files
        for entity in self.entities.values():
            with open(os.path.join(intel_dir, f"{entity.name.lower()}.py"), 'w', encoding='utf-8') as f:
                f.write(entity.export_intel())

        # Create tests data
        tests_data_dir = os.path.join(module_dir, 'tests_data')
        os.makedirs(tests_data_dir, exist_ok=True)
        with open(os.path.join(tests_data_dir, '__init__.py'), 'w', encoding='utf-8') as f:
            f.write('')
        # Create entity files
        for entity in self.entities.values():
            with open(os.path.join(tests_data_dir, f"{entity.name.lower()}s.py"), 'w', encoding='utf-8') as f:
                f.write(entity.export_tests_data())

        # Create integration tests
        integration_tests_dir = os.path.join(module_dir, 'integration_tests')
        os.makedirs(integration_tests_dir, exist_ok=True)
        with open(os.path.join(integration_tests_dir, '__init__.py'), 'w', encoding='utf-8') as f:
            f.write('')
        # Create entity files
        for entity in self.entities.values():
            with open(
                os.path.join(
                    integration_tests_dir,
                    f"test_{entity.name.lower()}s.py",
                ),
                'w',
                    encoding='utf-8',
            ) as f:
                f.write(entity.export_tests_integration())

        # Create docs
        docs_dir = os.path.join(module_dir, 'docs')
        os.makedirs(docs_dir, exist_ok=True)
        with open(os.path.join(docs_dir, 'index.rst'), 'w', encoding='utf-8') as f:
            f.write(self.export_docs_index())
        with open(os.path.join(docs_dir, 'config.md'), 'w', encoding='utf-8') as f:
            f.write(self.export_docs_config())
        with open(os.path.join(docs_dir, 'schema.md'), 'w', encoding='utf-8') as f:
            f.write(self.export_docs_schema())

    def export_intel(self) -> str:
        """ Generate the intel/__init__.py python file for the module.

        This method generates the intel/__init__.py python file for the module.
        The file contains the required methods to fetch the entities from the API and
        to create the nodes in the graph.
        This method also calls the sync call of the root entities using a recursive method.

        Returns:
            str: The content of the intel/__init__.py file.
        """
        template = self._jinja_env.get_template("intel.jinja")
        content = template.render(
            module=self,
        )
        for entity in self.entities.values():
            # Skip entities that are not the root of the tree
            if entity.parent_entity is not None:
                continue
            content += entity.export_sync_call(recursive=True) + '\n'
        return content

    def export_docs_index(self) -> str:
        """ Generate the docs/index.rst file for the module.

        Returns:
            str: The content of the docs/index.rst file.
        """
        template = self._jinja_env.get_template("docs_index.jinja")
        content = template.render(
            module=self,
        )
        return content

    def export_docs_config(self) -> str:
        """ Generate the docs/config.md file for the module.

        Returns:
            str: The content of the docs/config.md file.
        """
        template = self._jinja_env.get_template("docs_config.jinja")
        content = template.render(
            module=self,
        )
        return content

    def export_docs_schema(self) -> str:
        """ Generate the docs/schema.md file for the module.

        Returns:
            str: The content of the docs/schema.md file.
        """
        template = self._jinja_env.get_template("docs_schema.jinja")
        content = template.render(
            module=self,
        )
        return content

    def __repr__(self) -> str:
        return f'<Module {self.name}>'
