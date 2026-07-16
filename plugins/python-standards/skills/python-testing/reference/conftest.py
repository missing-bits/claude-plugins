# Annotated example conftest.py — one fixture per scope pattern.
import pytest


# Function-scope FACTORY (the default pattern): each test builds exactly
# the object it cares about; overrides keep irrelevant fields out of the
# test body.
@pytest.fixture
def make_profile():
    def _make(**overrides):
        defaults = {"name": "dji-default", "fps": 30, "lut": None}
        return Profile(**{**defaults, **overrides})

    return _make


# Session-scope RESOURCE: expensive and read-only — safe to share.
# Anything mutable at this scope is test pollution.
@pytest.fixture(scope="session")
def sample_footage_dir(tmp_path_factory):
    root = tmp_path_factory.mktemp("footage")
    (root / "clip001.mp4").write_bytes(b"\x00" * 16)
    return root


# autouse — RARE, and only with a reason every test genuinely needs:
# here, no test may ever touch the real user config.
@pytest.fixture(autouse=True)
def isolate_user_config(monkeypatch, tmp_path):
    monkeypatch.setenv("EXAMPLE_TOOL_CONFIG", str(tmp_path / "config.yaml"))
