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

# Custom output directory
wahlfach-matching --output-dir ./my-results
```

## How It Works

1. **Fetch** — Retrieves timetable data from WebUntis for the configured programs and semesters
2. **Aggregate** — Groups all periods by subject across all class groups
3. **Score** — Ranks elective subjects based on:
   - Schedule conflicts with mandatory subjects
   - Preferred weekday matches
   - Total commitment (number of sessions)
4. **Report** — Prints a ranked list of best-fit electives
5. **Export** — Generates `.ics` calendar files for top-ranked subjects

## Output

- Console ranking with scores, conflicts, and schedule details
- Individual `.ics` files per top-ranked subject (importable into any calendar app)
- Optional JSON report (`--json`)

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

## License

Apache-2.0
