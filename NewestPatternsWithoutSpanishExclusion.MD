~/PycharmProjects/wahlfach-matching main*
.venv ❯ wahlfach-matching --interactive
? Select study programs to fetch: ['MKIB']
? Select semesters to include: ['4', '6', '7']
? You have 8 static course(s). Manage them? No
? Timetable data source: Re-fetch from Untis (fresh data)
Fetching 3MKIB4...
  Got 119 periods across 18 weeks
Fetching 3MKIB6...
  Got 379 periods across 18 weeks
Fetching 3MKIB7...
  Got 286 periods across 18 weeks
Timetable data cached.

Found 36 unique subjects.

? Select subjects to EXCLUDE (never used in any combination): ['3MKIB4-P41      IT-Sicherheit', '3MKIB4-P43      Softwaretechnik 2'
, '3MKIB4-P44      Mobile Computing', '3MKIB4-P45      Digital Art', '3MKIB4-P46      Data Science', '3MKIB5--P51     1.Praxissemes
ter Begleitseminar', '3MKIB6-W103     Angewandte Künstliche Intelligenz', '3MKIB6-W104     Data Mining', '3MKIB6-W114     E-Health'
, '3MKIB6-W115     Medizinische Informationssysteme', '3MKIB6-W117     Medizinische Visualisierung und Simulation', '3MKIB6-W118   
  Standards u. Prozesse d. Medizinisch-Technischen Informatik', '3MKIB6-W120     Logistik und Produktion - Industrie 4.0', '3MKIB6-
W122     DevOps - Methoden und Werkzeuge', '3MKIB6-W123     Game Art', '3MKIB6-W125     AI x Creativity - Story; Style and Speculat
ion', '3VINF9--W5      Praktikantentag']
Excluded 17 subject(s).
? Select MUST-HAVE subjects (always in every combination): ['3MKIB4-P42      Datenbanksysteme 2', '3MKIB6--P74     BK:Bachlor Kollo
quium', '3MKIB6-P65      Innovation Lab', '3MKIB7-P73      Aspekte der Kommunikation']
? Select NICE-TO-HAVE subjects (preferred but optional): []

--- Summary ---
Must-have:    3MKIB4-P42, 3MKIB6--P74, 3MKIB6-P65, 3MKIB7-P73
Nice-to-have: (none)

? Maximum electives per combination (4-15): 15
? How many top combinations to show (1-20): 15
? Proceed with these settings? Yes
                 Static Courses Loaded                 
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
┃ Code            ┃ Category     ┃ Mode     ┃ Lessons ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
│ SPANISH1-TUE-AM │ nice-to-have │ 15 dates │      15 │
│ SPANISH1-TUE-PM │ nice-to-have │ 10 dates │      10 │
│ SPANISH1-WED    │ nice-to-have │ weekly   │      17 │
│ SPANISH1-THU    │ nice-to-have │ weekly   │      17 │
│ BTA             │ nice-to-have │ weekly   │      17 │
│ EC              │ nice-to-have │ 5 dates  │      10 │
│ ROS             │ nice-to-have │ 3 dates  │       9 │
│ IMR             │ nice-to-have │ 8 dates  │       8 │
└─────────────────┴──────────────┴──────────┴─────────┘

  Must-have:    4  Nice-to-have: 8  Candidates:   15
  Pairs analyzed: 351  Conflicts found: 209  Disjoint (fast skip): 0
╭───────────────────────────────────────────────────── Optimization Complete ─────────────────────────────────────────────────────╮
│  Combinations evaluated  4,194,304                                                                                              │
│  Conflict-free           4,320                                                                                                  │
│  Best score              65.5                                                                                                   │
│  Returning top           15                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│  SCHEDULE COMBINATION RESULTS                                                                                                   │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
Excluded:   3MKIB4-P41, 3MKIB4-P43, 3MKIB4-P44, 3MKIB4-P45, 3MKIB4-P46, 3MKIB5--P51, 3MKIB6-W103, 3MKIB6-W104, 3MKIB6-W114,        
            3MKIB6-W115, 3MKIB6-W117, 3MKIB6-W118, 3MKIB6-W120, 3MKIB6-W122, 3MKIB6-W123, 3MKIB6-W125, 3VINF9--W5                  
Must-have:  3MKIB4-P42, 3MKIB6--P74, 3MKIB6-P65, 3MKIB7-P73                                                                        

Found 15 combination(s)

╭──────────────────────────────────────────────────────── #1  Score: 65.5 ────────────────────────────────────────────────────────╮
│ Closeness (avg gap)     45 min                                                                                                  │
│ Earliest start          08:00                                                                                                   │
│ Average day start       10:23                                                                                                   │
│ Latest end              19:30                                                                                                   │
│ Average day end         17:47                                                                                                   │
│ Free days/week          0 (Sunday)                                                                                              │
│                                                                                                                                 │
│ ┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│ ┃ Tier       ┃ Code         ┃ Name      ┃ Schedule                                    ┃ Lessons ┃ Teacher(s)                  ┃ │
│ ┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩ │
│ │ MUST       │ 3MKIB4-P42   │ Datenban… │ Tue 09:45-13:00                             │      15 │ Hertkorn                    │ │
│ │            │              │ 2         │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6--P74  │ BK:Bachl… │ Wed 15:30-18:45                             │      28 │ Martinez Madrid             │ │
│ │            │              │ Kolloqui… │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6-P65   │ Innovati… │ Mon,Wed 13:45-17:00 / 15:30-18:45           │      31 │ Hartmann, INF N.N., Tullius │ │
│ │            │              │ Lab       │                                             │         │                             │ │
│ │ MUST       │ 3MKIB7-P73   │ Aspekte   │ Fri 09:45-13:00 / 13:45-17:00 / 13:45-18:45 │       7 │ Gaiduk                      │ │
│ │            │              │ der       │                                             │         │                             │ │
│ │            │              │ Kommunik… │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-TU… │ Spanish 1 │ Tue 08:00-09:30                             │      15 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 1,        │                                             │         │                             │ │
│ │            │              │ Dienstag  │                                             │         │                             │ │
│ │            │              │ Morgen)   │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-TU… │ Spanish 1 │ Tue 17:15-19:30                             │      10 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 2,        │                                             │         │                             │ │
│ │            │              │ Dienstag  │                                             │         │                             │ │
│ │            │              │ Abend)    │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-THU │ Spanish 1 │ Thu 17:15-19:30                             │      17 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 4,        │                                             │         │                             │ │
│ │            │              │ Donnerst… │                                             │         │                             │ │
│ │            │              │ Abend)    │                                             │         │                             │ │
│ │ NICE       │ BTA          │ Einführu… │ Tue 13:45-17:00                             │      17 │                             │ │
│ │            │              │ in        │                                             │         │                             │ │
│ │            │              │ Blockcha… │                                             │         │                             │ │
│ │            │              │ Technolo… │                                             │         │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ Anwendun… │                                             │         │                             │ │
│ │ NICE       │ EC           │ E-Commer… │ Sat 08:00-13:00 / 13:45-17:00               │      10 │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ E-Busine… │                                             │         │                             │ │
│ │ NICE       │ IMR          │ Interakt… │ Tue,Wed 13:45-15:15 / 17:15-18:45           │       8 │                             │ │
│ │            │              │ mobile    │                                             │         │                             │ │
│ │            │              │ Roboter   │                                             │         │                             │ │
│ │ COULD FIT  │ 3MKIB6-W105  │ Computer… │ Thu 11:30-13:00 / 13:45-15:15               │      52 │ Kloos                       │ │
│ │ COULD FIT  │ 3MKIB7--P72  │ Psycholo… │ Mon 17:15-18:45                             │      15 │ Rupp                        │ │
│ │ COULD FIT  │ 3MKIB7--W215 │ Business  │ Mon,Fri 08:00-09:30                         │      28 │ Schlegel                    │ │
│ │            │              │ Consulti… │                                             │         │                             │ │
│ │ COULD FIT  │ 3MKIB7-W229  │ Developm… │ Mon 09:45-13:00                             │      30 │                             │ │
│ │            │              │ of Smart  │                                             │         │                             │ │
│ │            │              │ Textiles  │                                             │         │                             │ │
│ └────────────┴──────────────┴───────────┴─────────────────────────────────────────────┴─────────┴─────────────────────────────┘ │
│   2 conflict(s):                                                                                                                │
│     SPANISH1-TUE-PM vs IMR on 2026-04-14 17:15-19:30                                                                            │
│     SPANISH1-TUE-PM vs IMR on 2026-05-12 17:15-19:30                                                                            │
│                                                                                                                                 │
│   6 nice-to-have(s) included; 4 filler(s) included; 2 internal conflict(s)                                                      │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭──────────────────────────────────────────────────────── #2  Score: 65.5 ────────────────────────────────────────────────────────╮
│ Closeness (avg gap)     46 min                                                                                                  │
│ Earliest start          08:00                                                                                                   │
│ Average day start       10:28                                                                                                   │
│ Latest end              19:30                                                                                                   │
│ Average day end         17:45                                                                                                   │
│ Free days/week          0 (Sunday)                                                                                              │
│                                                                                                                                 │
│ ┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│ ┃ Tier       ┃ Code         ┃ Name      ┃ Schedule                                    ┃ Lessons ┃ Teacher(s)                  ┃ │
│ ┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩ │
│ │ MUST       │ 3MKIB4-P42   │ Datenban… │ Tue 09:45-13:00                             │      15 │ Hertkorn                    │ │
│ │            │              │ 2         │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6--P74  │ BK:Bachl… │ Wed 15:30-18:45                             │      28 │ Martinez Madrid             │ │
│ │            │              │ Kolloqui… │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6-P65   │ Innovati… │ Mon,Wed 13:45-17:00 / 15:30-18:45           │      31 │ Hartmann, INF N.N., Tullius │ │
│ │            │              │ Lab       │                                             │         │                             │ │
│ │ MUST       │ 3MKIB7-P73   │ Aspekte   │ Fri 09:45-13:00 / 13:45-17:00 / 13:45-18:45 │       7 │ Gaiduk                      │ │
│ │            │              │ der       │                                             │         │                             │ │
│ │            │              │ Kommunik… │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-TU… │ Spanish 1 │ Tue 08:00-09:30                             │      15 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 1,        │                                             │         │                             │ │
│ │            │              │ Dienstag  │                                             │         │                             │ │
│ │            │              │ Morgen)   │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-TU… │ Spanish 1 │ Tue 17:15-19:30                             │      10 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 2,        │                                             │         │                             │ │
│ │            │              │ Dienstag  │                                             │         │                             │ │
│ │            │              │ Abend)    │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-THU │ Spanish 1 │ Thu 17:15-19:30                             │      17 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 4,        │                                             │         │                             │ │
│ │            │              │ Donnerst… │                                             │         │                             │ │
│ │            │              │ Abend)    │                                             │         │                             │ │
│ │ NICE       │ BTA          │ Einführu… │ Tue 13:45-17:00                             │      17 │                             │ │
│ │            │              │ in        │                                             │         │                             │ │
│ │            │              │ Blockcha… │                                             │         │                             │ │
│ │            │              │ Technolo… │                                             │         │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ Anwendun… │                                             │         │                             │ │
│ │ NICE       │ EC           │ E-Commer… │ Sat 08:00-13:00 / 13:45-17:00               │      10 │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ E-Busine… │                                             │         │                             │ │
│ │ COULD FIT  │ 3MKIB6-W105  │ Computer… │ Thu 11:30-13:00 / 13:45-15:15               │      52 │ Kloos                       │ │
│ │ COULD FIT  │ 3MKIB7--P72  │ Psycholo… │ Mon 17:15-18:45                             │      15 │ Rupp                        │ │
│ │ COULD FIT  │ 3MKIB7--W215 │ Business  │ Mon,Fri 08:00-09:30                         │      28 │ Schlegel                    │ │
│ │            │              │ Consulti… │                                             │         │                             │ │
│ │ COULD FIT  │ 3WIB-2-P22   │ Digital   │ Mon 09:45-13:00                             │      30 │ Schmäh                      │ │
│ │            │              │ Marketing │                                             │         │                             │ │
│ │            │              │ and Sales │                                             │         │                             │ │
│ └────────────┴──────────────┴───────────┴─────────────────────────────────────────────┴─────────┴─────────────────────────────┘ │
│   5 nice-to-have(s) included; 4 filler(s) included                                                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭──────────────────────────────────────────────────────── #3  Score: 65.5 ────────────────────────────────────────────────────────╮
│ Closeness (avg gap)     46 min                                                                                                  │
│ Earliest start          08:00                                                                                                   │
│ Average day start       10:28                                                                                                   │
│ Latest end              19:30                                                                                                   │
│ Average day end         17:45                                                                                                   │
│ Free days/week          0 (Sunday)                                                                                              │
│                                                                                                                                 │
│ ┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│ ┃ Tier       ┃ Code         ┃ Name      ┃ Schedule                                    ┃ Lessons ┃ Teacher(s)                  ┃ │
│ ┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩ │
│ │ MUST       │ 3MKIB4-P42   │ Datenban… │ Tue 09:45-13:00                             │      15 │ Hertkorn                    │ │
│ │            │              │ 2         │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6--P74  │ BK:Bachl… │ Wed 15:30-18:45                             │      28 │ Martinez Madrid             │ │
│ │            │              │ Kolloqui… │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6-P65   │ Innovati… │ Mon,Wed 13:45-17:00 / 15:30-18:45           │      31 │ Hartmann, INF N.N., Tullius │ │
│ │            │              │ Lab       │                                             │         │                             │ │
│ │ MUST       │ 3MKIB7-P73   │ Aspekte   │ Fri 09:45-13:00 / 13:45-17:00 / 13:45-18:45 │       7 │ Gaiduk                      │ │
│ │            │              │ der       │                                             │         │                             │ │
│ │            │              │ Kommunik… │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-TU… │ Spanish 1 │ Tue 08:00-09:30                             │      15 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 1,        │                                             │         │                             │ │
│ │            │              │ Dienstag  │                                             │         │                             │ │
│ │            │              │ Morgen)   │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-TU… │ Spanish 1 │ Tue 17:15-19:30                             │      10 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 2,        │                                             │         │                             │ │
│ │            │              │ Dienstag  │                                             │         │                             │ │
│ │            │              │ Abend)    │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-THU │ Spanish 1 │ Thu 17:15-19:30                             │      17 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 4,        │                                             │         │                             │ │
│ │            │              │ Donnerst… │                                             │         │                             │ │
│ │            │              │ Abend)    │                                             │         │                             │ │
│ │ NICE       │ BTA          │ Einführu… │ Tue 13:45-17:00                             │      17 │                             │ │
│ │            │              │ in        │                                             │         │                             │ │
│ │            │              │ Blockcha… │                                             │         │                             │ │
│ │            │              │ Technolo… │                                             │         │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ Anwendun… │                                             │         │                             │ │
│ │ NICE       │ EC           │ E-Commer… │ Sat 08:00-13:00 / 13:45-17:00               │      10 │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ E-Busine… │                                             │         │                             │ │
│ │ COULD FIT  │ 3MKIB6-W105  │ Computer… │ Thu 11:30-13:00 / 13:45-15:15               │      52 │ Kloos                       │ │
│ │ COULD FIT  │ 3MKIB7--P72  │ Psycholo… │ Mon 17:15-18:45                             │      15 │ Rupp                        │ │
│ │ COULD FIT  │ 3MKIB7--W215 │ Business  │ Mon,Fri 08:00-09:30                         │      28 │ Schlegel                    │ │
│ │            │              │ Consulti… │                                             │         │                             │ │
│ │ COULD FIT  │ 3MKIB7-W229  │ Developm… │ Mon 09:45-13:00                             │      30 │                             │ │
│ │            │              │ of Smart  │                                             │         │                             │ │
│ │            │              │ Textiles  │                                             │         │                             │ │
│ └────────────┴──────────────┴───────────┴─────────────────────────────────────────────┴─────────┴─────────────────────────────┘ │
│   5 nice-to-have(s) included; 4 filler(s) included                                                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭──────────────────────────────────────────────────────── #4  Score: 65.5 ────────────────────────────────────────────────────────╮
│ Closeness (avg gap)     45 min                                                                                                  │
│ Earliest start          08:00                                                                                                   │
│ Average day start       10:23                                                                                                   │
│ Latest end              19:30                                                                                                   │
│ Average day end         17:47                                                                                                   │
│ Free days/week          0 (Sunday)                                                                                              │
│                                                                                                                                 │
│ ┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│ ┃ Tier       ┃ Code         ┃ Name      ┃ Schedule                                    ┃ Lessons ┃ Teacher(s)                  ┃ │
│ ┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩ │
│ │ MUST       │ 3MKIB4-P42   │ Datenban… │ Tue 09:45-13:00                             │      15 │ Hertkorn                    │ │
│ │            │              │ 2         │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6--P74  │ BK:Bachl… │ Wed 15:30-18:45                             │      28 │ Martinez Madrid             │ │
│ │            │              │ Kolloqui… │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6-P65   │ Innovati… │ Mon,Wed 13:45-17:00 / 15:30-18:45           │      31 │ Hartmann, INF N.N., Tullius │ │
│ │            │              │ Lab       │                                             │         │                             │ │
│ │ MUST       │ 3MKIB7-P73   │ Aspekte   │ Fri 09:45-13:00 / 13:45-17:00 / 13:45-18:45 │       7 │ Gaiduk                      │ │
│ │            │              │ der       │                                             │         │                             │ │
│ │            │              │ Kommunik… │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-TU… │ Spanish 1 │ Tue 08:00-09:30                             │      15 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 1,        │                                             │         │                             │ │
│ │            │              │ Dienstag  │                                             │         │                             │ │
│ │            │              │ Morgen)   │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-TU… │ Spanish 1 │ Tue 17:15-19:30                             │      10 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 2,        │                                             │         │                             │ │
│ │            │              │ Dienstag  │                                             │         │                             │ │
│ │            │              │ Abend)    │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-THU │ Spanish 1 │ Thu 17:15-19:30                             │      17 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 4,        │                                             │         │                             │ │
│ │            │              │ Donnerst… │                                             │         │                             │ │
│ │            │              │ Abend)    │                                             │         │                             │ │
│ │ NICE       │ BTA          │ Einführu… │ Tue 13:45-17:00                             │      17 │                             │ │
│ │            │              │ in        │                                             │         │                             │ │
│ │            │              │ Blockcha… │                                             │         │                             │ │
│ │            │              │ Technolo… │                                             │         │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ Anwendun… │                                             │         │                             │ │
│ │ NICE       │ EC           │ E-Commer… │ Sat 08:00-13:00 / 13:45-17:00               │      10 │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ E-Busine… │                                             │         │                             │ │
│ │ NICE       │ IMR          │ Interakt… │ Tue,Wed 13:45-15:15 / 17:15-18:45           │       8 │                             │ │
│ │            │              │ mobile    │                                             │         │                             │ │
│ │            │              │ Roboter   │                                             │         │                             │ │
│ │ COULD FIT  │ 3MKIB6-W105  │ Computer… │ Thu 11:30-13:00 / 13:45-15:15               │      52 │ Kloos                       │ │
│ │ COULD FIT  │ 3MKIB7--P72  │ Psycholo… │ Mon 17:15-18:45                             │      15 │ Rupp                        │ │
│ │ COULD FIT  │ 3MKIB7--W215 │ Business  │ Mon,Fri 08:00-09:30                         │      28 │ Schlegel                    │ │
│ │            │              │ Consulti… │                                             │         │                             │ │
│ │ COULD FIT  │ 3WIB-2-P22   │ Digital   │ Mon 09:45-13:00                             │      30 │ Schmäh                      │ │
│ │            │              │ Marketing │                                             │         │                             │ │
│ │            │              │ and Sales │                                             │         │                             │ │
│ └────────────┴──────────────┴───────────┴─────────────────────────────────────────────┴─────────┴─────────────────────────────┘ │
│   2 conflict(s):                                                                                                                │
│     SPANISH1-TUE-PM vs IMR on 2026-04-14 17:15-19:30                                                                            │
│     SPANISH1-TUE-PM vs IMR on 2026-05-12 17:15-19:30                                                                            │
│                                                                                                                                 │
│   6 nice-to-have(s) included; 4 filler(s) included; 2 internal conflict(s)                                                      │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭──────────────────────────────────────────────────────── #5  Score: 65.4 ────────────────────────────────────────────────────────╮
│ Closeness (avg gap)     47 min                                                                                                  │
│ Earliest start          08:00                                                                                                   │
│ Average day start       10:23                                                                                                   │
│ Latest end              19:30                                                                                                   │
│ Average day end         17:32                                                                                                   │
│ Free days/week          0 (Sunday)                                                                                              │
│                                                                                                                                 │
│ ┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│ ┃ Tier       ┃ Code         ┃ Name      ┃ Schedule                                    ┃ Lessons ┃ Teacher(s)                  ┃ │
│ ┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩ │
│ │ MUST       │ 3MKIB4-P42   │ Datenban… │ Tue 09:45-13:00                             │      15 │ Hertkorn                    │ │
│ │            │              │ 2         │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6--P74  │ BK:Bachl… │ Wed 15:30-18:45                             │      28 │ Martinez Madrid             │ │
│ │            │              │ Kolloqui… │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6-P65   │ Innovati… │ Mon,Wed 13:45-17:00 / 15:30-18:45           │      31 │ Hartmann, INF N.N., Tullius │ │
│ │            │              │ Lab       │                                             │         │                             │ │
│ │ MUST       │ 3MKIB7-P73   │ Aspekte   │ Fri 09:45-13:00 / 13:45-17:00 / 13:45-18:45 │       7 │ Gaiduk                      │ │
│ │            │              │ der       │                                             │         │                             │ │
│ │            │              │ Kommunik… │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-TU… │ Spanish 1 │ Tue 08:00-09:30                             │      15 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 1,        │                                             │         │                             │ │
│ │            │              │ Dienstag  │                                             │         │                             │ │
│ │            │              │ Morgen)   │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-THU │ Spanish 1 │ Thu 17:15-19:30                             │      17 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 4,        │                                             │         │                             │ │
│ │            │              │ Donnerst… │                                             │         │                             │ │
│ │            │              │ Abend)    │                                             │         │                             │ │
│ │ NICE       │ BTA          │ Einführu… │ Tue 13:45-17:00                             │      17 │                             │ │
│ │            │              │ in        │                                             │         │                             │ │
│ │            │              │ Blockcha… │                                             │         │                             │ │
│ │            │              │ Technolo… │                                             │         │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ Anwendun… │                                             │         │                             │ │
│ │ NICE       │ EC           │ E-Commer… │ Sat 08:00-13:00 / 13:45-17:00               │      10 │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ E-Busine… │                                             │         │                             │ │
│ │ NICE       │ IMR          │ Interakt… │ Tue,Wed 13:45-15:15 / 17:15-18:45           │       8 │                             │ │
│ │            │              │ mobile    │                                             │         │                             │ │
│ │            │              │ Roboter   │                                             │         │                             │ │
│ │ COULD FIT  │ 3MKIB6-W105  │ Computer… │ Thu 11:30-13:00 / 13:45-15:15               │      52 │ Kloos                       │ │
│ │ COULD FIT  │ 3MKIB7--P72  │ Psycholo… │ Mon 17:15-18:45                             │      15 │ Rupp                        │ │
│ │ COULD FIT  │ 3MKIB7--W215 │ Business  │ Mon,Fri 08:00-09:30                         │      28 │ Schlegel                    │ │
│ │            │              │ Consulti… │                                             │         │                             │ │
│ │ COULD FIT  │ 3WIB-2-P22   │ Digital   │ Mon 09:45-13:00                             │      30 │ Schmäh                      │ │
│ │            │              │ Marketing │                                             │         │                             │ │
│ │            │              │ and Sales │                                             │         │                             │ │
│ └────────────┴──────────────┴───────────┴─────────────────────────────────────────────┴─────────┴─────────────────────────────┘ │
│   5 nice-to-have(s) included; 4 filler(s) included                                                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭──────────────────────────────────────────────────────── #6  Score: 65.4 ────────────────────────────────────────────────────────╮
│ Closeness (avg gap)     47 min                                                                                                  │
│ Earliest start          08:00                                                                                                   │
│ Average day start       10:23                                                                                                   │
│ Latest end              19:30                                                                                                   │
│ Average day end         17:32                                                                                                   │
│ Free days/week          0 (Sunday)                                                                                              │
│                                                                                                                                 │
│ ┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│ ┃ Tier       ┃ Code         ┃ Name      ┃ Schedule                                    ┃ Lessons ┃ Teacher(s)                  ┃ │
│ ┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩ │
│ │ MUST       │ 3MKIB4-P42   │ Datenban… │ Tue 09:45-13:00                             │      15 │ Hertkorn                    │ │
│ │            │              │ 2         │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6--P74  │ BK:Bachl… │ Wed 15:30-18:45                             │      28 │ Martinez Madrid             │ │
│ │            │              │ Kolloqui… │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6-P65   │ Innovati… │ Mon,Wed 13:45-17:00 / 15:30-18:45           │      31 │ Hartmann, INF N.N., Tullius │ │
│ │            │              │ Lab       │                                             │         │                             │ │
│ │ MUST       │ 3MKIB7-P73   │ Aspekte   │ Fri 09:45-13:00 / 13:45-17:00 / 13:45-18:45 │       7 │ Gaiduk                      │ │
│ │            │              │ der       │                                             │         │                             │ │
│ │            │              │ Kommunik… │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-TU… │ Spanish 1 │ Tue 08:00-09:30                             │      15 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 1,        │                                             │         │                             │ │
│ │            │              │ Dienstag  │                                             │         │                             │ │
│ │            │              │ Morgen)   │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-THU │ Spanish 1 │ Thu 17:15-19:30                             │      17 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 4,        │                                             │         │                             │ │
│ │            │              │ Donnerst… │                                             │         │                             │ │
│ │            │              │ Abend)    │                                             │         │                             │ │
│ │ NICE       │ BTA          │ Einführu… │ Tue 13:45-17:00                             │      17 │                             │ │
│ │            │              │ in        │                                             │         │                             │ │
│ │            │              │ Blockcha… │                                             │         │                             │ │
│ │            │              │ Technolo… │                                             │         │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ Anwendun… │                                             │         │                             │ │
│ │ NICE       │ EC           │ E-Commer… │ Sat 08:00-13:00 / 13:45-17:00               │      10 │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ E-Busine… │                                             │         │                             │ │
│ │ NICE       │ IMR          │ Interakt… │ Tue,Wed 13:45-15:15 / 17:15-18:45           │       8 │                             │ │
│ │            │              │ mobile    │                                             │         │                             │ │
│ │            │              │ Roboter   │                                             │         │                             │ │
│ │ COULD FIT  │ 3MKIB6-W105  │ Computer… │ Thu 11:30-13:00 / 13:45-15:15               │      52 │ Kloos                       │ │
│ │ COULD FIT  │ 3MKIB7--P72  │ Psycholo… │ Mon 17:15-18:45                             │      15 │ Rupp                        │ │
│ │ COULD FIT  │ 3MKIB7--W215 │ Business  │ Mon,Fri 08:00-09:30                         │      28 │ Schlegel                    │ │
│ │            │              │ Consulti… │                                             │         │                             │ │
│ │ COULD FIT  │ 3MKIB7-W229  │ Developm… │ Mon 09:45-13:00                             │      30 │                             │ │
│ │            │              │ of Smart  │                                             │         │                             │ │
│ │            │              │ Textiles  │                                             │         │                             │ │
│ └────────────┴──────────────┴───────────┴─────────────────────────────────────────────┴─────────┴─────────────────────────────┘ │
│   5 nice-to-have(s) included; 4 filler(s) included                                                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭──────────────────────────────────────────────────────── #7  Score: 64.6 ────────────────────────────────────────────────────────╮
│ Closeness (avg gap)     71 min                                                                                                  │
│ Earliest start          08:00                                                                                                   │
│ Average day start       09:46                                                                                                   │
│ Latest end              19:30                                                                                                   │
│ Average day end         17:47                                                                                                   │
│ Free days/week          0 (Sunday)                                                                                              │
│                                                                                                                                 │
│ ┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│ ┃ Tier       ┃ Code         ┃ Name      ┃ Schedule                                    ┃ Lessons ┃ Teacher(s)                  ┃ │
│ ┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩ │
│ │ MUST       │ 3MKIB4-P42   │ Datenban… │ Tue 09:45-13:00                             │      15 │ Hertkorn                    │ │
│ │            │              │ 2         │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6--P74  │ BK:Bachl… │ Wed 15:30-18:45                             │      28 │ Martinez Madrid             │ │
│ │            │              │ Kolloqui… │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6-P65   │ Innovati… │ Mon,Wed 13:45-17:00 / 15:30-18:45           │      31 │ Hartmann, INF N.N., Tullius │ │
│ │            │              │ Lab       │                                             │         │                             │ │
│ │ MUST       │ 3MKIB7-P73   │ Aspekte   │ Fri 09:45-13:00 / 13:45-17:00 / 13:45-18:45 │       7 │ Gaiduk                      │ │
│ │            │              │ der       │                                             │         │                             │ │
│ │            │              │ Kommunik… │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-TU… │ Spanish 1 │ Tue 08:00-09:30                             │      15 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 1,        │                                             │         │                             │ │
│ │            │              │ Dienstag  │                                             │         │                             │ │
│ │            │              │ Morgen)   │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-TU… │ Spanish 1 │ Tue 17:15-19:30                             │      10 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 2,        │                                             │         │                             │ │
│ │            │              │ Dienstag  │                                             │         │                             │ │
│ │            │              │ Abend)    │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-THU │ Spanish 1 │ Thu 17:15-19:30                             │      17 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 4,        │                                             │         │                             │ │
│ │            │              │ Donnerst… │                                             │         │                             │ │
│ │            │              │ Abend)    │                                             │         │                             │ │
│ │ NICE       │ BTA          │ Einführu… │ Tue 13:45-17:00                             │      17 │                             │ │
│ │            │              │ in        │                                             │         │                             │ │
│ │            │              │ Blockcha… │                                             │         │                             │ │
│ │            │              │ Technolo… │                                             │         │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ Anwendun… │                                             │         │                             │ │
│ │ NICE       │ EC           │ E-Commer… │ Sat 08:00-13:00 / 13:45-17:00               │      10 │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ E-Busine… │                                             │         │                             │ │
│ │ NICE       │ IMR          │ Interakt… │ Tue,Wed 13:45-15:15 / 17:15-18:45           │       8 │                             │ │
│ │            │              │ mobile    │                                             │         │                             │ │
│ │            │              │ Roboter   │                                             │         │                             │ │
│ │ COULD FIT  │ 3MKIB6-W107  │ Audio     │ Wed,Thu 08:00-11:15 / 09:45-13:00           │      28 │ INF N.N.                    │ │
│ │ COULD FIT  │ 3MKIB7--P72  │ Psycholo… │ Mon 17:15-18:45                             │      15 │ Rupp                        │ │
│ │ COULD FIT  │ 3MKIB7--W215 │ Business  │ Mon,Fri 08:00-09:30                         │      28 │ Schlegel                    │ │
│ │            │              │ Consulti… │                                             │         │                             │ │
│ │ COULD FIT  │ 3MKIB7-W229  │ Developm… │ Mon 09:45-13:00                             │      30 │                             │ │
│ │            │              │ of Smart  │                                             │         │                             │ │
│ │            │              │ Textiles  │                                             │         │                             │ │
│ └────────────┴──────────────┴───────────┴─────────────────────────────────────────────┴─────────┴─────────────────────────────┘ │
│   2 conflict(s):                                                                                                                │
│     SPANISH1-TUE-PM vs IMR on 2026-04-14 17:15-19:30                                                                            │
│     SPANISH1-TUE-PM vs IMR on 2026-05-12 17:15-19:30                                                                            │
│                                                                                                                                 │
│   6 nice-to-have(s) included; 4 filler(s) included; 2 internal conflict(s)                                                      │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭──────────────────────────────────────────────────────── #8  Score: 64.6 ────────────────────────────────────────────────────────╮
│ Closeness (avg gap)     71 min                                                                                                  │
│ Earliest start          08:00                                                                                                   │
│ Average day start       09:46                                                                                                   │
│ Latest end              19:30                                                                                                   │
│ Average day end         17:47                                                                                                   │
│ Free days/week          0 (Sunday)                                                                                              │
│                                                                                                                                 │
│ ┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│ ┃ Tier       ┃ Code         ┃ Name      ┃ Schedule                                    ┃ Lessons ┃ Teacher(s)                  ┃ │
│ ┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩ │
│ │ MUST       │ 3MKIB4-P42   │ Datenban… │ Tue 09:45-13:00                             │      15 │ Hertkorn                    │ │
│ │            │              │ 2         │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6--P74  │ BK:Bachl… │ Wed 15:30-18:45                             │      28 │ Martinez Madrid             │ │
│ │            │              │ Kolloqui… │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6-P65   │ Innovati… │ Mon,Wed 13:45-17:00 / 15:30-18:45           │      31 │ Hartmann, INF N.N., Tullius │ │
│ │            │              │ Lab       │                                             │         │                             │ │
│ │ MUST       │ 3MKIB7-P73   │ Aspekte   │ Fri 09:45-13:00 / 13:45-17:00 / 13:45-18:45 │       7 │ Gaiduk                      │ │
│ │            │              │ der       │                                             │         │                             │ │
│ │            │              │ Kommunik… │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-TU… │ Spanish 1 │ Tue 08:00-09:30                             │      15 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 1,        │                                             │         │                             │ │
│ │            │              │ Dienstag  │                                             │         │                             │ │
│ │            │              │ Morgen)   │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-TU… │ Spanish 1 │ Tue 17:15-19:30                             │      10 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 2,        │                                             │         │                             │ │
│ │            │              │ Dienstag  │                                             │         │                             │ │
│ │            │              │ Abend)    │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-THU │ Spanish 1 │ Thu 17:15-19:30                             │      17 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 4,        │                                             │         │                             │ │
│ │            │              │ Donnerst… │                                             │         │                             │ │
│ │            │              │ Abend)    │                                             │         │                             │ │
│ │ NICE       │ BTA          │ Einführu… │ Tue 13:45-17:00                             │      17 │                             │ │
│ │            │              │ in        │                                             │         │                             │ │
│ │            │              │ Blockcha… │                                             │         │                             │ │
│ │            │              │ Technolo… │                                             │         │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ Anwendun… │                                             │         │                             │ │
│ │ NICE       │ EC           │ E-Commer… │ Sat 08:00-13:00 / 13:45-17:00               │      10 │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ E-Busine… │                                             │         │                             │ │
│ │ NICE       │ IMR          │ Interakt… │ Tue,Wed 13:45-15:15 / 17:15-18:45           │       8 │                             │ │
│ │            │              │ mobile    │                                             │         │                             │ │
│ │            │              │ Roboter   │                                             │         │                             │ │
│ │ COULD FIT  │ 3MKIB6-W107  │ Audio     │ Wed,Thu 08:00-11:15 / 09:45-13:00           │      28 │ INF N.N.                    │ │
│ │ COULD FIT  │ 3MKIB7--P72  │ Psycholo… │ Mon 17:15-18:45                             │      15 │ Rupp                        │ │
│ │ COULD FIT  │ 3MKIB7--W215 │ Business  │ Mon,Fri 08:00-09:30                         │      28 │ Schlegel                    │ │
│ │            │              │ Consulti… │                                             │         │                             │ │
│ │ COULD FIT  │ 3WIB-2-P22   │ Digital   │ Mon 09:45-13:00                             │      30 │ Schmäh                      │ │
│ │            │              │ Marketing │                                             │         │                             │ │
│ │            │              │ and Sales │                                             │         │                             │ │
│ └────────────┴──────────────┴───────────┴─────────────────────────────────────────────┴─────────┴─────────────────────────────┘ │
│   2 conflict(s):                                                                                                                │
│     SPANISH1-TUE-PM vs IMR on 2026-04-14 17:15-19:30                                                                            │
│     SPANISH1-TUE-PM vs IMR on 2026-05-12 17:15-19:30                                                                            │
│                                                                                                                                 │
│   6 nice-to-have(s) included; 4 filler(s) included; 2 internal conflict(s)                                                      │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭──────────────────────────────────────────────────────── #9  Score: 64.5 ────────────────────────────────────────────────────────╮
│ Closeness (avg gap)     75 min                                                                                                  │
│ Earliest start          08:00                                                                                                   │
│ Average day start       09:50                                                                                                   │
│ Latest end              19:30                                                                                                   │
│ Average day end         17:45                                                                                                   │
│ Free days/week          0 (Sunday)                                                                                              │
│                                                                                                                                 │
│ ┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│ ┃ Tier       ┃ Code         ┃ Name      ┃ Schedule                                    ┃ Lessons ┃ Teacher(s)                  ┃ │
│ ┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩ │
│ │ MUST       │ 3MKIB4-P42   │ Datenban… │ Tue 09:45-13:00                             │      15 │ Hertkorn                    │ │
│ │            │              │ 2         │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6--P74  │ BK:Bachl… │ Wed 15:30-18:45                             │      28 │ Martinez Madrid             │ │
│ │            │              │ Kolloqui… │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6-P65   │ Innovati… │ Mon,Wed 13:45-17:00 / 15:30-18:45           │      31 │ Hartmann, INF N.N., Tullius │ │
│ │            │              │ Lab       │                                             │         │                             │ │
│ │ MUST       │ 3MKIB7-P73   │ Aspekte   │ Fri 09:45-13:00 / 13:45-17:00 / 13:45-18:45 │       7 │ Gaiduk                      │ │
│ │            │              │ der       │                                             │         │                             │ │
│ │            │              │ Kommunik… │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-TU… │ Spanish 1 │ Tue 08:00-09:30                             │      15 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 1,        │                                             │         │                             │ │
│ │            │              │ Dienstag  │                                             │         │                             │ │
│ │            │              │ Morgen)   │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-TU… │ Spanish 1 │ Tue 17:15-19:30                             │      10 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 2,        │                                             │         │                             │ │
│ │            │              │ Dienstag  │                                             │         │                             │ │
│ │            │              │ Abend)    │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-THU │ Spanish 1 │ Thu 17:15-19:30                             │      17 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 4,        │                                             │         │                             │ │
│ │            │              │ Donnerst… │                                             │         │                             │ │
│ │            │              │ Abend)    │                                             │         │                             │ │
│ │ NICE       │ BTA          │ Einführu… │ Tue 13:45-17:00                             │      17 │                             │ │
│ │            │              │ in        │                                             │         │                             │ │
│ │            │              │ Blockcha… │                                             │         │                             │ │
│ │            │              │ Technolo… │                                             │         │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ Anwendun… │                                             │         │                             │ │
│ │ NICE       │ EC           │ E-Commer… │ Sat 08:00-13:00 / 13:45-17:00               │      10 │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ E-Busine… │                                             │         │                             │ │
│ │ COULD FIT  │ 3MKIB6-W107  │ Audio     │ Wed,Thu 08:00-11:15 / 09:45-13:00           │      28 │ INF N.N.                    │ │
│ │ COULD FIT  │ 3MKIB7--P72  │ Psycholo… │ Mon 17:15-18:45                             │      15 │ Rupp                        │ │
│ │ COULD FIT  │ 3MKIB7--W215 │ Business  │ Mon,Fri 08:00-09:30                         │      28 │ Schlegel                    │ │
│ │            │              │ Consulti… │                                             │         │                             │ │
│ │ COULD FIT  │ 3MKIB7-W229  │ Developm… │ Mon 09:45-13:00                             │      30 │                             │ │
│ │            │              │ of Smart  │                                             │         │                             │ │
│ │            │              │ Textiles  │                                             │         │                             │ │
│ └────────────┴──────────────┴───────────┴─────────────────────────────────────────────┴─────────┴─────────────────────────────┘ │
│   5 nice-to-have(s) included; 4 filler(s) included                                                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭─────────────────────────────────────────────────────── #10  Score: 64.5 ────────────────────────────────────────────────────────╮
│ Closeness (avg gap)     75 min                                                                                                  │
│ Earliest start          08:00                                                                                                   │
│ Average day start       09:46                                                                                                   │
│ Latest end              19:30                                                                                                   │
│ Average day end         17:32                                                                                                   │
│ Free days/week          0 (Sunday)                                                                                              │
│                                                                                                                                 │
│ ┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│ ┃ Tier       ┃ Code         ┃ Name      ┃ Schedule                                    ┃ Lessons ┃ Teacher(s)                  ┃ │
│ ┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩ │
│ │ MUST       │ 3MKIB4-P42   │ Datenban… │ Tue 09:45-13:00                             │      15 │ Hertkorn                    │ │
│ │            │              │ 2         │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6--P74  │ BK:Bachl… │ Wed 15:30-18:45                             │      28 │ Martinez Madrid             │ │
│ │            │              │ Kolloqui… │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6-P65   │ Innovati… │ Mon,Wed 13:45-17:00 / 15:30-18:45           │      31 │ Hartmann, INF N.N., Tullius │ │
│ │            │              │ Lab       │                                             │         │                             │ │
│ │ MUST       │ 3MKIB7-P73   │ Aspekte   │ Fri 09:45-13:00 / 13:45-17:00 / 13:45-18:45 │       7 │ Gaiduk                      │ │
│ │            │              │ der       │                                             │         │                             │ │
│ │            │              │ Kommunik… │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-TU… │ Spanish 1 │ Tue 08:00-09:30                             │      15 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 1,        │                                             │         │                             │ │
│ │            │              │ Dienstag  │                                             │         │                             │ │
│ │            │              │ Morgen)   │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-THU │ Spanish 1 │ Thu 17:15-19:30                             │      17 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 4,        │                                             │         │                             │ │
│ │            │              │ Donnerst… │                                             │         │                             │ │
│ │            │              │ Abend)    │                                             │         │                             │ │
│ │ NICE       │ BTA          │ Einführu… │ Tue 13:45-17:00                             │      17 │                             │ │
│ │            │              │ in        │                                             │         │                             │ │
│ │            │              │ Blockcha… │                                             │         │                             │ │
│ │            │              │ Technolo… │                                             │         │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ Anwendun… │                                             │         │                             │ │
│ │ NICE       │ EC           │ E-Commer… │ Sat 08:00-13:00 / 13:45-17:00               │      10 │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ E-Busine… │                                             │         │                             │ │
│ │ NICE       │ IMR          │ Interakt… │ Tue,Wed 13:45-15:15 / 17:15-18:45           │       8 │                             │ │
│ │            │              │ mobile    │                                             │         │                             │ │
│ │            │              │ Roboter   │                                             │         │                             │ │
│ │ COULD FIT  │ 3MKIB6-W107  │ Audio     │ Wed,Thu 08:00-11:15 / 09:45-13:00           │      28 │ INF N.N.                    │ │
│ │ COULD FIT  │ 3MKIB7--P72  │ Psycholo… │ Mon 17:15-18:45                             │      15 │ Rupp                        │ │
│ │ COULD FIT  │ 3MKIB7--W215 │ Business  │ Mon,Fri 08:00-09:30                         │      28 │ Schlegel                    │ │
│ │            │              │ Consulti… │                                             │         │                             │ │
│ │ COULD FIT  │ 3WIB-2-P22   │ Digital   │ Mon 09:45-13:00                             │      30 │ Schmäh                      │ │
│ │            │              │ Marketing │                                             │         │                             │ │
│ │            │              │ and Sales │                                             │         │                             │ │
│ └────────────┴──────────────┴───────────┴─────────────────────────────────────────────┴─────────┴─────────────────────────────┘ │
│   5 nice-to-have(s) included; 4 filler(s) included                                                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭─────────────────────────────────────────────────────── #11  Score: 64.5 ────────────────────────────────────────────────────────╮
│ Closeness (avg gap)     75 min                                                                                                  │
│ Earliest start          08:00                                                                                                   │
│ Average day start       09:50                                                                                                   │
│ Latest end              19:30                                                                                                   │
│ Average day end         17:45                                                                                                   │
│ Free days/week          0 (Sunday)                                                                                              │
│                                                                                                                                 │
│ ┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│ ┃ Tier       ┃ Code         ┃ Name      ┃ Schedule                                    ┃ Lessons ┃ Teacher(s)                  ┃ │
│ ┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩ │
│ │ MUST       │ 3MKIB4-P42   │ Datenban… │ Tue 09:45-13:00                             │      15 │ Hertkorn                    │ │
│ │            │              │ 2         │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6--P74  │ BK:Bachl… │ Wed 15:30-18:45                             │      28 │ Martinez Madrid             │ │
│ │            │              │ Kolloqui… │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6-P65   │ Innovati… │ Mon,Wed 13:45-17:00 / 15:30-18:45           │      31 │ Hartmann, INF N.N., Tullius │ │
│ │            │              │ Lab       │                                             │         │                             │ │
│ │ MUST       │ 3MKIB7-P73   │ Aspekte   │ Fri 09:45-13:00 / 13:45-17:00 / 13:45-18:45 │       7 │ Gaiduk                      │ │
│ │            │              │ der       │                                             │         │                             │ │
│ │            │              │ Kommunik… │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-TU… │ Spanish 1 │ Tue 08:00-09:30                             │      15 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 1,        │                                             │         │                             │ │
│ │            │              │ Dienstag  │                                             │         │                             │ │
│ │            │              │ Morgen)   │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-TU… │ Spanish 1 │ Tue 17:15-19:30                             │      10 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 2,        │                                             │         │                             │ │
│ │            │              │ Dienstag  │                                             │         │                             │ │
│ │            │              │ Abend)    │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-THU │ Spanish 1 │ Thu 17:15-19:30                             │      17 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 4,        │                                             │         │                             │ │
│ │            │              │ Donnerst… │                                             │         │                             │ │
│ │            │              │ Abend)    │                                             │         │                             │ │
│ │ NICE       │ BTA          │ Einführu… │ Tue 13:45-17:00                             │      17 │                             │ │
│ │            │              │ in        │                                             │         │                             │ │
│ │            │              │ Blockcha… │                                             │         │                             │ │
│ │            │              │ Technolo… │                                             │         │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ Anwendun… │                                             │         │                             │ │
│ │ NICE       │ EC           │ E-Commer… │ Sat 08:00-13:00 / 13:45-17:00               │      10 │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ E-Busine… │                                             │         │                             │ │
│ │ COULD FIT  │ 3MKIB6-W107  │ Audio     │ Wed,Thu 08:00-11:15 / 09:45-13:00           │      28 │ INF N.N.                    │ │
│ │ COULD FIT  │ 3MKIB7--P72  │ Psycholo… │ Mon 17:15-18:45                             │      15 │ Rupp                        │ │
│ │ COULD FIT  │ 3MKIB7--W215 │ Business  │ Mon,Fri 08:00-09:30                         │      28 │ Schlegel                    │ │
│ │            │              │ Consulti… │                                             │         │                             │ │
│ │ COULD FIT  │ 3WIB-2-P22   │ Digital   │ Mon 09:45-13:00                             │      30 │ Schmäh                      │ │
│ │            │              │ Marketing │                                             │         │                             │ │
│ │            │              │ and Sales │                                             │         │                             │ │
│ └────────────┴──────────────┴───────────┴─────────────────────────────────────────────┴─────────┴─────────────────────────────┘ │
│   5 nice-to-have(s) included; 4 filler(s) included                                                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭─────────────────────────────────────────────────────── #12  Score: 64.5 ────────────────────────────────────────────────────────╮
│ Closeness (avg gap)     75 min                                                                                                  │
│ Earliest start          08:00                                                                                                   │
│ Average day start       09:46                                                                                                   │
│ Latest end              19:30                                                                                                   │
│ Average day end         17:32                                                                                                   │
│ Free days/week          0 (Sunday)                                                                                              │
│                                                                                                                                 │
│ ┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│ ┃ Tier       ┃ Code         ┃ Name      ┃ Schedule                                    ┃ Lessons ┃ Teacher(s)                  ┃ │
│ ┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩ │
│ │ MUST       │ 3MKIB4-P42   │ Datenban… │ Tue 09:45-13:00                             │      15 │ Hertkorn                    │ │
│ │            │              │ 2         │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6--P74  │ BK:Bachl… │ Wed 15:30-18:45                             │      28 │ Martinez Madrid             │ │
│ │            │              │ Kolloqui… │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6-P65   │ Innovati… │ Mon,Wed 13:45-17:00 / 15:30-18:45           │      31 │ Hartmann, INF N.N., Tullius │ │
│ │            │              │ Lab       │                                             │         │                             │ │
│ │ MUST       │ 3MKIB7-P73   │ Aspekte   │ Fri 09:45-13:00 / 13:45-17:00 / 13:45-18:45 │       7 │ Gaiduk                      │ │
│ │            │              │ der       │                                             │         │                             │ │
│ │            │              │ Kommunik… │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-TU… │ Spanish 1 │ Tue 08:00-09:30                             │      15 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 1,        │                                             │         │                             │ │
│ │            │              │ Dienstag  │                                             │         │                             │ │
│ │            │              │ Morgen)   │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-THU │ Spanish 1 │ Thu 17:15-19:30                             │      17 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 4,        │                                             │         │                             │ │
│ │            │              │ Donnerst… │                                             │         │                             │ │
│ │            │              │ Abend)    │                                             │         │                             │ │
│ │ NICE       │ BTA          │ Einführu… │ Tue 13:45-17:00                             │      17 │                             │ │
│ │            │              │ in        │                                             │         │                             │ │
│ │            │              │ Blockcha… │                                             │         │                             │ │
│ │            │              │ Technolo… │                                             │         │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ Anwendun… │                                             │         │                             │ │
│ │ NICE       │ EC           │ E-Commer… │ Sat 08:00-13:00 / 13:45-17:00               │      10 │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ E-Busine… │                                             │         │                             │ │
│ │ NICE       │ IMR          │ Interakt… │ Tue,Wed 13:45-15:15 / 17:15-18:45           │       8 │                             │ │
│ │            │              │ mobile    │                                             │         │                             │ │
│ │            │              │ Roboter   │                                             │         │                             │ │
│ │ COULD FIT  │ 3MKIB6-W107  │ Audio     │ Wed,Thu 08:00-11:15 / 09:45-13:00           │      28 │ INF N.N.                    │ │
│ │ COULD FIT  │ 3MKIB7--P72  │ Psycholo… │ Mon 17:15-18:45                             │      15 │ Rupp                        │ │
│ │ COULD FIT  │ 3MKIB7--W215 │ Business  │ Mon,Fri 08:00-09:30                         │      28 │ Schlegel                    │ │
│ │            │              │ Consulti… │                                             │         │                             │ │
│ │ COULD FIT  │ 3MKIB7-W229  │ Developm… │ Mon 09:45-13:00                             │      30 │                             │ │
│ │            │              │ of Smart  │                                             │         │                             │ │
│ │            │              │ Textiles  │                                             │         │                             │ │
│ └────────────┴──────────────┴───────────┴─────────────────────────────────────────────┴─────────┴─────────────────────────────┘ │
│   5 nice-to-have(s) included; 4 filler(s) included                                                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭─────────────────────────────────────────────────────── #13  Score: 63.6 ────────────────────────────────────────────────────────╮
│ Closeness (avg gap)     43 min                                                                                                  │
│ Earliest start          08:00                                                                                                   │
│ Average day start       09:46                                                                                                   │
│ Latest end              19:30                                                                                                   │
│ Average day end         17:47                                                                                                   │
│ Free days/week          0 (Sunday)                                                                                              │
│                                                                                                                                 │
│ ┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│ ┃ Tier       ┃ Code         ┃ Name      ┃ Schedule                                    ┃ Lessons ┃ Teacher(s)                  ┃ │
│ ┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩ │
│ │ MUST       │ 3MKIB4-P42   │ Datenban… │ Tue 09:45-13:00                             │      15 │ Hertkorn                    │ │
│ │            │              │ 2         │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6--P74  │ BK:Bachl… │ Wed 15:30-18:45                             │      28 │ Martinez Madrid             │ │
│ │            │              │ Kolloqui… │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6-P65   │ Innovati… │ Mon,Wed 13:45-17:00 / 15:30-18:45           │      31 │ Hartmann, INF N.N., Tullius │ │
│ │            │              │ Lab       │                                             │         │                             │ │
│ │ MUST       │ 3MKIB7-P73   │ Aspekte   │ Fri 09:45-13:00 / 13:45-17:00 / 13:45-18:45 │       7 │ Gaiduk                      │ │
│ │            │              │ der       │                                             │         │                             │ │
│ │            │              │ Kommunik… │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-TU… │ Spanish 1 │ Tue 08:00-09:30                             │      15 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 1,        │                                             │         │                             │ │
│ │            │              │ Dienstag  │                                             │         │                             │ │
│ │            │              │ Morgen)   │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-TU… │ Spanish 1 │ Tue 17:15-19:30                             │      10 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 2,        │                                             │         │                             │ │
│ │            │              │ Dienstag  │                                             │         │                             │ │
│ │            │              │ Abend)    │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-THU │ Spanish 1 │ Thu 17:15-19:30                             │      17 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 4,        │                                             │         │                             │ │
│ │            │              │ Donnerst… │                                             │         │                             │ │
│ │            │              │ Abend)    │                                             │         │                             │ │
│ │ NICE       │ BTA          │ Einführu… │ Tue 13:45-17:00                             │      17 │                             │ │
│ │            │              │ in        │                                             │         │                             │ │
│ │            │              │ Blockcha… │                                             │         │                             │ │
│ │            │              │ Technolo… │                                             │         │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ Anwendun… │                                             │         │                             │ │
│ │ NICE       │ EC           │ E-Commer… │ Sat 08:00-13:00 / 13:45-17:00               │      10 │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ E-Busine… │                                             │         │                             │ │
│ │ NICE       │ IMR          │ Interakt… │ Tue,Wed 13:45-15:15 / 17:15-18:45           │       8 │                             │ │
│ │            │              │ mobile    │                                             │         │                             │ │
│ │            │              │ Roboter   │                                             │         │                             │ │
│ │ COULD FIT  │ 3MKIB6-W105  │ Computer… │ Thu 11:30-13:00 / 13:45-15:15               │      52 │ Kloos                       │ │
│ │ COULD FIT  │ 3MKIB6-W107  │ Audio     │ Wed,Thu 08:00-11:15 / 09:45-13:00           │      28 │ INF N.N.                    │ │
│ │ COULD FIT  │ 3MKIB7--P72  │ Psycholo… │ Mon 17:15-18:45                             │      15 │ Rupp                        │ │
│ │ COULD FIT  │ 3MKIB7--W215 │ Business  │ Mon,Fri 08:00-09:30                         │      28 │ Schlegel                    │ │
│ │            │              │ Consulti… │                                             │         │                             │ │
│ │ COULD FIT  │ 3MKIB7-W229  │ Developm… │ Mon 09:45-13:00                             │      30 │                             │ │
│ │            │              │ of Smart  │                                             │         │                             │ │
│ │            │              │ Textiles  │                                             │         │                             │ │
│ └────────────┴──────────────┴───────────┴─────────────────────────────────────────────┴─────────┴─────────────────────────────┘ │
│   3 conflict(s):                                                                                                                │
│     SPANISH1-TUE-PM vs IMR on 2026-04-14 17:15-19:30                                                                            │
│     SPANISH1-TUE-PM vs IMR on 2026-05-12 17:15-19:30                                                                            │
│     3MKIB6-W105 vs 3MKIB6-W107 on 2026-07-02 11:30-13:00                                                                        │
│                                                                                                                                 │
│   6 nice-to-have(s) included; 5 filler(s) included; 3 internal conflict(s)                                                      │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭─────────────────────────────────────────────────────── #14  Score: 63.6 ────────────────────────────────────────────────────────╮
│ Closeness (avg gap)     43 min                                                                                                  │
│ Earliest start          08:00                                                                                                   │
│ Average day start       09:46                                                                                                   │
│ Latest end              19:30                                                                                                   │
│ Average day end         17:47                                                                                                   │
│ Free days/week          0 (Sunday)                                                                                              │
│                                                                                                                                 │
│ ┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│ ┃ Tier       ┃ Code         ┃ Name      ┃ Schedule                                    ┃ Lessons ┃ Teacher(s)                  ┃ │
│ ┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩ │
│ │ MUST       │ 3MKIB4-P42   │ Datenban… │ Tue 09:45-13:00                             │      15 │ Hertkorn                    │ │
│ │            │              │ 2         │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6--P74  │ BK:Bachl… │ Wed 15:30-18:45                             │      28 │ Martinez Madrid             │ │
│ │            │              │ Kolloqui… │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6-P65   │ Innovati… │ Mon,Wed 13:45-17:00 / 15:30-18:45           │      31 │ Hartmann, INF N.N., Tullius │ │
│ │            │              │ Lab       │                                             │         │                             │ │
│ │ MUST       │ 3MKIB7-P73   │ Aspekte   │ Fri 09:45-13:00 / 13:45-17:00 / 13:45-18:45 │       7 │ Gaiduk                      │ │
│ │            │              │ der       │                                             │         │                             │ │
│ │            │              │ Kommunik… │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-TU… │ Spanish 1 │ Tue 08:00-09:30                             │      15 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 1,        │                                             │         │                             │ │
│ │            │              │ Dienstag  │                                             │         │                             │ │
│ │            │              │ Morgen)   │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-TU… │ Spanish 1 │ Tue 17:15-19:30                             │      10 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 2,        │                                             │         │                             │ │
│ │            │              │ Dienstag  │                                             │         │                             │ │
│ │            │              │ Abend)    │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-THU │ Spanish 1 │ Thu 17:15-19:30                             │      17 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 4,        │                                             │         │                             │ │
│ │            │              │ Donnerst… │                                             │         │                             │ │
│ │            │              │ Abend)    │                                             │         │                             │ │
│ │ NICE       │ BTA          │ Einführu… │ Tue 13:45-17:00                             │      17 │                             │ │
│ │            │              │ in        │                                             │         │                             │ │
│ │            │              │ Blockcha… │                                             │         │                             │ │
│ │            │              │ Technolo… │                                             │         │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ Anwendun… │                                             │         │                             │ │
│ │ NICE       │ EC           │ E-Commer… │ Sat 08:00-13:00 / 13:45-17:00               │      10 │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ E-Busine… │                                             │         │                             │ │
│ │ NICE       │ IMR          │ Interakt… │ Tue,Wed 13:45-15:15 / 17:15-18:45           │       8 │                             │ │
│ │            │              │ mobile    │                                             │         │                             │ │
│ │            │              │ Roboter   │                                             │         │                             │ │
│ │ COULD FIT  │ 3MKIB6-W105  │ Computer… │ Thu 11:30-13:00 / 13:45-15:15               │      52 │ Kloos                       │ │
│ │ COULD FIT  │ 3MKIB6-W107  │ Audio     │ Wed,Thu 08:00-11:15 / 09:45-13:00           │      28 │ INF N.N.                    │ │
│ │ COULD FIT  │ 3MKIB7--P72  │ Psycholo… │ Mon 17:15-18:45                             │      15 │ Rupp                        │ │
│ │ COULD FIT  │ 3MKIB7--W215 │ Business  │ Mon,Fri 08:00-09:30                         │      28 │ Schlegel                    │ │
│ │            │              │ Consulti… │                                             │         │                             │ │
│ │ COULD FIT  │ 3WIB-2-P22   │ Digital   │ Mon 09:45-13:00                             │      30 │ Schmäh                      │ │
│ │            │              │ Marketing │                                             │         │                             │ │
│ │            │              │ and Sales │                                             │         │                             │ │
│ └────────────┴──────────────┴───────────┴─────────────────────────────────────────────┴─────────┴─────────────────────────────┘ │
│   3 conflict(s):                                                                                                                │
│     SPANISH1-TUE-PM vs IMR on 2026-04-14 17:15-19:30                                                                            │
│     SPANISH1-TUE-PM vs IMR on 2026-05-12 17:15-19:30                                                                            │
│     3MKIB6-W105 vs 3MKIB6-W107 on 2026-07-02 11:30-13:00                                                                        │
│                                                                                                                                 │
│   6 nice-to-have(s) included; 5 filler(s) included; 3 internal conflict(s)                                                      │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭─────────────────────────────────────────────────────── #15  Score: 63.5 ────────────────────────────────────────────────────────╮
│ Closeness (avg gap)     45 min                                                                                                  │
│ Earliest start          08:00                                                                                                   │
│ Average day start       09:46                                                                                                   │
│ Latest end              19:30                                                                                                   │
│ Average day end         17:32                                                                                                   │
│ Free days/week          0 (Sunday)                                                                                              │
│                                                                                                                                 │
│ ┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│ ┃ Tier       ┃ Code         ┃ Name      ┃ Schedule                                    ┃ Lessons ┃ Teacher(s)                  ┃ │
│ ┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩ │
│ │ MUST       │ 3MKIB4-P42   │ Datenban… │ Tue 09:45-13:00                             │      15 │ Hertkorn                    │ │
│ │            │              │ 2         │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6--P74  │ BK:Bachl… │ Wed 15:30-18:45                             │      28 │ Martinez Madrid             │ │
│ │            │              │ Kolloqui… │                                             │         │                             │ │
│ │ MUST       │ 3MKIB6-P65   │ Innovati… │ Mon,Wed 13:45-17:00 / 15:30-18:45           │      31 │ Hartmann, INF N.N., Tullius │ │
│ │            │              │ Lab       │                                             │         │                             │ │
│ │ MUST       │ 3MKIB7-P73   │ Aspekte   │ Fri 09:45-13:00 / 13:45-17:00 / 13:45-18:45 │       7 │ Gaiduk                      │ │
│ │            │              │ der       │                                             │         │                             │ │
│ │            │              │ Kommunik… │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-TU… │ Spanish 1 │ Tue 08:00-09:30                             │      15 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 1,        │                                             │         │                             │ │
│ │            │              │ Dienstag  │                                             │         │                             │ │
│ │            │              │ Morgen)   │                                             │         │                             │ │
│ │ NICE       │ SPANISH1-THU │ Spanish 1 │ Thu 17:15-19:30                             │      17 │                             │ │
│ │            │              │ Niveau    │                                             │         │                             │ │
│ │            │              │ A1.1      │                                             │         │                             │ │
│ │            │              │ (Gruppe   │                                             │         │                             │ │
│ │            │              │ 4,        │                                             │         │                             │ │
│ │            │              │ Donnerst… │                                             │         │                             │ │
│ │            │              │ Abend)    │                                             │         │                             │ │
│ │ NICE       │ BTA          │ Einführu… │ Tue 13:45-17:00                             │      17 │                             │ │
│ │            │              │ in        │                                             │         │                             │ │
│ │            │              │ Blockcha… │                                             │         │                             │ │
│ │            │              │ Technolo… │                                             │         │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ Anwendun… │                                             │         │                             │ │
│ │ NICE       │ EC           │ E-Commer… │ Sat 08:00-13:00 / 13:45-17:00               │      10 │                             │ │
│ │            │              │ und       │                                             │         │                             │ │
│ │            │              │ E-Busine… │                                             │         │                             │ │
│ │ NICE       │ IMR          │ Interakt… │ Tue,Wed 13:45-15:15 / 17:15-18:45           │       8 │                             │ │
│ │            │              │ mobile    │                                             │         │                             │ │
│ │            │              │ Roboter   │                                             │         │                             │ │
│ │ COULD FIT  │ 3MKIB6-W105  │ Computer… │ Thu 11:30-13:00 / 13:45-15:15               │      52 │ Kloos                       │ │
│ │ COULD FIT  │ 3MKIB6-W107  │ Audio     │ Wed,Thu 08:00-11:15 / 09:45-13:00           │      28 │ INF N.N.                    │ │
│ │ COULD FIT  │ 3MKIB7--P72  │ Psycholo… │ Mon 17:15-18:45                             │      15 │ Rupp                        │ │
│ │ COULD FIT  │ 3MKIB7--W215 │ Business  │ Mon,Fri 08:00-09:30                         │      28 │ Schlegel                    │ │
│ │            │              │ Consulti… │                                             │         │                             │ │
│ │ COULD FIT  │ 3MKIB7-W229  │ Developm… │ Mon 09:45-13:00                             │      30 │                             │ │
│ │            │              │ of Smart  │                                             │         │                             │ │
│ │            │              │ Textiles  │                                             │         │                             │ │
│ └────────────┴──────────────┴───────────┴─────────────────────────────────────────────┴─────────┴─────────────────────────────┘ │
│   1 conflict(s):                                                                                                                │
│     3MKIB6-W105 vs 3MKIB6-W107 on 2026-07-02 11:30-13:00                                                                        │
│                                                                                                                                 │
│   5 nice-to-have(s) included; 5 filler(s) included; 1 internal conflict(s)                                                      │
╰───────────────────────────────────────────────────────────────────────────────────────────