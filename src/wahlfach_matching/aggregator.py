"""Aggregate raw timetable periods into Subject models."""

from __future__ import annotations

from collections import defaultdict

from webuntis_public import Period, SemesterTimetable

from .models import Lesson, Subject


def aggregate_subjects(
    timetables: dict[str, SemesterTimetable],
) -> dict[str, Subject]:
    """Aggregate all periods from multiple timetables into unique subjects.

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

                subj.lessons.append(Lesson(
                    date=period.date,
                    weekday=period.date.strftime("%A"),
                    start=period.start_time,
                    end=period.end_time,
                    room=", ".join(r.name for r in period.rooms),
                    group=group_name,
                ))

    return dict(sorted(subjects.items()))
