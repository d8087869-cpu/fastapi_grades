roles = {
    "GUEST": ["GET"],
    "USER": ["GET", "POST"],
    "MANAGER": ["GET", "POST", "PUT"],
    "ADMIN": ["GET", "POST", "PUT", "DELETE"]}


def has_permission(user_type, method):
    return method in roles[user_type]