"""Interactive terminal prompts using InquirerPy."""

from __future__ import annotations

from InquirerPy import inquirer
from InquirerPy.separator import Separator

from .models import Subject

AVAILABLE_PROGRAMS = ["MKIB", "WIB", "INB", "MEB", "UIB"]
AVAILABLE_SEMESTERS = [1, 2, 3, 4, 5, 6, 7]


def select_programs() -> list[str]:
    """Let the user pick study programs via checkbox."""
    choices = [{"name": p, "value": p, "enabled": p == "MKIB"} for p in AVAILABLE_PROGRAMS]
    result = inquirer.checkbox(
        message="Select study programs to fetch:",
        choices=choices,
        validate=lambda r: len(r) > 0,
        invalid_message="Select at least one program.",
    ).execute()
    return result


def select_semesters() -> list[int]:
    """Let the user pick semester numbers via checkbox."""
    choices = [{"name": str(s), "value": s, "enabled": s in (4, 6, 7)} for s in AVAILABLE_SEMESTERS]
    result = inquirer.checkbox(
        message="Select semesters to include:",
        choices=choices,
        validate=lambda r: len(r) > 0,
        invalid_message="Select at least one semester.",
    ).execute()
    return result


def categorize_subjects(
    subjects: list[Subject],
) -> tuple[list[str], list[str]]:
    """Two-step categorization: first must-haves, then nice-to-haves.

    Returns (must_have_codes, nice_to_have_codes).
    """
    choices = [
        {"name": f"{s.code:<15s} {s.display_name}", "value": s.code}
        for s in subjects
    ]

    # Step 1: Pick must-haves
    must_have = inquirer.checkbox(
        message="Select MUST-HAVE subjects (always in every combination):",
        choices=choices,
    ).execute()

    # Step 2: Pick nice-to-haves from remaining
    remaining = [c for c in choices if c["value"] not in must_have]
    if remaining:
        nice_to_have = inquirer.checkbox(
            message="Select NICE-TO-HAVE subjects (preferred but optional):",
            choices=remaining,
        ).execute()
    else:
        nice_to_have = []

    return must_have, nice_to_have


def confirm_and_configure(
    must_have: list[str],
    nice_to_have: list[str],
) -> dict:
    """Show summary and let user confirm/adjust settings.

    Returns dict with keys: max_electives, max_combinations, confirmed.
    """
    print("\n--- Summary ---")
    print(f"Must-have:    {', '.join(must_have) if must_have else '(none)'}")
    print(f"Nice-to-have: {', '.join(nice_to_have) if nice_to_have else '(none)'}")
    print()

    max_electives = inquirer.number(
        message="Maximum electives per combination:",
        default=6,
        min_allowed=max(len(must_have), 1),
        max_allowed=15,
    ).execute()

    max_combinations = inquirer.number(
        message="How many top combinations to show:",
        default=5,
        min_allowed=1,
        max_allowed=20,
    ).execute()

    confirmed = inquirer.confirm(
        message="Proceed with these settings?",
        default=True,
    ).execute()

    return {
        "max_electives": int(max_electives),
        "max_combinations": int(max_combinations),
        "confirmed": confirmed,
    }


def select_action_after_results(
    combinations: list,
) -> str:
    """Ask what to do after showing results.

    Returns one of: "recategorize", "export", "exit".
    """
    choices = [
        {"name": "Re-categorize subjects", "value": "recategorize"},
        {"name": "Export selected combinations", "value": "export"},
        {"name": "Exit", "value": "exit"},
    ]
    result = inquirer.select(
        message="What would you like to do?",
        choices=choices,
    ).execute()
    return result


def select_combinations_to_export(
    combinations: list,
) -> list[int]:
    """Let user pick which combinations to export (1-based indices)."""
    choices = [
        {
            "name": f"Combination #{i} (score: {combo.score:.1f})",
            "value": i,
        }
        for i, combo in enumerate(combinations, 1)
    ]
    result = inquirer.checkbox(
        message="Select combinations to export:",
        choices=choices,
        validate=lambda r: len(r) > 0,
        invalid_message="Select at least one combination.",
    ).execute()
    return result


def select_export_formats() -> list[str]:
    """Let user pick export formats."""
    choices = [
        {"name": "JSON report", "value": "json", "enabled": True},
        {"name": "ICS calendar files", "value": "ics", "enabled": True},
    ]
    result = inquirer.checkbox(
        message="Select export formats:",
        choices=choices,
        validate=lambda r: len(r) > 0,
        invalid_message="Select at least one format.",
    ).execute()
    return result
