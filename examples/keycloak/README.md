# Keycloak Example

## Tests

### Using local specifications
```
uv run python3 cartography_openapi -v -n Keycloak -f ./example/keycloak/openapi.json RealmRepresentation=Realm ClientRepresentation=Client GroupRepresentation=Group UserRepresentation=User
```

### Using remote specifications
```
uv run python3 cartography_openapi -v -n Keycloak -u "https://www.keycloak.org/docs-api/latest/rest-api/openapi.json" RealmRepresentation=Realm ClientRepresentation=Client GroupRepresentation=Group UserRepresentation=User
```

## Results

You can check results on [keycloak_module](./keycloak_module/) or generate your owns
