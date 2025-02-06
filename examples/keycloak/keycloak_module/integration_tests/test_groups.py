from unittest.mock import patch

import requests

import cartography.intel.keycloak.groups
import tests.data.keycloak.groups
from tests.integration.util import check_nodes
from tests.integration.util import check_rels

TEST_UPDATE_TAG = 123456789


@patch.object(cartography.keycloak.groups, 'get', return_value=tests.data.keycloak.groups.KEYCLOAK_KEYCLOAKS)
def test_load_keycloak_groups(mock_api, neo4j_session):
    """
    Ensure that groups actually get loaded
    """

    # Arrange
    api_session = requests.Session()
    common_job_parameters = {
        "UPDATE_TAG": TEST_UPDATE_TAG,
        "BASE_URL": "https://fake.keycloak.com",
    }
    realm_id = 'CHANGEME'  # FIXME: Add here expected parent id node

    # Act
    cartography.intel.keycloak.groups.sync(
        neo4j_session,
        api_session,
        common_job_parameters,
        realm_id,
    )

    # Assert Groups exist
    expected_nodes = {
        # FIXME: Add here expected node from data
        # (123456, 'john.doe@domain.tld'),
    }
    assert check_nodes(
        neo4j_session,
        'KeycloakGroup',
        ['id', 'email']
    ) == expected_nodes

    # Assert Groups are connected with Realm
    expected_rels = {
        ('CHANGE_ME', realm_id),  # FIXME: Add here one of Groups id
    }
    assert check_rels(
        neo4j_session,
        'KeycloakGroup', 'id',
        'KeycloakRealm', 'id',
        'RESOURCE',
        rel_direction_right=True,
    ) == expected_rels
