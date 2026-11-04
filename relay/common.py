"""Shared helpers for the empire-alerts relay (Mac Mini side).

Stdlib only. Nothing here imports from ~/empire-trading: the relay must keep
working (and keep reporting Empire's health) even when Empire itself is broken.
"""

from __future__ import annotations

import json
import os
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

REPO = Path(os.environ.get("RELAY_REPO", Path(__file__).resolve().parent.parent))
STATE = Path(os.environ.get("RELAY_STATE_DIR", REPO / "state"))
LOGS = REPO / "logs"
CONFIG_PATH = Path(os.environ.get("RELAY_CONFIG", REPO / "config.json"))
ET = ZoneInfo("America/New_York")

DEFAULT_CONFIG = {
    "recipient": "",                 # your phone/Apple ID; lives ONLY in gitignored config.json
    "prefix": "Claude · ",           # so you can tell relay texts from Empire's own
    "quiet_start": 23,               # 11 PM ET
    "quiet_end": 8,                  # 8 AM ET
    "max_per_hour": 6,
    "max_per_day": 25,
    "max_per_run": 3,
    "max_age_hours": 24,             # default expiry when an alert has no expires_at
    "max_text_chars": 1500,
    "empire_dir": "~/empire-trading",
    "empire_api": "http://127.0.0.1:5050",
    "handoff_path": "~/ObsidianVault/OpenClaw/cetera-income/handoff/current_positions.json",
}


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def load_config() -> dict:
    cfg = dict(DEFAULT_CONFIG)
    try:
        cfg.update(json.loads(CONFIG_PATH.read_text()))
    except FileNotFoundError:
        pass
    env = os.environ.get("RELAY_RECIPIENT")
    if env:
        cfg["recipient"] = env
    return cfg


def log(name: str, msg: str) -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now(ET):%Y-%m-%d %H:%M:%S} {msg}"
    with open(LOGS / f"{name}.log", "a") as f:
        f.write(line + "\n")
    print(line)


def read_json(path: Path, default):
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def write_json_atomic(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + f".{os.getpid()}.tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, path)


class RepoLock:
    """mkdir lock shared by the sender and the snapshot publisher, so the two
    never run git at the same moment. A stale lock (>10 min) is stolen."""

    def __init__(self, timeout: float = 90):
        self.path = STATE / ".git.lock"
        self.timeout = timeout

    def __enter__(self):
        STATE.mkdir(parents=True, exist_ok=True)
        start = time.time()
        while True:
            try:
                self.path.mkdir()
                return self
            except FileExistsError:
                try:
                    if time.time() - self.path.stat().st_mtime > 600:
                        self.path.rmdir()
                        continue
                except FileNotFoundError:
                    continue
                if time.time() - start > self.timeout:
                    raise TimeoutError("relay repo lock busy")
                time.sleep(2)

    def __exit__(self, *exc):
        try:
            self.path.rmdir()
        except FileNotFoundError:
            pass


def git(*args: str, timeout: int = 60) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(REPO), *args],
        capture_output=True, text=True, timeout=timeout,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
    )
