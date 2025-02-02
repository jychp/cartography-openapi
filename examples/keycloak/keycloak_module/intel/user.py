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
from cartography.models.keycloak.user import KeycloakUserSchema
from cartography.util import timeit


logger = logging.getLogger(__name__)
# Connect and read timeouts of 60 seconds each; see https://requests.readthedocs.io/en/master/user/advanced/#timeouts
_TIMEOUT = (60, 60)


@timeit
def sync(
    neo4j_session: neo4j.Session,
    api_session: requests.Session,
    realm_id,
    update_tag: int,
    common_job_parameters: Dict[str, Any],
) -> List[Dict]:
    users = get(
        api_session,
        common_job_parameters['BASE_URL'],
        realm_id,
    )
    # FIXME: You can configure here a transform operation
    # formated_users = transform(users)
    load_users(
        neo4j_session,
        users,  # FIXME: replace with `formated_users` if your added a transform step
        realm_id,
        update_tag)
    cleanup(neo4j_session, common_job_parameters)

@timeit
def get(
    api_session: requests.Session,
    base_url: str,
    realm_id,
) -> Dict[str, Any]:
    # FIXME: You have to handle pagination if needed
    req = api_session.get(
        "{base_url}/admin/realms/{realm}/users".format(
            base_url=base_url,
            realm=realm_id,
        ),
        timeout=_TIMEOUT
    )
    req.raise_for_status()
    return req.json()

def load_users(
    neo4j_session: neo4j.Session,
    data: List[Dict[str, Any]],
    realm_id,
    update_tag: int,
) -> None:
    load(
        neo4j_session,
        KeycloakUserSchema(),
        data,
        lastupdated=update_tag,
        realm_id=realm_id,
    )


def cleanup(neo4j_session: neo4j.Session, common_job_parameters: Dict[str, Any]) -> None:
    GraphJob.from_node_schema(
        KeycloakUserSchema(),
        common_job_parameters
    ).run(neo4j_session)