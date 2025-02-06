from unittest.mock import patch

import requests

import cartography.intel.clevercloud.addons
import tests.data.clevercloud.addons
from tests.integration.util import check_nodes
from tests.integration.util import check_rels

TEST_UPDATE_TAG = 123456789


@patch.object(cartography.clevercloud.addons, 'get', return_value=tests.data.clevercloud.addons.CLEVERCLOUD_CLEVERCLOUDS)
def test_load_clevercloud_addons(mock_api, neo4j_session):
    """
    Ensure that addons actually get loaded
    """

    # Arrange
    api_session = requests.Session()
    common_job_parameters = {
        "UPDATE_TAG": TEST_UPDATE_TAG,
        "BASE_URL": "https://fake.clevercloud.com",
    }
    organization_id = 'CHANGEME'  # FIXME: Add here expected parent id node

    # Act
    cartography.intel.clevercloud.addons.sync(
        neo4j_session,
        api_session,
        common_job_parameters,
        organization_id,
    )

    # Assert Addons exist
    expected_nodes = {
        # FIXME: Add here expected node from data
        # (123456, 'john.doe@domain.tld'),
    }
    assert check_nodes(
        neo4j_session,
        'CleverCloudAddon',
        ['id', 'email']
    ) == expected_nodes

    # Assert Addons are connected with Organization
    expected_rels = {
        ('CHANGE_ME', organization_id),  # FIXME: Add here one of Addons id
    }
    assert check_rels(
        neo4j_session,
        'CleverCloudAddon', 'id',
        'CleverCloudOrganization', 'id',
        'RESOURCE',
        rel_direction_right=True,
    ) == expected_rels
