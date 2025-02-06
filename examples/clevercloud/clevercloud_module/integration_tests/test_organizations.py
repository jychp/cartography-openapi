from unittest.mock import patch

import requests

import cartography.intel.clevercloud.organizations
import tests.data.clevercloud.organizations
from tests.integration.util import check_nodes
from tests.integration.util import check_rels

TEST_UPDATE_TAG = 123456789


@patch.object(cartography.clevercloud.organizations, 'get', return_value=tests.data.clevercloud.organizations.CLEVERCLOUD_CLEVERCLOUDS)
def test_load_clevercloud_organizations(mock_api, neo4j_session):
    """
    Ensure that organizations actually get loaded
    """

    # Arrange
    api_session = requests.Session()
    common_job_parameters = {
        "UPDATE_TAG": TEST_UPDATE_TAG,
        "BASE_URL": "https://fake.clevercloud.com",
    }

    # Act
    cartography.intel.clevercloud.organizations.sync(
        neo4j_session,
        api_session,
        common_job_parameters,
    )

    # Assert Organizations exist
    expected_nodes = {
        # FIXME: Add here expected node from data
        # (123456, 'john.doe@domain.tld'),
    }
    assert check_nodes(
        neo4j_session,
        'CleverCloudOrganization',
        ['id', 'email']
    ) == expected_nodes

