## Keycloak Schema



### KeycloakRealm

#CHANGEME: Add here the description of the entity

| Field | Description |
|-------|-------------|
| firstseen| Timestamp of when a sync job first created this node  |
| lastupdated |  Timestamp of the last time the node was updated |
| id |  |
| realm |  |
| display_name |  |
| display_name_html |  |
| not_before |  |
| default_signature_algorithm |  |
| revoke_refresh_token |  |
| refresh_token_max_reuse |  |
| access_token_lifespan |  |
| access_token_lifespan_for_implicit_flow |  |
| sso_session_idle_timeout |  |
| sso_session_max_lifespan |  |
| sso_session_idle_timeout_remember_me |  |
| sso_session_max_lifespan_remember_me |  |
| offline_session_idle_timeout |  |
| offline_session_max_lifespan_enabled |  |
| offline_session_max_lifespan |  |
| client_session_idle_timeout |  |
| client_session_max_lifespan |  |
| client_offline_session_idle_timeout |  |
| client_offline_session_max_lifespan |  |
| access_code_lifespan |  |
| access_code_lifespan_user_action |  |
| access_code_lifespan_login |  |
| action_token_generated_by_admin_lifespan |  |
| action_token_generated_by_user_lifespan |  |
| oauth2_device_code_lifespan |  |
| oauth2_device_polling_interval |  |
| enabled |  |
| ssl_required |  |
| password_credential_grant_allowed |  |
| registration_allowed |  |
| registration_email_as_username |  |
| remember_me |  |
| verify_email |  |
| login_with_email_allowed |  |
| duplicate_emails_allowed |  |
| reset_password_allowed |  |
| edit_username_allowed |  |
| user_cache_enabled |  |
| realm_cache_enabled |  |
| brute_force_protected |  |
| permanent_lockout |  |
| max_temporary_lockouts |  |
| max_failure_wait_seconds |  |
| minimum_quick_login_wait_seconds |  |
| wait_increment_seconds |  |
| quick_login_check_milli_seconds |  |
| max_delta_time_seconds |  |
| failure_factor |  |
| private_key |  |
| public_key |  |
| certificate |  |
| code_secret |  |
| password_policy |  |
| otp_policy_type |  |
| otp_policy_algorithm |  |
| otp_policy_initial_counter |  |
| otp_policy_digits |  |
| otp_policy_look_ahead_window |  |
| otp_policy_period |  |
| otp_policy_code_reusable |  |
| web_authn_policy_rp_entity_name |  |
| web_authn_policy_rp_id |  |
| web_authn_policy_attestation_conveyance_preference |  |
| web_authn_policy_authenticator_attachment |  |
| web_authn_policy_require_resident_key |  |
| web_authn_policy_user_verification_requirement |  |
| web_authn_policy_create_timeout |  |
| web_authn_policy_avoid_same_authenticator_register |  |
| web_authn_policy_passwordless_rp_entity_name |  |
| web_authn_policy_passwordless_rp_id |  |
| web_authn_policy_passwordless_attestation_conveyance_preference |  |
| web_authn_policy_passwordless_authenticator_attachment |  |
| web_authn_policy_passwordless_require_resident_key |  |
| web_authn_policy_passwordless_user_verification_requirement |  |
| web_authn_policy_passwordless_create_timeout |  |
| web_authn_policy_passwordless_avoid_same_authenticator_register |  |
| login_theme |  |
| account_theme |  |
| admin_theme |  |
| email_theme |  |
| events_enabled |  |
| events_expiration |  |
| admin_events_enabled |  |
| admin_events_details_enabled |  |
| internationalization_enabled |  |
| default_locale |  |
| browser_flow |  |
| registration_flow |  |
| direct_grant_flow |  |
| reset_credentials_flow |  |
| client_authentication_flow |  |
| docker_authentication_flow |  |
| first_broker_login_flow |  |
| keycloak_version |  |
| user_managed_access_allowed |  |
| organizations_enabled |  |
| verifiable_credentials_enabled |  |
| admin_permissions_enabled |  |
| social |  |
| update_profile_on_initial_social_login |  |
| o_auth2_device_code_lifespan |  |
| o_auth2_device_polling_interval |  |
| bruteForceStrategy | None |
| roles_id | ID of the RolesRepresentation entity |
| groups_id | ID of the GroupRepresentation entity |
| default_role_id | ID of the RoleRepresentation entity |
| admin_permissions_client_id | ID of the ClientRepresentation entity |
| client_profiles_id | ID of the ClientProfilesRepresentation entity |
| client_policies_id | ID of the ClientPoliciesRepresentation entity |
| users_id | ID of the UserRepresentation entity |
| federated_users_id | ID of the UserRepresentation entity |
| scope_mappings_id | ID of the ScopeMappingRepresentation entity |
| clients_id | ID of the ClientRepresentation entity |
| client_scopes_id | ID of the ClientScopeRepresentation entity |
| user_federation_providers_id | ID of the UserFederationProviderRepresentation entity |
| user_federation_mappers_id | ID of the UserFederationMapperRepresentation entity |
| identity_providers_id | ID of the IdentityProviderRepresentation entity |
| identity_provider_mappers_id | ID of the IdentityProviderMapperRepresentation entity |
| protocol_mappers_id | ID of the ProtocolMapperRepresentation entity |
| components_id | ID of the MultivaluedHashMapStringComponentExportRepresentation entity |
| authentication_flows_id | ID of the AuthenticationFlowRepresentation entity |
| authenticator_config_id | ID of the AuthenticatorConfigRepresentation entity |
| required_actions_id | ID of the RequiredActionProviderRepresentation entity |
| organizations_id | ID of the OrganizationRepresentation entity |
| applications_id | ID of the ApplicationRepresentation entity |
| oauth_clients_id | ID of the OAuthClientRepresentation entity |
| client_templates_id | ID of the ClientTemplateRepresentation entity |

#### Relationships
- Some node types belong to an `KeycloakRealm`.
    ```
    (:KeycloakRealm)<-[:RESOURCE]-(
        :KeycloakClient,
        :KeycloakGroup,
        :KeycloakUser,
    )
    ```


### KeycloakClient

#CHANGEME: Add here the description of the entity

| Field | Description |
|-------|-------------|
| firstseen| Timestamp of when a sync job first created this node  |
| lastupdated |  Timestamp of the last time the node was updated |
| id |  |
| client_id |  |
| name |  |
| description |  |
| type |  |
| root_url |  |
| admin_url |  |
| base_url |  |
| surrogate_auth_required |  |
| enabled |  |
| always_display_in_console |  |
| client_authenticator_type |  |
| secret |  |
| registration_access_token |  |
| not_before |  |
| bearer_only |  |
| consent_required |  |
| standard_flow_enabled |  |
| implicit_flow_enabled |  |
| direct_access_grants_enabled |  |
| service_accounts_enabled |  |
| authorization_services_enabled |  |
| direct_grants_only |  |
| public_client |  |
| frontchannel_logout |  |
| protocol |  |
| full_scope_allowed |  |
| node_re_registration_timeout |  |
| client_template |  |
| use_template_config |  |
| use_template_scope |  |
| use_template_mappers |  |
| origin |  |
| protocol_mappers_id | ID of the ProtocolMapperRepresentation entity |
| authorization_settings_id | ID of the ResourceServerRepresentation entity |

#### Relationships
- `KeycloakClient` belongs to a `KeycloakRealm`
    ```
    (:KeycloakClient)-[:RESOURCE]->(:KeycloakRealm)
    ```


### KeycloakGroup

#CHANGEME: Add here the description of the entity

| Field | Description |
|-------|-------------|
| firstseen| Timestamp of when a sync job first created this node  |
| lastupdated |  Timestamp of the last time the node was updated |
| id |  |
| name |  |
| path |  |
| parent_id |  |
| sub_group_count |  |
| sub_groups_id | ID of the GroupRepresentation entity |

#### Relationships
- `KeycloakGroup` belongs to a `KeycloakRealm`
    ```
    (:KeycloakGroup)-[:RESOURCE]->(:KeycloakRealm)
    ```


### KeycloakUser

#CHANGEME: Add here the description of the entity

| Field | Description |
|-------|-------------|
| firstseen| Timestamp of when a sync job first created this node  |
| lastupdated |  Timestamp of the last time the node was updated |
| id |  |
| username |  |
| first_name |  |
| last_name |  |
| email |  |
| email_verified |  |
| self |  |
| origin |  |
| created_timestamp |  |
| enabled |  |
| totp |  |
| federation_link |  |
| service_account_client_id |  |
| not_before |  |
| user_profile_metadata_id | ID of the UserProfileMetadata entity |
| credentials_id | ID of the CredentialRepresentation entity |
| federated_identities_id | ID of the FederatedIdentityRepresentation entity |
| client_consents_id | ID of the UserConsentRepresentation entity |
| social_links_id | ID of the SocialLinkRepresentation entity |

#### Relationships
- `KeycloakUser` belongs to a `KeycloakRealm`
    ```
    (:KeycloakUser)-[:RESOURCE]->(:KeycloakRealm)
    ```
