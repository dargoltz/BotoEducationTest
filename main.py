import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import HttpUrl

from db import init_db, get_link_by_id, add_link_to_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/shorten", response_model=uuid.UUID, description="Make short redirect link")
async def add_link(link: HttpUrl) -> uuid.UUID:
    """В качестве короткой ссылки и ключа для доступа к ссылке будет использоваться uuid."""
    return add_link_to_db(link)


@app.get("/{link_id:uuid}", response_model=RedirectResponse, description="Redirect to original link")
async def redirect_to_link(link_id: uuid.UUID) -> RedirectResponse:
    return RedirectResponse(
        url=get_link_by_id(link_id),
        status_code=301
    )
