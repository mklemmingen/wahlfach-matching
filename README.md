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

# Combine with JSON export
wahlfach-matching --must-have MATH PHYS ART --json
```

### Interactive mode — browse, categorize, and iterate

```bash
# Launch interactive mode: pick programs, semesters, then categorize subjects
wahlfach-matching --interactive

# After results are shown, you can:
#   - Re-categorize subjects and re-run the optimizer
#   - Export selected combinations as JSON and/or ICS
#   - Exit
```

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
2. **Aggregate** — Groups all periods by subject across all class groups
3. **Score / Optimize** — In classic mode, ranks individual electives by conflict score. In combination mode, finds optimal multi-subject schedules considering conflicts, compactness, and free days
4. **Report** — Prints a ranked list of best-fit electives or schedule combinations
5. **Export** — Generates `.ics` calendar files and optional JSON reports

## Output

- Console ranking with scores, conflicts, and schedule details
- Individual `.ics` files per top-ranked subject or per combination (importable into any calendar app)
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
| `--max-combinations` | Number of top combinations to show (default: 5) |
| `--max-electives` | Max electives per combination (default: 6) |
| `--no-cache` | Disable timetable cache, always re-fetch |
| `--clear-cache` | Clear cached timetable data and exit |
| `--cache-ttl` | Cache time-to-live in hours (default: 24) |

## License

Apache-2.0
