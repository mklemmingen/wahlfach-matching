"""Aggregate raw timetable periods into Subject models."""

from __future__ import annotations

from collections import defaultdict

from webuntis_public import Period, SemesterTimetable

from .models import Lesson, Subject


def aggregate_subjects(
    timetables: dict[str, SemesterTimetable],
) -> dict[str, Subject]:
    """Aggregate all periods from multiple timetables into unique subjects.

    Deduplicates lessons (same date/time/room) that appear in multiple groups.
    Returns a dict keyed by subject code.
    """
    subjects: dict[str, Subject] = {}

    for group_name, timetable in timetables.items():
        for period in timetable.periods:
            for subj_elem in period.subjects:
                code = subj_elem.name
                if code not in subjects:
                    subjects[code] = Subject(
                        code=code,
                        long_name=subj_elem.long_name,
                        alternate_name=subj_elem.alternate_name,
                    )
                subj = subjects[code]
                if subj_elem.long_name:
                    subj.long_name = subj_elem.long_name
                if subj_elem.alternate_name:
                    subj.alternate_name = subj_elem.alternate_name

                subj.groups.add(group_name)
                subj.total_occurrences += 1
                subj.weekdays.add(period.date.strftime("%A"))

                time_slot = f"{period.start_time:%H:%M}-{period.end_time:%H:%M}"
                subj.time_slots.add(time_slot)
                subj.dates.add(period.date.isoformat())

                for t in period.teachers:
                    subj.teachers.add(t.long_name or t.name)
                for r in period.rooms:
                    subj.rooms.add(r.name)

                # Create lesson and check for duplicates before adding
                new_lesson = Lesson(
                    date=period.date,
                    weekday=period.date.strftime("%A"),
                    start=period.start_time,
                    end=period.end_time,
                    room=", ".join(r.name for r in period.rooms),
                    group=group_name,
                )

                # Only add if this exact lesson doesn't already exist
                # Dedup by (date, start, end) — same time = same lecture,
                # regardless of room string differences across groups
                lesson_key = (new_lesson.date, new_lesson.start, new_lesson.end)
                existing_keys = {
                    (l.date, l.start, l.end) for l in subj.lessons
                }
                if lesson_key not in existing_keys:
                    subj.lessons.append(new_lesson)

    return dict(sorted(subjects.items()))
