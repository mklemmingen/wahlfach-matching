"""Command-line interface for wahlfach-matching."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rich.console import Console

from .config import MatchConfig
from .ics_exporter import export_ics
from .matcher import run_matching
from .reporter import print_report, save_json_report

console = Console()


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
    parser.add_argument(
        "--exclude",
        nargs="*",
        default=[],
        help="Subject codes to exclude from all combinations",
    )
    parser.add_argument(
        "--exclusion-group",
        action="append",
        default=[],
        metavar="NAME:CODE1,CODE2,...",
        help="Define a mutual-exclusion group (repeatable). Courses in the same group won't appear together.",
    )

    # Scoring flags
    parser.add_argument(
        "--weight",
        action="append",
        default=[],
        metavar="CODE:MULTIPLIER",
        help="Boost a subject's score by multiplier (repeatable, e.g. --weight MATH:2.0)",
    )
    parser.add_argument(
        "--spread-across-week",
        action="store_true",
        default=False,
        help="Reward schedules that spread classes across more weekdays",
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

    # Static course management
    parser.add_argument(
        "--add-course",
        action="store_true",
        help="Interactively add a new static course",
    )
    parser.add_argument(
        "--list-courses",
        action="store_true",
        help="List all static courses",
    )
    parser.add_argument(
        "--remove-course",
        metavar="CODE",
        help="Remove a static course by code",
    )
    parser.add_argument(
        "--manage-courses",
        action="store_true",
        help="Interactive menu to manage static courses",
    )

    args = parser.parse_args(argv)

    # Parse --exclusion-group NAME:CODE1,CODE2,... into dict
    exclusion_groups: dict[str, list[str]] = {}
    for raw in (args.exclusion_group or []):
        if ":" not in raw:
            parser.error(f"Invalid --exclusion-group format: '{raw}'. Expected NAME:CODE1,CODE2,...")
        name, codes_str = raw.split(":", 1)
        codes = [c.strip() for c in codes_str.split(",") if c.strip()]
        if not name or not codes:
            parser.error(f"Invalid --exclusion-group: '{raw}'. Need a name and at least one code.")
        if name in exclusion_groups:
            exclusion_groups[name].extend(codes)
        else:
            exclusion_groups[name] = codes

    # Parse --weight CODE:MULTIPLIER into dict
    subject_weights: dict[str, float] = {}
    for raw in (args.weight or []):
        if ":" not in raw:
            parser.error(f"Invalid --weight format: '{raw}'. Expected CODE:MULTIPLIER (e.g. MATH:2.0)")
        code, mult_str = raw.split(":", 1)
        code = code.strip()
        if not code:
            parser.error(f"Invalid --weight: '{raw}'. Code must not be empty.")
        try:
            mult = float(mult_str)
        except ValueError:
            parser.error(f"Invalid --weight multiplier: '{mult_str}' is not a number.")
        if mult <= 0:
            parser.error(f"Invalid --weight multiplier: {mult} must be positive.")
        subject_weights[code] = mult

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
        excluded_subjects=args.exclude or [],
        exclusion_groups=exclusion_groups,
        subject_weights=subject_weights,
        spread_across_week=args.spread_across_week,
        use_cache=not args.no_cache,
        cache_ttl_hours=args.cache_ttl,
        remove_course=args.remove_course,
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


def _fetch_with_cache(config: MatchConfig, force_refetch: bool = False) -> dict[str, "Subject"]:
    """Fetch timetable data, using the cache when enabled.

    Parameters
    ----------
    force_refetch : bool
        If True, skip cache and re-fetch. Falls back to cache on failure.
    """
    from .aggregator import aggregate_subjects
    from .cache import SubjectCache
    from .fetcher import fetch_timetables

    cache = SubjectCache(
        cache_dir=str(Path(config.output_dir) / ".cache"),
        ttl_hours=config.cache_ttl_hours,
    )

    # Try cache first (unless force_refetch or cache disabled)
    if config.use_cache and not force_refetch:
        cached = cache.load(config)
        if cached is not None:
            console.print("[green]Loaded timetable data from cache.[/green]")
            return cached

    # Fetch fresh data
    with console.status("[bold cyan]Fetching timetable data from WebUntis...", spinner="dots"):
        try:
            timetables = fetch_timetables(config)
            if not timetables:
                raise RuntimeError("No timetable data fetched.")

            subjects = aggregate_subjects(timetables)

            # Save to cache for next time
            if config.use_cache:
                cache.save(config, subjects)
                console.print("[green]Timetable data cached.[/green]")

            return subjects

        except Exception as e:
            # Fallback to cache if fetch fails
            if config.use_cache:
                cached = cache.load(config)
                if cached is not None:
                    console.print(f"[yellow]Fetch failed ({e}). Falling back to cached data.[/yellow]")
                    return cached
            raise RuntimeError(f"Fetch failed and no cache available: {e}") from e


def _run_combination_batch(config: MatchConfig, save_json: bool) -> int:
    """Run combination matching in batch mode (--must-have / --nice-to-have)."""
    from .combination_reporter import print_combination_report, save_combination_json, save_combination_md
    from .ics_exporter import export_combination_ics

    try:
        subjects = _fetch_with_cache(config)
    except RuntimeError as e:
        console.print(f"[red]Error: {e}[/red]", file=sys.stderr)
        return 1

    console.print(f"\nFound [bold]{len(subjects)}[/bold] unique subjects.\n")

    # Identify mandatory subjects and run optimizer
    from .optimizer import find_best_combinations

    # Filter excluded subjects
    available = {k: v for k, v in subjects.items() if k not in config.excluded_subjects}
    mandatory = {code: available[code] for code in config.mandatory_subjects if code in available}
    combinations = find_best_combinations(available, mandatory, config, console=console)

    print_combination_report(combinations, config, console=console)

    # Always save MD results with UUID
    save_combination_md(combinations, config)

    if config.export_ics:
        console.print("\n[cyan]Exporting combination ICS files...[/cyan]")
        export_combination_ics(combinations, config)

    if save_json:
        save_combination_json(combinations, config)

    return 0


def _run_interactive(config: MatchConfig, save_json: bool) -> int:
    """Run interactive mode with terminal prompts and retry loop."""
    try:
        from .interactive import (
            add_static_course_interactive,
            categorize_subjects,
            confirm_and_configure,
            filter_out_subjects,
            list_static_courses_interactive,
            manage_static_courses_interactive,
            select_action_after_results,
            select_cache_strategy,
            select_combinations_to_export,
            select_course_to_remove,
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
        save_combination_md,
        save_selected_combination_json,
    )
    from .ics_exporter import export_combination_ics, export_selected_combination_ics
    from .optimizer import find_best_combinations
    from .cache import StaticCourseCache

    # Initialize static course cache
    static_course_cache = StaticCourseCache(
        cache_dir=str(Path(config.output_dir) / ".cache")
    )

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

    # Step 1b: Offer static course management
    existing_courses = static_course_cache.list_all()
    if existing_courses:
        from InquirerPy import inquirer
        manage = inquirer.confirm(
            message=f"You have {len(existing_courses)} static course(s). Manage them?",
            default=False,
        ).execute()
        if manage:
            try:
                while True:
                    action = manage_static_courses_interactive()
                    if action == "add":
                        course = add_static_course_interactive()
                        static_course_cache.save(course)
                        print(f"\n✓ Static course '{course.code}' saved.")
                    elif action == "list":
                        courses = static_course_cache.list_all()
                        list_static_courses_interactive(courses)
                    elif action == "remove":
                        courses = static_course_cache.list_all()
                        code = select_course_to_remove(courses)
                        if code:
                            static_course_cache.delete(code)
                            print(f"✓ Removed course '{code}'.")
                    elif action == "exit":
                        break
            except KeyboardInterrupt:
                print("\nCancelled.")
                return 0
    else:
        from InquirerPy import inquirer
        add_new = inquirer.confirm(
            message="Add a static course (e.g., external language course)?",
            default=False,
        ).execute()
        if add_new:
            try:
                course = add_static_course_interactive()
                static_course_cache.save(course)
                print(f"\n✓ Static course '{course.code}' saved.")
            except KeyboardInterrupt:
                print("\nCancelled.")
                return 0

    # Step 2: Ask about cache and fetch data
    from .cache import SubjectCache

    subject_cache = SubjectCache(
        cache_dir=str(Path(config.output_dir) / ".cache"),
        ttl_hours=config.cache_ttl_hours,
    )
    cache_available = subject_cache.load(config) is not None
    cache_strategy = select_cache_strategy(cache_available)
    force_refetch = cache_strategy == "refetch"

    try:
        subjects = _fetch_with_cache(config, force_refetch=force_refetch)
    except RuntimeError as e:
        console.print(f"[red]Error: {e}[/red]", file=sys.stderr)
        return 1

    console.print(f"\nFound [bold]{len(subjects)}[/bold] unique subjects.\n")

    mandatory = {code: subjects[code] for code in config.mandatory_subjects if code in subjects}
    subject_list = sorted(subjects.values(), key=lambda s: s.code)

    # Interactive loop: filter -> categorize -> optimize -> show -> action
    while True:
        # Step 3a: Filter out unwanted subjects
        excluded_codes = filter_out_subjects(subject_list)
        config.excluded_subjects = excluded_codes
        if excluded_codes:
            print(f"Excluded {len(excluded_codes)} subject(s).")

        # Step 3b: Categorize remaining subjects
        available = [s for s in subject_list if s.code not in excluded_codes]
        must_have_codes, nice_to_have_codes = categorize_subjects(available)

        # Step 4: Confirm and configure
        result = confirm_and_configure(must_have_codes, nice_to_have_codes)
        if not result["confirmed"]:
            print("Cancelled.")
            return 0

        config.must_have_subjects = must_have_codes
        config.nice_to_have_subjects = nice_to_have_codes
        config.max_electives = result["max_electives"]
        config.max_combinations = result["max_combinations"]

        # Step 5: Run combination matching (excluding filtered subjects)
        available_subjects = {
            code: subj for code, subj in subjects.items()
            if code not in config.excluded_subjects
        }
        combinations = find_best_combinations(available_subjects, mandatory, config, console=console)

        if not combinations:
            console.print("[yellow]No valid combinations found.[/yellow]")
            continue

        print_combination_report(combinations, config, console=console)

        # Always save results as MD with UUID
        save_combination_md(combinations, config)

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

    # Handle static course management
    from .cache import StaticCourseCache
    from .interactive import (
        add_static_course_interactive,
        list_static_courses_interactive,
        manage_static_courses_interactive,
        select_course_to_remove,
    )

    course_cache = StaticCourseCache(
        cache_dir=str(Path(config.output_dir) / ".cache")
    )

    if "--add-course" in effective_argv:
        try:
            course = add_static_course_interactive()
            course_cache.save(course)
            print(f"\n✓ Static course '{course.code}' saved.")
        except KeyboardInterrupt:
            print("\nCancelled.")
            return 0
        return 0

    if "--list-courses" in effective_argv:
        courses = course_cache.list_all()
        list_static_courses_interactive(courses)
        return 0

    if "--remove-course" in effective_argv:
        code = config.remove_course
        if course_cache.delete(code):
            print(f"✓ Removed course '{code}'.")
        else:
            print(f"Course '{code}' not found.")
        return 0

    if "--manage-courses" in effective_argv:
        try:
            while True:
                action = manage_static_courses_interactive()
                if action == "add":
                    course = add_static_course_interactive()
                    course_cache.save(course)
                    print(f"\n✓ Static course '{course.code}' saved.")
                elif action == "list":
                    courses = course_cache.list_all()
                    list_static_courses_interactive(courses)
                elif action == "remove":
                    courses = course_cache.list_all()
                    code = select_course_to_remove(courses)
                    if code:
                        course_cache.delete(code)
                        print(f"✓ Removed course '{code}'.")
                elif action == "exit":
                    break
        except KeyboardInterrupt:
            print("\nCancelled.")
            return 0
        return 0

    if config.interactive:
        return _run_interactive(config, save_json)
    elif config.must_have_subjects or config.nice_to_have_subjects:
        return _run_combination_batch(config, save_json)
    else:
        return _run_classic(config, save_json)
