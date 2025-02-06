## Keycloak Schema

.. _keycloak_schema:


### Realm

# FIXME: Add a short description of the node and complete fields description

| Field | Description |
|-------|-------------|
| firstseen| Timestamp of when a sync job first created this node  |
| lastupdated |  Timestamp of the last time the node was updated |
| id |       |
| realm |       |
| display_name |       |
| display_name_html |       |
| not_before |       |
| default_signature_algorithm |       |
| revoke_refresh_token |       |
| refresh_token_max_reuse |       |
| access_token_lifespan |       |
| access_token_lifespan_for_implicit_flow |       |
| sso_session_idle_timeout |       |
| sso_session_max_lifespan |       |
| sso_session_idle_timeout_remember_me |       |
| sso_session_max_lifespan_remember_me |       |
| offline_session_idle_timeout |       |
| offline_session_max_lifespan_enabled |       |
| offline_session_max_lifespan |       |
| client_session_idle_timeout |       |
| client_session_max_lifespan |       |
| client_offline_session_idle_timeout |       |
| client_offline_session_max_lifespan |       |
| access_code_lifespan |       |
| access_code_lifespan_user_action |       |
| access_code_lifespan_login |       |
| action_token_generated_by_admin_lifespan |       |
| action_token_generated_by_user_lifespan |       |
| oauth2_device_code_lifespan |       |
| oauth2_device_polling_interval |       |
| enabled |       |
| ssl_required |       |
| password_credential_grant_allowed |       |
| registration_allowed |       |
| registration_email_as_username |       |
| remember_me |       |
| verify_email |       |
| login_with_email_allowed |       |
| duplicate_emails_allowed |       |
| reset_password_allowed |       |
| edit_username_allowed |       |
| user_cache_enabled |       |
| realm_cache_enabled |       |
| brute_force_protected |       |
| permanent_lockout |       |
| max_temporary_lockouts |       |
| max_failure_wait_seconds |       |
| minimum_quick_login_wait_seconds |       |
| wait_increment_seconds |       |
| quick_login_check_milli_seconds |       |
| max_delta_time_seconds |       |
| failure_factor |       |
| private_key |       |
| public_key |       |
| certificate |       |
| code_secret |       |
| groups |       |
| default_roles |       |
| default_groups |       |
| required_credentials |       |
| password_policy |       |
| otp_policy_type |       |
| otp_policy_algorithm |       |
| otp_policy_initial_counter |       |
| otp_policy_digits |       |
| otp_policy_look_ahead_window |       |
| otp_policy_period |       |
| otp_policy_code_reusable |       |
| otp_supported_applications |       |
| localization_texts |       |
| web_authn_policy_rp_entity_name |       |
| web_authn_policy_signature_algorithms |       |
| web_authn_policy_rp_id |       |
| web_authn_policy_attestation_conveyance_preference |       |
| web_authn_policy_authenticator_attachment |       |
| web_authn_policy_require_resident_key |       |
| web_authn_policy_user_verification_requirement |       |
| web_authn_policy_create_timeout |       |
| web_authn_policy_avoid_same_authenticator_register |       |
| web_authn_policy_acceptable_aaguids |       |
| web_authn_policy_extra_origins |       |
| web_authn_policy_passwordless_rp_entity_name |       |
| web_authn_policy_passwordless_signature_algorithms |       |
| web_authn_policy_passwordless_rp_id |       |
| web_authn_policy_passwordless_attestation_conveyance_preference |       |
| web_authn_policy_passwordless_authenticator_attachment |       |
| web_authn_policy_passwordless_require_resident_key |       |
| web_authn_policy_passwordless_user_verification_requirement |       |
| web_authn_policy_passwordless_create_timeout |       |
| web_authn_policy_passwordless_avoid_same_authenticator_register |       |
| web_authn_policy_passwordless_acceptable_aaguids |       |
| web_authn_policy_passwordless_extra_origins |       |
| users |       |
| federated_users |       |
| scope_mappings |       |
| client_scope_mappings |       |
| clients |       |
| client_scopes |       |
| default_default_client_scopes |       |
| default_optional_client_scopes |       |
| browser_security_headers |       |
| smtp_server |       |
| user_federation_providers |       |
| user_federation_mappers |       |
| login_theme |       |
| account_theme |       |
| admin_theme |       |
| email_theme |       |
| events_enabled |       |
| events_expiration |       |
| events_listeners |       |
| enabled_event_types |       |
| admin_events_enabled |       |
| admin_events_details_enabled |       |
| identity_providers |       |
| identity_provider_mappers |       |
| protocol_mappers |       |
| internationalization_enabled |       |
| supported_locales |       |
| default_locale |       |
| authentication_flows |       |
| authenticator_config |       |
| required_actions |       |
| browser_flow |       |
| registration_flow |       |
| direct_grant_flow |       |
| reset_credentials_flow |       |
| client_authentication_flow |       |
| docker_authentication_flow |       |
| first_broker_login_flow |       |
| attributes |       |
| keycloak_version |       |
| user_managed_access_allowed |       |
| organizations_enabled |       |
| organizations |       |
| verifiable_credentials_enabled |       |
| admin_permissions_enabled |       |
| social |       |
| update_profile_on_initial_social_login |       |
| social_providers |       |
| application_scope_mappings |       |
| applications |       |
| oauth_clients |       |
| client_templates |       |
| o_auth2_device_code_lifespan |       |
| o_auth2_device_polling_interval |       |
| brute_force_strategy_id |       |
| roles_id |       |
| default_role_id |       |
| admin_permissions_client_id |       |
| client_profiles_id |       |
| client_policies_id |       |
| components_id |       |

#### Relationships
- Some node types belong to an `KeycloakRealm`.
    ```
    (:KeycloakRealm)<-[:RESOURCE]-(
        :KeycloakClient,
        :KeycloakGroup,
        :KeycloakUser,
    )


### Client

# FIXME: Add a short description of the node and complete fields description

| Field | Description |
|-------|-------------|
| firstseen| Timestamp of when a sync job first created this node  |
| lastupdated |  Timestamp of the last time the node was updated |
| id |       |
| client_id |       |
| name |       |
| description |       |
| type |       |
| root_url |       |
| admin_url |       |
| base_url |       |
| surrogate_auth_required |       |
| enabled |       |
| always_display_in_console |       |
| client_authenticator_type |       |
| secret |       |
| registration_access_token |       |
| default_roles |       |
| redirect_uris |       |
| web_origins |       |
| not_before |       |
| bearer_only |       |
| consent_required |       |
| standard_flow_enabled |       |
| implicit_flow_enabled |       |
| direct_access_grants_enabled |       |
| service_accounts_enabled |       |
| authorization_services_enabled |       |
| direct_grants_only |       |
| public_client |       |
| frontchannel_logout |       |
| protocol |       |
| attributes |       |
| authentication_flow_binding_overrides |       |
| full_scope_allowed |       |
| node_re_registration_timeout |       |
| registered_nodes |       |
| protocol_mappers |       |
| client_template |       |
| use_template_config |       |
| use_template_scope |       |
| use_template_mappers |       |
| default_client_scopes |       |
| optional_client_scopes |       |
| access |       |
| origin |       |
| authorization_settings_id |       |

#### Relationships
- `KeycloakClient` belongs to a `KeycloakRealm`
    ```
    (:KeycloakClient)-[:RESOURCE]->(:KeycloakRealm)
    ```


### Group

# FIXME: Add a short description of the node and complete fields description

| Field | Description |
|-------|-------------|
| firstseen| Timestamp of when a sync job first created this node  |
| lastupdated |  Timestamp of the last time the node was updated |
| id |       |
| name |       |
| path |       |
| parent_id |       |
| sub_group_count |       |
| sub_groups |       |
| attributes |       |
| realm_roles |       |
| client_roles |       |
| access |       |

#### Relationships
- `KeycloakGroup` belongs to a `KeycloakRealm`
    ```
    (:KeycloakGroup)-[:RESOURCE]->(:KeycloakRealm)
    ```


### User

# FIXME: Add a short description of the node and complete fields description

| Field | Description |
|-------|-------------|
| firstseen| Timestamp of when a sync job first created this node  |
| lastupdated |  Timestamp of the last time the node was updated |
| id |       |
| username |       |
| first_name |       |
| last_name |       |
| email |       |
| email_verified |       |
| attributes |       |
| self |       |
| origin |       |
| created_timestamp |       |
| enabled |       |
| totp |       |
| federation_link |       |
| service_account_client_id |       |
| credentials |       |
| disableable_credential_types |       |
| required_actions |       |
| federated_identities |       |
| realm_roles |       |
| client_roles |       |
| client_consents |       |
| not_before |       |
| application_roles |       |
| social_links |       |
| groups |       |
| access |       |
| user_profile_metadata_id |       |

#### Relationships
- `KeycloakUser` belongs to a `KeycloakRealm`
    ```
    (:KeycloakUser)-[:RESOURCE]->(:KeycloakRealm)
    ```
