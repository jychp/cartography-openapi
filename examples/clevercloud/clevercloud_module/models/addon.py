from dataclasses import dataclass

from cartography.models.core.common import PropertyRef
from cartography.models.core.nodes import CartographyNodeProperties
from cartography.models.core.nodes import CartographyNodeSchema
from cartography.models.core.relationships import CartographyRelProperties
from cartography.models.core.relationships import CartographyRelSchema
from cartography.models.core.relationships import LinkDirection
from cartography.models.core.relationships import make_target_node_matcher
from cartography.models.core.relationships import OtherRelationships
from cartography.models.core.relationships import TargetNodeMatcher


@dataclass(frozen=True)
class CleverCloudAddonNodeProperties(CartographyNodeProperties):
    id: PropertyRef = PropertyRef('id')
    name: PropertyRef = PropertyRef('name')
    real_id: PropertyRef = PropertyRef('realId')
    region: PropertyRef = PropertyRef('region')
    zone_id: PropertyRef = PropertyRef('zoneId')
    creation_date: PropertyRef = PropertyRef('creationDate')
    config_keys: PropertyRef = PropertyRef('configKeys')
    provider_id: PropertyRef = PropertyRef('provider.id')
    plan_id: PropertyRef = PropertyRef('plan.id')
    lastupdated: PropertyRef = PropertyRef('lastupdated', set_in_kwargs=True)


@dataclass(frozen=True)
class CleverCloudAddonToOrganizationRelProperties(CartographyRelProperties):
    lastupdated: PropertyRef = PropertyRef('lastupdated', set_in_kwargs=True)


@dataclass(frozen=True)
# (:CleverCloudAddon)-[:RESOURCE]->(:CleverCloudOrganization)
class CleverCloudAddonToOrganizationRel(CartographyRelSchema):
    target_node_label: str = 'CleverCloudOrganization'
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher(
        {'id': PropertyRef('organization_id', set_in_kwargs=True)},
    )
    direction: LinkDirection = LinkDirection.OUTWARD
    rel_label: str = "RESOURCE"
    properties: CleverCloudAddonToOrganizationRelProperties = CleverCloudAddonToOrganizationRelProperties()


# TODO: Add other links


@dataclass(frozen=True)
class CleverCloudAddonSchema(CartographyNodeSchema):
    label: str = 'CleverCloudAddon'
    properties: CleverCloudAddonNodeProperties = CleverCloudAddonNodeProperties()
    sub_resource_relationship: CleverCloudAddonToOrganizationRel = CleverCloudAddonToOrganizationRel()
