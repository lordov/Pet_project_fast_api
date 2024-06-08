import uvicorn
from fastapi import FastAPI

from api.router import all_routers

app = FastAPI(
    title="FastAPI project",
)


for router in all_routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app="src.main:app", reload=True)
