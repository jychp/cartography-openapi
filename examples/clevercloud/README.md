# CleverCloud Example

## Tests

### Using local specifications
```
poetry run python3 main.py -v n CleverCloud -f ./example/clevercloud/openapi.json -i "/self*" OrganisationView=Organization ApplicationView=Application AddonView=Addon
```

### Using remote specifications
```
poetry run python3 main.py -v n CleverCloud -u "https://api.clever-cloud.com/v2/openapi.json" -i "/self*" OrganisationView=Organization ApplicationView=Application AddonView=Addon
```

## Results

You can check results on [clevercloud_module](./clevercloud_module/) or generate your owns
