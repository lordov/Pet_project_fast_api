from api.endpoints.users.router import router as users_router
from api.endpoints.tasks.router import router_task as tasks_router
from api.endpoints.auth.router import router as auth_router


all_routers = [
    auth_router,
    users_router,
    tasks_router,
]
