# Codebook: data/processed/students.csv

*Plain-language note: this lists every column in the cleaned table, what it means, and where it came from. One row is one student who was randomly placed in a section. You only need this if you open the spreadsheet. Original column names are in parentheses; their definitions are in data/raw/kramer2023/README.md.*

| Column | Meaning | Source and transformation |
|---|---|---|
| row | Row number in the original file; use it to match rows | `Row`, unchanged |
| study_id | Anonymized student ID | `studyID`, unchanged |
| arm | "Active (MPC)" or "Lecture" | `Treatment`: TR → Active (MPC), CN → Lecture |
| active | 1 = active learning, 0 = lecture | from `Treatment` |
| trial_status | Completer, Departer, Switcher-SameDT, Switcher-DiffDT | `TrialStatus`, unchanged |
| stayed | 1 if still in the assigned section after drop/add | 1 when `TrialStatus` = Completer |
| section | Trial section, 1 to 32 (blank if never recorded) | `Section` |
| slot | Registration time slot, 1 to 16; the randomization block | `SecPair` |
| teacher | Anonymized instructor ID (C = lecture, T = active) | `TIDw` |
| grade | Letter grade; DR = dropped after drop/add; OF = other no-credit; blank = no grade | `Grade`, unchanged |
| learning_measure | Common end-of-term learning measure, 0 to 100 | `LearningMeasure`, unchanged |
| prior_prep | Average of SAT/ACT, high school GPA, and placement score, 0 to 100 | `MBS`, unchanged |
| female | 1 = F, 0 = M, blank = not recorded | `Gender` |
| hispanic | 1 if identified as Hispanic or Latino/a | `REHispanic` |
| black | 1 if identified as Black or African American | `REBlack` |
| first_time_college | 1 = first time in college; 0 = transfer or no cohort | `Cohort` |
| major_group | ECS, OSM, BIO, Other (see original README) | `MajorGrp` |
| pass_c_or_better | 1 if grade is A, A-, B+, B, B-, C+, or C; 0 if D, F, DR, or OF; blank if no grade | derived from `grade` |
| dfw | 1 if grade is D, F, DR, or OF | derived from `grade` |
| prior_prep_group | Lower, middle, or upper third of prior_prep across all students | derived from `prior_prep` |
