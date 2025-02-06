import logging
import requests

import neo4j

import cartography.intel.lastpass.users
from cartography.config import Config
from cartography.util import timeit

logger = logging.getLogger(__name__)


@timeit
def start_keycloak_ingestion(neo4j_session: neo4j.Session, config: Config) -> None:
    """
    If this module is configured, perform ingestion of Keycloak data. Otherwise warn and exit
    :param neo4j_session: Neo4J session for database interface
    :param config: A cartography.config object
    :return: None
    """

    # FIXME: Add here needed credentials
    if not config.keycloak_apikey:
        logger.info(
            'Keycloak import is not configured - skipping this module. '
            'See docs to configure.',
        )
        return

    # Create requests sessions
    api_session = requests.session()

    # FIXME: Configure the authentication
    api_session.headers.update(
        {'X-Api-Key': config.keycloak_apikey}
    )

    common_job_parameters = {
        "UPDATE_TAG": config.update_tag,
        "BASE_URL": "https://localhost",
    }

    for realm in cartography.intel.keycloak.realms.sync(
        neo4j_session,
        api_session,
        common_job_parameters,
    ):
        cartography.intel.keycloak.clients.sync(
            neo4j_session,
            api_session,
            common_job_parameters,
            realm_id=realm['id'],
        )
    
        cartography.intel.keycloak.groups.sync(
            neo4j_session,
            api_session,
            common_job_parameters,
            realm_id=realm['id'],
        )
    
        cartography.intel.keycloak.users.sync(
            neo4j_session,
            api_session,
            common_job_parameters,
            realm_id=realm['id'],
        )
    

