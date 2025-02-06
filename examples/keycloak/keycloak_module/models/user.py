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
class KeycloakUserNodeProperties(CartographyNodeProperties):
    id: PropertyRef = PropertyRef('id')
    username: PropertyRef = PropertyRef('username')
    first_name: PropertyRef = PropertyRef('firstName')
    last_name: PropertyRef = PropertyRef('lastName')
    email: PropertyRef = PropertyRef('email')
    email_verified: PropertyRef = PropertyRef('emailVerified')
    attributes: PropertyRef = PropertyRef('attributes')
    self: PropertyRef = PropertyRef('self')
    origin: PropertyRef = PropertyRef('origin')
    created_timestamp: PropertyRef = PropertyRef('createdTimestamp')
    enabled: PropertyRef = PropertyRef('enabled')
    totp: PropertyRef = PropertyRef('totp')
    federation_link: PropertyRef = PropertyRef('federationLink')
    service_account_client_id: PropertyRef = PropertyRef('serviceAccountClientId')
    credentials: PropertyRef = PropertyRef('credentials')
    disableable_credential_types: PropertyRef = PropertyRef('disableableCredentialTypes')
    required_actions: PropertyRef = PropertyRef('requiredActions')
    federated_identities: PropertyRef = PropertyRef('federatedIdentities')
    realm_roles: PropertyRef = PropertyRef('realmRoles')
    client_roles: PropertyRef = PropertyRef('clientRoles')
    client_consents: PropertyRef = PropertyRef('clientConsents')
    not_before: PropertyRef = PropertyRef('notBefore')
    application_roles: PropertyRef = PropertyRef('applicationRoles')
    social_links: PropertyRef = PropertyRef('socialLinks')
    groups: PropertyRef = PropertyRef('groups')
    access: PropertyRef = PropertyRef('access')
    user_profile_metadata_id: PropertyRef = PropertyRef('userProfileMetadata.id')
    lastupdated: PropertyRef = PropertyRef('lastupdated', set_in_kwargs=True)


@dataclass(frozen=True)
class KeycloakUserToRealmRelProperties(CartographyRelProperties):
    lastupdated: PropertyRef = PropertyRef('lastupdated', set_in_kwargs=True)


@dataclass(frozen=True)
# (:KeycloakUser)-[:RESOURCE]->(:KeycloakRealm)
class KeycloakUserToRealmRel(CartographyRelSchema):
    target_node_label: str = 'KeycloakRealm'
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher(
        {'id': PropertyRef('realm_id', set_in_kwargs=True)},
    )
    direction: LinkDirection = LinkDirection.OUTWARD
    rel_label: str = "RESOURCE"
    properties: KeycloakUserToRealmRelProperties = KeycloakUserToRealmRelProperties()


# TODO: Add other links


@dataclass(frozen=True)
class KeycloakUserSchema(CartographyNodeSchema):
    label: str = 'KeycloakUser'
    properties: KeycloakUserNodeProperties = KeycloakUserNodeProperties()
    sub_resource_relationship: KeycloakUserToRealmRel = KeycloakUserToRealmRel()
