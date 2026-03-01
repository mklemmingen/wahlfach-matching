"""Tests for the file-based timetable cache."""

import time as _time
from datetime import date, time
from unittest.mock import patch

from wahlfach_matching.cache import SubjectCache, _deserialize_subjects, _serialize_subjects
from wahlfach_matching.config import MatchConfig
from wahlfach_matching.models import Lesson, Subject


def _make_subjects() -> dict[str, Subject]:
    return {
        "MATH": Subject(
            code="MATH",
            long_name="Mathematics",
            alternate_name="Math",
            groups={"MKIB-4"},
            teachers={"Prof. A"},
            rooms={"R101"},
            total_occurrences=5,
            weekdays={"Monday", "Wednesday"},
            time_slots={"08:00-09:30"},
            dates={"2026-03-02", "2026-03-04"},
            lessons=[
                Lesson(
                    date=date(2026, 3, 2),
                    weekday="Monday",
                    start=time(8, 0),
                    end=time(9, 30),
                    room="R101",
                    group="MKIB-4",
                ),
            ],
        ),
        "ART": Subject(
            code="ART",
            long_name="Art History",
            groups=set(),
            teachers=set(),
            rooms=set(),
            total_occurrences=2,
            weekdays={"Friday"},
            time_slots={"14:00-15:30"},
            dates={"2026-03-06"},
            lessons=[],
        ),
    }


class TestSerializeDeserialize:
    def test_round_trip(self):
        subjects = _make_subjects()
        raw = _serialize_subjects(subjects)
        restored = _deserialize_subjects(raw)

        assert set(restored.keys()) == {"MATH", "ART"}

        math = restored["MATH"]
        assert math.code == "MATH"
        assert math.long_name == "Mathematics"
        assert math.alternate_name == "Math"
        assert math.groups == {"MKIB-4"}
        assert math.teachers == {"Prof. A"}
        assert math.rooms == {"R101"}
        assert math.total_occurrences == 5
        assert math.weekdays == {"Monday", "Wednesday"}
        assert math.time_slots == {"08:00-09:30"}
        assert math.dates == {"2026-03-02", "2026-03-04"}

        assert len(math.lessons) == 1
        lesson = math.lessons[0]
        assert lesson.date == date(2026, 3, 2)
        assert lesson.weekday == "Monday"
        assert lesson.start == time(8, 0)
        assert lesson.end == time(9, 30)
        assert lesson.room == "R101"
        assert lesson.group == "MKIB-4"

    def test_empty_subjects(self):
        raw = _serialize_subjects({})
        restored = _deserialize_subjects(raw)
        assert restored == {}

    def test_sets_become_sorted_lists_in_json(self):
        subjects = _make_subjects()
        raw = _serialize_subjects(subjects)
        # Sets should serialize as sorted lists
        assert raw["MATH"]["weekdays"] == ["Monday", "Wednesday"]
        assert raw["MATH"]["groups"] == ["MKIB-4"]


class TestCacheKey:
    def test_same_config_same_key(self):
        cache = SubjectCache()
        cfg1 = MatchConfig(programs=["MKIB", "WIB"], semesters=[4, 6])
        cfg2 = MatchConfig(programs=["WIB", "MKIB"], semesters=[6, 4])
        assert cache._cache_key(cfg1) == cache._cache_key(cfg2)

    def test_different_config_different_key(self):
        cache = SubjectCache()
        cfg1 = MatchConfig(programs=["MKIB"], semesters=[4])
        cfg2 = MatchConfig(programs=["WIB"], semesters=[4])
        assert cache._cache_key(cfg1) != cache._cache_key(cfg2)


class TestCacheSaveLoad:
    def test_save_and_load(self, tmp_path):
        cache = SubjectCache(cache_dir=str(tmp_path / ".cache"), ttl_hours=24)
        config = MatchConfig(programs=["MKIB"], semesters=[4, 6])
        subjects = _make_subjects()

        cache.save(config, subjects)
        loaded = cache.load(config)

        assert loaded is not None
        assert set(loaded.keys()) == {"MATH", "ART"}
        assert loaded["MATH"].code == "MATH"
        assert loaded["MATH"].long_name == "Mathematics"
        assert len(loaded["MATH"].lessons) == 1

    def test_load_returns_none_when_no_cache(self, tmp_path):
        cache = SubjectCache(cache_dir=str(tmp_path / ".cache"), ttl_hours=24)
        config = MatchConfig()
        assert cache.load(config) is None

    def test_ttl_expiry(self, tmp_path):
        cache = SubjectCache(cache_dir=str(tmp_path / ".cache"), ttl_hours=1)
        config = MatchConfig()
        subjects = _make_subjects()

        cache.save(config, subjects)

        # Patch time to simulate expiry (2 hours later)
        with patch("wahlfach_matching.cache._time.time", return_value=_time.time() + 7200):
            assert cache.load(config) is None

    def test_clear(self, tmp_path):
        cache = SubjectCache(cache_dir=str(tmp_path / ".cache"), ttl_hours=24)
        config = MatchConfig()
        subjects = _make_subjects()

        cache.save(config, subjects)
        assert cache.load(config) is not None

        cache.clear()
        assert cache.load(config) is None

    def test_clear_nonexistent_dir(self, tmp_path):
        cache = SubjectCache(cache_dir=str(tmp_path / "nonexistent"))
        cache.clear()  # should not raise
