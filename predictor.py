"""Local shim for Nitro-style pre-judging scripts.

The real contest platform provides ``predictor.exchange``.  Locally we emulate
the small part of that API needed by pre-judging scripts:

* ``exchange(b"")`` returns the raw bytes of ``submission.pkl``.
* ``exchange(request_bytes)`` loads ``submission.pkl`` and calls it if it is a
  callable object, returning the callable's bytes response.

This file does not know any task-specific protocol.  The submission itself must
understand the request bytes produced by the corresponding pre-judging script.
"""

from __future__ import annotations

from pathlib import Path
import os
import pickle
from typing import Any

try:
    import cloudpickle
except ImportError:  # pragma: no cover - fallback for very small local envs
    cloudpickle = pickle


_SUBMISSION: Any = None


def _submission_path() -> Path:
    """Return the local submission path.

    Set your path to point at a different file when a task uses
    another package name or when several submissions are in one folder.
    """
    configured = os.environ.get("")
    if configured:
        return Path(configured)

    candidates = [
        Path("submission.pkl"),
        Path("submission.zip"),
        Path("submission.pt"),
        Path("submission.pth"),
        Path("submission.onnx"),
        Path("submission.npy"),
        Path("submission.npz"),
        Path("submission"),
    ]
    existing = [path for path in candidates if path.is_file()]
    if len(existing) == 1:
        return existing[0]
    if len(existing) > 1:
        names = ", ".join(str(path) for path in existing)
        raise RuntimeError(
            "Several local submission files found. Set "
            f"PREDICTOR_SUBMISSION_PATH explicitly. Candidates: {names}"
        )
    return Path("submission.pkl")


def _load_submission() -> Any:
    global _SUBMISSION
    if _SUBMISSION is None:
        path = _submission_path()
        with path.open("rb") as f:
            _SUBMISSION = cloudpickle.load(f)
    return _SUBMISSION


def exchange(payload: bytes) -> bytes:
    """Local replacement for the platform's byte-in/byte-out exchange API."""
    if not isinstance(payload, (bytes, bytearray)):
        raise TypeError(f"exchange payload must be bytes, got {type(payload).__name__}")

    path = _submission_path()

    # Many data-task scorers call exchange(b"") to fetch uploaded raw bytes.
    if bytes(payload) == b"":
        return path.read_bytes()

    submission = _load_submission()
    if not callable(submission):
        raise TypeError(
            "Non-empty exchange payload requires a callable submission.pkl. "
            f"Loaded object type: {type(submission).__name__}"
        )

    response = submission(bytes(payload))
    if not isinstance(response, (bytes, bytearray)):
        raise TypeError(
            "Callable submission must return bytes from exchange requests. "
            f"Got: {type(response).__name__}"
        )
    return bytes(response)
