"""Tests for the interactive module (mocked InquirerPy)."""

from datetime import date, time
from unittest.mock import MagicMock, patch

from wahlfach_matching.models import Lesson, Subject


def _make_subject(code: str) -> Subject:
    return Subject(
        code=code,
        long_name=f"Long {code}",
        lessons=[
            Lesson(date=date(2026, 3, 2), weekday="Monday", start=time(8, 0), end=time(9, 30)),
        ],
        total_occurrences=1,
    )


class TestSelectPrograms:
    @patch("wahlfach_matching.interactive.inquirer")
    def test_returns_selected(self, mock_inquirer):
        mock_inquirer.checkbox.return_value.execute.return_value = ["MKIB", "WIB"]
        from wahlfach_matching.interactive import select_programs
        result = select_programs()
        assert result == ["MKIB", "WIB"]


class TestSelectSemesters:
    @patch("wahlfach_matching.interactive.inquirer")
    def test_returns_selected(self, mock_inquirer):
        mock_inquirer.checkbox.return_value.execute.return_value = [4, 6]
        from wahlfach_matching.interactive import select_semesters
        result = select_semesters()
        assert result == [4, 6]


class TestCategorizeSubjects:
    @patch("wahlfach_matching.interactive.inquirer")
    def test_two_step_categorization(self, mock_inquirer):
        subjects = [_make_subject("MATH"), _make_subject("ART"), _make_subject("PHYS")]

        # First call: must-have selection returns MATH
        # Second call: nice-to-have selection returns ART
        mock_checkbox = MagicMock()
        mock_checkbox.execute.side_effect = [["MATH"], ["ART"]]
        mock_inquirer.checkbox.return_value = mock_checkbox

        from wahlfach_matching.interactive import categorize_subjects
        must, nice = categorize_subjects(subjects)
        assert must == ["MATH"]
        assert nice == ["ART"]


class TestConfirmAndConfigure:
    @patch("wahlfach_matching.interactive.inquirer")
    def test_confirmed(self, mock_inquirer):
        mock_number = MagicMock()
        mock_number.execute.side_effect = [6, 5]
        mock_inquirer.number.return_value = mock_number

        mock_confirm = MagicMock()
        mock_confirm.execute.return_value = True
        mock_inquirer.confirm.return_value = mock_confirm

        from wahlfach_matching.interactive import confirm_and_configure
        result = confirm_and_configure(["MATH"], ["ART"])
        assert result["confirmed"] is True
        assert result["max_electives"] == 6
        assert result["max_combinations"] == 5

    @patch("wahlfach_matching.interactive.inquirer")
    def test_cancelled(self, mock_inquirer):
        mock_number = MagicMock()
        mock_number.execute.return_value = 6
        mock_inquirer.number.return_value = mock_number

        mock_confirm = MagicMock()
        mock_confirm.execute.return_value = False
        mock_inquirer.confirm.return_value = mock_confirm

        from wahlfach_matching.interactive import confirm_and_configure
        result = confirm_and_configure(["MATH"], ["ART"])
        assert result["confirmed"] is False
