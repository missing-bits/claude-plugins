# Exception classes, handler wiring, and the error envelope — the ONE
# place domain failures become HTTP statuses.
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

logger = logging.getLogger(__name__)


# --- domain exceptions: raised by services, no HTTP knowledge ---
class DomainError(Exception):
    code = "domain_error"


class ProfileNotFoundError(DomainError):
    code = "profile_not_found"

    def __init__(self, name: str) -> None:
        super().__init__(f"profile '{name}' does not exist")


# --- the envelope: every error response has exactly this shape ---
class ErrorBody(BaseModel):
    code: str
    message: str


class ErrorEnvelope(BaseModel):
    error: ErrorBody


STATUS_BY_EXCEPTION: dict[type[DomainError], int] = {
    ProfileNotFoundError: 404,
}


def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
        status = STATUS_BY_EXCEPTION.get(type(exc), 400)
        envelope = ErrorEnvelope(error=ErrorBody(code=exc.code, message=str(exc)))
        return JSONResponse(status_code=status, content=envelope.model_dump())

    @app.exception_handler(Exception)
    async def unexpected_error_handler(request: Request, exc: Exception) -> JSONResponse:
        # The traceback goes to the LOG with request context — never to the body.
        logger.exception("unhandled error on %s %s", request.method, request.url.path)
        envelope = ErrorEnvelope(
            error=ErrorBody(code="internal_error", message="internal server error")
        )
        return JSONResponse(status_code=500, content=envelope.model_dump())
