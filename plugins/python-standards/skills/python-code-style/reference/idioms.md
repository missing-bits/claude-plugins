# Idioms — before/after pairs

One pair per rule in SKILL.md.

## style-comprehensions

```python
# Before — loop building a value
names = []
for user in users:
    if user.active:
        names.append(user.name)

# After — a transform is a comprehension
names = [user.name for user in users if user.active]
```

```python
# Before — side effects hidden in a comprehension
[cache.invalidate(key) for key in stale_keys]

# After — effects are a loop
for key in stale_keys:
    cache.invalidate(key)
```

## style-early-return

```python
# Before — arrow code
def process(order):
    if order is not None:
        if order.items:
            if not order.cancelled:
                return ship(order)
    return None

# After — guards first, happy path at the shallowest indent
def process(order):
    if order is None:
        return None
    if not order.items or order.cancelled:
        return None
    return ship(order)
```

## style-eafp

```python
# Before — LBYL race: key checked, then read
if name in config:
    value = config[name]
else:
    value = DEFAULT

# After — the operation reports failure itself
try:
    value = config[name]
except KeyError:
    value = DEFAULT
# (or: value = config.get(name, DEFAULT) when no handling is needed)
```

## style-fstrings

```python
# Before
message = "run %s finished in %d s" % (run_id, elapsed)
message = "run {} finished in {} s".format(run_id, elapsed)

# After
message = f"run {run_id} finished in {elapsed} s"

# Exception — logging stays lazy (ruff G004):
logger.info("run %s finished in %s s", run_id, elapsed)
```

## style-pathlib

```python
# Before
import os
path = os.path.join(base, "profiles", name + ".yaml")
if os.path.exists(path):
    with open(path) as f:
        ...

# After
from pathlib import Path
path = Path(base) / "profiles" / f"{name}.yaml"
if path.exists():
    with path.open() as f:
        ...
```
