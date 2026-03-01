"""Tests for the combinatorial schedule optimizer."""

from datetime import date, time

from wahlfach_matching.config import MatchConfig
from wahlfach_matching.models import Lesson, Subject
from wahlfach_matching.optimizer import (
    _compute_metrics,
    _lessons_conflict,
    _subjects_conflict,
    find_best_combinations,
)


def _make_subject(code: str, lessons: list[Lesson] | None = None) -> Subject:
    subj = Subject(code=code, total_occurrences=len(lessons or []))
    if lessons:
        subj.lessons = lessons
        for le in lessons:
            subj.weekdays.add(le.weekday)
            subj.time_slots.add(f"{le.start:%H:%M}-{le.end:%H:%M}")
    return subj


class TestLessonsConflict:
    def test_same_date_overlapping(self):
        a = Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(8, 0), end=time(9, 30))
        b = Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(9, 0), end=time(10, 30))
        assert _lessons_conflict(a, b) is True

    def test_same_date_no_overlap(self):
        a = Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(8, 0), end=time(9, 0))
        b = Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(9, 0), end=time(10, 0))
        assert _lessons_conflict(a, b) is False

    def test_different_dates(self):
        a = Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(8, 0), end=time(9, 30))
        b = Lesson(date=date(2026, 3, 9), weekday="Monday", start=time(8, 0), end=time(9, 30))
        assert _lessons_conflict(a, b) is False

    def test_exact_same_slot(self):
        a = Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(8, 0), end=time(9, 30))
        b = Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(8, 0), end=time(9, 30))
        assert _lessons_conflict(a, b) is True


class TestSubjectsConflict:
    def test_no_conflict(self):
        a = _make_subject("A", [
            Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(8, 0), end=time(9, 30)),
        ])
        b = _make_subject("B", [
            Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(10, 0), end=time(11, 30)),
        ])
        assert _subjects_conflict(a, b) == []

    def test_with_conflict(self):
        a = _make_subject("A", [
            Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(8, 0), end=time(9, 30)),
        ])
        b = _make_subject("B", [
            Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(9, 0), end=time(10, 30)),
        ])
        conflicts = _subjects_conflict(a, b)
        assert len(conflicts) == 1
        assert "A vs B" in conflicts[0]


class TestComputeMetrics:
    def test_single_subject(self):
        subj = _make_subject("A", [
            Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(8, 0), end=time(9, 30)),
            Lesson(date=date(2026, 3, 4), weekday="Wednesday", start=time(10, 0), end=time(11, 30)),
        ])
        metrics = _compute_metrics([subj])
        assert metrics.earliest_start == "08:00"
        assert metrics.latest_end == "11:30"
        assert metrics.free_days_per_week == 3  # Tue, Thu, Fri

    def test_closeness_consecutive(self):
        subj = _make_subject("A", [
            Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(8, 0), end=time(9, 0)),
            Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(9, 30), end=time(10, 30)),
        ])
        metrics = _compute_metrics([subj])
        assert metrics.closeness == 30.0  # 30 min gap

    def test_empty_subjects(self):
        metrics = _compute_metrics([])
        assert metrics.free_days_per_week == 0
        assert metrics.earliest_start == ""


class TestFindBestCombinations:
    def test_basic_combinations(self):
        must = _make_subject("MUST", [
            Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(8, 0), end=time(9, 30)),
        ])
        nice = _make_subject("NICE", [
            Lesson(date=date(2026, 3, 4), weekday="Wednesday", start=time(10, 0), end=time(11, 30)),
        ])
        filler = _make_subject("FILL", [
            Lesson(date=date(2026, 3, 5), weekday="Thursday", start=time(14, 0), end=time(15, 30)),
        ])
        subjects = {"MUST": must, "NICE": nice, "FILL": filler}
        config = MatchConfig(
            must_have_subjects=["MUST"],
            nice_to_have_subjects=["NICE"],
            max_electives=3,
            max_combinations=5,
        )
        combos = find_best_combinations(subjects, {}, config)
        assert len(combos) > 0
        # Must-have should be in every combination
        for combo in combos:
            must_codes = [s.code for s in combo.must_have_subjects]
            assert "MUST" in must_codes

    def test_respects_max_combinations(self):
        subjects = {}
        for i in range(10):
            code = f"SUBJ{i}"
            subjects[code] = _make_subject(code, [
                Lesson(date=date(2026, 3, 2 + i % 5), weekday="Monday",
                       start=time(8 + i, 0), end=time(9 + i, 30)),
            ])
        config = MatchConfig(
            nice_to_have_subjects=["SUBJ0", "SUBJ1"],
            max_electives=4,
            max_combinations=3,
        )
        combos = find_best_combinations(subjects, {}, config)
        assert len(combos) <= 3

    def test_only_must_haves_when_full(self):
        subjects = {}
        for i in range(3):
            code = f"M{i}"
            subjects[code] = _make_subject(code, [
                Lesson(date=date(2026, 3, 2 + i), weekday=["Monday", "Tuesday", "Wednesday"][i],
                       start=time(8, 0), end=time(9, 30)),
            ])
        config = MatchConfig(
            must_have_subjects=["M0", "M1", "M2"],
            max_electives=3,  # exactly the must-haves
            max_combinations=5,
        )
        combos = find_best_combinations(subjects, {}, config)
        assert len(combos) == 1
        assert len(combos[0].subjects) == 3

    def test_excludes_mandatory_from_candidates(self):
        mandatory = _make_subject("MAND", [
            Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(8, 0), end=time(9, 30)),
        ])
        nice = _make_subject("NICE", [
            Lesson(date=date(2026, 3, 4), weekday="Wednesday", start=time(10, 0), end=time(11, 30)),
        ])
        subjects = {"MAND": mandatory, "NICE": nice}
        config = MatchConfig(
            nice_to_have_subjects=["NICE"],
            max_electives=3,
            max_combinations=5,
        )
        combos = find_best_combinations(subjects, {"MAND": mandatory}, config)
        for combo in combos:
            codes = [s.code for s in combo.subjects]
            assert "MAND" not in codes

    def test_conflict_penalty(self):
        # Two subjects at the same time should score lower than two non-conflicting
        a = _make_subject("A", [
            Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(8, 0), end=time(9, 30)),
        ])
        b_conflict = _make_subject("B", [
            Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(8, 0), end=time(9, 30)),
        ])
        b_no_conflict = _make_subject("C", [
            Lesson(date=date(2026, 3, 4), weekday="Wednesday", start=time(10, 0), end=time(11, 30)),
        ])
        subjects = {"A": a, "B": b_conflict, "C": b_no_conflict}
        config = MatchConfig(
            nice_to_have_subjects=["A", "B", "C"],
            max_electives=2,
            max_combinations=10,
        )
        combos = find_best_combinations(subjects, {}, config)
        # The combination {A, C} should rank higher than {A, B} due to conflict penalty
        for combo in combos:
            codes = sorted(s.code for s in combo.subjects)
            if codes == ["A", "C"]:
                ac_score = combo.score
            elif codes == ["A", "B"]:
                ab_score = combo.score
        assert ac_score > ab_score
