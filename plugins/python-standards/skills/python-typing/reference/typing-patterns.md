# Typing patterns — worked examples

## Protocol vs ABC for the same seam

The seam: pipeline stages that process a clip.

```python
# Protocol — you own the call site; anyone can provide a stage
from typing import Protocol

class Stage(Protocol):
    name: str
    def run(self, clip: Clip) -> Clip: ...

def run_pipeline(stages: Iterable[Stage], clip: Clip) -> Clip:
    for stage in stages:
        clip = stage.run(clip)
    return clip
# Third-party stages need no import from us — matching shape suffices.
```

```python
# ABC — you own the hierarchy and enforce an invariant in the base
from abc import ABC, abstractmethod

class Stage(ABC):
    def run(self, clip: Clip) -> Clip:
        self._validate(clip)          # shared invariant, enforced once
        return self._process(clip)

    @abstractmethod
    def _process(self, clip: Clip) -> Clip: ...
# Right when every implementation lives in this codebase and must
# inherit the validation.
```

## A generic function

```python
def first_matching[T](items: Iterable[T], pred: Callable[[T], bool]) -> T | None:
    for item in items:
        if pred(item):
            return item
    return None
```

## TypedDict vs model

```python
# TypedDict — shaping data you do NOT own (a parsed JSON payload
# passing through, no behavior, no validation on construction):
class ProfileRow(TypedDict):
    name: str
    fps: int

# pydantic model — data crossing a trust boundary that must be
# validated (API input, config files) — see python-web-api for API use:
class Profile(BaseModel):
    name: str
    fps: int = Field(gt=0)
```

## Narrowing

```python
def describe(value: int | str | None) -> str:
    if value is None:            # narrows to int | str below
        return "empty"
    if isinstance(value, int):   # narrows to int
        return f"number {value}"
    return value.upper()         # str — no cast needed

# assert-based narrowing at internal boundaries where None is a bug:
profile = registry.get(name)
assert profile is not None, f"unregistered profile: {name}"
profile.apply()                  # narrowed to Profile
```
