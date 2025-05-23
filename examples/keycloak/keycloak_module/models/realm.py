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
class KeycloakRealmNodeProperties(CartographyNodeProperties):
    id: PropertyRef = PropertyRef('id')
    realm: PropertyRef = PropertyRef('realm')
    display_name: PropertyRef = PropertyRef('displayName')
    display_name_html: PropertyRef = PropertyRef('displayNameHtml')
    not_before: PropertyRef = PropertyRef('notBefore')
    default_signature_algorithm: PropertyRef = PropertyRef('defaultSignatureAlgorithm')
    revoke_refresh_token: PropertyRef = PropertyRef('revokeRefreshToken')
    refresh_token_max_reuse: PropertyRef = PropertyRef('refreshTokenMaxReuse')
    access_token_lifespan: PropertyRef = PropertyRef('accessTokenLifespan')
    access_token_lifespan_for_implicit_flow: PropertyRef = PropertyRef('accessTokenLifespanForImplicitFlow')
    sso_session_idle_timeout: PropertyRef = PropertyRef('ssoSessionIdleTimeout')
    sso_session_max_lifespan: PropertyRef = PropertyRef('ssoSessionMaxLifespan')
    sso_session_idle_timeout_remember_me: PropertyRef = PropertyRef('ssoSessionIdleTimeoutRememberMe')
    sso_session_max_lifespan_remember_me: PropertyRef = PropertyRef('ssoSessionMaxLifespanRememberMe')
    offline_session_idle_timeout: PropertyRef = PropertyRef('offlineSessionIdleTimeout')
    offline_session_max_lifespan_enabled: PropertyRef = PropertyRef('offlineSessionMaxLifespanEnabled')
    offline_session_max_lifespan: PropertyRef = PropertyRef('offlineSessionMaxLifespan')
    client_session_idle_timeout: PropertyRef = PropertyRef('clientSessionIdleTimeout')
    client_session_max_lifespan: PropertyRef = PropertyRef('clientSessionMaxLifespan')
    client_offline_session_idle_timeout: PropertyRef = PropertyRef('clientOfflineSessionIdleTimeout')
    client_offline_session_max_lifespan: PropertyRef = PropertyRef('clientOfflineSessionMaxLifespan')
    access_code_lifespan: PropertyRef = PropertyRef('accessCodeLifespan')
    access_code_lifespan_user_action: PropertyRef = PropertyRef('accessCodeLifespanUserAction')
    access_code_lifespan_login: PropertyRef = PropertyRef('accessCodeLifespanLogin')
    action_token_generated_by_admin_lifespan: PropertyRef = PropertyRef('actionTokenGeneratedByAdminLifespan')
    action_token_generated_by_user_lifespan: PropertyRef = PropertyRef('actionTokenGeneratedByUserLifespan')
    oauth2_device_code_lifespan: PropertyRef = PropertyRef('oauth2DeviceCodeLifespan')
    oauth2_device_polling_interval: PropertyRef = PropertyRef('oauth2DevicePollingInterval')
    enabled: PropertyRef = PropertyRef('enabled')
    ssl_required: PropertyRef = PropertyRef('sslRequired')
    password_credential_grant_allowed: PropertyRef = PropertyRef('passwordCredentialGrantAllowed')
    registration_allowed: PropertyRef = PropertyRef('registrationAllowed')
    registration_email_as_username: PropertyRef = PropertyRef('registrationEmailAsUsername')
    remember_me: PropertyRef = PropertyRef('rememberMe')
    verify_email: PropertyRef = PropertyRef('verifyEmail')
    login_with_email_allowed: PropertyRef = PropertyRef('loginWithEmailAllowed')
    duplicate_emails_allowed: PropertyRef = PropertyRef('duplicateEmailsAllowed')
    reset_password_allowed: PropertyRef = PropertyRef('resetPasswordAllowed')
    edit_username_allowed: PropertyRef = PropertyRef('editUsernameAllowed')
    user_cache_enabled: PropertyRef = PropertyRef('userCacheEnabled')
    realm_cache_enabled: PropertyRef = PropertyRef('realmCacheEnabled')
    brute_force_protected: PropertyRef = PropertyRef('bruteForceProtected')
    permanent_lockout: PropertyRef = PropertyRef('permanentLockout')
    max_temporary_lockouts: PropertyRef = PropertyRef('maxTemporaryLockouts')
    max_failure_wait_seconds: PropertyRef = PropertyRef('maxFailureWaitSeconds')
    minimum_quick_login_wait_seconds: PropertyRef = PropertyRef('minimumQuickLoginWaitSeconds')
    wait_increment_seconds: PropertyRef = PropertyRef('waitIncrementSeconds')
    quick_login_check_milli_seconds: PropertyRef = PropertyRef('quickLoginCheckMilliSeconds')
    max_delta_time_seconds: PropertyRef = PropertyRef('maxDeltaTimeSeconds')
    failure_factor: PropertyRef = PropertyRef('failureFactor')
    private_key: PropertyRef = PropertyRef('privateKey')
    public_key: PropertyRef = PropertyRef('publicKey')
    certificate: PropertyRef = PropertyRef('certificate')
    code_secret: PropertyRef = PropertyRef('codeSecret')
    password_policy: PropertyRef = PropertyRef('passwordPolicy')
    otp_policy_type: PropertyRef = PropertyRef('otpPolicyType')
    otp_policy_algorithm: PropertyRef = PropertyRef('otpPolicyAlgorithm')
    otp_policy_initial_counter: PropertyRef = PropertyRef('otpPolicyInitialCounter')
    otp_policy_digits: PropertyRef = PropertyRef('otpPolicyDigits')
    otp_policy_look_ahead_window: PropertyRef = PropertyRef('otpPolicyLookAheadWindow')
    otp_policy_period: PropertyRef = PropertyRef('otpPolicyPeriod')
    otp_policy_code_reusable: PropertyRef = PropertyRef('otpPolicyCodeReusable')
    web_authn_policy_rp_entity_name: PropertyRef = PropertyRef('webAuthnPolicyRpEntityName')
    web_authn_policy_rp_id: PropertyRef = PropertyRef('webAuthnPolicyRpId')
    web_authn_policy_attestation_conveyance_preference: PropertyRef = PropertyRef('webAuthnPolicyAttestationConveyancePreference')
    web_authn_policy_authenticator_attachment: PropertyRef = PropertyRef('webAuthnPolicyAuthenticatorAttachment')
    web_authn_policy_require_resident_key: PropertyRef = PropertyRef('webAuthnPolicyRequireResidentKey')
    web_authn_policy_user_verification_requirement: PropertyRef = PropertyRef('webAuthnPolicyUserVerificationRequirement')
    web_authn_policy_create_timeout: PropertyRef = PropertyRef('webAuthnPolicyCreateTimeout')
    web_authn_policy_avoid_same_authenticator_register: PropertyRef = PropertyRef('webAuthnPolicyAvoidSameAuthenticatorRegister')
    web_authn_policy_passwordless_rp_entity_name: PropertyRef = PropertyRef('webAuthnPolicyPasswordlessRpEntityName')
    web_authn_policy_passwordless_rp_id: PropertyRef = PropertyRef('webAuthnPolicyPasswordlessRpId')
    web_authn_policy_passwordless_attestation_conveyance_preference: PropertyRef = PropertyRef('webAuthnPolicyPasswordlessAttestationConveyancePreference')
    web_authn_policy_passwordless_authenticator_attachment: PropertyRef = PropertyRef('webAuthnPolicyPasswordlessAuthenticatorAttachment')
    web_authn_policy_passwordless_require_resident_key: PropertyRef = PropertyRef('webAuthnPolicyPasswordlessRequireResidentKey')
    web_authn_policy_passwordless_user_verification_requirement: PropertyRef = PropertyRef('webAuthnPolicyPasswordlessUserVerificationRequirement')
    web_authn_policy_passwordless_create_timeout: PropertyRef = PropertyRef('webAuthnPolicyPasswordlessCreateTimeout')
    web_authn_policy_passwordless_avoid_same_authenticator_register: PropertyRef = PropertyRef('webAuthnPolicyPasswordlessAvoidSameAuthenticatorRegister')
    login_theme: PropertyRef = PropertyRef('loginTheme')
    account_theme: PropertyRef = PropertyRef('accountTheme')
    admin_theme: PropertyRef = PropertyRef('adminTheme')
    email_theme: PropertyRef = PropertyRef('emailTheme')
    events_enabled: PropertyRef = PropertyRef('eventsEnabled')
    events_expiration: PropertyRef = PropertyRef('eventsExpiration')
    admin_events_enabled: PropertyRef = PropertyRef('adminEventsEnabled')
    admin_events_details_enabled: PropertyRef = PropertyRef('adminEventsDetailsEnabled')
    internationalization_enabled: PropertyRef = PropertyRef('internationalizationEnabled')
    default_locale: PropertyRef = PropertyRef('defaultLocale')
    browser_flow: PropertyRef = PropertyRef('browserFlow')
    registration_flow: PropertyRef = PropertyRef('registrationFlow')
    direct_grant_flow: PropertyRef = PropertyRef('directGrantFlow')
    reset_credentials_flow: PropertyRef = PropertyRef('resetCredentialsFlow')
    client_authentication_flow: PropertyRef = PropertyRef('clientAuthenticationFlow')
    docker_authentication_flow: PropertyRef = PropertyRef('dockerAuthenticationFlow')
    first_broker_login_flow: PropertyRef = PropertyRef('firstBrokerLoginFlow')
    keycloak_version: PropertyRef = PropertyRef('keycloakVersion')
    user_managed_access_allowed: PropertyRef = PropertyRef('userManagedAccessAllowed')
    organizations_enabled: PropertyRef = PropertyRef('organizationsEnabled')
    verifiable_credentials_enabled: PropertyRef = PropertyRef('verifiableCredentialsEnabled')
    admin_permissions_enabled: PropertyRef = PropertyRef('adminPermissionsEnabled')
    social: PropertyRef = PropertyRef('social')
    update_profile_on_initial_social_login: PropertyRef = PropertyRef('updateProfileOnInitialSocialLogin')
    o_auth2_device_code_lifespan: PropertyRef = PropertyRef('oAuth2DeviceCodeLifespan')
    o_auth2_device_polling_interval: PropertyRef = PropertyRef('oAuth2DevicePollingInterval')
    bruteForceStrategy: PropertyRef = PropertyRef('bruteForceStrategy')
    roles_id: PropertyRef = PropertyRef('roles.id')
    groups_id: PropertyRef = PropertyRef('groups.id')
    default_role_id: PropertyRef = PropertyRef('defaultRole.id')
    admin_permissions_client_id: PropertyRef = PropertyRef('adminPermissionsClient.id')
    client_profiles_id: PropertyRef = PropertyRef('clientProfiles.id')
    client_policies_id: PropertyRef = PropertyRef('clientPolicies.id')
    users_id: PropertyRef = PropertyRef('users.id')
    federated_users_id: PropertyRef = PropertyRef('federatedUsers.id')
    scope_mappings_id: PropertyRef = PropertyRef('scopeMappings.id')
    clients_id: PropertyRef = PropertyRef('clients.id')
    client_scopes_id: PropertyRef = PropertyRef('clientScopes.id')
    user_federation_providers_id: PropertyRef = PropertyRef('userFederationProviders.id')
    user_federation_mappers_id: PropertyRef = PropertyRef('userFederationMappers.id')
    identity_providers_id: PropertyRef = PropertyRef('identityProviders.id')
    identity_provider_mappers_id: PropertyRef = PropertyRef('identityProviderMappers.id')
    protocol_mappers_id: PropertyRef = PropertyRef('protocolMappers.id')
    components_id: PropertyRef = PropertyRef('components.id')
    authentication_flows_id: PropertyRef = PropertyRef('authenticationFlows.id')
    authenticator_config_id: PropertyRef = PropertyRef('authenticatorConfig.id')
    required_actions_id: PropertyRef = PropertyRef('requiredActions.id')
    organizations_id: PropertyRef = PropertyRef('organizations.id')
    applications_id: PropertyRef = PropertyRef('applications.id')
    oauth_clients_id: PropertyRef = PropertyRef('oauthClients.id')
    client_templates_id: PropertyRef = PropertyRef('clientTemplates.id')
    lastupdated: PropertyRef = PropertyRef('lastupdated', set_in_kwargs=True)






@dataclass(frozen=True)
class KeycloakRealmSchema(CartographyNodeSchema):
    label: str = 'KeycloakRealm'
    properties: KeycloakRealmNodeProperties = KeycloakRealmNodeProperties()
