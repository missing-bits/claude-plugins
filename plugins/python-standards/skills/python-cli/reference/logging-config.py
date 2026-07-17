# Canonical CLI logging setup — stderr only, stdout stays clean for data.
import logging
import sys


def configure_logging(*, debug: bool = False) -> None:
    """INFO by default; --verbose flips DEBUG and re-enables tracebacks.

    Handlers write to stderr so command output remains pipeable.
    Format stays human-first: a CLI's logs are read live in a terminal,
    not shipped to an aggregator (a service's logging is python-web-api's
    concern).
    """
    level = logging.DEBUG if debug else logging.INFO
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(
        logging.Formatter("%(levelname)s %(name)s: %(message)s")
    )
    root = logging.getLogger()
    root.setLevel(level)
    root.handlers[:] = [handler]

    # Expected failures print one message, not a traceback; --verbose
    # restores full tracebacks for debugging.
    if not debug:
        sys.tracebacklimit = 0
