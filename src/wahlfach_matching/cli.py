"""Command-line interface for wahlfach-matching."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .config import MatchConfig
from .ics_exporter import export_ics
from .matcher import run_matching
from .reporter import print_report, save_json_report


def parse_args(argv: list[str] | None = None) -> MatchConfig:
    """Parse CLI arguments into a MatchConfig."""
    parser = argparse.ArgumentParser(
        prog="wahlfach-matching",
        description="Score and rank elective courses based on schedule conflicts and preferences.",
    )
    parser.add_argument(
        "--programs",
        nargs="+",
        default=["MKIB"],
        help="Study programs to fetch (default: MKIB)",
    )
    parser.add_argument(
        "--semesters",
        nargs="+",
        type=int,
        default=[4, 6, 7],
        help="Semester numbers to fetch (default: 4 6 7)",
    )
    parser.add_argument(
        "--mandatory",
        nargs="*",
        default=[],
        help="Subject codes of mandatory courses (time slots will be blocked)",
    )
    parser.add_argument(
        "--preferred-days",
        nargs="*",
        default=[],
        help="Preferred weekdays (e.g. Monday Wednesday)",
    )
    parser.add_argument(
        "--max-conflicts",
        type=int,
        default=0,
        help="Maximum acceptable schedule conflicts (0 = show all)",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Number of top results to display (default: 10)",
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory for output files (default: output/)",
    )
    parser.add_argument(
        "--no-ics",
        action="store_true",
        help="Skip ICS calendar file export",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Also save a JSON report",
    )

    # Combination mode flags
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run interactive mode: browse and categorize subjects",
    )
    parser.add_argument(
        "--must-have",
        nargs="*",
        default=[],
        help="Subject codes that must be in every combination",
    )
    parser.add_argument(
        "--nice-to-have",
        nargs="*",
        default=[],
        help="Subject codes preferred but not required",
    )
    parser.add_argument(
        "--max-combinations",
        type=int,
        default=5,
        help="Number of top combinations to show (default: 5)",
    )
    parser.add_argument(
        "--max-electives",
        type=int,
        default=6,
        help="Maximum number of electives in a combination (default: 6)",
    )

    # Cache flags
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable timetable cache, always re-fetch",
    )
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear cached timetable data and exit",
    )
    parser.add_argument(
        "--cache-ttl",
        type=int,
        default=24,
        help="Cache time-to-live in hours (default: 24)",
    )

    args = parser.parse_args(argv)
    return MatchConfig(
        programs=args.programs,
        semesters=args.semesters,
        mandatory_subjects=args.mandatory or [],
        preferred_weekdays=args.preferred_days or [],
        max_conflicts=args.max_conflicts,
        top_n=args.top,
        output_dir=args.output_dir,
        export_ics=not args.no_ics,
        interactive=args.interactive,
        must_have_subjects=args.must_have or [],
        nice_to_have_subjects=args.nice_to_have or [],
        max_combinations=args.max_combinations,
        max_electives=args.max_electives,
        use_cache=not args.no_cache,
        cache_ttl_hours=args.cache_ttl,
    )


def _run_classic(config: MatchConfig, save_json: bool) -> int:
    """Run the classic single-subject ranking mode."""
    try:
        subjects, results = run_matching(config)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    print_report(subjects, results, config)

    if config.export_ics:
        print("\nExporting ICS calendar files...")
        export_ics(results, config)

    if save_json:
        save_json_report(subjects, results, config)

    return 0


def _fetch_with_cache(config: MatchConfig) -> dict[str, "Subject"]:
    """Fetch timetable data, using the cache when enabled."""
    from .aggregator import aggregate_subjects
    from .cache import SubjectCache
    from .fetcher import fetch_timetables

    if config.use_cache:
        cache = SubjectCache(
            cache_dir=str(Path(config.output_dir) / ".cache"),
            ttl_hours=config.cache_ttl_hours,
        )
        cached = cache.load(config)
        if cached is not None:
            print("Loaded timetable data from cache.")
            return cached

    print("\nFetching timetable data...")
    timetables = fetch_timetables(config)
    if not timetables:
        raise RuntimeError("No timetable data fetched.")

    subjects = aggregate_subjects(timetables)

    if config.use_cache:
        cache.save(config, subjects)
        print("Timetable data cached.")

    return subjects


def _run_combination_batch(config: MatchConfig, save_json: bool) -> int:
    """Run combination matching in batch mode (--must-have / --nice-to-have)."""
    from .combination_reporter import print_combination_report, save_combination_json
    from .ics_exporter import export_combination_ics

    try:
        subjects = _fetch_with_cache(config)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    print(f"\nFound {len(subjects)} unique subjects.\n")

    # Identify mandatory subjects and run optimizer
    from .optimizer import find_best_combinations

    mandatory = {code: subjects[code] for code in config.mandatory_subjects if code in subjects}
    combinations = find_best_combinations(subjects, mandatory, config)

    print_combination_report(combinations, config)

    if config.export_ics:
        print("\nExporting combination ICS files...")
        export_combination_ics(combinations, config)

    if save_json:
        save_combination_json(combinations, config)

    return 0


def _run_interactive(config: MatchConfig, save_json: bool) -> int:
    """Run interactive mode with terminal prompts and retry loop."""
    try:
        from .interactive import (
            categorize_subjects,
            confirm_and_configure,
            select_action_after_results,
            select_combinations_to_export,
            select_export_formats,
            select_programs,
            select_semesters,
        )
    except ImportError:
        print(
            "Error: Interactive mode requires InquirerPy. "
            "Install it with: pip install InquirerPy",
            file=sys.stderr,
        )
        return 1

    from .combination_reporter import (
        print_combination_report,
        save_combination_json,
        save_selected_combination_json,
    )
    from .ics_exporter import export_combination_ics, export_selected_combination_ics
    from .optimizer import find_best_combinations

    # Step 1: Select programs and semesters interactively
    programs = select_programs()
    if not programs:
        print("No programs selected. Exiting.")
        return 0
    config.programs = programs

    semesters = select_semesters()
    if not semesters:
        print("No semesters selected. Exiting.")
        return 0
    config.semesters = semesters

    # Step 2: Fetch and aggregate (with cache)
    try:
        subjects = _fetch_with_cache(config)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    print(f"\nFound {len(subjects)} unique subjects.\n")

    mandatory = {code: subjects[code] for code in config.mandatory_subjects if code in subjects}
    subject_list = sorted(subjects.values(), key=lambda s: s.code)

    # Interactive loop: categorize -> optimize -> show -> action
    while True:
        # Step 3: Categorize subjects
        must_have_codes, nice_to_have_codes = categorize_subjects(subject_list)

        # Step 4: Confirm and configure
        result = confirm_and_configure(must_have_codes, nice_to_have_codes)
        if not result["confirmed"]:
            print("Cancelled.")
            return 0

        config.must_have_subjects = must_have_codes
        config.nice_to_have_subjects = nice_to_have_codes
        config.max_electives = result["max_electives"]
        config.max_combinations = result["max_combinations"]

        # Step 5: Run combination matching
        combinations = find_best_combinations(subjects, mandatory, config)

        if not combinations:
            print("No valid combinations found.")
            continue

        print_combination_report(combinations, config)

        # Step 6: Ask what to do next
        action = select_action_after_results(combinations)

        if action == "recategorize":
            print("\n--- Starting over with re-categorization ---\n")
            continue

        if action == "export":
            indices = select_combinations_to_export(combinations)
            formats = select_export_formats()

            if "json" in formats:
                save_selected_combination_json(combinations, indices, config)
            if "ics" in formats:
                print("\nExporting selected combination ICS files...")
                export_selected_combination_ics(combinations, indices, config)
            continue

        # action == "exit"
        break

    return 0


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the CLI."""
    config = parse_args(argv)

    effective_argv = argv if argv is not None else sys.argv[1:]
    save_json = "--json" in effective_argv

    # Handle --clear-cache before anything else
    if "--clear-cache" in effective_argv:
        from .cache import SubjectCache

        cache = SubjectCache(
            cache_dir=str(Path(config.output_dir) / ".cache"),
            ttl_hours=config.cache_ttl_hours,
        )
        cache.clear()
        print("Cache cleared.")
        return 0

    if config.interactive:
        return _run_interactive(config, save_json)
    elif config.must_have_subjects or config.nice_to_have_subjects:
        return _run_combination_batch(config, save_json)
    else:
        return _run_classic(config, save_json)
