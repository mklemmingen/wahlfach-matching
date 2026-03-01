"""High-level matching orchestrator."""

from __future__ import annotations

from .aggregator import aggregate_subjects
from .config import MatchConfig
from .fetcher import fetch_timetables
from .models import MatchResult, ScheduleCombination, Subject
from .optimizer import find_best_combinations
from .scorer import score_all


def run_matching(config: MatchConfig) -> tuple[dict[str, Subject], list[MatchResult]]:
    """Execute the full matching pipeline: fetch -> aggregate -> score.

    Returns (all_subjects, scored_results).
    """
    # 1. Fetch timetable data
    timetables = fetch_timetables(config)
    if not timetables:
        raise RuntimeError("No timetable data fetched.")

    # 2. Aggregate into subjects
    subjects = aggregate_subjects(timetables)
    print(f"\nFound {len(subjects)} unique subjects across all groups.\n")

    # 3. Identify mandatory subjects
    mandatory: dict[str, Subject] = {}
    for code in config.mandatory_subjects:
        if code in subjects:
            mandatory[code] = subjects[code]
        else:
            print(f"Warning: mandatory subject '{code}' not found in timetable data.")

    # 4. Score and rank
    results = score_all(subjects, mandatory, config)

    return subjects, results


def run_combination_matching(
    config: MatchConfig,
) -> tuple[dict[str, Subject], list[ScheduleCombination]]:
    """Execute the combination matching pipeline: fetch -> aggregate -> optimize.

    Returns (all_subjects, combinations).
    """
    # 1. Fetch timetable data
    timetables = fetch_timetables(config)
    if not timetables:
        raise RuntimeError("No timetable data fetched.")

    # 2. Aggregate into subjects
    subjects = aggregate_subjects(timetables)
    print(f"\nFound {len(subjects)} unique subjects across all groups.\n")

    # 3. Identify mandatory subjects
    mandatory: dict[str, Subject] = {}
    for code in config.mandatory_subjects:
        if code in subjects:
            mandatory[code] = subjects[code]
        else:
            print(f"Warning: mandatory subject '{code}' not found in timetable data.")

    # 4. Find best combinations
    combinations = find_best_combinations(subjects, mandatory, config)

    return subjects, combinations
