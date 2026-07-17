# Exception classes, handler wiring, and the RFC 9457 Problem Details
# response — the ONE place domain failures become HTTP statuses.
# Every error body is application/problem+json: type, title, status,
# detail (RFC members) plus `code` (our extension member — the short
# machine-readable slug clients switch on).
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

logger = logging.getLogger(__name__)

PROBLEM_JSON = "application/problem+json"


# --- domain exceptions: raised by services, no HTTP knowledge ---
class DomainError(Exception):
    code = "domain_error"
    title = "Domain error"


class ProfileNotFoundError(DomainError):
    code = "profile_not_found"
    title = "Profile not found"

    def __init__(self, name: str) -> None:
        super().__init__(f"profile '{name}' does not exist")


# --- RFC 9457 Problem Details + the `code` extension member ---
class Problem(BaseModel):
    # Relative URI reference is valid per the RFC; point it at real,
    # dereferenceable documentation once external consumers appear.
    type: str
    title: str
    status: int
    detail: str
    code: str  # extension member: stable slug for machine handling


STATUS_BY_EXCEPTION: dict[type[DomainError], int] = {
    ProfileNotFoundError: 404,
}


def problem_response(*, status: int, title: str, detail: str, code: str) -> JSONResponse:
    problem = Problem(
        type=f"/errors/{code.replace('_', '-')}",
        title=title,
        status=status,
        detail=detail,
        code=code,
    )
    return JSONResponse(
        status_code=status,
        content=problem.model_dump(),
        media_type=PROBLEM_JSON,
    )


def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
        status = STATUS_BY_EXCEPTION.get(type(exc), 400)
        return problem_response(
            status=status, title=exc.title, detail=str(exc), code=exc.code
        )

    @app.exception_handler(Exception)
    async def unexpected_error_handler(request: Request, exc: Exception) -> JSONResponse:
        # The traceback goes to the LOG with request context — never to the body.
        logger.exception("unhandled error on %s %s", request.method, request.url.path)
        return problem_response(
            status=500,
            title="Internal server error",
            detail="internal server error",
            code="internal_error",
        )
