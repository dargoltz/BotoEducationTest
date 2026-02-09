import uuid

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import HttpUrl

app = FastAPI()


@app.post("/shorten", response_model=uuid.UUID, description="Make short redirect link")
async def add_link(link: HttpUrl) -> uuid.UUID:
    """В качестве короткой ссылки и ключа для доступа к ссылке будет использоваться uuid."""
    ...  # todo implement


@app.get("/{link_id:uuid}", response_model=RedirectResponse, description="Redirect to original link")
async def redirect_to_link(link_id: uuid.UUID) -> RedirectResponse:
    return RedirectResponse(
        url=...,  # todo implement
        status_code=301
    )
