# Annotated example tests.
import pytest


# Parametrized: SAME behavior over different inputs, ids name the case.
@pytest.mark.parametrize(
    ("filename", "expected"),
    [
        ("clip.mp4", "video"),
        ("clip.MP4", "video"),
        ("photo.jpg", "image"),
    ],
    ids=["lowercase-video", "uppercase-video", "image"],
)
def test_media_kind_from_extension(filename, expected):
    assert media_kind(filename) == expected


# Fixture-consuming test: the factory keeps irrelevant fields out.
def test_lut_applies_only_when_configured(make_profile):
    profile = make_profile(lut="d-log-to-rec709")
    assert profile.needs_lut()


# Exception assertion: pytest.raises with match pins the failure mode,
# not just the exception type.
def test_missing_profile_raises():
    registry = ProfileRegistry([])
    with pytest.raises(ProfileNotFoundError, match="gopro-13"):
        registry.get("gopro-13")
