from dataclasses import dataclass

from cartography.models.core.common import PropertyRef
from cartography.models.core.nodes import CartographyNodeProperties
from cartography.models.core.nodes import CartographyNodeSchema
from cartography.models.core.relationships import CartographyRelProperties
from cartography.models.core.relationships import CartographyRelSchema
from cartography.models.core.relationships import LinkDirection
from cartography.models.core.relationships import make_target_node_matcher
from cartography.models.core.relationships import TargetNodeMatcher


@dataclass(frozen=True)
class KeycloakGroupNodeProperties(CartographyNodeProperties):
    id: PropertyRef = PropertyRef('id')
    name: PropertyRef = PropertyRef('name')
    path: PropertyRef = PropertyRef('path')
    parent_id: PropertyRef = PropertyRef('parentId')
    sub_group_count: PropertyRef = PropertyRef('subGroupCount')
    sub_groups_id: PropertyRef = PropertyRef('subGroups.id')
    lastupdated: PropertyRef = PropertyRef('lastupdated', set_in_kwargs=True)


@dataclass(frozen=True)
class KeycloakGroupToRealmRelProperties(CartographyRelProperties):
    lastupdated: PropertyRef = PropertyRef('lastupdated', set_in_kwargs=True)


@dataclass(frozen=True)
# (:KeycloakGroup)<-[:RESOURCE]-(:KeycloakRealm)
class KeycloakGroupToRealmRel(CartographyRelSchema):
    target_node_label: str = 'KeycloakRealm'
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher(
        {'id': PropertyRef('realm_id', set_in_kwargs=True)},
    )
    direction: LinkDirection = LinkDirection.INWARD
    rel_label: str = "RESOURCE"
    properties: KeycloakGroupToRealmRelProperties = KeycloakGroupToRealmRelProperties()




@dataclass(frozen=True)
class KeycloakGroupSchema(CartographyNodeSchema):
    label: str = 'KeycloakGroup'
    properties: KeycloakGroupNodeProperties = KeycloakGroupNodeProperties()
    sub_resource_relationship: KeycloakGroupToRealmRel = KeycloakGroupToRealmRel()
