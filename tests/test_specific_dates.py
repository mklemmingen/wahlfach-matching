"""Tests for specific_dates feature: model, cache round-trip, and conflict optimization."""

from datetime import date, datetime, time

from wahlfach_matching.cache import (
    StaticCourseCache,
    _deserialize_static_courses,
    _serialize_static_courses,
)
from wahlfach_matching.models import Lesson, StaticCourse, Subject, TimeSlot
from wahlfach_matching.optimizer import (
    _precompute_conflict_matrix,
    _precompute_mandatory_conflicts,
    _subjects_conflict,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_ec() -> StaticCourse:
    """EC: Saturday block course, 5 specific dates, 2 slots per day."""
    return StaticCourse(
        code="EC",
        name="E-Commerce",
        category="nice_to_have",
        schedule=[
            TimeSlot("Saturday", time(8, 0), time(13, 0)),
            TimeSlot("Saturday", time(13, 45), time(17, 0)),
        ],
        specific_dates=[
            date(2026, 3, 28),
            date(2026, 4, 18),
            date(2026, 5, 9),
            date(2026, 6, 6),
            date(2026, 7, 4),
        ],
    )


def _make_ros() -> StaticCourse:
    """ROS: Thursday block course, 3 specific dates, 3 slots per day."""
    return StaticCourse(
        code="ROS",
        name="Robotersysteme",
        category="nice_to_have",
        schedule=[
            TimeSlot("Thursday", time(9, 45), time(13, 0)),
            TimeSlot("Thursday", time(13, 45), time(17, 0)),
            TimeSlot("Thursday", time(17, 15), time(18, 45)),
        ],
        specific_dates=[
            date(2026, 3, 12),
            date(2026, 4, 16),
            date(2026, 6, 11),
        ],
    )


def _make_imr() -> StaticCourse:
    """IMR: Tue+Wed block, 4 weeks × 2 days = 8 specific dates."""
    return StaticCourse(
        code="IMR",
        name="Interaktive mobile Roboter",
        category="nice_to_have",
        schedule=[
            TimeSlot("Tuesday", time(17, 15), time(18, 45)),
            TimeSlot("Wednesday", time(13, 45), time(15, 15)),
        ],
        specific_dates=[
            date(2026, 3, 10),   # Tue
            date(2026, 3, 11),   # Wed
            date(2026, 4, 14),   # Tue
            date(2026, 4, 15),   # Wed
            date(2026, 5, 12),   # Tue
            date(2026, 5, 13),   # Wed
            date(2026, 6, 9),    # Tue
            date(2026, 6, 10),   # Wed
        ],
    )


def _make_subject(code: str, lessons: list[Lesson]) -> Subject:
    """Helper: build a Subject with populated dates."""
    subj = Subject(code=code, total_occurrences=len(lessons), lessons=lessons)
    for le in lessons:
        subj.weekdays.add(le.weekday)
        subj.time_slots.add(f"{le.start:%H:%M}-{le.end:%H:%M}")
        subj.dates.add(le.date.isoformat())
    return subj


# ---------------------------------------------------------------------------
# to_lessons() tests
# ---------------------------------------------------------------------------

class TestToLessonsSpecificDates:
    def test_ec_generates_10_lessons(self):
        ec = _make_ec()
        lessons = ec.to_lessons()
        assert len(lessons) == 10  # 5 dates × 2 Saturday slots

    def test_ros_generates_9_lessons(self):
        ros = _make_ros()
        lessons = ros.to_lessons()
        assert len(lessons) == 9  # 3 dates × 3 Thursday slots

    def test_imr_generates_8_lessons(self):
        imr = _make_imr()
        lessons = imr.to_lessons()
        assert len(lessons) == 8  # 4 Tuesdays × 1 slot + 4 Wednesdays × 1 slot

    def test_specific_dates_ignores_start_end(self):
        """start_date/end_date should be ignored when specific_dates is set."""
        ec = _make_ec()
        lessons = ec.to_lessons(start_date=date(2026, 1, 1), end_date=date(2026, 12, 31))
        assert len(lessons) == 10  # still 10, not weekly expansion

    def test_empty_list_returns_no_lessons(self):
        course = StaticCourse(
            code="EMPTY",
            name="Empty",
            category="nice_to_have",
            schedule=[TimeSlot("Monday", time(8, 0), time(9, 0))],
            specific_dates=[],
        )
        assert course.to_lessons() == []

    def test_none_falls_back_to_weekly(self):
        """specific_dates=None should use existing weekly expansion."""
        course = StaticCourse(
            code="WEEKLY",
            name="Weekly",
            category="nice_to_have",
            schedule=[TimeSlot("Monday", time(8, 0), time(9, 0))],
            specific_dates=None,
        )
        # Weekly with date range should generate multiple lessons
        lessons = course.to_lessons(
            start_date=date(2026, 3, 2),
            end_date=date(2026, 3, 30),
        )
        assert len(lessons) >= 4  # ~4 Mondays in March

    def test_weekday_mismatch_skipped(self):
        """Dates whose weekday doesn't match any TimeSlot produce no lessons."""
        course = StaticCourse(
            code="MISMATCH",
            name="Mismatch",
            category="nice_to_have",
            schedule=[TimeSlot("Monday", time(8, 0), time(9, 0))],
            specific_dates=[date(2026, 3, 11)],  # Wednesday
        )
        assert course.to_lessons() == []

    def test_lesson_fields_correct(self):
        """Verify lesson date, weekday, start, end are populated correctly."""
        ec = _make_ec()
        lessons = ec.to_lessons()
        mar28_lessons = [l for l in lessons if l.date == date(2026, 3, 28)]
        assert len(mar28_lessons) == 2
        assert all(l.weekday == "Saturday" for l in mar28_lessons)
        starts = sorted(l.start for l in mar28_lessons)
        assert starts == [time(8, 0), time(13, 45)]


# ---------------------------------------------------------------------------
# Cache round-trip tests
# ---------------------------------------------------------------------------

class TestCacheSpecificDates:
    def test_round_trip_with_dates(self):
        """specific_dates list survives serialize → deserialize."""
        ec = _make_ec()
        courses = {"EC": ec}
        raw = _serialize_static_courses(courses)
        restored = _deserialize_static_courses(raw)
        assert restored["EC"].specific_dates == ec.specific_dates

    def test_round_trip_none(self):
        """specific_dates=None survives round-trip."""
        course = StaticCourse(
            code="WEEKLY",
            name="Weekly",
            category="nice_to_have",
            schedule=[TimeSlot("Monday", time(8, 0), time(9, 0))],
            specific_dates=None,
        )
        raw = _serialize_static_courses({"WEEKLY": course})
        restored = _deserialize_static_courses(raw)
        assert restored["WEEKLY"].specific_dates is None

    def test_backward_compat_missing_key(self):
        """If 'specific_dates' key is absent in JSON, defaults to None."""
        raw = {
            "OLD": {
                "code": "OLD",
                "name": "Old Course",
                "category": "must_have",
                "schedule": [{"weekday": "Monday", "start": "08:00", "end": "09:00"}],
                "created_at": datetime.now().isoformat(),
            }
        }
        restored = _deserialize_static_courses(raw)
        assert restored["OLD"].specific_dates is None

    def test_file_round_trip(self, tmp_path):
        """Full save/load cycle via StaticCourseCache."""
        cache = StaticCourseCache(cache_dir=str(tmp_path / ".cache"))
        ec = _make_ec()
        cache.save(ec)

        loaded = cache.load_by_code("EC")
        assert loaded is not None
        assert loaded.specific_dates == ec.specific_dates
        assert len(loaded.specific_dates) == 5


# ---------------------------------------------------------------------------
# Conflict optimization tests
# ---------------------------------------------------------------------------

class TestConflictOptimization:
    def test_disjoint_dates_no_conflict(self):
        """Subjects on different dates should have 0 conflicts (fast path)."""
        a = _make_subject("A", [
            Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(8, 0), end=time(9, 30)),
        ])
        b = _make_subject("B", [
            Lesson(date=date(2026, 3, 3), weekday="Tuesday", start=time(8, 0), end=time(9, 30)),
        ])
        assert _subjects_conflict(a, b) == []

    def test_same_date_overlap_detected(self):
        """Overlapping lessons on same date still detected."""
        a = _make_subject("A", [
            Lesson(date=date(2026, 3, 12), weekday="Thursday", start=time(11, 30), end=time(15, 15)),
        ])
        b = _make_subject("B", [
            Lesson(date=date(2026, 3, 12), weekday="Thursday", start=time(9, 45), end=time(13, 0)),
        ])
        conflicts = _subjects_conflict(a, b)
        assert len(conflicts) == 1

    def test_precompute_conflict_matrix_structure(self):
        """Matrix keys are sorted code pairs; values are conflict lists."""
        a = _make_subject("A", [
            Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(8, 0), end=time(9, 30)),
        ])
        b = _make_subject("B", [
            Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(9, 0), end=time(10, 30)),
        ])
        c = _make_subject("C", [
            Lesson(date=date(2026, 3, 3), weekday="Tuesday", start=time(8, 0), end=time(9, 30)),
        ])
        matrix = _precompute_conflict_matrix([a, b, c])
        assert ("A", "B") in matrix
        assert len(matrix[("A", "B")]) == 1
        assert matrix.get(("A", "C"), []) == []
        assert matrix.get(("B", "C"), []) == []

    def test_precompute_mandatory_conflicts(self):
        """Mandatory conflict cache matches direct computation."""
        subj = _make_subject("X", [
            Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(8, 0), end=time(9, 30)),
        ])
        mandatory_slots = {"Monday": [("08:00", "09:00")]}
        cache = _precompute_mandatory_conflicts([subj], mandatory_slots)
        assert cache["X"] == 1

    def test_precompute_mandatory_no_conflict(self):
        subj = _make_subject("X", [
            Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(10, 0), end=time(11, 0)),
        ])
        mandatory_slots = {"Monday": [("08:00", "09:00")]}
        cache = _precompute_mandatory_conflicts([subj], mandatory_slots)
        assert cache["X"] == 0

    def test_ros_cg_conflict_count_specific_dates(self):
        """ROS with 3 specific Thursdays vs CG (weekly Thursday) → exactly 3 conflicts."""
        ros = _make_ros()
        ros_lessons = ros.to_lessons()
        ros_subj = _make_subject("ROS", ros_lessons)

        # CG runs every Thursday 11:30-15:15 across the semester
        cg_lessons = []
        d = date(2026, 3, 5)
        from datetime import timedelta
        while d <= date(2026, 7, 10):
            if d.weekday() == 3:  # Thursday
                cg_lessons.append(
                    Lesson(date=d, weekday="Thursday", start=time(11, 30), end=time(15, 15))
                )
            d += timedelta(days=1)
        cg_subj = _make_subject("CG", cg_lessons)

        conflicts = _subjects_conflict(ros_subj, cg_subj)
        # ROS has 3 Thursdays, each with 09:45-13:00 overlapping CG 11:30-15:15
        # and 13:45-17:00 also overlapping CG 11:30-15:15
        # So 3 dates × 2 overlapping slots = 6 conflicts
        assert len(conflicts) == 6
