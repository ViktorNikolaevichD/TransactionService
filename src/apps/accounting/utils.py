import hashlib
from typing import Any

from config import settings


def verify_signature(data: dict[str, Any]) -> bool:
    data = data.copy()
    sign = data.pop("signature")
    sorted_keys = sorted(data.keys())

    concat_str = "".join(str(data[key]) for key in sorted_keys) + settings.SECRET_KEY
    calc_hash = hashlib.sha256(concat_str.encode()).hexdigest()

    return sign == calc_hash
