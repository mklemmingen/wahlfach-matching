"""Wahlfach Matching — CLI tool for scoring and matching elective courses."""

from .config import MatchConfig
from .models import Lesson, MatchResult, Subject, TimeSlot

__all__ = [
    "Lesson",
    "MatchConfig",
    "MatchResult",
    "Subject",
    "TimeSlot",
]

__version__ = "0.1.0"
