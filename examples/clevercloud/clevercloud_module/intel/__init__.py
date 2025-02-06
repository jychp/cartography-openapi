import logging
import requests

import neo4j

import cartography.intel.lastpass.users
from cartography.config import Config
from cartography.util import timeit

logger = logging.getLogger(__name__)


@timeit
def start_clevercloud_ingestion(neo4j_session: neo4j.Session, config: Config) -> None:
    """
    If this module is configured, perform ingestion of CleverCloud data. Otherwise warn and exit
    :param neo4j_session: Neo4J session for database interface
    :param config: A cartography.config object
    :return: None
    """

    # FIXME: Add here needed credentials
    if not config.clevercloud_apikey:
        logger.info(
            'CleverCloud import is not configured - skipping this module. '
            'See docs to configure.',
        )
        return

    # Create requests sessions
    api_session = requests.session()

    # FIXME: Configure the authentication
    api_session.headers.update(
        {'X-Api-Key': config.clevercloud_apikey}
    )

    common_job_parameters = {
        "UPDATE_TAG": config.update_tag,
        "BASE_URL": "https://api.clever-cloud.com/v2",
    }

    for organization in cartography.intel.clevercloud.organizations.sync(
        neo4j_session,
        api_session,
        common_job_parameters,
    ):
        cartography.intel.clevercloud.applications.sync(
            neo4j_session,
            api_session,
            common_job_parameters,
            organization_id=organization['id'],
        )
    
        cartography.intel.clevercloud.addons.sync(
            neo4j_session,
            api_session,
            common_job_parameters,
            organization_id=organization['id'],
        )
    

