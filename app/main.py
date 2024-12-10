from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.events import router as events_router
from app.routers.rooms import router as rooms_router
from config.database import create_tables
from config.settings import MIDDLEWARE


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="Tango Recruitment App",
    description="This application was made as part of Tango recruitment process.",
    lifespan=lifespan,
)

for middleware in MIDDLEWARE:
    app.add_middleware(middleware[0], **middleware[1])


app.include_router(auth_router)
app.include_router(events_router)
app.include_router(rooms_router)
