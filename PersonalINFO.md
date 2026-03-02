# Personal Info / Known Limitations

## Modules Not Found in WebUntis

Some elective modules that are offered this semester are **not yet listed in the WebUntis timetable system**. Their schedules are not available for automatic fetching and conflict detection.

This means the total number of modules shown by the tool may be **fewer than what is actually offered**. If you know a course is offered this semester but it doesn't appear in the fetched results, you should add it manually as a static course (see below).

### Known categories of missing modules

- **Language courses** (e.g., Spanish, French) offered through the SLI (Sprachlehrinstitut) — these are typically not managed in WebUntis
- **External or cross-faculty electives** not scheduled through the standard system
- **Newly added courses** that haven't been entered into WebUntis yet at fetch time
- **Block seminars or weekend workshops** with irregular schedules that may not appear in weekly timetable views
- **Courses from other departments** shared across programs but not linked to your semester groups in Untis

### How to add missing modules

If you know the schedule of a course not found in Untis, add it as a **static course** so the optimizer can include it in conflict checks and combination scoring:

```bash
# Via dedicated command
wahlfach-matching --add-course

# Or through interactive mode (offers static course management at startup)
wahlfach-matching --interactive
```

You will be prompted for:
1. Course code (e.g., SPAN1, IOT_LAB)
2. Course name
3. Category (must-have or nice-to-have)
4. Weekly schedule (weekday + start/end times)

The static course will then be merged with fetched Untis data during optimization.

## Notes

- Timetable data is fetched from the public WebUntis REST API for HS Reutlingen
- Data accuracy depends on what is published in WebUntis at the time of fetching
- Always verify your final schedule against the official course catalog and faculty announcements
- The tool automatically deduplicates lessons that appear in multiple semester groups
