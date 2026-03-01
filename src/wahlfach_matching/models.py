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


@dataclass
class CombinationMetrics:
    """Quality-of-life ratings for a schedule combination."""
    closeness: float = 0.0       # avg gap between consecutive lessons (lower = more compact)
    earliest_start: str = ""     # earliest lesson start across all days (e.g. "08:00")
    avg_start: str = ""          # average first-lesson-of-day start time
    latest_end: str = ""         # latest lesson end across all days
    avg_end: str = ""            # average last-lesson-of-day end time
    free_days_per_week: int = 0  # weekdays with zero lessons


@dataclass
class ScheduleCombination:
    """A candidate schedule: a set of subjects that work together."""
    subjects: list[Subject]
    must_have_subjects: list[Subject]
    nice_to_have_subjects: list[Subject]
    filler_subjects: list[Subject]  # uncategorized "could fit in here"
    score: float = 0.0
    internal_conflicts: list[tuple[str, str, str]] = field(default_factory=list)
    nice_to_have_count: int = 0
    filler_count: int = 0
    metrics: CombinationMetrics = field(default_factory=CombinationMetrics)
    notes: list[str] = field(default_factory=list)
