"""Domain models for the elective matching optimizer."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time


@dataclass(frozen=True)
class TimeSlot:
    """A single time slot in the weekly schedule."""
    weekday: str  # e.g. "Monday"
    start: time
    end: time

    @property
    def key(self) -> str:
        return f"{self.weekday} {self.start:%H:%M}-{self.end:%H:%M}"


@dataclass
class Subject:
    """An aggregated subject from the timetable."""
    code: str
    long_name: str = ""
    alternate_name: str = ""
    groups: set[str] = field(default_factory=set)
    teachers: set[str] = field(default_factory=set)
    rooms: set[str] = field(default_factory=set)
    total_occurrences: int = 0
    weekdays: set[str] = field(default_factory=set)
    time_slots: set[str] = field(default_factory=set)
    dates: set[str] = field(default_factory=set)
    lessons: list[Lesson] = field(default_factory=list)

    @property
    def display_name(self) -> str:
        return self.alternate_name or self.long_name or self.code


@dataclass(frozen=True)
class Lesson:
    """A single lesson occurrence."""
    date: date
    weekday: str
    start: time
    end: time
    room: str = ""
    group: str = ""


@dataclass
class MatchResult:
    """Result of scoring a subject against user constraints."""
    subject: Subject
    score: float = 0.0
    conflict_count: int = 0
    conflict_slots: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
