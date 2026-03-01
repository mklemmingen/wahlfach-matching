"""Report generation for schedule combinations."""

from __future__ import annotations

import json
from pathlib import Path

from .config import MatchConfig
from .models import ScheduleCombination, Subject

_WEEKDAY_NAMES = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")


def _subject_schedule_summary(subj: Subject) -> str:
    """Short schedule summary like 'Mon,Wed 08:00-09:30'."""
    days = sorted(subj.weekdays, key=lambda d: _WEEKDAY_NAMES.index(d) if d in _WEEKDAY_NAMES else 99)
    day_abbr = ",".join(d[:3] for d in days)
    slots = sorted(subj.time_slots)
    return f"{day_abbr} {' / '.join(slots)}" if slots else day_abbr


def _free_day_names(free_count: int, subjects: list[Subject]) -> str:
    """Return names of free weekdays."""
    occupied = set()
    for subj in subjects:
        occupied.update(subj.weekdays)
    free = [d for d in _WEEKDAY_NAMES if d not in occupied]
    if free:
        return f"{free_count} ({', '.join(free)})"
    return str(free_count)


def print_combination_report(
    combinations: list[ScheduleCombination],
    config: MatchConfig,
) -> None:
    """Print a structured text report of schedule combinations."""
    print("=" * 70)
    print("SCHEDULE COMBINATION RESULTS")
    print("=" * 70)
    print(f"Found {len(combinations)} combination(s)\n")

    for i, combo in enumerate(combinations, 1):
        m = combo.metrics
        print(f"Combination #{i}   Score: {combo.score}")
        print(f"\u2500\u2500 Ratings \u2500" + "\u2500" * 40)
        print(f"  Closeness (avg gap):    {m.closeness:.0f} min")
        print(f"  Earliest start:         {m.earliest_start}")
        print(f"  Average day start:      {m.avg_start}")
        print(f"  Latest end:             {m.latest_end}")
        print(f"  Average day end:        {m.avg_end}")
        print(f"  Free days per week:     {_free_day_names(m.free_days_per_week, combo.subjects)}")
        print(f"\u2500\u2500 Subjects \u2500" + "\u2500" * 39)

        for subj in combo.must_have_subjects:
            sched = _subject_schedule_summary(subj)
            print(f"  [MUST]      {subj.code:<10s} {subj.display_name:<25s} {sched}")

        for subj in combo.nice_to_have_subjects:
            sched = _subject_schedule_summary(subj)
            print(f"  [NICE]      {subj.code:<10s} {subj.display_name:<25s} {sched}")

        for subj in combo.filler_subjects:
            sched = _subject_schedule_summary(subj)
            print(f"  [COULD FIT] {subj.code:<10s} {subj.display_name:<25s} {sched}")

        if combo.internal_conflicts:
            print(f"\u2500\u2500 Conflicts \u2500" + "\u2500" * 38)
            for a_code, b_code, desc in combo.internal_conflicts:
                print(f"  {desc}")

        if combo.notes:
            print(f"  Notes: {'; '.join(combo.notes)}")

        print()


def save_combination_json(
    combinations: list[ScheduleCombination],
    config: MatchConfig,
) -> Path:
    """Save combination results as JSON. Returns the file path."""
    out_dir = Path(config.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "combinations.json"

    def _subj_dict(subj: Subject, tier: str) -> dict:
        return {
            "code": subj.code,
            "display_name": subj.display_name,
            "tier": tier,
            "weekdays": sorted(subj.weekdays),
            "time_slots": sorted(subj.time_slots),
            "occurrences": subj.total_occurrences,
            "teachers": sorted(subj.teachers),
        }

    data = {
        "config": {
            "programs": config.programs,
            "semesters": config.semesters,
            "mandatory_subjects": config.mandatory_subjects,
            "must_have_subjects": config.must_have_subjects,
            "nice_to_have_subjects": config.nice_to_have_subjects,
            "max_electives": config.max_electives,
        },
        "combinations": [
            {
                "rank": i,
                "score": combo.score,
                "metrics": {
                    "closeness": combo.metrics.closeness,
                    "earliest_start": combo.metrics.earliest_start,
                    "avg_start": combo.metrics.avg_start,
                    "latest_end": combo.metrics.latest_end,
                    "avg_end": combo.metrics.avg_end,
                    "free_days_per_week": combo.metrics.free_days_per_week,
                },
                "subjects": (
                    [_subj_dict(s, "must") for s in combo.must_have_subjects]
                    + [_subj_dict(s, "nice") for s in combo.nice_to_have_subjects]
                    + [_subj_dict(s, "filler") for s in combo.filler_subjects]
                ),
                "internal_conflicts": [
                    {"subject_a": a, "subject_b": b, "description": d}
                    for a, b, d in combo.internal_conflicts
                ],
                "notes": combo.notes,
            }
            for i, combo in enumerate(combinations, 1)
        ],
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Combination JSON saved to {path}")
    return path


def save_selected_combination_json(
    combinations: list[ScheduleCombination],
    indices: list[int],
    config: MatchConfig,
) -> Path:
    """Save only selected combinations as JSON. indices are 1-based."""
    out_dir = Path(config.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "selected_combinations.json"

    def _subj_dict(subj: Subject, tier: str) -> dict:
        return {
            "code": subj.code,
            "display_name": subj.display_name,
            "tier": tier,
            "weekdays": sorted(subj.weekdays),
            "time_slots": sorted(subj.time_slots),
            "occurrences": subj.total_occurrences,
            "teachers": sorted(subj.teachers),
        }

    selected = []
    for idx in indices:
        if 1 <= idx <= len(combinations):
            combo = combinations[idx - 1]
            selected.append({
                "rank": idx,
                "score": combo.score,
                "metrics": {
                    "closeness": combo.metrics.closeness,
                    "earliest_start": combo.metrics.earliest_start,
                    "avg_start": combo.metrics.avg_start,
                    "latest_end": combo.metrics.latest_end,
                    "avg_end": combo.metrics.avg_end,
                    "free_days_per_week": combo.metrics.free_days_per_week,
                },
                "subjects": (
                    [_subj_dict(s, "must") for s in combo.must_have_subjects]
                    + [_subj_dict(s, "nice") for s in combo.nice_to_have_subjects]
                    + [_subj_dict(s, "filler") for s in combo.filler_subjects]
                ),
                "internal_conflicts": [
                    {"subject_a": a, "subject_b": b, "description": d}
                    for a, b, d in combo.internal_conflicts
                ],
                "notes": combo.notes,
            })

    data = {
        "config": {
            "programs": config.programs,
            "semesters": config.semesters,
            "must_have_subjects": config.must_have_subjects,
            "nice_to_have_subjects": config.nice_to_have_subjects,
        },
        "combinations": selected,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Selected combinations JSON saved to {path}")
    return path
