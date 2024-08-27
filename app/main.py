from contextlib import asynccontextmanager
from datetime import date
import time
from typing import Optional
from app.prometheus.router import router as router_prometheus
from fastapi import FastAPI, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from app.users.router import router as router_users
from app.logger import logger
from fastapi import FastAPI
import sentry_sdk
from fastapi_versioning import VersionedFastAPI

sentry_sdk.init(
    dsn="https://1abc04bfac496a0f5cfa28988f3a18c0@o4507840651919360.ingest.de.sentry.io/4507840663126096",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

@asynccontextmanager
async def lifespan(_: FastAPI):
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield

app = FastAPI(lifespan=lifespan)       
 


app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_pages)
app.include_router(router_hotels)
app.include_router(router_images)
app.include_router(router_prometheus)    


app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}',
#     description='Greet users with a nice message',
#     middleware=[
#         Middleware(SessionMiddleware, secret_key='mysecretkey')
#     ]
)


instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)
instrumentator.instrument(app).expose(app)

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)   
admin.add_view(BookingsAdmin)    
admin.add_view(RoomsAdmin)
admin.add_view(HotelsAdmin)

app.mount("/static", StaticFiles(directory="app/static"), "static")

