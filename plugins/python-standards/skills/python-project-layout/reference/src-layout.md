# src layout — canonical tree and boundary examples

## The tree

```
example-tool/
├── pyproject.toml          # single manifest (see reference/pyproject.toml)
├── uv.lock                 # committed
├── README.md
├── src/
│   └── example_tool/       # the ONE importable package
│       ├── __init__.py
│       ├── cli.py          # entry point target ([project.scripts])
│       ├── config.py
│       └── profiles/       # subpackage per cohesive area
│           ├── __init__.py
│           └── loader.py
└── tests/                  # beside src/, never inside the package
    ├── conftest.py
    └── test_profiles.py
```

## Boundary example — keep together

`profiles/loader.py` parses profile files AND validates them. Both jobs
serve the same audience (every caller wants a validated profile), share
the same vocabulary, and change together when the format changes. Two
modules here would couple tighter than one.

## Boundary example — split now

`cli.py` has grown a `retry_with_backoff()` helper that `stages.py` now
imports. The helper serves a second audience and has nothing to do with
argument parsing — move it to `retry.py`. Signals: a caller imports the
module for something unrelated to its name; the module's top-level names
no longer fit one sentence.
