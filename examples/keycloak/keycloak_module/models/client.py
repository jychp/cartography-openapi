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
class KeycloakClientNodeProperties(CartographyNodeProperties):
    id: PropertyRef = PropertyRef('id')
    client_id: PropertyRef = PropertyRef('clientId')
    name: PropertyRef = PropertyRef('name')
    description: PropertyRef = PropertyRef('description')
    type: PropertyRef = PropertyRef('type')
    root_url: PropertyRef = PropertyRef('rootUrl')
    admin_url: PropertyRef = PropertyRef('adminUrl')
    base_url: PropertyRef = PropertyRef('baseUrl')
    surrogate_auth_required: PropertyRef = PropertyRef('surrogateAuthRequired')
    enabled: PropertyRef = PropertyRef('enabled')
    always_display_in_console: PropertyRef = PropertyRef('alwaysDisplayInConsole')
    client_authenticator_type: PropertyRef = PropertyRef('clientAuthenticatorType')
    secret: PropertyRef = PropertyRef('secret')
    registration_access_token: PropertyRef = PropertyRef('registrationAccessToken')
    default_roles: PropertyRef = PropertyRef('defaultRoles')
    redirect_uris: PropertyRef = PropertyRef('redirectUris')
    web_origins: PropertyRef = PropertyRef('webOrigins')
    not_before: PropertyRef = PropertyRef('notBefore')
    bearer_only: PropertyRef = PropertyRef('bearerOnly')
    consent_required: PropertyRef = PropertyRef('consentRequired')
    standard_flow_enabled: PropertyRef = PropertyRef('standardFlowEnabled')
    implicit_flow_enabled: PropertyRef = PropertyRef('implicitFlowEnabled')
    direct_access_grants_enabled: PropertyRef = PropertyRef('directAccessGrantsEnabled')
    service_accounts_enabled: PropertyRef = PropertyRef('serviceAccountsEnabled')
    authorization_services_enabled: PropertyRef = PropertyRef('authorizationServicesEnabled')
    direct_grants_only: PropertyRef = PropertyRef('directGrantsOnly')
    public_client: PropertyRef = PropertyRef('publicClient')
    frontchannel_logout: PropertyRef = PropertyRef('frontchannelLogout')
    protocol: PropertyRef = PropertyRef('protocol')
    attributes: PropertyRef = PropertyRef('attributes')
    authentication_flow_binding_overrides: PropertyRef = PropertyRef('authenticationFlowBindingOverrides')
    full_scope_allowed: PropertyRef = PropertyRef('fullScopeAllowed')
    node_re_registration_timeout: PropertyRef = PropertyRef('nodeReRegistrationTimeout')
    registered_nodes: PropertyRef = PropertyRef('registeredNodes')
    protocol_mappers: PropertyRef = PropertyRef('protocolMappers')
    client_template: PropertyRef = PropertyRef('clientTemplate')
    use_template_config: PropertyRef = PropertyRef('useTemplateConfig')
    use_template_scope: PropertyRef = PropertyRef('useTemplateScope')
    use_template_mappers: PropertyRef = PropertyRef('useTemplateMappers')
    default_client_scopes: PropertyRef = PropertyRef('defaultClientScopes')
    optional_client_scopes: PropertyRef = PropertyRef('optionalClientScopes')
    access: PropertyRef = PropertyRef('access')
    origin: PropertyRef = PropertyRef('origin')
    authorization_settings_id: PropertyRef = PropertyRef('authorizationSettings.id')
    lastupdated: PropertyRef = PropertyRef('lastupdated', set_in_kwargs=True)


@dataclass(frozen=True)
class KeycloakClientToRealmRelProperties(CartographyRelProperties):
    lastupdated: PropertyRef = PropertyRef('lastupdated', set_in_kwargs=True)


@dataclass(frozen=True)
# (:KeycloakClient)-[:RESOURCE]->(:KeycloakRealm)
class KeycloakClientToRealmRel(CartographyRelSchema):
    target_node_label: str = 'KeycloakRealm'
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher(
        {'id': PropertyRef('realm_id', set_in_kwargs=True)},
    )
    direction: LinkDirection = LinkDirection.OUTWARD
    rel_label: str = "RESOURCE"
    properties: KeycloakClientToRealmRelProperties = KeycloakClientToRealmRelProperties()


# TODO: Add other links


@dataclass(frozen=True)
class KeycloakClientSchema(CartographyNodeSchema):
    label: str = 'KeycloakClient'
    properties: KeycloakClientNodeProperties = KeycloakClientNodeProperties()
    sub_resource_relationship: KeycloakClientToRealmRel = KeycloakClientToRealmRel()
