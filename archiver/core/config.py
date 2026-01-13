"""Configuration management for the archiver."""

import json
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT_DIR = Path.home() / "Desktop" / "content archiver"
ARCHIVER_DIR = DEFAULT_OUTPUT_DIR / ".archiver"
CONFIG_FILE = ARCHIVER_DIR / "config.json"
DATABASE_FILE = ARCHIVER_DIR / "archive.db"

DEFAULT_CONFIG = {
    "output_dir": str(DEFAULT_OUTPUT_DIR),
    "rate_limit_per_second": 1.0,
    "youtube_quality": "best",
    "download_thumbnails": True,
}


def ensure_dirs() -> None:
    """Ensure the archiver directories exist."""
    DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVER_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> dict[str, Any]:
    """Load configuration from file, or return defaults."""
    ensure_dirs()
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE) as f:
                config = json.load(f)
                return {**DEFAULT_CONFIG, **config}
        except json.JSONDecodeError:
            pass
    return DEFAULT_CONFIG.copy()


def save_config(config: dict[str, Any]) -> None:
    """Save configuration to file."""
    ensure_dirs()
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def get_output_dir() -> Path:
    """Get the output directory path."""
    config = load_config()
    return Path(config["output_dir"])
