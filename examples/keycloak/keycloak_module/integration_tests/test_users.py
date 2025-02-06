from unittest.mock import patch

import requests

import cartography.intel.keycloak.users
import tests.data.keycloak.users
from tests.integration.util import check_nodes
from tests.integration.util import check_rels

TEST_UPDATE_TAG = 123456789


@patch.object(cartography.keycloak.users, 'get', return_value=tests.data.keycloak.users.KEYCLOAK_KEYCLOAKS)
def test_load_keycloak_users(mock_api, neo4j_session):
    """
    Ensure that users actually get loaded
    """

    # Arrange
    api_session = requests.Session()
    common_job_parameters = {
        "UPDATE_TAG": TEST_UPDATE_TAG,
        "BASE_URL": "https://fake.keycloak.com",
    }
    realm_id = 'CHANGEME'  # FIXME: Add here expected parent id node

    # Act
    cartography.intel.keycloak.users.sync(
        neo4j_session,
        api_session,
        common_job_parameters,
        realm_id,
    )

    # Assert Users exist
    expected_nodes = {
        # FIXME: Add here expected node from data
        # (123456, 'john.doe@domain.tld'),
    }
    assert check_nodes(
        neo4j_session,
        'KeycloakUser',
        ['id', 'email']
    ) == expected_nodes

    # Assert Users are connected with Realm
    expected_rels = {
        ('CHANGE_ME', realm_id),  # FIXME: Add here one of Users id
    }
    assert check_rels(
        neo4j_session,
        'KeycloakUser', 'id',
        'KeycloakRealm', 'id',
        'RESOURCE',
        rel_direction_right=True,
    ) == expected_rels
