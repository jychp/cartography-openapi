import logging
from typing import Any
from typing import Dict
from typing import List
import requests

import neo4j

from cartography.client.core.tx import load
from cartography.graph.job import GraphJob
from cartography.models.keycloak.user import KeycloakUserSchema
from cartography.util import timeit


logger = logging.getLogger(__name__)
# Connect and read timeouts of 60 seconds each; see https://requests.readthedocs.io/en/master/user/advanced/#timeouts
_TIMEOUT = (60, 60)


@timeit
def sync(
    neo4j_session: neo4j.Session,
    api_session: requests.Session,
    common_job_parameters: Dict[str, Any],
    realm: str,
) -> List[Dict]:
    users = get(
        api_session,
        common_job_parameters['BASE_URL'],
        realm,
    )
    # CHANGEME: You can configure here a transform operation
    # formated_users = transform(users)
    load_users(
        neo4j_session,
        users,  # CHANGEME: replace with `formated_users` if your added a transform step
        realm,
        common_job_parameters['UPDATE_TAG'])
    cleanup(neo4j_session, common_job_parameters)
    return users


@timeit
def get(
    api_session: requests.Session,
    base_url: str,
    realm: str,
) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    # CHANGEME: You have to handle pagination if needed
    req = api_session.get(
        "{base_url}".format(
            base_url=base_url,
            realm=realm,
        ),
        timeout=_TIMEOUT
    )
    req.raise_for_status()
    results = req.json()
    return results


@timeit
def load_users(
    neo4j_session: neo4j.Session,
    data: List[Dict[str, Any]],
    realm: str,
    update_tag: int,
) -> None:
    logger.info("Loading %d KeycloakUserSchema into Neo4j.", len(data))
    load(
        neo4j_session,
        KeycloakUserSchema(),
        data,
        lastupdated=update_tag,
        realm=realm,
    )


@timeit
def cleanup(neo4j_session: neo4j.Session, common_job_parameters: Dict[str, Any]) -> None:
    GraphJob.from_node_schema(
        KeycloakUserSchema(),
        common_job_parameters
    ).run(neo4j_session)