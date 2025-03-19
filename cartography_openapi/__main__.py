import argparse
import sys

from loguru import logger

from cartography_openapi.parser import OpenAPIParser


def main() -> None:
    # ARGS PARSING
    parser = argparse.ArgumentParser("Cartogtaphy - Import OpenAPI")
    parser.add_argument(
        "-v",
        "--verbose",
        help="Display DEBUG level messsages",
        action="store_true",
    )
    parser.add_argument(
        "-u",
        "--url",
        help="URL of the OpenAPI specifications",
    )
    parser.add_argument(
        "-f",
        "--file",
        help="Path of the OpenAPI specifications",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output directory",
        default=".",
    )
    parser.add_argument(
        "-n",
        "--name",
        help="Name of the intel module",
        required=True,
    )
    parser.add_argument(
        "-i",
        "--ignore",
        help="Ignore specific paths (e.g. /path/to/ignore or /path/to/*)",
        action="append",
    )
    parser.add_argument(
        "elements",
        type=str,
        nargs="+",
        help="Names of elements to import (RemoteName=LocalName)",
    )
    args = parser.parse_args()
    if not args.verbose:
        logger.remove(0)
        logger.add(sys.stderr, level="INFO")

    if args.url is None and args.file is None:
        logger.error("You must provide either a URL or a file")
        exit(1)
    if args.url and args.file:
        logger.error("You must provide either a URL or a file, not both")
        exit(1)

    openapi_parser = OpenAPIParser(args.name, args.url, args.file, args.ignore)
    components_to_models: dict[str, str] = {}
    for element in args.elements:
        if "=" in element:
            remote_name, local_name = element.split("=", 1)
        else:
            remote_name = element
            local_name = None
        components_to_models[remote_name] = local_name
    if openapi_parser.build_module(**components_to_models):
        openapi_parser.export(args.output)


if __name__ == "__main__":
    main()
