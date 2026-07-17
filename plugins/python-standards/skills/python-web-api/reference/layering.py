# Router → service → repository for one resource, in one file for
# readability — in a real project each layer is its own module
# (see python-project-layout for the tree).
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel


# --- repository: data access only; knows nothing about HTTP or rules ---
class ProfileRepository:
    async def get(self, name: str) -> ProfileRecord | None: ...
    async def save(self, record: ProfileRecord) -> None: ...


# --- service: business rules; plain arguments, no fastapi import ---
class ProfileService:
    def __init__(self, repo: ProfileRepository) -> None:
        self._repo = repo

    async def rename(self, old: str, new: str) -> ProfileRecord:
        record = await self._repo.get(old)
        if record is None:
            raise ProfileNotFoundError(old)     # domain exception —
        record.name = new                        # mapping to HTTP happens
        await self._repo.save(record)            # in the exception handler
        return record


# --- router: HTTP only; DI wiring lives HERE and nowhere deeper ---
router = APIRouter(prefix="/profiles")


class RenameRequest(BaseModel):                  # request model ≠ domain object
    new_name: str


class ProfileResponse(BaseModel):                # response model ≠ domain object
    name: str
    fps: int


def get_service() -> ProfileService:             # composition root for DI
    return ProfileService(ProfileRepository())


@router.post("/{name}/rename", response_model=ProfileResponse)
async def rename_profile(
    name: str,
    body: RenameRequest,
    service: Annotated[ProfileService, Depends(get_service)],
) -> ProfileResponse:
    record = await service.rename(name, body.new_name)
    return ProfileResponse(name=record.name, fps=record.fps)
