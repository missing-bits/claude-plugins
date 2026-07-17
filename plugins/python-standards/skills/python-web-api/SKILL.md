---
name: python-web-api
description: Use when building or extending a FastAPI web service — router, service, and repository layering, pydantic request and response models, async boundaries, and HTTP error handling.
---

# Python web APIs (FastAPI)

Tightly scoped to FastAPI services. Cite rules in review findings as
`(standard: python-web-api, rule: <id>)`.

## Layering

`router → service → repository`, dependencies point one way only:

| Layer | Owns | May import |
|---|---|---|
| router | HTTP: paths, status codes, request/response models, DI wiring | service |
| service | business logic, transactions, domain rules | repository, domain types |
| repository | data access (DB, external APIs) | domain types, drivers |

- FastAPI dependency injection (`Depends`) lives at the **router layer
  only** — services receive plain arguments, so they test without HTTP.
- A router importing a repository, or a service importing `fastapi`,
  fails review. Worked example:
  [reference/layering.py](reference/layering.py).
(id: `web-layering`)

## pydantic v2 models

- Request and response models are **separate classes from domain
  objects** — API shape and domain shape evolve independently.
- Validation happens at the boundary (pydantic on the way in); inside
  the service layer, data is already trusted and typed.
- Response models are declared on the route (`response_model=`), so
  accidental field leaks are impossible.
(id: `web-boundary-models`)

## Async boundaries

- Route handlers are `async def` (PEP 492 coroutines); **no blocking IO
  inside an async path**. The named offenders: sync HTTP clients
  (`requests`), `time.sleep`, unpooled/sync DB drivers, blocking file
  IO on large files.
- Genuinely sync work (CPU-bound, legacy driver) is offloaded:
  `run_in_threadpool` / `asyncio.to_thread`, or the handler is honest
  and declared plain `def` (FastAPI threads it).
(id: `web-async-boundaries`)

## HTTP error handling

- Domain exceptions map to statuses in ONE place — exception handlers
  registered on the app; routes and services never build
  `HTTPException` from business logic.
- Every error response is an **RFC 9457 Problem Details** document
  (`Content-Type: application/problem+json`): `type` (a stable URI
  reference — relative `/errors/<slug>` is fine until external
  consumers need dereferenceable docs), `title`, `status`, `detail`,
  plus our extension member `code` — the short machine-readable slug
  clients switch on. Model and wiring in
  [reference/error-handling.py](reference/error-handling.py).
- Stack traces never reach a response body; they go to the log with the
  request id.
(id: `web-error-envelope`)

## Review severities

- Critical: blocking IO in an async path under load
  (`web-async-boundaries` — it stalls the event loop for every request).
- Important: layering violations, stack traces in responses, missing
  `response_model`.
- Minor: everything else in this skill.
