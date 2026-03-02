"""Export timetable data to ICS calendar files."""

from __future__ import annotations

import datetime
from pathlib import Path

from icalendar import Calendar, Event

from .config import MatchConfig
from .models import MatchResult, ScheduleCombination


def export_ics(
    results: list[MatchResult],
    config: MatchConfig,
    *,
    top_n: int | None = None,
) -> list[Path]:
    """Export top-scored subjects to individual ICS files.

    Returns a list of created file paths.
    """
    out_dir = Path(config.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    n = top_n or config.top_n
    created: list[Path] = []

    for r in results[:n]:
        subj = r.subject
        cal = Calendar()
        cal.add("prodid", "-//WahlfachMatching//wahlfach-matching//EN")
        cal.add("version", "2.0")
        cal.add("x-wr-calname", f"{subj.code} - {subj.display_name}")

        seen: set[tuple] = set()
        event_count = 0
        for lesson in subj.lessons:
            key = (lesson.date, lesson.start, lesson.end)
            if key in seen:
                continue
            seen.add(key)

            event = Event()
            summary = subj.display_name if subj.display_name != subj.code else subj.code
            event.add("summary", summary)
            event.add("dtstart", datetime.datetime.combine(lesson.date, lesson.start))
            event.add("dtend", datetime.datetime.combine(lesson.date, lesson.end))
            if lesson.room:
                event.add("location", lesson.room)
            description_parts = [f"Subject: {subj.code}"]
            if subj.teachers:
                description_parts.append(f"Teachers: {', '.join(sorted(subj.teachers))}")
            if lesson.group:
                description_parts.append(f"Group: {lesson.group}")
            event.add("description", "\n".join(description_parts))
            cal.add_component(event)
            event_count += 1

        safe_name = subj.code.replace("/", "_").replace(" ", "_")
        path = out_dir / f"{safe_name}.ics"
        with open(path, "wb") as f:
            f.write(cal.to_ical())
        created.append(path)
        print(f"  Exported {event_count} events to {path}")

    return created


def _build_combination_calendar(
    combo: ScheduleCombination,
    cal_name: str,
    include_tag_in_summary: bool = False,
) -> tuple[Calendar, int]:
    """Build a deduplicated ICS calendar from a schedule combination.

    Returns (calendar, event_count).
    """
    cal = Calendar()
    cal.add("prodid", "-//WahlfachMatching//wahlfach-matching//EN")
    cal.add("version", "2.0")
    cal.add("x-wr-calname", cal_name)

    must_codes = {s.code for s in combo.must_have_subjects}
    nice_codes = {s.code for s in combo.nice_to_have_subjects}

    # Dedup across all subjects in the combination by (subject_code, date, start, end)
    seen: set[tuple] = set()
    event_count = 0

    for subj in combo.subjects:
        if subj.code in must_codes:
            tag = "[MUST]"
        elif subj.code in nice_codes:
            tag = "[NICE]"
        else:
            tag = "[COULD FIT]"

        for lesson in subj.lessons:
            key = (subj.code, lesson.date, lesson.start, lesson.end)
            if key in seen:
                continue
            seen.add(key)

            event = Event()
            display = subj.display_name if subj.display_name != subj.code else subj.code
            summary = f"{tag} {display}" if include_tag_in_summary else display
            event.add("summary", summary)
            event.add("dtstart", datetime.datetime.combine(lesson.date, lesson.start))
            event.add("dtend", datetime.datetime.combine(lesson.date, lesson.end))
            if lesson.room:
                event.add("location", lesson.room)
            description_parts = [f"Subject: {subj.code}", f"Tier: {tag}"]
            if subj.teachers:
                description_parts.append(f"Teachers: {', '.join(sorted(subj.teachers))}")
            if lesson.group:
                description_parts.append(f"Group: {lesson.group}")
            event.add("description", "\n".join(description_parts))
            cal.add_component(event)
            event_count += 1

    return cal, event_count


def export_combination_ics(
    combinations: list[ScheduleCombination],
    config: MatchConfig,
) -> list[Path]:
    """Export each schedule combination as a single ICS file.

    Events are deduplicated per combination. Tier is in description, not summary.
    Returns a list of created file paths.
    """
    out_dir = Path(config.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []

    for i, combo in enumerate(combinations, 1):
        cal, event_count = _build_combination_calendar(
            combo, f"Combination {i}", include_tag_in_summary=False,
        )
        path = out_dir / f"combination_{i}.ics"
        with open(path, "wb") as f:
            f.write(cal.to_ical())
        created.append(path)
        print(f"  Exported {event_count} events to {path}")

    return created


def export_selected_combination_ics(
    combinations: list[ScheduleCombination],
    indices: list[int],
    config: MatchConfig,
) -> list[Path]:
    """Export only selected combinations as ICS files. indices are 1-based."""
    out_dir = Path(config.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []

    for idx in indices:
        if idx < 1 or idx > len(combinations):
            continue
        combo = combinations[idx - 1]

        cal, event_count = _build_combination_calendar(
            combo, f"Combination {idx}", include_tag_in_summary=True,
        )
        path = out_dir / f"combination_{idx}.ics"
        with open(path, "wb") as f:
            f.write(cal.to_ical())
        created.append(path)
        print(f"  Exported {event_count} events to {path}")

    return created
