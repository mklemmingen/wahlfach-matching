"""Combinatorial schedule optimizer — find best subject combinations."""

from __future__ import annotations

import heapq
from collections import defaultdict
from datetime import time
from itertools import combinations

from .config import MatchConfig
from .models import CombinationMetrics, Lesson, ScheduleCombination, Subject

ALL_WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")


def _lessons_conflict(a: Lesson, b: Lesson) -> bool:
    """Check if two specific lessons overlap (same date + time overlap)."""
    if a.date != b.date:
        return False
    return a.start < b.end and b.start < a.end


def _subjects_conflict(a: Subject, b: Subject) -> list[str]:
    """Return conflict descriptions between two subjects."""
    conflicts: list[str] = []
    for la in a.lessons:
        for lb in b.lessons:
            if _lessons_conflict(la, lb):
                desc = (
                    f"{a.code} vs {b.code} on {la.date.isoformat()} "
                    f"{la.start:%H:%M}-{la.end:%H:%M}"
                )
                conflicts.append(desc)
    return conflicts


def _time_to_minutes(t: time) -> int:
    """Convert a time to minutes since midnight."""
    return t.hour * 60 + t.minute


def _minutes_to_timestr(minutes: int) -> str:
    """Convert minutes since midnight to HH:MM string."""
    h, m = divmod(int(minutes), 60)
    return f"{h:02d}:{m:02d}"


def _compute_metrics(subjects: list[Subject]) -> CombinationMetrics:
    """Compute all quality-of-life metrics for a set of subjects."""
    all_lessons: list[Lesson] = []
    for subj in subjects:
        all_lessons.extend(subj.lessons)

    if not all_lessons:
        return CombinationMetrics()

    # Group lessons by (date, weekday)
    by_day: dict[tuple[str, str], list[Lesson]] = defaultdict(list)
    for le in all_lessons:
        by_day[(le.date.isoformat(), le.weekday)].append(le)

    # Closeness: avg gap between consecutive lessons on the same day
    total_gap = 0.0
    gap_count = 0
    for day_lessons in by_day.values():
        sorted_lessons = sorted(day_lessons, key=lambda l: l.start)
        for i in range(1, len(sorted_lessons)):
            gap = _time_to_minutes(sorted_lessons[i].start) - _time_to_minutes(sorted_lessons[i - 1].end)
            if gap > 0:
                total_gap += gap
                gap_count += 1
    closeness = total_gap / gap_count if gap_count > 0 else 0.0

    # Earliest start
    earliest = min(_time_to_minutes(le.start) for le in all_lessons)

    # Latest end
    latest = max(_time_to_minutes(le.end) for le in all_lessons)

    # Average start: for each day, find first lesson start, average those
    day_starts: list[int] = []
    day_ends: list[int] = []
    for day_lessons in by_day.values():
        day_starts.append(min(_time_to_minutes(le.start) for le in day_lessons))
        day_ends.append(max(_time_to_minutes(le.end) for le in day_lessons))
    avg_start = sum(day_starts) / len(day_starts) if day_starts else 0
    avg_end = sum(day_ends) / len(day_ends) if day_ends else 0

    # Free days per week: weekdays not present in any lesson
    occupied_weekdays = {le.weekday for le in all_lessons}
    free_days = sum(1 for wd in ALL_WEEKDAYS if wd not in occupied_weekdays)

    return CombinationMetrics(
        closeness=round(closeness, 1),
        earliest_start=_minutes_to_timestr(earliest),
        avg_start=_minutes_to_timestr(int(avg_start)),
        latest_end=_minutes_to_timestr(latest),
        avg_end=_minutes_to_timestr(int(avg_end)),
        free_days_per_week=free_days,
    )


def _build_mandatory_slots(
    mandatory_subjects: dict[str, Subject],
) -> dict[str, list[tuple[str, str]]]:
    """Build a weekday → [(start, end)] map from mandatory subjects."""
    slots: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for subj in mandatory_subjects.values():
        for le in subj.lessons:
            slots[le.weekday].append((f"{le.start:%H:%M}", f"{le.end:%H:%M}"))
    return dict(slots)


def _count_mandatory_conflicts(
    subject: Subject,
    mandatory_slots: dict[str, list[tuple[str, str]]],
) -> int:
    """Count how many lessons of a subject conflict with mandatory slots."""
    count = 0
    for le in subject.lessons:
        le_start = f"{le.start:%H:%M}"
        le_end = f"{le.end:%H:%M}"
        for m_start, m_end in mandatory_slots.get(le.weekday, []):
            if le_start < m_end and m_start < le_end:
                count += 1
                break
    return count


def _score_combination(
    must_have: list[Subject],
    nice_to_have: list[Subject],
    fillers: list[Subject],
    mandatory_slots: dict[str, list[tuple[str, str]]],
    config: MatchConfig,
) -> ScheduleCombination:
    """Score a candidate combination and return a ScheduleCombination."""
    all_subjects = must_have + nice_to_have + fillers

    # Internal conflicts between all pairs
    internal_conflicts: list[tuple[str, str, str]] = []
    for i, a in enumerate(all_subjects):
        for b in all_subjects[i + 1:]:
            for desc in _subjects_conflict(a, b):
                internal_conflicts.append((a.code, b.code, desc))

    # Mandatory slot conflicts
    mandatory_conflict_count = 0
    for subj in all_subjects:
        mandatory_conflict_count += _count_mandatory_conflicts(subj, mandatory_slots)

    # Scoring
    score = 0.0
    notes: list[str] = []

    # Nice-to-have bonus
    score += len(nice_to_have) * 10.0
    if nice_to_have:
        notes.append(f"{len(nice_to_have)} nice-to-have(s) included")

    # Filler bonus (smaller)
    score += len(fillers) * 3.0
    if fillers:
        notes.append(f"{len(fillers)} filler(s) included")

    # Penalty for internal conflicts
    score -= len(internal_conflicts) * 5.0
    if internal_conflicts:
        notes.append(f"{len(internal_conflicts)} internal conflict(s)")

    # Penalty for mandatory conflicts
    score -= mandatory_conflict_count * 8.0
    if mandatory_conflict_count:
        notes.append(f"{mandatory_conflict_count} mandatory conflict(s)")

    # Metrics bonus: reward compactness and free days
    metrics = _compute_metrics(all_subjects)
    score += metrics.free_days_per_week * 2.0
    if metrics.closeness > 0:
        # Reward compact schedules (lower gap = higher score)
        score += max(0, 5.0 - metrics.closeness / 30.0)

    return ScheduleCombination(
        subjects=all_subjects,
        must_have_subjects=must_have,
        nice_to_have_subjects=nice_to_have,
        filler_subjects=fillers,
        score=round(score, 1),
        internal_conflicts=internal_conflicts,
        nice_to_have_count=len(nice_to_have),
        filler_count=len(fillers),
        metrics=metrics,
        notes=notes,
    )


def find_best_combinations(
    subjects: dict[str, Subject],
    mandatory_subjects: dict[str, Subject],
    config: MatchConfig,
) -> list[ScheduleCombination]:
    """Find the best schedule combinations.

    Parameters
    ----------
    subjects:
        All available subjects (keyed by code).
    mandatory_subjects:
        Already-enrolled subjects whose time slots are blocked.
    config:
        User preferences including must_have_subjects, nice_to_have_subjects,
        max_electives, and max_combinations.
    """
    mandatory_slots = _build_mandatory_slots(mandatory_subjects)

    # Resolve must-have and nice-to-have subjects
    must_have: list[Subject] = []
    for code in config.must_have_subjects:
        if code in subjects and code not in mandatory_subjects:
            must_have.append(subjects[code])

    nice_to_have: list[Subject] = []
    for code in config.nice_to_have_subjects:
        if code in subjects and code not in mandatory_subjects and code not in config.must_have_subjects:
            nice_to_have.append(subjects[code])

    must_have_codes = {s.code for s in must_have}
    nice_to_have_codes = {s.code for s in nice_to_have}

    # Build candidate pool: uncategorized subjects (not mandatory, not must-have, not nice-to-have)
    fillers: list[Subject] = []
    for code, subj in subjects.items():
        if code in mandatory_subjects:
            continue
        if code in must_have_codes or code in nice_to_have_codes:
            continue
        fillers.append(subj)

    # Pre-filter: remove candidates conflicting with ALL must-haves
    if must_have:
        def conflicts_with_all_must_have(subj: Subject) -> bool:
            for mh in must_have:
                if not _subjects_conflict(subj, mh):
                    return False
            return True
        fillers = [f for f in fillers if not conflicts_with_all_must_have(f)]

    # Sort by individual merit (fewer mandatory conflicts first)
    fillers.sort(key=lambda s: _count_mandatory_conflicts(s, mandatory_slots))

    # Cap pool for performance
    fillers = fillers[:50]

    # Remaining slots after must-haves
    remaining_slots = config.max_electives - len(must_have)
    if remaining_slots <= 0:
        # Only must-haves fit — return single combination
        combo = _score_combination(must_have, [], [], mandatory_slots, config)
        return [combo]

    # Build candidate pool: nice-to-have first, then fillers
    candidate_pool = nice_to_have + fillers

    # Use a min-heap to track top-N combinations (by score)
    # Heap entries: (score, index, combination) — index for tie-breaking
    heap: list[tuple[float, int, ScheduleCombination]] = []
    counter = 0

    # Enumerate subsets of size 1..remaining_slots from candidate_pool
    max_pool = min(len(candidate_pool), remaining_slots)
    for size in range(0, max_pool + 1):
        for subset in combinations(candidate_pool, size):
            subset_nice = [s for s in subset if s.code in nice_to_have_codes]
            subset_fillers = [s for s in subset if s.code not in nice_to_have_codes]

            combo = _score_combination(
                must_have, subset_nice, subset_fillers, mandatory_slots, config,
            )

            if len(heap) < config.max_combinations:
                heapq.heappush(heap, (combo.score, counter, combo))
            elif combo.score > heap[0][0]:
                heapq.heapreplace(heap, (combo.score, counter, combo))
            counter += 1

    # Extract and sort by score descending
    results = [entry[2] for entry in heap]
    results.sort(key=lambda c: -c.score)
    return results
