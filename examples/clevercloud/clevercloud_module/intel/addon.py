import logging
from typing import Any
from typing import Dict
from typing import List
import requests

import neo4j
from dateutil import parser as dt_parse
from requests import Session

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
    organization_id,
) -> List[Dict]:
    addons = get(
        api_session,
        common_job_parameters['BASE_URL'],
        organization_id,
    )
    # FIXME: You can configure here a transform operation
    # formated_addons = transform(addons)
    load_addons(
        neo4j_session,
        addons,  # FIXME: replace with `formated_addons` if your added a transform step
        organization_id,
        common_job_parameters['UPDATE_TAG'])
    cleanup(neo4j_session, common_job_parameters)


@timeit
def get(
    api_session: requests.Session,
    base_url: str,
    organization_id,
) -> Dict[str, Any]:
    results: List[Dict[str, Any]] = []
    # FIXME: You have to handle pagination if needed
    req = api_session.get(
        "{base_url}/organisations/{id}/addons".format(
            base_url=base_url,
            id=organization_id,
        ),
        timeout=_TIMEOUT
    )
    req.raise_for_status()
    results = req.json()
    return results


def load_addons(
    neo4j_session: neo4j.Session,
    data: List[Dict[str, Any]],
    organization_id,
    update_tag: int,
) -> None:
    load(
        neo4j_session,
        CleverCloudAddonSchema(),
        data,
        lastupdated=update_tag,
        organization_id=organization_id,
    )


def cleanup(neo4j_session: neo4j.Session, common_job_parameters: Dict[str, Any]) -> None:
    GraphJob.from_node_schema(
        CleverCloudAddonSchema(),
        common_job_parameters
    ).run(neo4j_session)