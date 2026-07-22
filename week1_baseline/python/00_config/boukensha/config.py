from __future__ import annotations

import os
import tomllib
from pathlib import Path

from dotenv import load_dotenv


class Config:
    """The single source of truth for all settings.

    Resolves the .boukensha config directory in this order:
      1. BOUKENSHA_DIR environment variable
      2. ~/.boukensha (default)
    """

    DEFAULT_DIR = Path.home() / ".boukensha"
    PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

    def __init__(self) -> None:
        self.dir = self._resolve_dir()
        self._load_env()
        self.settings = self._load_settings()

    # ---------- tasks -----------------------------------------------------

    def tasks(self, name: str | None = None) -> dict | None:
        all_tasks = self.dig("tasks") or {}
        return all_tasks.get(name) if name else all_tasks

    @property
    def user_prompts_dir(self) -> Path:
        return self.dir / "prompts"

    # ---------- MUD connection ---------------------------------------------

    @property
    def mud_host(self) -> str:
        return self.dig("mud", "host") or "localhost"

    @property
    def mud_port(self) -> int:
        return self.dig("mud", "port") or 4000

    @property
    def mud_username(self) -> str | None:
        return self.dig("mud", "username")

    @property
    def mud_password(self) -> str | None:
        return self.dig("mud", "password")

    # ---------- low-level helpers -------------------------------------------

    def dig(self, *keys: str):
        node = self.settings
        for key in keys:
            if not isinstance(node, dict):
                return None
            node = node.get(key)
        return node

    def __repr__(self) -> str:
        task_names = ",".join((self.tasks() or {}).keys())
        return f"<Config dir={self.dir} tasks={task_names}>"

    def _resolve_dir(self) -> Path:
        raw = os.environ.get("BOUKENSHA_DIR") or str(self.DEFAULT_DIR)
        return Path(raw).expanduser().resolve()

    def _load_env(self) -> None:
        env_file = self.dir / ".env"
        if env_file.exists():
            load_dotenv(env_file)

    def _load_settings(self) -> dict:
        settings_file = self.dir / "settings.toml"
        if settings_file.exists():
            with settings_file.open("rb") as f:
                return tomllib.load(f)
        return {}
