"""Configuration for the wahlfach-matching CLI."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MatchConfig:
    """User preferences for elective matching."""
    # Which program groups to fetch timetable data for
    programs: list[str] = field(default_factory=lambda: ["MKIB"])
    semesters: list[int] = field(default_factory=lambda: [4, 6, 7])

    # Mandatory subjects the user is already enrolled in (their time slots are blocked)
    mandatory_subjects: list[str] = field(default_factory=list)

    # Preferred weekdays (higher score if subject falls on these)
    preferred_weekdays: list[str] = field(default_factory=list)

    # Maximum acceptable conflicts
    max_conflicts: int = 0

    # Scoring weights
    weight_no_conflict: float = 10.0
    weight_preferred_day: float = 2.0
    weight_few_occurrences: float = 1.0

    # Output
    output_dir: str = "output"
    export_ics: bool = True
    top_n: int = 10

    # Interactive / combination mode
    interactive: bool = False
    must_have_subjects: list[str] = field(default_factory=list)
    nice_to_have_subjects: list[str] = field(default_factory=list)
    max_combinations: int = 5
    max_electives: int = 6

    # Cache
    use_cache: bool = True
    cache_ttl_hours: int = 24
