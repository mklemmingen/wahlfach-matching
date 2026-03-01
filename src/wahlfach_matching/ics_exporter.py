"""Export timetable data to ICS calendar files."""

from __future__ import annotations

import datetime
from pathlib import Path

from icalendar import Calendar, Event

from .config import MatchConfig
from .models import MatchResult


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
