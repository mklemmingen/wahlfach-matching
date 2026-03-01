"""Tests for the scoring logic."""

from datetime import date, time

from wahlfach_matching.config import MatchConfig
from wahlfach_matching.models import Lesson, Subject
from wahlfach_matching.scorer import score_all, score_subject


def _make_subject(code: str, lessons: list[Lesson] | None = None) -> Subject:
    subj = Subject(code=code, total_occurrences=len(lessons or []))
    if lessons:
        subj.lessons = lessons
        for le in lessons:
            subj.weekdays.add(le.weekday)
    return subj


class TestScoreSubject:
    def test_no_conflict(self):
        subj = _make_subject("ELEC", [
            Lesson(date=date(2026, 3, 4), weekday="Wednesday", start=time(10, 0), end=time(11, 30)),
        ])
        config = MatchConfig()
        result = score_subject(subj, {}, config)
        assert result.conflict_count == 0
        assert result.score >= config.weight_no_conflict

    def test_conflict_detected(self):
        subj = _make_subject("ELEC", [
            Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(8, 0), end=time(9, 30)),
        ])
        mandatory_slots = {"Monday": [("08:00", "09:30")]}
        config = MatchConfig()
        result = score_subject(subj, mandatory_slots, config)
        assert result.conflict_count == 1

    def test_partial_overlap(self):
        subj = _make_subject("ELEC", [
            Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(9, 0), end=time(10, 30)),
        ])
        mandatory_slots = {"Monday": [("08:00", "09:30")]}
        config = MatchConfig()
        result = score_subject(subj, mandatory_slots, config)
        assert result.conflict_count == 1

    def test_preferred_day_bonus(self):
        subj = _make_subject("ELEC", [
            Lesson(date=date(2026, 3, 4), weekday="Wednesday", start=time(10, 0), end=time(11, 30)),
        ])
        config = MatchConfig(preferred_weekdays=["Wednesday"])
        result = score_subject(subj, {}, config)
        assert result.score > MatchConfig().weight_no_conflict


class TestScoreAll:
    def test_skips_mandatory(self):
        mandatory = {"MATH": _make_subject("MATH")}
        subjects = {
            "MATH": _make_subject("MATH"),
            "ELEC": _make_subject("ELEC"),
        }
        config = MatchConfig()
        results = score_all(subjects, mandatory, config)
        codes = [r.subject.code for r in results]
        assert "MATH" not in codes
        assert "ELEC" in codes

    def test_sorted_by_score_desc(self):
        subjects = {
            "A": _make_subject("A", [
                Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(8, 0), end=time(9, 30)),
            ]),
            "B": _make_subject("B", [
                Lesson(date=date(2026, 3, 4), weekday="Wednesday", start=time(10, 0), end=time(11, 30)),
            ]),
        }
        mandatory_slots_subj = _make_subject("MAND", [
            Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(8, 0), end=time(9, 30)),
        ])
        config = MatchConfig()
        results = score_all(subjects, {"MAND": mandatory_slots_subj}, config)
        # B should rank higher (no conflict), A has conflict with MAND
        assert results[0].subject.code == "B"
