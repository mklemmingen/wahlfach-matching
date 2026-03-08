#!/usr/bin/env python3
"""Generate an ICS calendar file for 'Digital Marketing und Sales' in 3MKIB6.

Usage:
    python generate_marketing_sales_ics.py

The script will:
1. Try to load cached timetable data (from output/.cache/)
2. If no cache exists, fetch fresh data from WebUntis
3. Find the 'Digital Marketing und Sales' subject
4. Export it as an ICS file to output/
"""

from __future__ import annotations

import datetime
import sys
from pathlib import Path

from icalendar import Calendar, Event

GROUP = "3MKIB6"
SEARCH_TERM = "digital marketing"  # case-insensitive substring match


def _load_subjects() -> dict[str, "Subject"]:
    """Load subjects from cache or fetch from WebUntis."""
    from wahlfach_matching.cache import SubjectCache
    from wahlfach_matching.config import MatchConfig

    # Build a config matching 3MKIB6 (program=MKIB, semester=6)
    config = MatchConfig(programs=["MKIB"], semesters=[6])

    # Try cache first
    cache = SubjectCache(
        cache_dir=str(Path(config.output_dir) / ".cache"),
        ttl_hours=config.cache_ttl_hours,
    )
    cached = cache.load(config)
    if cached is not None:
        print("Loaded timetable data from cache.")
        return cached

    # No cache — fetch live
    print(f"No cache found. Fetching timetable for {GROUP} from WebUntis...")
    from hsrt_timetable import HSRTClient
    from wahlfach_matching.aggregator import aggregate_subjects

    client = HSRTClient(rate_limit=0.3)
    semester = client.get_current_semester()
    if semester is None:
        print("ERROR: Cannot determine current semester.")
        sys.exit(1)

    tt = client.fetch_program_semester(GROUP, semester=semester)
    print(f"  Got {len(tt.periods)} periods across {len(tt.weeks)} weeks")

    timetables = {GROUP: tt}
    subjects = aggregate_subjects(timetables)

    # Save to cache for next time
    cache.save(config, subjects)
    print("Timetable data cached for future runs.")

    return subjects


def _find_subject(subjects: dict[str, "Subject"]) -> "Subject":
    """Find 'Digital Marketing und Sales' in the subjects dict."""
    matches = [
        subj
        for code, subj in subjects.items()
        if SEARCH_TERM in code.lower()
        or SEARCH_TERM in subj.long_name.lower()
        or SEARCH_TERM in subj.alternate_name.lower()
        or SEARCH_TERM in subj.display_name.lower()
    ]

    if not matches:
        print(f"\nNo subject matching '{SEARCH_TERM}' found.")
        print("Available subjects:")
        for code, subj in sorted(subjects.items()):
            print(f"  {code:30s}  {subj.display_name}")
        sys.exit(1)

    if len(matches) > 1:
        print(f"\nMultiple matches for '{SEARCH_TERM}':")
        for subj in matches:
            print(f"  {subj.code:30s}  {subj.display_name}")
        print("Using the first match.")

    return matches[0]


def _build_ics(subj: "Subject") -> tuple[Calendar, int]:
    """Build an ICS calendar for the given subject. Returns (calendar, event_count)."""
    cal = Calendar()
    cal.add("prodid", "-//WahlfachMatching//digital-marketing-sales//EN")
    cal.add("version", "2.0")
    cal.add("x-wr-calname", f"{subj.code} - {subj.display_name}")

    seen: set[tuple] = set()
    event_count = 0
    for lesson in sorted(subj.lessons, key=lambda l: (l.date, l.start)):
        key = (lesson.date, lesson.start, lesson.end)
        if key in seen:
            continue
        seen.add(key)

        event = Event()
        event.add("summary", subj.display_name)
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

    return cal, event_count


def main() -> None:
    subjects = _load_subjects()
    subj = _find_subject(subjects)

    print(f"\nFound: {subj.code} — {subj.display_name}")
    print(f"  Teachers: {', '.join(sorted(subj.teachers)) if subj.teachers else '(none)'}")
    print(f"  Rooms:    {', '.join(sorted(subj.rooms)) if subj.rooms else '(none)'}")
    print(f"  Lessons:  {len(subj.lessons)}")

    cal, event_count = _build_ics(subj)

    # Write ICS file
    out_dir = Path("output")
    out_dir.mkdir(parents=True, exist_ok=True)
    safe_name = subj.code.replace("/", "_").replace(" ", "_")
    ics_path = out_dir / f"{safe_name}.ics"

    with open(ics_path, "wb") as f:
        f.write(cal.to_ical())

    print(f"\nExported {event_count} events to {ics_path}")

    # Print event summary table
    print(f"\n{'Date':<14} {'Day':<11} {'Time':<14} {'Room'}")
    print("-" * 55)
    seen: set[tuple] = set()
    for lesson in sorted(subj.lessons, key=lambda l: (l.date, l.start)):
        key = (lesson.date, lesson.start, lesson.end)
        if key in seen:
            continue
        seen.add(key)
        print(
            f"{lesson.date.isoformat():<14} "
            f"{lesson.weekday:<11} "
            f"{lesson.start:%H:%M}-{lesson.end:%H:%M}   "
            f"{lesson.room}"
        )


if __name__ == "__main__":
    main()
