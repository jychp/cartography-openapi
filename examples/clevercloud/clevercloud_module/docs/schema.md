## CleverCloud Schema



### CleverCloudOrganization

#CHANGEME: Add here the description of the entity

| Field | Description |
|-------|-------------|
| firstseen| Timestamp of when a sync job first created this node  |
| lastupdated |  Timestamp of the last time the node was updated |
| id |  |
| name |  |
| description |  |
| billing_email |  |
| address |  |
| city |  |
| zipcode |  |
| country |  |
| company |  |
| vat |  |
| avatar |  |
| vat_state |  |
| customer_full_name |  |
| can_pay |  |
| clever_enterprise |  |
| emergency_number |  |
| can_sepa |  |
| is_trusted |  |

#### Relationships
- Some node types belong to an `CleverCloudOrganization`.
    ```
    (:CleverCloudOrganization)<-[:RESOURCE]-(
        :CleverCloudApplication,
        :CleverCloudAddon,
    )
    ```


### CleverCloudApplication

#CHANGEME: Add here the description of the entity

| Field | Description |
|-------|-------------|
| firstseen| Timestamp of when a sync job first created this node  |
| lastupdated |  Timestamp of the last time the node was updated |
| id |  |
| name |  |
| description |  |
| zone |  |
| zone_id |  |
| creation_date |  |
| last_deploy |  |
| archived |  |
| sticky_sessions |  |
| homogeneous |  |
| favourite |  |
| cancel_on_push |  |
| webhook_url |  |
| webhook_secret |  |
| separate_build |  |
| owner_id |  |
| state |  |
| commit_id |  |
| appliance |  |
| branch |  |
| force_https |  |
| deploy_url |  |
| instance_id | ID of the InstanceView entity |
| deployment_id | ID of the DeploymentInfoView entity |
| vhosts_id | ID of the VhostView entity |
| build_flavor_id | ID of the FlavorView entity |
| env_id | ID of the AddonEnvironmentView entity |

#### Relationships
- `CleverCloudApplication` belongs to a `CleverCloudOrganization`
    ```
    (:CleverCloudApplication)-[:RESOURCE]->(:CleverCloudOrganization)
    ```


### CleverCloudAddon

#CHANGEME: Add here the description of the entity

| Field | Description |
|-------|-------------|
| firstseen| Timestamp of when a sync job first created this node  |
| lastupdated |  Timestamp of the last time the node was updated |
| id |  |
| name |  |
| real_id |  |
| region |  |
| zone_id |  |
| creation_date |  |
| provider_id | ID of the AddonProviderInfoView entity |
| plan_id | ID of the AddonPlanView entity |

#### Relationships
- `CleverCloudAddon` belongs to a `CleverCloudOrganization`
    ```
    (:CleverCloudAddon)-[:RESOURCE]->(:CleverCloudOrganization)
    ```
