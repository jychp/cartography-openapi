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
class CleverCloudApplicationNodeProperties(CartographyNodeProperties):
    id: PropertyRef = PropertyRef('id')
    name: PropertyRef = PropertyRef('name')
    description: PropertyRef = PropertyRef('description')
    zone: PropertyRef = PropertyRef('zone')
    zone_id: PropertyRef = PropertyRef('zoneId')
    vhosts: PropertyRef = PropertyRef('vhosts')
    creation_date: PropertyRef = PropertyRef('creationDate')
    last_deploy: PropertyRef = PropertyRef('last_deploy')
    archived: PropertyRef = PropertyRef('archived')
    sticky_sessions: PropertyRef = PropertyRef('stickySessions')
    homogeneous: PropertyRef = PropertyRef('homogeneous')
    favourite: PropertyRef = PropertyRef('favourite')
    cancel_on_push: PropertyRef = PropertyRef('cancelOnPush')
    webhook_url: PropertyRef = PropertyRef('webhookUrl')
    webhook_secret: PropertyRef = PropertyRef('webhookSecret')
    separate_build: PropertyRef = PropertyRef('separateBuild')
    owner_id: PropertyRef = PropertyRef('ownerId')
    state: PropertyRef = PropertyRef('state')
    commit_id: PropertyRef = PropertyRef('commitId')
    appliance: PropertyRef = PropertyRef('appliance')
    branch: PropertyRef = PropertyRef('branch')
    force_https: PropertyRef = PropertyRef('forceHttps')
    env: PropertyRef = PropertyRef('env')
    deploy_url: PropertyRef = PropertyRef('deployUrl')
    instance_id: PropertyRef = PropertyRef('instance.id')
    deployment_id: PropertyRef = PropertyRef('deployment.id')
    build_flavor_id: PropertyRef = PropertyRef('buildFlavor.id')
    lastupdated: PropertyRef = PropertyRef('lastupdated', set_in_kwargs=True)


@dataclass(frozen=True)
class CleverCloudApplicationToOrganizationRelProperties(CartographyRelProperties):
    lastupdated: PropertyRef = PropertyRef('lastupdated', set_in_kwargs=True)


@dataclass(frozen=True)
# (:CleverCloudApplication)-[:RESOURCE]->(:CleverCloudOrganization)
class CleverCloudApplicationToOrganizationRel(CartographyRelSchema):
    target_node_label: str = 'CleverCloudOrganization'
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher(
        {'id': PropertyRef('organization_id', set_in_kwargs=True)},
    )
    direction: LinkDirection = LinkDirection.OUTWARD
    rel_label: str = "RESOURCE"
    properties: CleverCloudApplicationToOrganizationRelProperties = CleverCloudApplicationToOrganizationRelProperties()


# TODO: Add other links


@dataclass(frozen=True)
class CleverCloudApplicationSchema(CartographyNodeSchema):
    label: str = 'CleverCloudApplication'
    properties: CleverCloudApplicationNodeProperties = CleverCloudApplicationNodeProperties()
    sub_resource_relationship: CleverCloudApplicationToOrganizationRel = CleverCloudApplicationToOrganizationRel()
