"""Score elective subjects against user constraints."""

from __future__ import annotations

from .config import MatchConfig
from .models import MatchResult, Subject


def _time_ranges_overlap(a_start: str, a_end: str, b_start: str, b_end: str) -> bool:
    """Check if two HH:MM time ranges overlap."""
    return a_start < b_end and b_start < a_end


def score_subject(
    subject: Subject,
    mandatory_slots: dict[str, list[tuple[str, str]]],
    config: MatchConfig,
) -> MatchResult:
    """Score a single subject against mandatory time slots and preferences.

    Parameters
    ----------
    subject:
        The elective subject to score.
    mandatory_slots:
        Dict of weekday -> list of (start_time, end_time) strings for blocked slots.
    config:
        User preferences and scoring weights.
    """
    result = MatchResult(subject=subject)
    conflict_slots: list[str] = []

    # Check for time conflicts with mandatory subjects
    for lesson in subject.lessons:
        weekday = lesson.weekday
        lesson_start = f"{lesson.start:%H:%M}"
        lesson_end = f"{lesson.end:%H:%M}"
        if weekday in mandatory_slots:
            for m_start, m_end in mandatory_slots[weekday]:
                if _time_ranges_overlap(lesson_start, lesson_end, m_start, m_end):
                    slot_key = f"{weekday} {lesson_start}-{lesson_end}"
                    if slot_key not in conflict_slots:
                        conflict_slots.append(slot_key)

    result.conflict_count = len(conflict_slots)
    result.conflict_slots = conflict_slots

    # Scoring
    if result.conflict_count == 0:
        result.score += config.weight_no_conflict
        result.notes.append("No schedule conflicts")
    else:
        result.notes.append(f"{result.conflict_count} conflict(s)")

    # Preferred weekday bonus
    for weekday in subject.weekdays:
        if weekday in config.preferred_weekdays:
            result.score += config.weight_preferred_day
            result.notes.append(f"Preferred day: {weekday}")

    # Fewer occurrences = less commitment (slight bonus for flexibility)
    if subject.total_occurrences <= 20:
        result.score += config.weight_few_occurrences

    return result


def score_all(
    subjects: dict[str, Subject],
    mandatory_subjects: dict[str, Subject],
    config: MatchConfig,
) -> list[MatchResult]:
    """Score all candidate subjects and return sorted results (best first).

    Parameters
    ----------
    subjects:
        All aggregated subjects.
    mandatory_subjects:
        Subjects the user is already enrolled in (used to determine blocked slots).
    config:
        User preferences.
    """
    # Build mandatory time slots by weekday
    mandatory_slots: dict[str, list[tuple[str, str]]] = {}
    for subj in mandatory_subjects.values():
        for lesson in subj.lessons:
            weekday = lesson.weekday
            slot = (f"{lesson.start:%H:%M}", f"{lesson.end:%H:%M}")
            mandatory_slots.setdefault(weekday, []).append(slot)

    results: list[MatchResult] = []
    for code, subject in subjects.items():
        if code in mandatory_subjects:
            continue  # skip subjects already enrolled
        result = score_subject(subject, mandatory_slots, config)
        if config.max_conflicts == 0 or result.conflict_count <= config.max_conflicts:
            results.append(result)

    results.sort(key=lambda r: (-r.score, r.conflict_count, r.subject.code))
    return results
