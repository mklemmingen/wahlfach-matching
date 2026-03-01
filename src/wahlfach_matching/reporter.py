"""Text and JSON report generation."""

from __future__ import annotations

import json
import os
from pathlib import Path

from .config import MatchConfig
from .models import MatchResult, Subject


def print_report(
    subjects: dict[str, Subject],
    results: list[MatchResult],
    config: MatchConfig,
) -> None:
    """Print a human-readable ranking report to stdout."""
    print("=" * 80)
    print("ELECTIVE MATCHING RESULTS")
    print("=" * 80)
    print(f"Total subjects found: {len(subjects)}")
    print(f"Candidates scored: {len(results)}")
    if config.mandatory_subjects:
        print(f"Mandatory (blocked): {', '.join(config.mandatory_subjects)}")
    print()

    top = results[: config.top_n]
    for i, r in enumerate(top, 1):
        subj = r.subject
        print(f"{i:3d}. {subj.code:<20s} Score: {r.score:.1f}")
        if subj.display_name != subj.code:
            print(f"     Name:        {subj.display_name}")
        print(f"     Groups:      {', '.join(sorted(subj.groups))}")
        print(f"     Teachers:    {', '.join(sorted(subj.teachers))}")
        print(f"     Weekdays:    {', '.join(sorted(subj.weekdays))}")
        print(f"     Time slots:  {', '.join(sorted(subj.time_slots))}")
        print(f"     Occurrences: {subj.total_occurrences}")
        if r.conflict_count > 0:
            print(f"     Conflicts:   {r.conflict_count} ({', '.join(r.conflict_slots)})")
        else:
            print(f"     Conflicts:   None")
        print(f"     Notes:       {'; '.join(r.notes)}")
        print()


def save_json_report(
    subjects: dict[str, Subject],
    results: list[MatchResult],
    config: MatchConfig,
) -> Path:
    """Save a JSON report to the output directory. Returns the file path."""
    out_dir = Path(config.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "matching_results.json"

    data = {
        "config": {
            "programs": config.programs,
            "semesters": config.semesters,
            "mandatory_subjects": config.mandatory_subjects,
        },
        "total_subjects": len(subjects),
        "results": [
            {
                "rank": i,
                "code": r.subject.code,
                "display_name": r.subject.display_name,
                "score": r.score,
                "conflict_count": r.conflict_count,
                "conflict_slots": r.conflict_slots,
                "groups": sorted(r.subject.groups),
                "teachers": sorted(r.subject.teachers),
                "weekdays": sorted(r.subject.weekdays),
                "time_slots": sorted(r.subject.time_slots),
                "occurrences": r.subject.total_occurrences,
                "notes": r.notes,
            }
            for i, r in enumerate(results[: config.top_n], 1)
        ],
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"JSON report saved to {path}")
    return path
