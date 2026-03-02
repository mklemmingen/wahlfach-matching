"""Combinatorial schedule optimizer — find best subject combinations."""

from __future__ import annotations

import heapq
import math
from collections import defaultdict
from datetime import date, time
from itertools import combinations
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, MofNCompleteColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich.text import Text

from .config import MatchConfig
from .models import CombinationMetrics, Lesson, ScheduleCombination, StaticCourse, Subject

ALL_WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")


def _static_course_to_subject(course: StaticCourse, start_date: date | None = None, end_date: date | None = None) -> Subject:
    """Convert a StaticCourse to a Subject for pattern matching.

    Parameters
    ----------
    course : StaticCourse
        The static course to convert
    start_date : date, optional
        Start date of the semester (for generating lessons across full duration)
    end_date : date, optional
        End date of the semester (for generating lessons across full duration)
    """
    lessons = course.to_lessons(start_date=start_date, end_date=end_date)
    weekdays = {lesson.weekday for lesson in lessons}
    time_slots = {f"{lesson.start:%H:%M}-{lesson.end:%H:%M}" for lesson in lessons}

    return Subject(
        code=course.code,
        long_name=course.name,
        alternate_name=course.display_name,
        groups=set(),
        teachers=set(),
        rooms=set(),
        total_occurrences=len(lessons),
        weekdays=weekdays,
        time_slots=time_slots,
        dates={lesson.date.isoformat() for lesson in lessons},
        lessons=lessons,
        exclusion_group=course.exclusion_group,
    )


def _load_static_courses(config: MatchConfig, subjects: dict[str, Subject]) -> tuple[dict[str, Subject], dict[str, str]]:
    """Load static courses from cache and convert to Subject objects.

    Uses date range from fetched subjects to span static courses across entire semester.

    Returns
    -------
    tuple
        (converted_subjects_dict, category_mapping_dict)
        where category_mapping maps course_code -> "must_have" or "nice_to_have"
    """
    from .cache import StaticCourseCache

    cache = StaticCourseCache(cache_dir=str(Path(config.output_dir) / ".cache"))
    static_courses = cache.load_all()

    if not static_courses or not subjects:
        return {}, {}

    # Find date range from fetched subjects
    all_dates = set()
    for subj in subjects.values():
        for lesson in subj.lessons:
            all_dates.add(lesson.date)

    if not all_dates:
        start_date = None
        end_date = None
    else:
        start_date = min(all_dates)
        end_date = max(all_dates)

    converted = {}
    category_map = {}
    for code, course in static_courses.items():
        converted[code] = _static_course_to_subject(course, start_date=start_date, end_date=end_date)
        category_map[code] = course.category  # "must_have" or "nice_to_have"

    return converted, category_map


def _lessons_conflict(a: Lesson, b: Lesson) -> bool:
    """Check if two specific lessons overlap (same date + time overlap)."""
    if a.date != b.date:
        return False
    return a.start < b.end and b.start < a.end


def _subjects_conflict(a: Subject, b: Subject) -> list[str]:
    """Return conflict descriptions between two subjects.

    Uses date-indexed lookup for O(n+m) instead of O(n*m).
    """
    # Quick-reject: if both subjects have date info and share no dates, they can't conflict
    if a.dates and b.dates and a.dates.isdisjoint(b.dates):
        return []

    # Build date-indexed lookup for the smaller subject
    if len(a.lessons) <= len(b.lessons):
        indexed, other, indexed_is_a = a, b, True
    else:
        indexed, other, indexed_is_a = b, a, False

    by_date: dict[date, list[Lesson]] = {}
    for le in indexed.lessons:
        by_date.setdefault(le.date, []).append(le)

    conflicts: list[str] = []
    for lo in other.lessons:
        for li in by_date.get(lo.date, []):
            if li.start < lo.end and lo.start < li.end:
                la, lb = (li, lo) if indexed_is_a else (lo, li)
                desc = (
                    f"{a.code} vs {b.code} on {la.date.isoformat()} "
                    f"{la.start:%H:%M}-{la.end:%H:%M}"
                )
                conflicts.append(desc)
    return conflicts


def _time_to_minutes(t: time) -> int:
    """Convert a time to minutes since midnight."""
    return t.hour * 60 + t.minute


def _minutes_to_timestr(minutes: int) -> str:
    """Convert minutes since midnight to HH:MM string."""
    h, m = divmod(int(minutes), 60)
    return f"{h:02d}:{m:02d}"


def _compute_metrics(subjects: list[Subject]) -> CombinationMetrics:
    """Compute all quality-of-life metrics for a set of subjects."""
    all_lessons: list[Lesson] = []
    for subj in subjects:
        all_lessons.extend(subj.lessons)

    if not all_lessons:
        return CombinationMetrics()

    # Group lessons by (date, weekday)
    by_day: dict[tuple[str, str], list[Lesson]] = defaultdict(list)
    for le in all_lessons:
        by_day[(le.date.isoformat(), le.weekday)].append(le)

    # Closeness: avg gap between consecutive lessons on the same day
    total_gap = 0.0
    gap_count = 0
    for day_lessons in by_day.values():
        sorted_lessons = sorted(day_lessons, key=lambda l: l.start)
        for i in range(1, len(sorted_lessons)):
            gap = _time_to_minutes(sorted_lessons[i].start) - _time_to_minutes(sorted_lessons[i - 1].end)
            if gap > 0:
                total_gap += gap
                gap_count += 1
    closeness = total_gap / gap_count if gap_count > 0 else 0.0

    # Earliest start
    earliest = min(_time_to_minutes(le.start) for le in all_lessons)

    # Latest end
    latest = max(_time_to_minutes(le.end) for le in all_lessons)

    # Average start: for each day, find first lesson start, average those
    day_starts: list[int] = []
    day_ends: list[int] = []
    for day_lessons in by_day.values():
        day_starts.append(min(_time_to_minutes(le.start) for le in day_lessons))
        day_ends.append(max(_time_to_minutes(le.end) for le in day_lessons))
    avg_start = sum(day_starts) / len(day_starts) if day_starts else 0
    avg_end = sum(day_ends) / len(day_ends) if day_ends else 0

    # Free days per week: weekdays not present in any lesson
    occupied_weekdays = {le.weekday for le in all_lessons}
    free_days = sum(1 for wd in ALL_WEEKDAYS if wd not in occupied_weekdays)

    return CombinationMetrics(
        closeness=round(closeness, 1),
        earliest_start=_minutes_to_timestr(earliest),
        avg_start=_minutes_to_timestr(int(avg_start)),
        latest_end=_minutes_to_timestr(latest),
        avg_end=_minutes_to_timestr(int(avg_end)),
        free_days_per_week=free_days,
    )


def _build_mandatory_slots(
    mandatory_subjects: dict[str, Subject],
) -> dict[str, list[tuple[str, str]]]:
    """Build a weekday → [(start, end)] map from mandatory subjects."""
    slots: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for subj in mandatory_subjects.values():
        for le in subj.lessons:
            slots[le.weekday].append((f"{le.start:%H:%M}", f"{le.end:%H:%M}"))
    return dict(slots)


def _count_mandatory_conflicts(
    subject: Subject,
    mandatory_slots: dict[str, list[tuple[str, str]]],
) -> int:
    """Count how many lessons of a subject conflict with mandatory slots."""
    count = 0
    for le in subject.lessons:
        le_start = f"{le.start:%H:%M}"
        le_end = f"{le.end:%H:%M}"
        for m_start, m_end in mandatory_slots.get(le.weekday, []):
            if le_start < m_end and m_start < le_end:
                count += 1
                break
    return count


def _precompute_conflict_matrix(
    subjects: list[Subject],
) -> dict[tuple[str, str], list[str]]:
    """Pre-compute pairwise conflict descriptions for all subject pairs.

    Returns a dict mapping ``(code_a, code_b)`` (sorted) to conflict descriptions.
    """
    matrix: dict[tuple[str, str], list[str]] = {}
    for i, a in enumerate(subjects):
        for b in subjects[i + 1:]:
            key = (a.code, b.code) if a.code < b.code else (b.code, a.code)
            matrix[key] = _subjects_conflict(a, b)
    return matrix


def _precompute_mandatory_conflicts(
    subjects: list[Subject],
    mandatory_slots: dict[str, list[tuple[str, str]]],
) -> dict[str, int]:
    """Pre-compute mandatory conflict count for each subject."""
    return {subj.code: _count_mandatory_conflicts(subj, mandatory_slots) for subj in subjects}


def _score_combination(
    must_have: list[Subject],
    nice_to_have: list[Subject],
    fillers: list[Subject],
    mandatory_slots: dict[str, list[tuple[str, str]]],
    config: MatchConfig,
    conflict_matrix: dict[tuple[str, str], list[str]] | None = None,
    mandatory_conflict_cache: dict[str, int] | None = None,
) -> ScheduleCombination:
    """Score a candidate combination and return a ScheduleCombination."""
    all_subjects = must_have + nice_to_have + fillers

    # Internal conflicts between all pairs
    internal_conflicts: list[tuple[str, str, str]] = []
    for i, a in enumerate(all_subjects):
        for b in all_subjects[i + 1:]:
            key = (a.code, b.code) if a.code < b.code else (b.code, a.code)
            if conflict_matrix is not None:
                descs = conflict_matrix.get(key, [])
            else:
                descs = _subjects_conflict(a, b)
            for desc in descs:
                internal_conflicts.append((a.code, b.code, desc))

    # Mandatory slot conflicts
    mandatory_conflict_count = 0
    for subj in all_subjects:
        if mandatory_conflict_cache is not None:
            mandatory_conflict_count += mandatory_conflict_cache.get(subj.code, 0)
        else:
            mandatory_conflict_count += _count_mandatory_conflicts(subj, mandatory_slots)

    # Scoring
    score = 0.0
    notes: list[str] = []

    # Nice-to-have bonus
    score += len(nice_to_have) * 10.0
    if nice_to_have:
        notes.append(f"{len(nice_to_have)} nice-to-have(s) included")

    # Filler bonus (smaller)
    score += len(fillers) * 3.0
    if fillers:
        notes.append(f"{len(fillers)} filler(s) included")

    # Penalty for internal conflicts
    score -= len(internal_conflicts) * 5.0
    if internal_conflicts:
        notes.append(f"{len(internal_conflicts)} internal conflict(s)")

    # Penalty for mandatory conflicts
    score -= mandatory_conflict_count * 8.0
    if mandatory_conflict_count:
        notes.append(f"{mandatory_conflict_count} mandatory conflict(s)")

    # Metrics bonus: reward compactness and free days
    metrics = _compute_metrics(all_subjects)
    score += metrics.free_days_per_week * 2.0
    if metrics.closeness > 0:
        # Reward compact schedules (lower gap = higher score)
        score += max(0, 5.0 - metrics.closeness / 30.0)

    return ScheduleCombination(
        subjects=all_subjects,
        must_have_subjects=must_have,
        nice_to_have_subjects=nice_to_have,
        filler_subjects=fillers,
        score=round(score, 1),
        internal_conflicts=internal_conflicts,
        nice_to_have_count=len(nice_to_have),
        filler_count=len(fillers),
        metrics=metrics,
        notes=notes,
    )


def _build_exclusion_index(
    subjects: dict[str, Subject],
    config: MatchConfig,
) -> dict[str, str]:
    """Build a code → group reverse index from Subject.exclusion_group fields and config.exclusion_groups.

    Returns a dict mapping subject code to its exclusion group name.
    """
    code_to_group: dict[str, str] = {}

    # From Subject.exclusion_group fields
    for subj in subjects.values():
        if subj.exclusion_group:
            code_to_group[subj.code] = subj.exclusion_group

    # From config.exclusion_groups (CLI-defined)
    for group_name, codes in config.exclusion_groups.items():
        for code in codes:
            code_to_group[code] = group_name

    return code_to_group


def _violates_exclusion_groups(
    subset: tuple[Subject, ...],
    code_to_group: dict[str, str],
) -> bool:
    """Return True if 2+ subjects in the subset share an exclusion group."""
    seen: set[str] = set()
    for s in subset:
        grp = code_to_group.get(s.code)
        if grp:
            if grp in seen:
                return True
            seen.add(grp)
    return False


def find_best_combinations(
    subjects: dict[str, Subject],
    mandatory_subjects: dict[str, Subject],
    config: MatchConfig,
    console: Console | None = None,
) -> list[ScheduleCombination]:
    """Find the best schedule combinations.

    Parameters
    ----------
    subjects:
        All available subjects (keyed by code).
    mandatory_subjects:
        Already-enrolled subjects whose time slots are blocked.
    config:
        User preferences including must_have_subjects, nice_to_have_subjects,
        max_electives, and max_combinations.
    console:
        Rich Console for progress output. If None, progress is suppressed.
    """
    quiet = console is None
    if quiet:
        console = Console(quiet=True)

    # ── Phase 1: Load static courses ──────────────────────────────────────
    with console.status("[bold cyan]Loading static courses...", spinner="dots") as status:
        static_subjects, static_categories = _load_static_courses(config, subjects)
        all_subjects = {**subjects, **static_subjects}

    if static_subjects:
        # Show static course summary
        static_table = Table(
            title="[bold]Static Courses Loaded",
            show_header=True,
            header_style="bold",
            border_style="cyan",
            padding=(0, 1),
        )
        static_table.add_column("Code", style="bold yellow")
        static_table.add_column("Category")
        static_table.add_column("Mode")
        static_table.add_column("Lessons", justify="right")

        for code, subj in static_subjects.items():
            cat = static_categories.get(code, "?")
            if cat == "must_have":
                cat_style = "[green]must-have"
            elif cat == "nice_to_have":
                cat_style = "[blue]nice-to-have"
            else:
                cat_style = "[dim]filler"
            # Determine mode from the original static course
            from .cache import StaticCourseCache
            sc_cache = StaticCourseCache(cache_dir=str(Path(config.output_dir) / ".cache"))
            raw_course = sc_cache.load_by_code(code)
            if raw_course and raw_course.specific_dates is not None:
                mode = f"[magenta]{len(raw_course.specific_dates)} dates"
            else:
                mode = "[dim]weekly"
            static_table.add_row(code, cat_style, mode, str(subj.total_occurrences))

        console.print(static_table)
        console.print()

    # ── Phase 1b: Build exclusion index ────────────────────────────────────
    code_to_group = _build_exclusion_index(all_subjects, config)

    if code_to_group:
        # Collect unique groups for display
        groups_seen: dict[str, list[str]] = {}
        for code, grp in code_to_group.items():
            groups_seen.setdefault(grp, []).append(code)

        excl_info = Text()
        excl_info.append("  Exclusion groups: ", style="dim")
        parts = [f"{name} ({len(codes)} courses)" for name, codes in groups_seen.items()]
        excl_info.append(", ".join(parts), style="bold magenta")
        console.print(excl_info)

    # ── Phase 2: Resolve categories ───────────────────────────────────────
    must_have_with_static = list(config.must_have_subjects)
    nice_to_have_with_static = list(config.nice_to_have_subjects)

    for code, category in static_categories.items():
        if category == "must_have" and code not in must_have_with_static:
            must_have_with_static.append(code)
        elif category == "nice_to_have" and code not in nice_to_have_with_static:
            nice_to_have_with_static.append(code)

    mandatory_slots = _build_mandatory_slots(mandatory_subjects)

    must_have: list[Subject] = []
    for code in must_have_with_static:
        if code in all_subjects and code not in mandatory_subjects:
            must_have.append(all_subjects[code])

    nice_to_have: list[Subject] = []
    for code in nice_to_have_with_static:
        if code in all_subjects and code not in mandatory_subjects and code not in must_have_with_static:
            nice_to_have.append(all_subjects[code])

    must_have_codes = {s.code for s in must_have}
    nice_to_have_codes = {s.code for s in nice_to_have}

    # ── Phase 2b: Validate exclusion groups ──────────────────────────────
    if code_to_group:
        # Check: 2+ must-haves in the same group → impossible
        must_have_groups: dict[str, list[str]] = {}
        for s in must_have:
            grp = code_to_group.get(s.code)
            if grp:
                must_have_groups.setdefault(grp, []).append(s.code)
        for grp, codes in must_have_groups.items():
            if len(codes) > 1:
                console.print(
                    f"[bold red]Error: Must-have subjects {codes} are in the same "
                    f"exclusion group '{grp}'. No valid combinations possible.[/bold red]"
                )
                return []

        # Prune: if a must-have is in a group, remove siblings from nice-to-have and filler pools
        must_have_group_names = set(must_have_groups.keys())
        nice_to_have = [
            s for s in nice_to_have
            if code_to_group.get(s.code) not in must_have_group_names
        ]
        nice_to_have_codes = {s.code for s in nice_to_have}

    # Build candidate pool
    fillers: list[Subject] = []
    must_have_group_names = set()
    if code_to_group:
        for s in must_have:
            grp = code_to_group.get(s.code)
            if grp:
                must_have_group_names.add(grp)

    for code, subj in all_subjects.items():
        if code in mandatory_subjects:
            continue
        if code in must_have_codes or code in nice_to_have_codes:
            continue
        # Prune fillers whose group conflicts with a must-have
        if code_to_group and code_to_group.get(code) in must_have_group_names:
            continue
        fillers.append(subj)

    initial_filler_count = len(fillers)

    # Pre-filter: remove candidates conflicting with ALL must-haves
    if must_have:
        def conflicts_with_all_must_have(subj: Subject) -> bool:
            for mh in must_have:
                if not _subjects_conflict(subj, mh):
                    return False
            return True
        fillers = [f for f in fillers if not conflicts_with_all_must_have(f)]

    fillers.sort(key=lambda s: _count_mandatory_conflicts(s, mandatory_slots))
    fillers = fillers[:50]

    pruned_count = initial_filler_count - len(fillers)

    # Show pool summary
    pool_info = Text()
    pool_info.append("  Must-have:    ", style="dim")
    pool_info.append(f"{len(must_have)}", style="bold green")
    pool_info.append("  Nice-to-have: ", style="dim")
    pool_info.append(f"{len(nice_to_have)}", style="bold blue")
    pool_info.append("  Candidates:   ", style="dim")
    pool_info.append(f"{len(fillers)}", style="bold yellow")
    if pruned_count > 0:
        pool_info.append(f"  ({pruned_count} pruned)", style="dim red")
    console.print(pool_info)

    remaining_slots = config.max_electives - len(must_have)
    if remaining_slots <= 0:
        combo = _score_combination(must_have, [], [], mandatory_slots, config)
        console.print("[dim]Only must-haves fit. Single combination returned.\n")
        return [combo]

    candidate_pool = nice_to_have + fillers

    # ── Phase 3: Precompute conflicts ─────────────────────────────────────
    all_scorable = must_have + candidate_pool
    n_pairs = len(all_scorable) * (len(all_scorable) - 1) // 2

    with console.status(
        f"[bold cyan]Precomputing conflict matrix ({n_pairs} pairs)...",
        spinner="dots",
    ):
        conflict_matrix = _precompute_conflict_matrix(all_scorable)
        mandatory_conflict_cache = _precompute_mandatory_conflicts(all_scorable, mandatory_slots)

    # Count conflict stats from the matrix
    pairs_with_conflicts = sum(1 for v in conflict_matrix.values() if v)
    total_conflicts_found = sum(len(v) for v in conflict_matrix.values())
    disjoint_pairs = n_pairs - len(conflict_matrix)  # pairs skipped by quick-reject

    conflict_info = Text()
    conflict_info.append("  Pairs analyzed: ", style="dim")
    conflict_info.append(f"{n_pairs}", style="bold")
    conflict_info.append("  Conflicts found: ", style="dim")
    conflict_info.append(f"{total_conflicts_found}", style="bold red" if total_conflicts_found else "bold green")
    conflict_info.append("  Disjoint (fast skip): ", style="dim")
    conflict_info.append(f"{disjoint_pairs}", style="bold cyan")
    console.print(conflict_info)

    # ── Phase 4: Enumerate and score combinations ─────────────────────────
    heap: list[tuple[float, int, ScheduleCombination]] = []
    counter = 0

    max_pool = min(len(candidate_pool), remaining_slots)
    total_combos = sum(math.comb(len(candidate_pool), k) for k in range(0, max_pool + 1))

    best_score = float("-inf")
    conflict_free_count = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(bar_width=30),
        MofNCompleteColumn(),
        TextColumn("[dim]{task.fields[info]}"),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task(
            "Scoring combinations",
            total=total_combos,
            info="",
        )

        for size in range(0, max_pool + 1):
            for subset in combinations(candidate_pool, size):
                # Skip subsets that violate exclusion groups (hard constraint)
                if code_to_group and _violates_exclusion_groups(subset, code_to_group):
                    counter += 1
                    if counter % 500 == 0:
                        progress.update(
                            task,
                            completed=counter,
                            info=f"best: {best_score:.1f}  conflict-free: {conflict_free_count}",
                        )
                    continue

                subset_nice = [s for s in subset if s.code in nice_to_have_codes]
                subset_fillers = [s for s in subset if s.code not in nice_to_have_codes]

                combo = _score_combination(
                    must_have, subset_nice, subset_fillers, mandatory_slots, config,
                    conflict_matrix=conflict_matrix,
                    mandatory_conflict_cache=mandatory_conflict_cache,
                )

                if not combo.internal_conflicts:
                    conflict_free_count += 1

                if len(heap) < config.max_combinations:
                    heapq.heappush(heap, (combo.score, counter, combo))
                elif combo.score > heap[0][0]:
                    heapq.heapreplace(heap, (combo.score, counter, combo))

                if combo.score > best_score:
                    best_score = combo.score

                counter += 1

                # Update progress every 500 iterations to avoid overhead
                if counter % 500 == 0 or counter == total_combos:
                    progress.update(
                        task,
                        completed=counter,
                        info=f"best: {best_score:.1f}  conflict-free: {conflict_free_count}",
                    )

        # Final update
        progress.update(task, completed=total_combos)

    # ── Summary ───────────────────────────────────────────────────────────
    results = [entry[2] for entry in heap]
    results.sort(key=lambda c: -c.score)

    summary = Table.grid(padding=(0, 2))
    summary.add_column(style="dim")
    summary.add_column(style="bold")
    summary.add_row("Combinations evaluated", f"{counter:,}")
    summary.add_row("Conflict-free", f"{conflict_free_count:,}")
    summary.add_row("Best score", f"{best_score:.1f}" if best_score > float("-inf") else "N/A")
    summary.add_row("Returning top", f"{len(results)}")

    console.print(Panel(summary, title="[bold green]Optimization Complete", border_style="green", padding=(0, 2)))
    console.print()

    return results
