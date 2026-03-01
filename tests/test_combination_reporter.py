"""Tests for the combination reporter."""

import json
from datetime import date, time

from wahlfach_matching.combination_reporter import (
    print_combination_report,
    save_combination_json,
)
from wahlfach_matching.config import MatchConfig
from wahlfach_matching.models import (
    CombinationMetrics,
    Lesson,
    ScheduleCombination,
    Subject,
)


def _make_subject(code: str, lessons: list[Lesson] | None = None) -> Subject:
    subj = Subject(code=code, long_name=f"Long {code}", total_occurrences=len(lessons or []))
    if lessons:
        subj.lessons = lessons
        for le in lessons:
            subj.weekdays.add(le.weekday)
            subj.time_slots.add(f"{le.start:%H:%M}-{le.end:%H:%M}")
    return subj


def _make_combo() -> ScheduleCombination:
    must = _make_subject("MATH", [
        Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(8, 0), end=time(9, 30)),
    ])
    nice = _make_subject("ART", [
        Lesson(date=date(2026, 3, 6), weekday="Friday", start=time(10, 0), end=time(11, 30)),
    ])
    filler = _make_subject("ELEC1", [
        Lesson(date=date(2026, 3, 3), weekday="Tuesday", start=time(14, 0), end=time(15, 30)),
    ])
    return ScheduleCombination(
        subjects=[must, nice, filler],
        must_have_subjects=[must],
        nice_to_have_subjects=[nice],
        filler_subjects=[filler],
        score=42.5,
        nice_to_have_count=1,
        filler_count=1,
        metrics=CombinationMetrics(
            closeness=25.0,
            earliest_start="08:00",
            avg_start="09:15",
            latest_end="15:30",
            avg_end="12:10",
            free_days_per_week=2,
        ),
        notes=["1 nice-to-have(s) included", "1 filler(s) included"],
    )


class TestPrintCombinationReport:
    def test_prints_without_error(self, capsys):
        combo = _make_combo()
        config = MatchConfig()
        print_combination_report([combo], config)
        captured = capsys.readouterr()
        assert "Combination #1" in captured.out
        assert "42.5" in captured.out
        assert "[MUST]" in captured.out
        assert "[NICE]" in captured.out
        assert "[COULD FIT]" in captured.out
        assert "MATH" in captured.out
        assert "ART" in captured.out
        assert "ELEC1" in captured.out

    def test_ratings_displayed(self, capsys):
        combo = _make_combo()
        config = MatchConfig()
        print_combination_report([combo], config)
        captured = capsys.readouterr()
        assert "25 min" in captured.out
        assert "08:00" in captured.out
        assert "09:15" in captured.out
        assert "15:30" in captured.out

    def test_multiple_combinations(self, capsys):
        combos = [_make_combo(), _make_combo()]
        combos[1].score = 30.0
        config = MatchConfig()
        print_combination_report(combos, config)
        captured = capsys.readouterr()
        assert "Combination #1" in captured.out
        assert "Combination #2" in captured.out


class TestSaveCombinationJson:
    def test_creates_json_file(self, tmp_path):
        combo = _make_combo()
        config = MatchConfig(output_dir=str(tmp_path))
        path = save_combination_json([combo], config)
        assert path.exists()
        data = json.loads(path.read_text())
        assert len(data["combinations"]) == 1

    def test_json_structure(self, tmp_path):
        combo = _make_combo()
        config = MatchConfig(output_dir=str(tmp_path))
        path = save_combination_json([combo], config)
        data = json.loads(path.read_text())
        c = data["combinations"][0]
        assert c["rank"] == 1
        assert c["score"] == 42.5
        assert "metrics" in c
        assert c["metrics"]["closeness"] == 25.0
        assert len(c["subjects"]) == 3
        tiers = [s["tier"] for s in c["subjects"]]
        assert "must" in tiers
        assert "nice" in tiers
        assert "filler" in tiers
