from unittest.mock import patch

import requests

import cartography.intel.keycloak.realms
import tests.data.keycloak.realms
from tests.integration.util import check_nodes
from tests.integration.util import check_rels

TEST_UPDATE_TAG = 123456789
TEST_REALM = "CHANGEME"


@patch.object(cartography.intel.keycloak.realms, 'get', return_value=tests.data.keycloak.realms.KEYCLOAK_REALMS)
def test_load_keycloak_realms(mock_api, neo4j_session):
    """
    Ensure that realms actually get loaded
    """

    # Arrange
    api_session = requests.Session()
    common_job_parameters = {
        "UPDATE_TAG": TEST_UPDATE_TAG,
        "BASE_URL": "https://fake.keycloak.com",
        "realm": TEST_REALM,
    }

    # Act
    cartography.intel.keycloak.realms.sync(
        neo4j_session,
        api_session,
        common_job_parameters,
        realm,
    )

    # Assert Realms exist
    expected_nodes = {
        # CHANGEME: Add here expected node from data
        # (123456, 'john.doe@domain.tld'),
    }
    assert check_nodes(
        neo4j_session,
        'KeycloakRealm',
        ['id', 'email']
    ) == expected_nodes

