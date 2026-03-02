# wahlfach-matching

CLI tool for scoring and ranking elective courses at Hochschule Reutlingen based on schedule conflicts and personal preferences.

Built on [`hsrt-timetable`](https://pypi.org/project/hsrt-timetable/) and [`webuntis-public`](https://pypi.org/project/webuntis-public/).

## Installation

Install directly from GitHub using [pipx](https://pipx.pypa.io/) (recommended for CLI tools):

```bash
pipx install git+https://github.com/mklemmingen/wahlfach-matching.git
```

Or with pip:

```bash
pip install git+https://github.com/mklemmingen/wahlfach-matching.git
```

Or clone and install locally:

```bash
git clone https://github.com/mklemmingen/wahlfach-matching.git
cd wahlfach-matching
pip install .
```

## Usage

### Interactive mode — browse, categorize, and iterate

```bash
# Launch interactive mode: pick programs, semesters, then categorize subjects
wahlfach-matching --interactive

# After results are shown, you can:
#   - Re-categorize subjects and re-run the optimizer
#   - Export selected combinations as JSON and/or ICS
#   - Exit
```

### Classic mode — rank individual electives

```bash
# Basic: score all electives for MKIB semesters 4, 6, 7
wahlfach-matching

# Specify mandatory subjects (their time slots will be blocked)
wahlfach-matching --mandatory MATH PHYS

# Prefer certain weekdays
wahlfach-matching --preferred-days Monday Wednesday

# Show top 20 results
wahlfach-matching --top 20

# Skip ICS export, save JSON report
wahlfach-matching --no-ics --json

# Fetch different programs/semesters
wahlfach-matching --programs MKIB WIB --semesters 4 6
```

### Combination mode — find the best schedule with specific classes together

```bash
# Find best schedules that always include 3 specific classes
wahlfach-matching --must-have MATH PHYS ART

# Must-haves + nice-to-haves: MATH and PHYS are required, ART and MUSIC are preferred
wahlfach-matching --must-have MATH PHYS --nice-to-have ART MUSIC

# Show top 10 combinations with up to 8 electives each
wahlfach-matching --must-have MATH PHYS ART --max-combinations 10 --max-electives 8

# Exclude subjects from all combinations
wahlfach-matching --must-have MATH PHYS --exclude AKI DM

# Combine with JSON export
wahlfach-matching --must-have MATH PHYS ART --json
```

### Static course management

Courses not listed in WebUntis (language courses, block seminars, external electives) can be added manually as **static courses**. These are merged with fetched Untis data during optimization and included in conflict checks, scoring, and ICS export.

```bash
# Add a new static course interactively
wahlfach-matching --add-course

# List all saved static courses
wahlfach-matching --list-courses

# Remove a static course by code
wahlfach-matching --remove-course SPAN1

# Full management menu (add, list, remove)
wahlfach-matching --manage-courses
```

When adding a course, you are prompted for:
1. **Course code** (e.g., `SPAN1`, `EC`, `ROS`)
2. **Course name**
3. **Category** — must-have or nice-to-have
4. **Weekly schedule** — one or more weekday + start/end time pairs
5. **Scheduling mode**:
   - **Weekly** — repeats every week across the semester (default for regular courses)
   - **Specific dates** — only occurs on explicitly listed dates (for block courses, Saturday seminars, irregular schedules)
6. **Notes** (optional)

#### Specific dates for block courses

Block courses, Saturday seminars, and irregular courses often only meet on specific dates rather than every week. The `specific_dates` feature prevents phantom lessons from inflating conflict counts and distorting scores.

Example: A Saturday block course meeting on 5 specific Saturdays with 2 time slots per day generates **10 real lessons** instead of ~36 phantom lessons from weekly expansion across 18 weeks.

When adding a course via `--add-course` or interactive mode, choose "Specific dates" as the scheduling mode, then enter each date in YYYY-MM-DD format. The tool validates that each date's weekday matches the schedule's time slots.

Static courses are stored in `output/.cache/static_courses.json` and persist across runs.

### Cache options

Timetable data is cached locally (default: 24h) to avoid re-fetching on subsequent runs.

```bash
# Force re-fetch (ignore cache)
wahlfach-matching --no-cache --must-have MATH PHYS

# Set cache TTL to 48 hours
wahlfach-matching --cache-ttl 48

# Clear cached data
wahlfach-matching --clear-cache
```

## How It Works

1. **Fetch** — Retrieves timetable data from WebUntis for the configured programs and semesters (cached locally by default)
2. **Merge** — Loads static courses from cache and merges them with fetched data, expanding weekly courses across the semester date range or using specific dates for block courses
3. **Precompute** — Builds a pairwise conflict matrix using date-indexed lookups (O(n+m) per pair, with fast disjoint-date rejection) and caches mandatory conflict counts
4. **Optimize** — Enumerates candidate combinations, scoring each for internal conflicts, mandatory slot conflicts, compactness, and free days. Uses a min-heap to track the top-N results. Progress is displayed via a rich progress bar
5. **Report** — Prints results using rich panels, tables, and color-coded conflict info
6. **Export** — Generates `.ics` calendar files, Markdown reports (with UUID), and optional JSON

## Output

- Rich terminal output with progress bars, panels, and color-coded tables
- Individual `.ics` files per combination (importable into any calendar app)
- Markdown results with UUID in `output/results/`
- Optional JSON report (`--json`)
- Selective export in interactive mode (pick which combinations to export)

## Options

| Flag | Description |
|------|-------------|
| `--programs` | Study programs to fetch (default: MKIB) |
| `--semesters` | Semester numbers (default: 4 6 7) |
| `--mandatory` | Subject codes already enrolled in |
| `--preferred-days` | Weekdays to favor (e.g. Monday) |
| `--max-conflicts` | Max acceptable conflicts (0 = show all) |
| `--top` | Number of results to show (default: 10) |
| `--output-dir` | Output directory (default: output/) |
| `--no-ics` | Skip ICS export |
| `--json` | Save JSON report |
| `--interactive` | Run interactive mode with prompts |
| `--must-have` | Subject codes that must be in every combination |
| `--nice-to-have` | Subject codes preferred but not required |
| `--exclude` | Subject codes to exclude from all combinations |
| `--max-combinations` | Number of top combinations to show (default: 5) |
| `--max-electives` | Max electives per combination (default: 6) |
| `--add-course` | Interactively add a new static course |
| `--list-courses` | List all saved static courses |
| `--remove-course CODE` | Remove a static course by code |
| `--manage-courses` | Interactive static course management menu |
| `--no-cache` | Disable timetable cache, always re-fetch |
| `--clear-cache` | Clear cached timetable data and exit |
| `--cache-ttl` | Cache time-to-live in hours (default: 24) |

## Known Limitations

Some elective modules are **not listed in WebUntis** and their schedules cannot be fetched automatically. The total number of modules shown may be fewer than what is actually offered.

### Categories of commonly missing modules

- **Language courses** (e.g., Spanish, French) offered through the SLI (Sprachlehrinstitut)
- **External or cross-faculty electives** not scheduled through the standard system
- **Newly added courses** not yet entered into WebUntis at fetch time
- **Block seminars or weekend workshops** with irregular schedules
- **Courses from other departments** shared across programs but not linked to your semester groups

Use `--add-course` or the interactive mode's static course management to add these manually with their known schedules.

### Data accuracy

- Timetable data is fetched from the public WebUntis REST API for HS Reutlingen
- Accuracy depends on what is published in WebUntis at the time of fetching
- Always verify your final schedule against the official course catalog and faculty announcements
- The tool automatically deduplicates lessons that appear in multiple semester groups

## License

Apache-2.0
