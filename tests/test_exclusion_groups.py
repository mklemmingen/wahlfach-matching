"""Tests for mutual-exclusion group functionality."""

import json
from datetime import date, datetime, time

from wahlfach_matching.cache import (
    StaticCourseCache,
    _deserialize_static_courses,
    _serialize_static_courses,
)
from wahlfach_matching.cli import parse_args
from wahlfach_matching.config import MatchConfig
from wahlfach_matching.models import Lesson, StaticCourse, Subject, TimeSlot
from wahlfach_matching.optimizer import (
    _build_exclusion_index,
    _violates_exclusion_groups,
    find_best_combinations,
)


def _make_subject(code: str, lessons: list[Lesson] | None = None, exclusion_group: str | None = None) -> Subject:
    subj = Subject(code=code, total_occurrences=len(lessons or []), exclusion_group=exclusion_group)
    if lessons:
        subj.lessons = lessons
        for le in lessons:
            subj.weekdays.add(le.weekday)
            subj.time_slots.add(f"{le.start:%H:%M}-{le.end:%H:%M}")
    return subj


def _make_lesson(day_offset: int = 0, hour: int = 8) -> Lesson:
    return Lesson(
        date=date(2026, 3, 2 + day_offset),
        weekday="Monday",
        start=time(hour, 0),
        end=time(hour + 1, 30),
    )


class TestViolatesExclusionGroups:
    def test_no_groups_no_violation(self):
        a = _make_subject("A")
        b = _make_subject("B")
        assert _violates_exclusion_groups((a, b), {}) is False

    def test_different_groups_no_violation(self):
        a = _make_subject("A")
        b = _make_subject("B")
        code_to_group = {"A": "GROUP1", "B": "GROUP2"}
        assert _violates_exclusion_groups((a, b), code_to_group) is False

    def test_same_group_violation(self):
        a = _make_subject("A")
        b = _make_subject("B")
        code_to_group = {"A": "SPANISH1", "B": "SPANISH1"}
        assert _violates_exclusion_groups((a, b), code_to_group) is True

    def test_three_subjects_one_pair_violates(self):
        a = _make_subject("A")
        b = _make_subject("B")
        c = _make_subject("C")
        code_to_group = {"A": "SPANISH1", "C": "SPANISH1"}
        assert _violates_exclusion_groups((a, b, c), code_to_group) is True

    def test_single_subject_never_violates(self):
        a = _make_subject("A")
        code_to_group = {"A": "SPANISH1"}
        assert _violates_exclusion_groups((a,), code_to_group) is False

    def test_empty_subset(self):
        assert _violates_exclusion_groups((), {"A": "G"}) is False


class TestBuildExclusionIndex:
    def test_from_subject_fields(self):
        subjects = {
            "A": _make_subject("A", exclusion_group="SPANISH1"),
            "B": _make_subject("B", exclusion_group="SPANISH1"),
            "C": _make_subject("C"),
        }
        config = MatchConfig()
        index = _build_exclusion_index(subjects, config)
        assert index == {"A": "SPANISH1", "B": "SPANISH1"}

    def test_from_config_groups(self):
        subjects = {"A": _make_subject("A"), "B": _make_subject("B")}
        config = MatchConfig(exclusion_groups={"LANG": ["A", "B"]})
        index = _build_exclusion_index(subjects, config)
        assert index == {"A": "LANG", "B": "LANG"}

    def test_merge_static_and_config(self):
        subjects = {
            "A": _make_subject("A", exclusion_group="SPANISH1"),
            "B": _make_subject("B"),
            "C": _make_subject("C"),
        }
        config = MatchConfig(exclusion_groups={"OTHER": ["B", "C"]})
        index = _build_exclusion_index(subjects, config)
        assert index["A"] == "SPANISH1"
        assert index["B"] == "OTHER"
        assert index["C"] == "OTHER"

    def test_config_overrides_subject_field(self):
        subjects = {"A": _make_subject("A", exclusion_group="OLD")}
        config = MatchConfig(exclusion_groups={"NEW": ["A"]})
        index = _build_exclusion_index(subjects, config)
        # Config is applied after subject fields, so it overrides
        assert index["A"] == "NEW"

    def test_empty_when_no_groups(self):
        subjects = {"A": _make_subject("A"), "B": _make_subject("B")}
        config = MatchConfig()
        index = _build_exclusion_index(subjects, config)
        assert index == {}


class TestFindBestCombinationsExclusion:
    def test_subsets_with_two_group_members_skipped(self, tmp_path):
        """Combinations with 2 courses from the same group should never appear."""
        sp1 = _make_subject("SP1", [_make_lesson(0, 8)], exclusion_group="SPANISH1")
        sp2 = _make_subject("SP2", [_make_lesson(1, 10)], exclusion_group="SPANISH1")
        other = _make_subject("OTHER", [_make_lesson(2, 14)])
        subjects = {"SP1": sp1, "SP2": sp2, "OTHER": other}
        config = MatchConfig(
            nice_to_have_subjects=["SP1", "SP2", "OTHER"],
            max_electives=3,
            max_combinations=10,
            output_dir=str(tmp_path),
        )
        combos = find_best_combinations(subjects, {}, config)
        for combo in combos:
            codes = {s.code for s in combo.subjects}
            assert not ({"SP1", "SP2"} <= codes), "SP1 and SP2 should never appear together"

    def test_must_have_conflict_same_group_returns_empty(self, tmp_path):
        """2 must-haves in the same group → error, return []."""
        sp1 = _make_subject("SP1", [_make_lesson(0)], exclusion_group="SPANISH1")
        sp2 = _make_subject("SP2", [_make_lesson(1)], exclusion_group="SPANISH1")
        subjects = {"SP1": sp1, "SP2": sp2}
        config = MatchConfig(
            must_have_subjects=["SP1", "SP2"],
            max_electives=3,
            max_combinations=5,
            output_dir=str(tmp_path),
        )
        combos = find_best_combinations(subjects, {}, config)
        assert combos == []

    def test_must_have_removes_siblings_from_pool(self, tmp_path):
        """A must-have in a group should remove all siblings from nice-to-have and filler pools."""
        sp1 = _make_subject("SP1", [_make_lesson(0, 8)], exclusion_group="SPANISH1")
        sp2 = _make_subject("SP2", [_make_lesson(1, 10)], exclusion_group="SPANISH1")
        other = _make_subject("OTHER", [_make_lesson(2, 14)])
        subjects = {"SP1": sp1, "SP2": sp2, "OTHER": other}
        config = MatchConfig(
            must_have_subjects=["SP1"],
            nice_to_have_subjects=["SP2", "OTHER"],
            max_electives=3,
            max_combinations=10,
            output_dir=str(tmp_path),
        )
        combos = find_best_combinations(subjects, {}, config)
        for combo in combos:
            codes = {s.code for s in combo.subjects}
            assert "SP2" not in codes, "SP2 should be pruned since SP1 is must-have in same group"
            assert "SP1" in codes, "SP1 must-have should always be present"

    def test_no_exclusion_group_backward_compat(self, tmp_path):
        """Subjects without exclusion_group work normally."""
        a = _make_subject("A", [_make_lesson(0, 8)])
        b = _make_subject("B", [_make_lesson(1, 10)])
        subjects = {"A": a, "B": b}
        config = MatchConfig(
            nice_to_have_subjects=["A", "B"],
            max_electives=3,
            max_combinations=5,
            output_dir=str(tmp_path),
        )
        combos = find_best_combinations(subjects, {}, config)
        assert len(combos) > 0
        # A and B should be able to appear together
        found_both = any(
            {"A", "B"} <= {s.code for s in combo.subjects}
            for combo in combos
        )
        assert found_both


class TestStaticCourseCacheExclusionGroup:
    def test_round_trip_with_exclusion_group(self, tmp_path):
        course = StaticCourse(
            code="SP1",
            name="Spanish 1",
            category="nice_to_have",
            schedule=[TimeSlot(weekday="Tuesday", start=time(8, 0), end=time(9, 30))],
            exclusion_group="SPANISH1",
        )
        cache = StaticCourseCache(cache_dir=str(tmp_path))
        cache.save(course)
        loaded = cache.load_all()
        assert loaded["SP1"].exclusion_group == "SPANISH1"

    def test_round_trip_without_exclusion_group(self, tmp_path):
        course = StaticCourse(
            code="OTHER",
            name="Other Course",
            category="must_have",
            schedule=[TimeSlot(weekday="Monday", start=time(10, 0), end=time(11, 30))],
        )
        cache = StaticCourseCache(cache_dir=str(tmp_path))
        cache.save(course)
        loaded = cache.load_all()
        assert loaded["OTHER"].exclusion_group is None

    def test_deserialize_missing_field_backward_compat(self):
        """JSON without exclusion_group field should deserialize with None."""
        raw = {
            "TEST": {
                "code": "TEST",
                "name": "Test",
                "category": "must_have",
                "notes": "",
                "created_at": "2026-03-02T12:00:00",
                "schedule": [{"weekday": "Monday", "start": "08:00", "end": "09:30"}],
                "specific_dates": None,
            }
        }
        courses = _deserialize_static_courses(raw)
        assert courses["TEST"].exclusion_group is None

    def test_serialize_includes_exclusion_group(self):
        course = StaticCourse(
            code="SP1",
            name="Spanish 1",
            category="nice_to_have",
            schedule=[TimeSlot(weekday="Tuesday", start=time(8, 0), end=time(9, 30))],
            exclusion_group="SPANISH1",
        )
        raw = _serialize_static_courses({"SP1": course})
        assert raw["SP1"]["exclusion_group"] == "SPANISH1"


class TestCLIExclusionGroupParsing:
    def test_single_group(self):
        config = parse_args(["--exclusion-group", "SPANISH1:SP1,SP2,SP3"])
        assert config.exclusion_groups == {"SPANISH1": ["SP1", "SP2", "SP3"]}

    def test_multiple_groups(self):
        config = parse_args([
            "--exclusion-group", "SPANISH1:SP1,SP2",
            "--exclusion-group", "FRENCH1:FR1,FR2",
        ])
        assert config.exclusion_groups == {
            "SPANISH1": ["SP1", "SP2"],
            "FRENCH1": ["FR1", "FR2"],
        }

    def test_default_empty(self):
        config = parse_args([])
        assert config.exclusion_groups == {}

    def test_repeated_group_merges(self):
        config = parse_args([
            "--exclusion-group", "LANG:SP1,SP2",
            "--exclusion-group", "LANG:SP3",
        ])
        assert config.exclusion_groups == {"LANG": ["SP1", "SP2", "SP3"]}
