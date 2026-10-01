import enum

class Permission(str, enum.Enum):
    # Traffic
    TRAFFIC_READ = "traffic.read"
    TRAFFIC_ANALYZE = "traffic.analyze"
    TRAFFIC_OPTIMIZE = "traffic.optimize"
    TRAFFIC_CONTROL = "traffic.control"
    TRAFFIC_OVERRIDE = "traffic.override"
    
    # Infrastructure
    DEVICE_READ = "device.read"
    DEVICE_CONFIGURE = "device.configure"
    DEVICE_RESTART = "device.restart"
    DEVICE_COMMAND = "device.command"
    
    # AI/ML
    MODEL_READ = "model.read"
    MODEL_TRAIN = "model.train"
    MODEL_DEPLOY = "model.deploy"
    MODEL_ROLLBACK = "model.rollback"
    EXPERIMENT_CREATE = "experiment.create"
    EXPERIMENT_RUN = "experiment.run"
    
    # Digital Twin
    DIGITAL_TWIN_READ = "digital_twin.read"
    DIGITAL_TWIN_CREATE = "digital_twin.create"
    DIGITAL_TWIN_UPDATE = "digital_twin.update"
    DIGITAL_TWIN_SIMULATE = "digital_twin.simulate"
    
    # IoT
    IOT_READ = "iot.read"
    IOT_CONFIGURE = "iot.configure"
    IOT_COMMAND = "iot.command"
    IOT_FIRMWARE_UPDATE = "iot.firmware_update"
    
    # Administration
    USERS_READ = "users.read"
    USERS_MANAGE = "users.manage"
    ROLES_READ = "roles.read"
    ROLES_MANAGE = "roles.manage"
    TENANT_MANAGE = "tenant.manage"
    ORGANIZATION_MANAGE = "organization.manage"
    
    # Commercial
    BILLING_READ = "billing.read"
    BILLING_MANAGE = "billing.manage"
    SUBSCRIPTION_MANAGE = "subscription.manage"
    USAGE_READ = "usage.read"
    
    # Security
    AUDIT_READ = "audit.read"
    SECURITY_MANAGE = "security.manage"
    API_KEY_MANAGE = "api_key.manage"

# Predefined Role Templates (Collections of Permissions)
ROLE_PERMISSIONS = {
    "Viewer": {
        Permission.TRAFFIC_READ,
        Permission.DEVICE_READ,
        Permission.MODEL_READ,
        Permission.DIGITAL_TWIN_READ,
        Permission.IOT_READ
    },
    "Traffic Operator": {
        Permission.TRAFFIC_READ,
        Permission.TRAFFIC_ANALYZE,
        Permission.TRAFFIC_OPTIMIZE,
        Permission.TRAFFIC_CONTROL,
        Permission.DEVICE_READ
    },
    "Traffic Manager": {
        Permission.TRAFFIC_READ,
        Permission.TRAFFIC_ANALYZE,
        Permission.TRAFFIC_OPTIMIZE,
        Permission.TRAFFIC_CONTROL,
        Permission.DEVICE_READ,
        Permission.DEVICE_CONFIGURE,
        Permission.USERS_READ
    },
    "City Admin": {
        # Full tenant scope except platform/billing root
        Permission.TRAFFIC_READ, Permission.TRAFFIC_ANALYZE, Permission.TRAFFIC_OPTIMIZE, Permission.TRAFFIC_CONTROL, Permission.TRAFFIC_OVERRIDE,
        Permission.DEVICE_READ, Permission.DEVICE_CONFIGURE, Permission.DEVICE_RESTART, Permission.DEVICE_COMMAND,
        Permission.USERS_READ, Permission.USERS_MANAGE,
        Permission.ROLES_READ, Permission.AUDIT_READ,
        Permission.API_KEY_MANAGE, Permission.TENANT_MANAGE
    },
    "AI/ML Engineer": {
        Permission.MODEL_READ, Permission.MODEL_TRAIN, Permission.MODEL_DEPLOY, Permission.MODEL_ROLLBACK,
        Permission.EXPERIMENT_CREATE, Permission.EXPERIMENT_RUN, Permission.TRAFFIC_READ
    },
    "Auditor": {
        Permission.AUDIT_READ, Permission.TRAFFIC_READ, Permission.USERS_READ, Permission.ROLES_READ, Permission.BILLING_READ
    }
}
