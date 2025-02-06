## CleverCloud Schema

.. _clevercloud_schema:


### Organization

# FIXME: Add a short description of the node and complete fields description

| Field | Description |
|-------|-------------|
| firstseen| Timestamp of when a sync job first created this node  |
| lastupdated |  Timestamp of the last time the node was updated |
| id |       |
| name |       |
| description |       |
| billing_email |       |
| address |       |
| city |       |
| zipcode |       |
| country |       |
| company |       |
| vat |       |
| avatar |       |
| vat_state |       |
| customer_full_name |       |
| can_pay |       |
| clever_enterprise |       |
| emergency_number |       |
| can_sepa |       |
| is_trusted |       |

#### Relationships
- Some node types belong to an `CleverCloudOrganization`.
    ```
    (:CleverCloudOrganization)<-[:RESOURCE]-(
        :CleverCloudApplication,
        :CleverCloudAddon,
    )


### Application

# FIXME: Add a short description of the node and complete fields description

| Field | Description |
|-------|-------------|
| firstseen| Timestamp of when a sync job first created this node  |
| lastupdated |  Timestamp of the last time the node was updated |
| id |       |
| name |       |
| description |       |
| zone |       |
| zone_id |       |
| vhosts |       |
| creation_date |       |
| last_deploy |       |
| archived |       |
| sticky_sessions |       |
| homogeneous |       |
| favourite |       |
| cancel_on_push |       |
| webhook_url |       |
| webhook_secret |       |
| separate_build |       |
| owner_id |       |
| state |       |
| commit_id |       |
| appliance |       |
| branch |       |
| force_https |       |
| env |       |
| deploy_url |       |
| instance_id |       |
| deployment_id |       |
| build_flavor_id |       |

#### Relationships
- `CleverCloudApplication` belongs to a `CleverCloudOrganization`
    ```
    (:CleverCloudApplication)-[:RESOURCE]->(:CleverCloudOrganization)
    ```


### Addon

# FIXME: Add a short description of the node and complete fields description

| Field | Description |
|-------|-------------|
| firstseen| Timestamp of when a sync job first created this node  |
| lastupdated |  Timestamp of the last time the node was updated |
| id |       |
| name |       |
| real_id |       |
| region |       |
| zone_id |       |
| creation_date |       |
| config_keys |       |
| provider_id |       |
| plan_id |       |

#### Relationships
- `CleverCloudAddon` belongs to a `CleverCloudOrganization`
    ```
    (:CleverCloudAddon)-[:RESOURCE]->(:CleverCloudOrganization)
    ```
