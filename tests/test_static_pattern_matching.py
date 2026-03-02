"""Tests for static course pattern matching integration."""

from datetime import date, time

import pytest

from wahlfach_matching.cache import StaticCourseCache
from wahlfach_matching.config import MatchConfig
from wahlfach_matching.models import Lesson, StaticCourse, Subject, TimeSlot
from wahlfach_matching.optimizer import _load_static_courses


@pytest.fixture()
def static_cache(tmp_path):
    """Create a StaticCourseCache with test courses."""
    cache = StaticCourseCache(str(tmp_path))

    must_have_course = StaticCourse(
        code="TEST_MUST",
        name="Test Must Have Course",
        category="must_have",
        schedule=[TimeSlot("Monday", time(10, 0), time(12, 0))],
    )
    nice_to_have_course = StaticCourse(
        code="TEST_NICE",
        name="Test Nice To Have Course",
        category="nice_to_have",
        schedule=[TimeSlot("Tuesday", time(14, 0), time(16, 0))],
    )

    cache.save(must_have_course)
    cache.save(nice_to_have_course)
    return cache, tmp_path


class TestStaticPatternMatching:
    def test_static_courses_saved_and_loaded(self, static_cache):
        cache, cache_dir = static_cache
        courses = cache.list_all()
        assert len(courses) == 2
        codes = {c.code for c in courses}
        assert codes == {"TEST_MUST", "TEST_NICE"}

    def test_category_mapping(self, tmp_path):
        """_load_static_courses reads from output_dir/.cache/static_courses.json."""
        # Set up the expected directory layout: output_dir/.cache/
        output_dir = tmp_path / "output"
        cache_dir = output_dir / ".cache"
        cache_dir.mkdir(parents=True)

        cache = StaticCourseCache(str(cache_dir))
        cache.save(StaticCourse(
            code="TEST_MUST",
            name="Test Must Have Course",
            category="must_have",
            schedule=[TimeSlot("Monday", time(10, 0), time(12, 0))],
        ))
        cache.save(StaticCourse(
            code="TEST_NICE",
            name="Test Nice To Have Course",
            category="nice_to_have",
            schedule=[TimeSlot("Tuesday", time(14, 0), time(16, 0))],
        ))

        config = MatchConfig(output_dir=str(output_dir))
        # _load_static_courses needs non-empty subjects to derive date range
        dummy_subj = Subject(code="DUMMY", long_name="Dummy", total_occurrences=1)
        dummy_subj.lessons = [
            Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(8, 0), end=time(9, 30)),
            Lesson(date=date(2026, 7, 10), weekday="Friday", start=time(8, 0), end=time(9, 30)),
        ]
        subjects_with_dates = {"DUMMY": dummy_subj}
        static_subjects, static_categories = _load_static_courses(config, subjects_with_dates)

        assert "TEST_MUST" in static_categories
        assert "TEST_NICE" in static_categories
        assert static_categories["TEST_MUST"] == "must_have"
        assert static_categories["TEST_NICE"] == "nice_to_have"

    def test_must_have_category(self, static_cache):
        cache, _ = static_cache
        courses = cache.list_all()
        must = [c for c in courses if c.code == "TEST_MUST"][0]
        assert must.category == "must_have"

    def test_nice_to_have_category(self, static_cache):
        cache, _ = static_cache
        courses = cache.list_all()
        nice = [c for c in courses if c.code == "TEST_NICE"][0]
        assert nice.category == "nice_to_have"
