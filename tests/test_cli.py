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
