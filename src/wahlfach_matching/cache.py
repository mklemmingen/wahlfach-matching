"""File-based timetable cache to avoid re-fetching on subsequent runs."""

from __future__ import annotations

import hashlib
import json
import time as _time
from datetime import date, time
from pathlib import Path

from .config import MatchConfig
from .models import Lesson, Subject


class SubjectCache:
    """Cache aggregated Subject dictionaries to disk as JSON."""

    def __init__(self, cache_dir: str = "output/.cache", ttl_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.ttl_hours = ttl_hours

    def _cache_key(self, config: MatchConfig) -> str:
        """Deterministic hash from (programs, semesters)."""
        raw = json.dumps(
            {"programs": sorted(config.programs), "semesters": sorted(config.semesters)},
            sort_keys=True,
        )
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def _cache_path(self, config: MatchConfig) -> Path:
        return self.cache_dir / f"subjects_{self._cache_key(config)}.json"

    def _manifest_path(self, config: MatchConfig) -> Path:
        return self.cache_dir / f"manifest_{self._cache_key(config)}.json"

    def load(self, config: MatchConfig) -> dict[str, Subject] | None:
        """Return cached subjects if fresh, else None."""
        manifest_path = self._manifest_path(config)
        cache_path = self._cache_path(config)

        if not manifest_path.exists() or not cache_path.exists():
            return None

        with open(manifest_path, encoding="utf-8") as f:
            manifest = json.load(f)

        age_hours = (_time.time() - manifest["timestamp"]) / 3600
        if age_hours > manifest.get("ttl_hours", self.ttl_hours):
            return None

        with open(cache_path, encoding="utf-8") as f:
            raw = json.load(f)

        return _deserialize_subjects(raw)

    def save(self, config: MatchConfig, subjects: dict[str, Subject]) -> None:
        """Serialize subjects dict to JSON with metadata manifest."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        manifest = {
            "timestamp": _time.time(),
            "programs": sorted(config.programs),
            "semesters": sorted(config.semesters),
            "ttl_hours": self.ttl_hours,
        }

        with open(self._manifest_path(config), "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        raw = _serialize_subjects(subjects)
        with open(self._cache_path(config), "w", encoding="utf-8") as f:
            json.dump(raw, f, indent=2, ensure_ascii=False)

    def clear(self) -> None:
        """Remove all cached files."""
        if not self.cache_dir.exists():
            return
        for p in self.cache_dir.iterdir():
            if p.is_file():
                p.unlink()


def _serialize_subjects(subjects: dict[str, Subject]) -> dict:
    """Convert subjects dict to JSON-safe structure."""
    result = {}
    for code, subj in subjects.items():
        result[code] = {
            "code": subj.code,
            "long_name": subj.long_name,
            "alternate_name": subj.alternate_name,
            "groups": sorted(subj.groups),
            "teachers": sorted(subj.teachers),
            "rooms": sorted(subj.rooms),
            "total_occurrences": subj.total_occurrences,
            "weekdays": sorted(subj.weekdays),
            "time_slots": sorted(subj.time_slots),
            "dates": sorted(subj.dates),
            "lessons": [
                {
                    "date": lesson.date.isoformat(),
                    "weekday": lesson.weekday,
                    "start": lesson.start.strftime("%H:%M"),
                    "end": lesson.end.strftime("%H:%M"),
                    "room": lesson.room,
                    "group": lesson.group,
                }
                for lesson in subj.lessons
            ],
        }
    return result


def _deserialize_subjects(raw: dict) -> dict[str, Subject]:
    """Reconstruct Subject dicts from JSON data."""
    subjects: dict[str, Subject] = {}
    for code, data in raw.items():
        lessons = [
            Lesson(
                date=date.fromisoformat(l["date"]),
                weekday=l["weekday"],
                start=time.fromisoformat(l["start"]),
                end=time.fromisoformat(l["end"]),
                room=l.get("room", ""),
                group=l.get("group", ""),
            )
            for l in data["lessons"]
        ]
        subjects[code] = Subject(
            code=data["code"],
            long_name=data.get("long_name", ""),
            alternate_name=data.get("alternate_name", ""),
            groups=set(data.get("groups", [])),
            teachers=set(data.get("teachers", [])),
            rooms=set(data.get("rooms", [])),
            total_occurrences=data.get("total_occurrences", 0),
            weekdays=set(data.get("weekdays", [])),
            time_slots=set(data.get("time_slots", [])),
            dates=set(data.get("dates", [])),
            lessons=lessons,
        )
    return subjects
