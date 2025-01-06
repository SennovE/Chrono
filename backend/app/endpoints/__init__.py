from .auth import api_router as auth_router
from .healh_check import api_router as healh_check_router
from .user import api_router as user_debag
from .task import api_router as task_router

list_of_routes = [
    auth_router,
    healh_check_router,
    user_debag,
    task_router,
]

__all__ = [
    "list_of_routes",
]