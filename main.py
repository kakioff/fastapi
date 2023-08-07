from typing import Any, Union
from fastapi import FastAPI, Depends, Request, Header, status
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from pydantic import BaseModel, EmailStr
import redis.asyncio as redis
from ipaddress import ip_address
from models import SendData
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



import routers
app.include_router(routers.router)

from routers import websocket
@app.on_event("startup")
async def startup():
    r = redis.from_url(
        "redis://localhost:6379", encoding="utf-8", decode_responses=True
    )
    await FastAPILimiter.init(r)

class IndexModel:
    ip: str
    ua: str

@app.get("/", dependencies=[Depends(RateLimiter(times=50, seconds=1))])
def index_page(request: Request, user_agent:Union[str, None] = Header(default=None)):
    response = IndexModel()
    response.ip = request.client.host
    response.ua = user_agent or ""
    return response
