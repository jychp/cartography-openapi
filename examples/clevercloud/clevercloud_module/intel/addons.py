import logging
from typing import Any
from typing import Dict
from typing import List
import requests

import neo4j

from cartography.client.core.tx import load
from cartography.graph.job import GraphJob
from cartography.models.clevercloud.addon import CleverCloudAddonSchema
from cartography.util import timeit


logger = logging.getLogger(__name__)
# Connect and read timeouts of 60 seconds each; see https://requests.readthedocs.io/en/master/user/advanced/#timeouts
_TIMEOUT = (60, 60)


@timeit
def sync(
    neo4j_session: neo4j.Session,
    api_session: requests.Session,
    common_job_parameters: Dict[str, Any],
    id: str,
) -> List[Dict]:
    addons = get(
        api_session,
        common_job_parameters['BASE_URL'],
        id,
    )
    # CHANGEME: You can configure here a transform operation
    # formated_addons = transform(addons)
    load_addons(
        neo4j_session,
        addons,  # CHANGEME: replace with `formated_addons` if your added a transform step
        id,
        common_job_parameters['UPDATE_TAG'])
    cleanup(neo4j_session, common_job_parameters)
    return addons


@timeit
def get(
    api_session: requests.Session,
    base_url: str,
    id: str,
) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    # CHANGEME: You have to handle pagination if needed
    req = api_session.get(
        "{base_url}".format(
            base_url=base_url,
            id=id,
        ),
        timeout=_TIMEOUT
    )
    req.raise_for_status()
    results = req.json()
    return results


@timeit
def load_addons(
    neo4j_session: neo4j.Session,
    data: List[Dict[str, Any]],
    id: str,
    update_tag: int,
) -> None:
    logger.info("Loading %d CleverCloudAddonSchema into Neo4j.", len(data))
    load(
        neo4j_session,
        CleverCloudAddonSchema(),
        data,
        lastupdated=update_tag,
        id=id,
    )


@timeit
def cleanup(neo4j_session: neo4j.Session, common_job_parameters: Dict[str, Any]) -> None:
    GraphJob.from_node_schema(
        CleverCloudAddonSchema(),
        common_job_parameters
    ).run(neo4j_session)