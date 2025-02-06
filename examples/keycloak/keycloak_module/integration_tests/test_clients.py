from unittest.mock import patch

import requests

import cartography.intel.keycloak.clients
import tests.data.keycloak.clients
from tests.integration.util import check_nodes
from tests.integration.util import check_rels

TEST_UPDATE_TAG = 123456789


@patch.object(cartography.keycloak.clients, 'get', return_value=tests.data.keycloak.clients.KEYCLOAK_KEYCLOAKS)
def test_load_keycloak_clients(mock_api, neo4j_session):
    """
    Ensure that clients actually get loaded
    """

    # Arrange
    api_session = requests.Session()
    common_job_parameters = {
        "UPDATE_TAG": TEST_UPDATE_TAG,
        "BASE_URL": "https://fake.keycloak.com",
    }
    realm_id = 'CHANGEME'  # FIXME: Add here expected parent id node

    # Act
    cartography.intel.keycloak.clients.sync(
        neo4j_session,
        api_session,
        common_job_parameters,
        realm_id,
    )

    # Assert Clients exist
    expected_nodes = {
        # FIXME: Add here expected node from data
        # (123456, 'john.doe@domain.tld'),
    }
    assert check_nodes(
        neo4j_session,
        'KeycloakClient',
        ['id', 'email']
    ) == expected_nodes

    # Assert Clients are connected with Realm
    expected_rels = {
        ('CHANGE_ME', realm_id),  # FIXME: Add here one of Clients id
    }
    assert check_rels(
        neo4j_session,
        'KeycloakClient', 'id',
        'KeycloakRealm', 'id',
        'RESOURCE',
        rel_direction_right=True,
    ) == expected_rels
