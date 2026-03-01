"""Wahlfach Matching — CLI tool for scoring and matching elective courses."""

from .config import MatchConfig
from .models import CombinationMetrics, Lesson, MatchResult, ScheduleCombination, Subject, TimeSlot

__all__ = [
    "CombinationMetrics",
    "Lesson",
    "MatchConfig",
    "MatchResult",
    "ScheduleCombination",
    "Subject",
    "TimeSlot",
]

__version__ = "0.1.0"
