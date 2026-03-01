"""Fetch timetable data using hsrt-timetable."""

from __future__ import annotations

from hsrt_timetable import HSRTClient, semester_group_name
from webuntis_public import SemesterTimetable

from .config import MatchConfig


def fetch_timetables(config: MatchConfig) -> dict[str, SemesterTimetable]:
    """Fetch timetable data for all configured program groups.

    Returns a mapping of group name -> SemesterTimetable.
    """
    client = HSRTClient(rate_limit=0.3)
    semester = client.get_current_semester()
    if semester is None:
        raise RuntimeError("Cannot determine current semester. Check HSRT calendar data.")

    timetables: dict[str, SemesterTimetable] = {}
    for program in config.programs:
        for sem_num in config.semesters:
            group_name = semester_group_name(program, sem_num)
            print(f"Fetching {group_name}...")
            try:
                tt = client.fetch_program_semester(group_name, semester=semester)
                timetables[group_name] = tt
                print(f"  Got {len(tt.periods)} periods across {len(tt.weeks)} weeks")
            except Exception as e:
                print(f"  Error: {e}")

    return timetables
