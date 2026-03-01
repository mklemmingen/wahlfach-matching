"""Command-line interface for wahlfach-matching."""

from __future__ import annotations

import argparse
import sys

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
    )


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the CLI."""
    config = parse_args(argv)

    try:
        subjects, results = run_matching(config)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    print_report(subjects, results, config)

    if config.export_ics:
        print("\nExporting ICS calendar files...")
        export_ics(results, config)

    # Check if --json was passed (we need to look at argv for this)
    effective_argv = argv if argv is not None else sys.argv[1:]
    if "--json" in effective_argv:
        save_json_report(subjects, results, config)

    return 0
