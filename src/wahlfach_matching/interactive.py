"""Interactive terminal prompts using InquirerPy."""

from __future__ import annotations

from datetime import date, time

from InquirerPy import inquirer
from InquirerPy.separator import Separator

from .models import WEEKDAY_NAMES, StaticCourse, Subject, TimeSlot

AVAILABLE_PROGRAMS = ["MKIB", "WIB", "INB", "MEB", "UIB"]
AVAILABLE_SEMESTERS = [1, 2, 3, 4, 5, 6, 7]
AVAILABLE_WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


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


def filter_out_subjects(
    subjects: list[Subject],
) -> list[str]:
    """Let the user pick subjects to exclude from all combinations.

    Returns a list of excluded subject codes.
    """
    choices = [
        {"name": f"{s.code:<15s} {s.display_name}", "value": s.code}
        for s in subjects
    ]
    result = inquirer.checkbox(
        message="Select subjects to EXCLUDE (never used in any combination):",
        choices=choices,
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

    # Get max_electives using text input with validation (avoids InquirerPy number bug)
    min_electives = max(len(must_have), 1)
    while True:
        max_electives_str = inquirer.text(
            message=f"Maximum electives per combination ({min_electives}-15):",
            default="6",
            validate=lambda x: x.isdigit() or "Please enter a valid number",
            invalid_message="Please enter a valid number",
        ).execute().strip()
        max_electives = int(max_electives_str)
        if min_electives <= max_electives <= 15:
            break
        print(f"⚠ Must be between {min_electives} and 15")

    # Get max_combinations using text input with validation
    while True:
        max_combinations_str = inquirer.text(
            message="How many top combinations to show (1-20):",
            default="5",
            validate=lambda x: x.isdigit() or "Please enter a valid number",
            invalid_message="Please enter a valid number",
        ).execute().strip()
        max_combinations = int(max_combinations_str)
        if 1 <= max_combinations <= 20:
            break
        print("⚠ Must be between 1 and 20")

    confirmed = inquirer.confirm(
        message="Proceed with these settings?",
        default=True,
    ).execute()

    return {
        "max_electives": max_electives,
        "max_combinations": max_combinations,
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


def select_cache_strategy(cache_available: bool) -> str:
    """Ask user whether to use cached data or re-fetch.

    Returns one of: "use_cache", "refetch".
    """
    if cache_available:
        choices = [
            {"name": "Use cached data (faster)", "value": "use_cache"},
            {"name": "Re-fetch from Untis (fresh data)", "value": "refetch"},
        ]
    else:
        choices = [
            {"name": "Fetch from Untis", "value": "refetch"},
        ]
        # No real choice — just inform and proceed
        print("No cached data available. Will fetch from Untis.")
        return "refetch"

    result = inquirer.select(
        message="Timetable data source:",
        choices=choices,
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


# =============================================================================
# Static Course Management
# =============================================================================


def add_static_course_interactive() -> StaticCourse:
    """Interactively prompt user to add a new static course.

    Returns the created StaticCourse object.
    """
    print("\n=== Add New Static Course ===\n")

    # Course code
    code = inquirer.text(
        message="Course code (e.g., SPAN1, IOT_MANUAL):",
        validate=lambda x: len(x.strip()) > 0 and all(c.isalnum() or c in "_-" for c in x.strip()),
        invalid_message="Code must be non-empty and contain only letters, digits, underscores, or hyphens.",
    ).execute().strip().upper()

    # Course name
    name = inquirer.text(
        message="Course name (e.g., Spanish 1 (Niveau A1.1)):",
        validate=lambda x: len(x.strip()) > 0,
        invalid_message="Name cannot be empty.",
    ).execute().strip()

    # Category
    category_choice = inquirer.select(
        message="Course category:",
        choices=[
            {"name": "Must-have (always in every combination)", "value": "must_have"},
            {"name": "Nice-to-have (preferred but optional)", "value": "nice_to_have"},
        ],
    ).execute()

    # Semester (optional)
    semester = None
    if inquirer.confirm(
        message="Add semester context?",
        default=False,
    ).execute():
        semester = inquirer.number(
            message="Semester number (1-7):",
            min_allowed=1,
            max_allowed=7,
            default=6,
        ).execute()

    # Schedule: loop to add time slots
    schedule: list[TimeSlot] = []
    while True:
        weekday = inquirer.select(
            message="Select weekday (or 'Done' to finish):",
            choices=[
                {"name": d, "value": d} for d in AVAILABLE_WEEKDAYS
            ] + [{"name": "Done adding times", "value": None}],
        ).execute()

        if weekday is None:
            if not schedule:
                print("Please add at least one time slot.")
                continue
            break

        start_str = inquirer.text(
            message=f"Start time ({weekday}, format HH:MM):",
            validate=lambda x: _validate_time_format(x),
            invalid_message="Invalid time format. Use HH:MM (e.g., 17:15).",
        ).execute().strip()
        start = time.fromisoformat(start_str)

        end_str = inquirer.text(
            message=f"End time ({weekday}, format HH:MM):",
            validate=lambda x: _validate_time_format(x),
            invalid_message="Invalid time format. Use HH:MM (e.g., 19:30).",
        ).execute().strip()
        end = time.fromisoformat(end_str)

        if start >= end:
            print("Error: End time must be after start time.")
            continue

        schedule.append(TimeSlot(weekday=weekday, start=start, end=end))
        print(f"✓ Added {weekday} {start:%H:%M}-{end:%H:%M}")

    # Scheduling mode: weekly or specific dates
    specific_dates: list[date] | None = None
    schedule_mode = inquirer.select(
        message="Scheduling mode:",
        choices=[
            {"name": "Weekly (repeats every week across the semester)", "value": "weekly"},
            {"name": "Specific dates (block / irregular course)", "value": "specific"},
        ],
    ).execute()

    if schedule_mode == "specific":
        specific_dates = _collect_specific_dates(schedule)

    # Optional notes
    notes = ""
    if inquirer.confirm(
        message="Add notes?",
        default=False,
    ).execute():
        notes = inquirer.text(
            message="Notes (optional):",
        ).execute().strip()

    # Optional exclusion group
    exclusion_group: str | None = None
    if inquirer.confirm(
        message="Add to a mutual-exclusion group? (courses in same group won't appear together)",
        default=False,
    ).execute():
        exclusion_group = inquirer.text(
            message="Exclusion group name (e.g., SPANISH1):",
            validate=lambda x: len(x.strip()) > 0,
            invalid_message="Group name cannot be empty.",
        ).execute().strip().upper()

    # Create and return the course
    course = StaticCourse(
        code=code,
        name=name,
        category=category_choice,
        schedule=schedule,
        specific_dates=specific_dates,
        semester=semester,
        notes=notes,
        exclusion_group=exclusion_group,
    )

    return course


def list_static_courses_interactive(courses: list[StaticCourse]) -> None:
    """Display all static courses in a formatted table."""
    if not courses:
        print("\nNo static courses found.")
        return

    print("\n=== Static Courses ===\n")
    for course in courses:
        category_badge = "MUST" if course.category == "must_have" else "⭐ NICE"
        sem_str = f" (Sem {course.semester})" if course.semester else ""
        if course.specific_dates is not None:
            mode_str = f" [{len(course.specific_dates)} specific dates]"
        else:
            mode_str = " [weekly]"
        group_str = f" [group: {course.exclusion_group}]" if course.exclusion_group else ""
        print(f"{category_badge:12} | {course.code:<15} | {course.name}{sem_str}{mode_str}{group_str}")
        for slot in course.schedule:
            print(f"{'':12} | {'':15} | → {slot.weekday} {slot.start:%H:%M}-{slot.end:%H:%M}")
        if course.specific_dates:
            dates_str = ", ".join(d.isoformat() for d in course.specific_dates[:5])
            if len(course.specific_dates) > 5:
                dates_str += f" (+{len(course.specific_dates) - 5} more)"
            print(f"{'':12} | {'':15} | Dates: {dates_str}")
        if course.notes:
            print(f"{'':12} | {'':15} | Note: {course.notes}")
        print()


def manage_static_courses_interactive() -> str:
    """Show management menu for static courses.

    Returns one of: "add", "list", "remove", "exit".
    """
    choices = [
        {"name": "Add new course", "value": "add"},
        {"name": "List all courses", "value": "list"},
        {"name": "Remove course", "value": "remove"},
        {"name": "Exit management", "value": "exit"},
    ]
    result = inquirer.select(
        message="Manage static courses:",
        choices=choices,
    ).execute()
    return result


def select_course_to_remove(courses: list[StaticCourse]) -> str | None:
    """Let user pick a course to remove.

    Returns course code, or None if cancelled.
    """
    if not courses:
        print("No static courses to remove.")
        return None

    choices = [
        {
            "name": f"{c.code:<15} | {c.name}",
            "value": c.code,
        }
        for c in courses
    ]

    result = inquirer.select(
        message="Select course to remove:",
        choices=choices + [{"name": "Cancel", "value": None}],
    ).execute()

    if result is None:
        print("Cancelled.")
        return None

    confirmed = inquirer.confirm(
        message=f"Remove '{result}'?",
        default=False,
    ).execute()

    return result if confirmed else None


def _collect_specific_dates(schedule: list[TimeSlot]) -> list[date]:
    """Interactively collect specific dates for a block/irregular course.

    Validates that each date's weekday matches at least one TimeSlot in the schedule.
    """
    valid_weekdays = {slot.weekday for slot in schedule}
    weekday_list = ", ".join(sorted(valid_weekdays))
    print(f"\nEnter specific dates (weekday must match: {weekday_list}).")
    print("Enter dates in YYYY-MM-DD format. Type 'done' to finish.\n")

    dates: list[date] = []
    while True:
        raw = inquirer.text(
            message=f"Date #{len(dates) + 1} (YYYY-MM-DD or 'done'):",
            validate=lambda x: x.strip().lower() == "done" or _validate_date_format(x),
            invalid_message="Invalid format. Use YYYY-MM-DD or 'done'.",
        ).execute().strip()

        if raw.lower() == "done":
            if not dates:
                print("Please enter at least one date.")
                continue
            break

        d = date.fromisoformat(raw)
        weekday_name = WEEKDAY_NAMES[d.weekday()]
        if weekday_name not in valid_weekdays:
            print(f"  {raw} is a {weekday_name} — no time slots for that day. Skipped.")
            continue

        dates.append(d)
        matching_slots = [s for s in schedule if s.weekday == weekday_name]
        slot_strs = ", ".join(f"{s.start:%H:%M}-{s.end:%H:%M}" for s in matching_slots)
        print(f"  Added {raw} ({weekday_name}) — {slot_strs}")

    dates.sort()
    return dates


def _validate_time_format(time_str: str) -> bool:
    """Validate that string is in HH:MM format."""
    try:
        parts = time_str.strip().split(":")
        if len(parts) != 2:
            return False
        h, m = int(parts[0]), int(parts[1])
        return 0 <= h < 24 and 0 <= m < 60
    except (ValueError, AttributeError):
        return False


def _validate_date_format(date_str: str) -> bool:
    """Validate that string is in YYYY-MM-DD format."""
    try:
        date.fromisoformat(date_str.strip())
        return True
    except (ValueError, AttributeError):
        return False

