"""Tests for the aggregation logic."""

import datetime

from webuntis_public import Element, ElementType, Period, SemesterTimetable, WeeklyTimetable

from wahlfach_matching.aggregator import aggregate_subjects


def _make_timetable(group_name: str) -> dict[str, SemesterTimetable]:
    period = Period(
        date=datetime.date(2026, 3, 2),
        start_time=datetime.time(8, 0),
        end_time=datetime.time(9, 30),
        subjects=(Element(ElementType.SUBJECT, 50, "MATH", "Mathematics", "MA"),),
        teachers=(Element(ElementType.TEACHER, 10, "Mueller", "Prof. Mueller"),),
        rooms=(Element(ElementType.ROOM, 20, "A101"),),
    )
    week = WeeklyTimetable(
        class_id=100,
        week_start=datetime.date(2026, 3, 2),
        periods=(period,),
    )
    sem = SemesterTimetable(
        class_id=100,
        start=datetime.date(2026, 3, 2),
        end=datetime.date(2026, 7, 5),
        weeks=(week,),
    )
    return {group_name: sem}


class TestAggregateSubjects:
    def test_basic_aggregation(self):
        timetables = _make_timetable("3MKIB4")
        subjects = aggregate_subjects(timetables)
        assert "MATH" in subjects
        subj = subjects["MATH"]
        assert subj.long_name == "Mathematics"
        assert subj.alternate_name == "MA"
        assert "3MKIB4" in subj.groups
        assert subj.total_occurrences == 1

    def test_multiple_groups(self):
        tt1 = _make_timetable("3MKIB4")
        tt2 = _make_timetable("3MKIB6")
        combined = {**tt1, **tt2}
        subjects = aggregate_subjects(combined)
        assert "3MKIB4" in subjects["MATH"].groups
        assert "3MKIB6" in subjects["MATH"].groups
        assert subjects["MATH"].total_occurrences == 2

    def test_lessons_populated(self):
        subjects = aggregate_subjects(_make_timetable("3MKIB4"))
        subj = subjects["MATH"]
        assert len(subj.lessons) == 1
        assert subj.lessons[0].room == "A101"
