import hashlib
import json
from typing import Any, Dict


def deterministic_hash(payload: Dict[str, Any]) -> str:
    """
    Compute a deterministic hash of inputs.
    Assumes payload is JSON-serializable and order-independent.
    """
    encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
