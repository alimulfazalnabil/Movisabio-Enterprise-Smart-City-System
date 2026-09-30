import enum

class Role(str, enum.Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    CITY_ADMIN = "CITY_ADMIN"
    TRAFFIC_ENGINEER = "TRAFFIC_ENGINEER"
    OPERATOR = "OPERATOR"
    MAINTENANCE = "MAINTENANCE"
    ANALYST = "ANALYST"
    RESEARCHER = "RESEARCHER"
    VIEWER = "VIEWER"
    SERVICE_ACCOUNT = "SERVICE_ACCOUNT"

class Permission(str, enum.Enum):
    READ_TRAFFIC = "READ_TRAFFIC"
    CONTROL_SIGNAL = "CONTROL_SIGNAL"
    ENABLE_AUTONOMOUS_MODE = "ENABLE_AUTONOMOUS_MODE"

ROLE_PERMISSIONS = {
    Role.SUPER_ADMIN: [Permission.READ_TRAFFIC, Permission.CONTROL_SIGNAL, Permission.ENABLE_AUTONOMOUS_MODE],
    Role.CITY_ADMIN: [Permission.READ_TRAFFIC, Permission.CONTROL_SIGNAL],
    Role.TRAFFIC_ENGINEER: [Permission.READ_TRAFFIC, Permission.CONTROL_SIGNAL, Permission.ENABLE_AUTONOMOUS_MODE],
    Role.OPERATOR: [Permission.READ_TRAFFIC, Permission.CONTROL_SIGNAL],
    Role.ANALYST: [Permission.READ_TRAFFIC],
    Role.VIEWER: [Permission.READ_TRAFFIC],
    Role.SERVICE_ACCOUNT: [Permission.READ_TRAFFIC, Permission.CONTROL_SIGNAL]
}

def has_permission(role: Role, permission: Permission) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, [])
