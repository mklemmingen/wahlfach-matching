"""Tests for CLI argument parsing."""

from wahlfach_matching.cli import parse_args


class TestParseArgs:
    def test_defaults(self):
        config = parse_args([])
        assert config.programs == ["MKIB"]
        assert config.semesters == [4, 6, 7]
        assert config.mandatory_subjects == []
        assert config.top_n == 10
        assert config.export_ics is True
        assert config.interactive is False
        assert config.must_have_subjects == []
        assert config.nice_to_have_subjects == []
        assert config.max_combinations == 5
        assert config.max_electives == 6

    def test_custom_programs(self):
        config = parse_args(["--programs", "MKIB", "WIB"])
        assert config.programs == ["MKIB", "WIB"]

    def test_mandatory(self):
        config = parse_args(["--mandatory", "MATH", "PHYS"])
        assert config.mandatory_subjects == ["MATH", "PHYS"]

    def test_no_ics(self):
        config = parse_args(["--no-ics"])
        assert config.export_ics is False

    def test_top(self):
        config = parse_args(["--top", "20"])
        assert config.top_n == 20

    def test_interactive_flag(self):
        config = parse_args(["--interactive"])
        assert config.interactive is True

    def test_must_have(self):
        config = parse_args(["--must-have", "MATH", "PHYS"])
        assert config.must_have_subjects == ["MATH", "PHYS"]

    def test_nice_to_have(self):
        config = parse_args(["--nice-to-have", "ART", "MUSIC"])
        assert config.nice_to_have_subjects == ["ART", "MUSIC"]

    def test_max_combinations(self):
        config = parse_args(["--max-combinations", "10"])
        assert config.max_combinations == 10

    def test_max_electives(self):
        config = parse_args(["--max-electives", "8"])
        assert config.max_electives == 8

    def test_combination_mode_triggered(self):
        config = parse_args(["--must-have", "MATH"])
        assert config.must_have_subjects == ["MATH"]
        assert config.interactive is False
