from unittest.mock import patch

import requests

import cartography.intel.clevercloud.applications
import tests.data.clevercloud.applications
import cartography.tests.data.clevercloud.applications
from tests.integration.util import check_nodes
from tests.integration.util import check_rels

TEST_UPDATE_TAG = 123456789
TEST_ID = "CHANGEME"


@patch.object(cartography.intel.clevercloud.applications, 'get', return_value=tests.data.clevercloud.applications.CLEVERCLOUD_APPLICATIONS)
def test_load_clevercloud_applications(mock_api, neo4j_session):
    """
    Ensure that applications actually get loaded
    """

    # Arrange
    api_session = requests.Session()
    common_job_parameters = {
        "UPDATE_TAG": TEST_UPDATE_TAG,
        "BASE_URL": "https://fake.clevercloud.com",
        "id": TEST_ID,
    }

    # Act
    cartography.intel.clevercloud.applications.sync(
        neo4j_session,
        api_session,
        common_job_parameters,
        id,
    )

    # Assert Applications exist
    expected_nodes = {
        # CHANGEME: Add here expected node from data
        # (123456, 'john.doe@domain.tld'),
    }
    assert check_nodes(
        neo4j_session,
        'CleverCloudApplication',
        ['id', 'email']
    ) == expected_nodes

    # Assert Applications are connected with Organization
    expected_rels = {
        ('CHANGE_ME', organization_id),  # CHANGEME: Add here one of Applications id
    }
    assert check_rels(
        neo4j_session,
        'CleverCloudApplication', 'id',
        'CleverCloudOrganization', 'id',
        'RESOURCE',
        rel_direction_right=False,
    ) == expected_rels
