"""Report generation for schedule combinations."""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path

from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
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

    # Header
    header = Text()
    header.append("SCHEDULE COMBINATION RESULTS", style="bold white")
    console.print(Panel(header, border_style="bright_blue", padding=(0, 2)))

    # Filter summary
    filter_grid = Table.grid(padding=(0, 2))
    filter_grid.add_column(style="dim")
    filter_grid.add_column()
    if config.excluded_subjects:
        filter_grid.add_row("Excluded:", ", ".join(config.excluded_subjects))
    if config.must_have_subjects:
        filter_grid.add_row("Must-have:", "[green]" + ", ".join(config.must_have_subjects) + "[/green]")
    if config.nice_to_have_subjects:
        filter_grid.add_row("Nice-to-have:", "[blue]" + ", ".join(config.nice_to_have_subjects) + "[/blue]")
    console.print(filter_grid)

    console.print(f"\nFound [bold]{len(combinations)}[/bold] combination(s)\n")

    for i, combo in enumerate(combinations, 1):
        m = combo.metrics

        # ── Ratings table ─────────────────────────────────────
        ratings = Table.grid(padding=(0, 2))
        ratings.add_column(style="dim", min_width=22)
        ratings.add_column(style="bold")
        ratings.add_row("Closeness (avg gap)", f"{m.closeness:.0f} min")
        ratings.add_row("Earliest start", m.earliest_start)
        ratings.add_row("Average day start", m.avg_start)
        ratings.add_row("Latest end", m.latest_end)
        ratings.add_row("Average day end", m.avg_end)
        ratings.add_row("Free days/week", _free_day_names(m.free_days_per_week, combo.subjects))

        # ── Subjects table ────────────────────────────────────
        subj_table = Table(
            show_header=True,
            header_style="bold",
            border_style="dim",
            padding=(0, 1),
            expand=True,
        )
        subj_table.add_column("Tier", width=10)
        subj_table.add_column("Code", style="bold yellow", width=12)
        subj_table.add_column("Name", ratio=2)
        subj_table.add_column("Schedule")
        subj_table.add_column("Lessons", justify="right", width=7)
        subj_table.add_column("Teacher(s)", style="dim")

        for subj in combo.must_have_subjects:
            sched = _subject_schedule_summary(subj)
            teachers = ", ".join(sorted(subj.teachers)) if subj.teachers else ""
            subj_table.add_row(
                "[bold green]MUST",
                subj.code, subj.display_name, sched,
                str(subj.total_occurrences), teachers,
            )
        for subj in combo.nice_to_have_subjects:
            sched = _subject_schedule_summary(subj)
            teachers = ", ".join(sorted(subj.teachers)) if subj.teachers else ""
            subj_table.add_row(
                "[bold blue]NICE",
                subj.code, subj.display_name, sched,
                str(subj.total_occurrences), teachers,
            )
        for subj in combo.filler_subjects:
            sched = _subject_schedule_summary(subj)
            teachers = ", ".join(sorted(subj.teachers)) if subj.teachers else ""
            subj_table.add_row(
                "[dim]COULD FIT",
                subj.code, subj.display_name, sched,
                str(subj.total_occurrences), teachers,
            )

        # ── Build the combo panel content ─────────────────────
        parts: list = [ratings, "", subj_table]

        # Missing nice-to-haves
        included_nice_codes = {s.code for s in combo.nice_to_have_subjects}
        missing_nice = [c for c in config.nice_to_have_subjects if c not in included_nice_codes]
        if missing_nice:
            parts.append(Text(f"  Missing nice-to-haves: {', '.join(missing_nice)}", style="dim italic"))

        # Conflicts
        if combo.internal_conflicts:
            conflict_text = Text()
            conflict_text.append(f"  {len(combo.internal_conflicts)} conflict(s):\n", style="bold red")
            for _, _, desc in combo.internal_conflicts:
                conflict_text.append(f"    {desc}\n", style="red")
            parts.append(conflict_text)

        # Notes
        if combo.notes:
            parts.append(Text(f"  {'; '.join(combo.notes)}", style="dim"))

        # Score badge
        score_style = "bold green" if combo.score > 0 else "bold red"
        title = f"[bold]#{i}[/bold]  Score: [{score_style}]{combo.score}[/{score_style}]"

        # Wrap everything in a panel
        from rich.console import Group
        console.print(Panel(
            Group(*parts),
            title=title,
            border_style="bright_blue" if i == 1 else "blue",
            padding=(0, 1),
        ))
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
