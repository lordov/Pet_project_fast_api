from src.api.users.router import router as users_router
from src.api.tasks.router import router_task as tasks_router
from src.api.auth.router import router as auth_router


all_routers = [
    auth_router,
    users_router,
    tasks_router,
]
