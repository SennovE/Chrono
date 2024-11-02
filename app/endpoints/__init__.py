from .user import apiRouter as api_router

list_of_routes = [
    api_router,
]

__all__ = [
    "list_of_routes",
]