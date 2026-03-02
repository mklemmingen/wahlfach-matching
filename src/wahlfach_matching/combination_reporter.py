"""Report generation for schedule combinations."""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path

from rich.console import Console, Group
from rich.table import Table
from rich.text import Text

from .config import MatchConfig
from .models import ScheduleCombination, Subject

_WEEKDAY_NAMES = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")


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
    console: Console | None = None,
) -> None:
    """Print a structured rich report of schedule combinations."""
    if console is None:
        console = Console()

    # Filter summary
    console.print("SCHEDULE COMBINATION RESULTS")
    lines = []
    if config.must_have_subjects:
        lines.append(f"Must-have: {', '.join(config.must_have_subjects)}")
    if config.nice_to_have_subjects:
        lines.append(f"Nice-to-have: {', '.join(config.nice_to_have_subjects)}")
    if config.excluded_subjects:
        lines.append(f"Excluded: {', '.join(config.excluded_subjects)}")
    if config.exclusion_groups:
        groups_str = ", ".join(f"{n} ({', '.join(c)})" for n, c in config.exclusion_groups.items())
        lines.append(f"Exclusion groups: {groups_str}")
    for line in lines:
        console.print(f"  {line}")
    console.print(f"{len(combinations)} combination(s)\n")

    for i, combo in enumerate(combinations, 1):
        m = combo.metrics

        # Header line
        console.print(f"--- #{i}  score={combo.score}  gap={m.closeness:.0f}min  "
                       f"start={m.earliest_start}-{m.latest_end}  "
                       f"free={_free_day_names(m.free_days_per_week, combo.subjects)} ---")

        # Subjects table
        subj_table = Table(
            show_header=True,
            box=None,
            padding=(0, 1),
            expand=False,
            show_edge=False,
        )
        subj_table.add_column("Tier", width=8)
        subj_table.add_column("Code", width=18)
        subj_table.add_column("Name", min_width=20)
        subj_table.add_column("Schedule")
        subj_table.add_column("Lsn", justify="right", width=4)

        for subj in combo.must_have_subjects:
            subj_table.add_row("MUST", subj.code, subj.display_name,
                               _subject_schedule_summary(subj), str(subj.total_occurrences))
        for subj in combo.nice_to_have_subjects:
            subj_table.add_row("NICE", subj.code, subj.display_name,
                               _subject_schedule_summary(subj), str(subj.total_occurrences))
        for subj in combo.filler_subjects:
            subj_table.add_row("FILL", subj.code, subj.display_name,
                               _subject_schedule_summary(subj), str(subj.total_occurrences))
        console.print(subj_table)

        # Extra info on one line each
        included_nice_codes = {s.code for s in combo.nice_to_have_subjects}
        missing_nice = [c for c in config.nice_to_have_subjects if c not in included_nice_codes]
        if missing_nice:
            console.print(f"  Missing: {', '.join(missing_nice)}")
        if combo.internal_conflicts:
            console.print(f"  Conflicts ({len(combo.internal_conflicts)}):")
            for _, _, desc in combo.internal_conflicts:
                console.print(f"    {desc}")
        if combo.notes:
            console.print(f"  {'; '.join(combo.notes)}")
        console.print()


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
            "excluded_subjects": config.excluded_subjects,
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
            "excluded_subjects": config.excluded_subjects,
        },
        "combinations": selected,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Selected combinations JSON saved to {path}")
    return path


def save_combination_md(
    combinations: list[ScheduleCombination],
    config: MatchConfig,
    run_id: str | None = None,
) -> Path:
    """Save combination results as a human-readable Markdown file with UUID.

    Parameters
    ----------
    run_id : str, optional
        A UUID for this run. Generated if not provided.

    Returns the file path.
    """
    if run_id is None:
        run_id = uuid.uuid4().hex[:12]

    out_dir = Path(config.output_dir) / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"results_{run_id}.md"

    lines: list[str] = []
    lines.append(f"# Schedule Combination Results")
    lines.append(f"")
    lines.append(f"**Run ID:** `{run_id}`  ")
    lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  ")
    lines.append(f"")

    # Parameters section
    lines.append(f"## Parameters")
    lines.append(f"")
    lines.append(f"| Parameter | Value |")
    lines.append(f"|-----------|-------|")
    lines.append(f"| Programs | {', '.join(config.programs)} |")
    lines.append(f"| Semesters | {', '.join(str(s) for s in config.semesters)} |")
    lines.append(f"| Must-have | {', '.join(config.must_have_subjects) or '(none)'} |")
    lines.append(f"| Nice-to-have | {', '.join(config.nice_to_have_subjects) or '(none)'} |")
    lines.append(f"| Excluded | {', '.join(config.excluded_subjects) or '(none)'} |")
    lines.append(f"| Max electives | {config.max_electives} |")
    lines.append(f"| Max combinations | {config.max_combinations} |")
    lines.append(f"")

    # Combinations
    lines.append(f"## Combinations ({len(combinations)} found)")
    lines.append(f"")

    for i, combo in enumerate(combinations, 1):
        m = combo.metrics
        lines.append(f"### Combination #{i} (Score: {combo.score})")
        lines.append(f"")
        lines.append(f"**Ratings:**")
        lines.append(f"- Closeness (avg gap): {m.closeness:.0f} min")
        lines.append(f"- Earliest start: {m.earliest_start}")
        lines.append(f"- Avg day start: {m.avg_start}")
        lines.append(f"- Latest end: {m.latest_end}")
        lines.append(f"- Avg day end: {m.avg_end}")
        free_str = _free_day_names(m.free_days_per_week, combo.subjects)
        lines.append(f"- Free days/week: {free_str}")
        lines.append(f"")

        lines.append(f"**Subjects:**")
        lines.append(f"")
        lines.append(f"| Tier | Code | Name | Schedule | Teacher(s) |")
        lines.append(f"|------|------|------|----------|------------|")
        for subj in combo.must_have_subjects:
            sched = _subject_schedule_summary(subj)
            teachers = ", ".join(sorted(subj.teachers)) if subj.teachers else "-"
            lines.append(f"| MUST | {subj.code} | {subj.display_name} | {sched} | {teachers} |")
        for subj in combo.nice_to_have_subjects:
            sched = _subject_schedule_summary(subj)
            teachers = ", ".join(sorted(subj.teachers)) if subj.teachers else "-"
            lines.append(f"| NICE | {subj.code} | {subj.display_name} | {sched} | {teachers} |")
        for subj in combo.filler_subjects:
            sched = _subject_schedule_summary(subj)
            teachers = ", ".join(sorted(subj.teachers)) if subj.teachers else "-"
            lines.append(f"| COULD FIT | {subj.code} | {subj.display_name} | {sched} | {teachers} |")
        lines.append(f"")

        # Show which nice-to-haves didn't make it
        included_nice_codes = {s.code for s in combo.nice_to_have_subjects}
        missing_nice = [c for c in config.nice_to_have_subjects if c not in included_nice_codes]
        if missing_nice:
            lines.append(f"**Nice-to-have not in this combo:** {', '.join(missing_nice)}")
            lines.append(f"")

        if combo.internal_conflicts:
            lines.append(f"**Conflicts:**")
            for _, _, desc in combo.internal_conflicts:
                lines.append(f"- {desc}")
            lines.append(f"")

        if combo.notes:
            lines.append(f"**Notes:** {'; '.join(combo.notes)}")
            lines.append(f"")

    content = "\n".join(lines) + "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Results saved to {path} (ID: {run_id})")
    return path
