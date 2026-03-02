"""Domain models for the elective matching optimizer."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time


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


@dataclass
class StaticCourse:
    """A manually-added static course with fixed schedule."""
    code: str  # short identifier (e.g., "SPAN1")
    name: str  # full name (e.g., "Spanish 1 (Niveau A1.1)")
    category: str  # "must_have" or "nice_to_have"
    schedule: list[TimeSlot]  # list of weekday + time slots
    semester: int | None = None  # optional context
    notes: str = ""  # optional notes
    created_at: datetime = field(default_factory=datetime.now)
    is_static: bool = field(default=True, init=False)

    @property
    def display_name(self) -> str:
        """Return the name, falling back to code if empty."""
        return self.name or self.code

    def to_lessons(self, start_date: date | None = None, end_date: date | None = None) -> list[Lesson]:
        """Convert static schedule to Lesson objects for entire semester duration.

        Parameters
        ----------
        start_date : date, optional
            Start date of the semester. If None, uses a single representative week.
        end_date : date, optional
            End date of the semester. If None, uses a single representative week.

        Returns
        -------
        list[Lesson]
            Lesson objects for every occurrence of the schedule across the date range.
            If no date range provided, returns lessons for a single representative week.
        """
        from datetime import timedelta

        if start_date is None or end_date is None:
            # Fallback: single week behavior
            reference_date = date.today()
            weekday_names = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
            days_until_monday = (7 - reference_date.weekday()) % 7
            if days_until_monday > 0:
                reference_date = reference_date + timedelta(days=days_until_monday)

            lessons = []
            for slot in self.schedule:
                slot_weekday_idx = weekday_names.index(slot.weekday)
                lesson_date = reference_date + timedelta(days=slot_weekday_idx)
                lessons.append(
                    Lesson(
                        date=lesson_date,
                        weekday=slot.weekday,
                        start=slot.start,
                        end=slot.end,
                        room="",
                        group="",
                    )
                )
            return lessons

        # Generate lessons for entire semester
        weekday_names = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
        lessons = []

        # Iterate through each week in the semester
        current_date = start_date
        while current_date <= end_date:
            # Find the Monday of this week
            days_since_monday = current_date.weekday()
            week_monday = current_date - timedelta(days=days_since_monday)

            # Add all scheduled time slots for this week
            for slot in self.schedule:
                slot_weekday_idx = weekday_names.index(slot.weekday)
                lesson_date = week_monday + timedelta(days=slot_weekday_idx)

                # Only add if within semester range
                if start_date <= lesson_date <= end_date:
                    lessons.append(
                        Lesson(
                            date=lesson_date,
                            weekday=slot.weekday,
                            start=slot.start,
                            end=slot.end,
                            room="",
                            group="",
                        )
                    )

            # Move to next week
            current_date += timedelta(days=7)

        return lessons

