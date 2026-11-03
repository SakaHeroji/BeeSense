"""Storage settings shared with the frontend; DSNs stay in server environment."""

import re
from copy import deepcopy

DEFAULT_STORAGE = {
    "destination": "excel",
    "postgresql": {
        "host": "127.0.0.1",
        "port": 5432,
        "connection_string_env": "BEESENSE_POSTGRESQL_DSN",
    },
}


def storage_config(value=None):
    cfg = deepcopy(DEFAULT_STORAGE)
    if value is None:
        return cfg
    if not isinstance(value, dict) or set(value) - set(cfg):
        raise ValueError("Unknown storage settings")
    postgres = value.get("postgresql", {})
    if not isinstance(postgres, dict) or set(postgres) - set(cfg["postgresql"]):
        raise ValueError(
            "PostgreSQL settings accept host, port and connection_string_env"
        )
    cfg.update({key: val for key, val in value.items() if key != "postgresql"})
    cfg["postgresql"].update(postgres)
    if cfg["destination"] not in {"excel", "postgresql", "both"}:
        raise ValueError("storage.destination must be excel, postgresql or both")
    p = cfg["postgresql"]
    if not isinstance(p["host"], str) or not re.fullmatch(
        r"[A-Za-z0-9_.:\[\]-]{1,253}", p["host"]
    ):
        raise ValueError(
            "PostgreSQL host must be an IP address or hostname without credentials"
        )
    if type(p["port"]) is not int or not 1 <= p["port"] <= 65535:
        raise ValueError("PostgreSQL port must be 1..65535")
    if not isinstance(p["connection_string_env"], str) or not re.fullmatch(
        r"[A-Z_][A-Z0-9_]{0,127}", p["connection_string_env"]
    ):
        raise ValueError(
            "Use a server environment variable for the PostgreSQL connection string"
        )
    return cfg


def require_excel_storage(config):
    if config["storage"]["destination"] != "excel":
        raise ValueError(
            "PostgreSQL storage requires the Crawler HTTP service. The standalone CLI currently writes Excel only."
        )
