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

        for lesson in subj.lessons:
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

        safe_name = subj.code.replace("/", "_").replace(" ", "_")
        path = out_dir / f"{safe_name}.ics"
        with open(path, "wb") as f:
            f.write(cal.to_ical())
        created.append(path)
        print(f"  Exported {len(subj.lessons)} events to {path}")

    return created


def export_combination_ics(
    combinations: list[ScheduleCombination],
    config: MatchConfig,
) -> list[Path]:
    """Export each schedule combination as a single ICS file.

    Events are tagged with [MUST], [NICE], or [COULD FIT] in the summary.
    Returns a list of created file paths.
    """
    out_dir = Path(config.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []

    for i, combo in enumerate(combinations, 1):
        cal = Calendar()
        cal.add("prodid", "-//WahlfachMatching//wahlfach-matching//EN")
        cal.add("version", "2.0")
        cal.add("x-wr-calname", f"Combination {i}")

        must_codes = {s.code for s in combo.must_have_subjects}
        nice_codes = {s.code for s in combo.nice_to_have_subjects}

        for subj in combo.subjects:
            if subj.code in must_codes:
                tag = "[MUST]"
            elif subj.code in nice_codes:
                tag = "[NICE]"
            else:
                tag = "[COULD FIT]"

            for lesson in subj.lessons:
                event = Event()
                display = subj.display_name if subj.display_name != subj.code else subj.code
                event.add("summary", f"{tag} {display}")
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

        path = out_dir / f"combination_{i}.ics"
        with open(path, "wb") as f:
            f.write(cal.to_ical())
        created.append(path)
        total_events = sum(len(s.lessons) for s in combo.subjects)
        print(f"  Exported {total_events} events to {path}")

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

        cal = Calendar()
        cal.add("prodid", "-//WahlfachMatching//wahlfach-matching//EN")
        cal.add("version", "2.0")
        cal.add("x-wr-calname", f"Combination {idx}")

        must_codes = {s.code for s in combo.must_have_subjects}
        nice_codes = {s.code for s in combo.nice_to_have_subjects}

        for subj in combo.subjects:
            if subj.code in must_codes:
                tag = "[MUST]"
            elif subj.code in nice_codes:
                tag = "[NICE]"
            else:
                tag = "[COULD FIT]"

            for lesson in subj.lessons:
                event = Event()
                display = subj.display_name if subj.display_name != subj.code else subj.code
                event.add("summary", f"{tag} {display}")
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

        path = out_dir / f"combination_{idx}.ics"
        with open(path, "wb") as f:
            f.write(cal.to_ical())
        created.append(path)
        total_events = sum(len(s.lessons) for s in combo.subjects)
        print(f"  Exported {total_events} events to {path}")

    return created
