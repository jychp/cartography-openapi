# cartography-openapi

[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/jychp/cartography-openapi/badge)](https://scorecard.dev/viewer/?uri=github.com/jychp/cartography-openapi)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/9995/badge)](https://www.bestpractices.dev/projects/9995)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=jychp_cartography-openapi&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=jychp_cartography-openapi)
![build](https://github.com/jychp/cartography-openapi/actions/workflows/ci.yml/badge.svg)

**cartography-openapi** is a tool for generating modules for [Cartography](https://github.com/cartography-cncf/cartography) from specification files in OpenAPI format.

## Why ?

Developing modules for Cartography can be confusing, especially regarding the data model and various requirements. Importing multiple resources can also be tedious.

With this in mind, **cartography-openapi** helps generate the skeleton of a module, allowing developers to focus on added value (drift detection, custom links, etc.).

For more details, refer to the [Cartography developer documentation](https://cartography-cncf.github.io/cartography/dev/index.html).

## Supported formats

**cartography-openapi** supports importing files in OpenAPI v3 format.

For more details, refer to the [OpenAPI Specification](https://swagger.io/specification/)

## How it's work

### Parse
_See `cartography_openapi.parser.Parser._parse`_

- Parse the server block to try to determine the API `base_url`.
- Parse the components:
  - List properties that will become fields (with types such as string, int, etc.).
  - List properties that will become relationships to other nodes (fields that return another object).
- Parse the paths:
  - Keep only paths with the `GET` method that return known components.
  - Extract path parameters, query parameters, and body parameters.

### Build
_See `cartography_openapi.parser.Parser.build_module`_

- Entities will be built in the order they were declared in the command invocation.
- For each entity, the tool will:
  - Find the corresponding component in the API.
  - Identify the best path (1) to enumerate the list of these components.
  - Identify the best path (1) to access a single component.
  - From the identified paths, determine if a parent entity can be defined.

### Best path finding (1)
_See `cartography_openapi.component.Component.set_enumeration_path` and `cartography_openapi.component.Component.set_direct_path`._
This part is the **core** of the tool’s functionality. It empirically determines:
- The paths used to **list** all entities.
- The paths used to **access** a specific component.

The logic is as follows:
If the path to access a **Realm** is `/admin/realm/{realmId}` and the path to access a **Group** is `/admin/realm/{realmId}/group/{groupId}`, then:
- **Group** is considered a sub-resource of **Realm**.
- An **edge** must exist between the two nodes.
- The enumeration must be handled **recursively**.

Path evaluation is based on the following criteria:
- No previous path
- Linkable vs non-linkable (the path is a sub-path of the direct path of another component)
- The new path is better because it has less parameters
- The new path is better because it is shorter (allow to prefer x/groups over x/groups-default)

### Export
_See `cartography_openapi.module.Module.export`_

- The model (nodes & relationships) of each entity is exported to a specific file using a Jinja template.
- Each entity generates an "intel" file containing the logic to **sync, get, transform, and load** the entity into Cartography.
- The module generates the `__init__.py` file for the module's intel, which calls each entity-specific file via the `sync` function.
- The `sync` function, which will be called by Cartography, is built recursively to handle sub-resources:
  - **Example:** Synchronizing tenants
    - For each tenant, synchronize environments
    - For each environment, synchronize resources

## Install

### Using pypi

```pip3 install cartography-openapi```

### Using uv

```
uv sync --frozen
uv run python3 cartography_openapi
```

## Usage

### Quick start

```
wget https://www.keycloak.org/docs-api/latest/rest-api/openapi.json
uv run python3 main.py -v -n Keycloak -f ./openapi.json RealmRepresentation=Realm ClientRepresentation=Client GroupRepresentation=Group UserRepresentation=User
```

For more examples, refer to the [examples](./examples/) folder.

### Options & parameters

You must provide the list of API components to include in the module.
You can specify a different name for these components (e.g., RealmRepresentation=Realm will import the RealmRepresentation component of the API under the Realm node).

⚠️ **WARNING:** The order in which components are passed is **IMPORTANT**. They are resolved in the given order and will only be linked if the parent component (e.g., Realm/Tenant) has already been imported.


| Option               | Required | Description             |
| -------------------- | -------- | ----------------------- |
| --name (-n)          | YES      | Name of the intel module
| --url (-u) <URL>     | (*)      | URL of the OpenAPI specifications
| --file (-f) <PATH>   | (*)      | Path of the OpenAPI specifications
| --verbose (-v)       |          | Display debug level messsages
| --output (-o) <PATH> |          | Output directory (default `.`)
| --ignore (-i) <URI>  |          | Ignore specific paths (e.g. /path/to/ignore or /path/to/*)


(*) You must provide one (and only one source) for the OpenAPI specification

### Export the module

**cartography-openapi** will generate a `<OUTPUT>/<NAME>_module` folder containing the necessary files to add the module to Cartography. This folder includes:
- The `model` folder, which must be moved to `cartography/model/<NAME>`
- The `intel` folder, which must be moved to `cartography/intel/<NAME>`
- The `tests_data` folder, which must be moved to `tests/data/<NAME>`
- The `tests_integration` folder, wich must be moved to `tests/integration/cartography/intel/<NAME>`
- The `docs` folder, wich must be moved to `docs/root/modules/<NAME>`

⚠️ **WARNING**: cartography-openapi only generates a skeleton. You must modify, adapt, and test it yourself.

The following operations must be performed manually:
- Add the necessary configuration keys in `cartography/config.py`
- Add the required parameters in `cartography/cli.py`
- Import your module in `cartography/sync.py`
- Update the cartography `README.md`

### Known issues & limitations

**cartography-openapi** is a Proof of Concept, and many features are still missing (we are actively working on them):
- The generated code does not handle authentication for API calls
- The generated code does not manage links to other entities (except for `sub-resource` links)
- Only API response with array are supported (not dict like `{'users': [], 'count': 12}`)
- List components are not supported
- Tests data are not provided

## License

This project is licensed under the [Apache 2.0 License](./LICENSE).

## Modules generated

None so far :(

## ROADMAP

Here are the topics we are working on for upcoming releases:

- [ ] handle API response with dict like `{'users': [], 'count': 12}`
- [ ] handle API response where list are handled as componenet (ex: UserView, UserListView)
- [ ] handle authentication
- [ ] handle query with variable param in path
- [ ] handle "other_links"
- [ ] generate Cartography data for tests
- [ ] generate Cartography config
