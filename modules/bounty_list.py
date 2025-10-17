"""Blood Token bounty list utilities and editable storage."""

from __future__ import annotations

from typing import Callable, Dict, Optional

BLOOD_TOKEN_TEMPLATE = (
    "Bounty List Example Format:\n"
    "Thunderlake | Must kill with knife\n"
    "PlayerName2 | Must say \"there can be only one!\" in chat\n"
    "PlayerName3 | Kill using railgun"
)

_LISTENERS: list[Callable[[Dict[str, Optional[str]]], None]] = []

# Keep a mutable mapping so observers can hold a reference that updates in place.
_BLOOD_TOKEN_TARGETS: Dict[str, Optional[str]] = {
    "Thunderlake": "Must kill with knife",
}


def get_bounty_targets() -> Dict[str, Optional[str]]:
    """Return a shallow copy of the active Blood Token bounty list."""

    return dict(_BLOOD_TOKEN_TARGETS)


def register_listener(callback: Callable[[Dict[str, Optional[str]]], None]) -> None:
    """Register a callback that should run whenever the bounty list changes."""

    if callback in _LISTENERS:
        return
    _LISTENERS.append(callback)


def unregister_listener(callback: Callable[[Dict[str, Optional[str]]], None]) -> None:
    """Remove a previously registered listener, if present."""

    try:
        _LISTENERS.remove(callback)
    except ValueError:
        pass


def set_bounty_targets(new_targets: Dict[str, Optional[str]]) -> None:
    """Replace the active Blood Token list and notify listeners."""

    _BLOOD_TOKEN_TARGETS.clear()
    _BLOOD_TOKEN_TARGETS.update(new_targets)

    snapshot = get_bounty_targets()
    for callback in list(_LISTENERS):
        try:
            callback(snapshot)
        except Exception:
            continue


def parse_bounty_list(raw_text: str) -> Dict[str, Optional[str]]:
    """Parse user-provided bounty text into a mapping."""

    parsed: Dict[str, Optional[str]] = {}

    for line in raw_text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue

        if "|" in stripped:
            name_part, requirement_part = stripped.split("|", 1)
            handle = name_part.strip()
            requirement = requirement_part.strip() or None
        else:
            handle = stripped
            requirement = None

        if not handle:
            continue

        parsed[handle] = requirement

    if not parsed:
        raise ValueError("No valid Blood Token bounty entries were provided.")

    return parsed


def format_bounty_targets(targets: Optional[Dict[str, Optional[str]]] = None) -> str:
    """Format the provided targets (or current list) for display/editing."""

    source = targets if targets is not None else _BLOOD_TOKEN_TARGETS
    lines = []
    for handle, requirement in source.items():
        if requirement:
            lines.append(f"{handle} | {requirement}")
        else:
            lines.append(handle)

    return "\n".join(lines)

