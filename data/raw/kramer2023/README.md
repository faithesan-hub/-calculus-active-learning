---
editor_options:
  markdown:
    wrap: 70
---

# Anonymized Dataset Accompanying the Paper 'Establishing a New Standard of Care for Calculus Using Trials with Randomized Student Allocation'

----------------------------------------------------------------------

Data contained in this archive were collected from an NSF funded study
carried out as a large-scale pragmatic trial that randomly allocated
students to the treatment and control conditions to establish a new
standard of care for calculus instruction. The treatment group used
the Modeling Practices of Calculus (MPC) pedagogy and curriculum with
the control group employed pre-existing instructional practices
(primarily traditional lecture). Identical end-of-semester learning
measures were used to rigorously assess student learning outcomes in
the two conditions in the trial. Sets of open answer, learning measure
questions were collectively developed and embedded as part of the
identical end-of-semester learning measures given each semester to the
treatment and control sections in the MPC Calculus 1 trials in order
to assess end-of-course student learning in each of the groups.

A total of 1,019 students were randomly assigned to either an active
learning based curriculum in calculus or a traditional lecture-based
approach. 516 students were assigned to the treatment group and 417
remained that in turn provided 373 outcome data points while 503
students were assigned to the control group and 394 remained in the
treatment section at the drop/add deadline in the control condition
providing 310 data points for analysis.

Each data point contains an instance of student allocation in the
study including the demographic data collected, indicators of study
arm assignment, and outcome data.

## Description of the data and file structure

The file anonymizedarchive.csv contains 1019 rows of data with 20
columns. The columns are described in the codebook files and listed
below. Fields marked with [I] are sourced from institutionally
collected data. Fields marked with [P] were collected during the
project from study related activities.

| Field           | Description                                                                                                                                     |
|----------------------|------------------------------------------------|
| studyID         | [P] Anonymized Study Tracking ID                                                                                                                |
| Treatment       | [P] Trial Assignment Group TR=Treatment, CN=Control                                                                                             |
| TrialStatus     | [P] Status in Trial after assignment                                                                                                            |
| LearningMeasure | [P] End of Term Learning Outcome Measure Scaled to 0 to 100                                                                                     |
| Grade           | [I] Course Grade assigned from grade report on the letter grade scale A, B, C, D, and F with + or -. DR=student dropped course, OF=other failing grade outcomes including imcompletes and no credit awarded, NA=no grade was awarded                                                                                                    |
| MBS             | [I] Average of SAT/ACT/HSGPA/MPS scaled to 0 to 100                                                                                             |
| Gender          | [I] Student Gender                                                                                                                              |
| RaEth           | [I] Race or Ethnicity of Student as Descriptive Text                                                                                            |
| RE              | [I] Race or Ethnicity of Student recoded as numeric in single column form                                                                       |
| TIDw            | [I] Teacher ID with Repetitions                                                                                                                 |
| Section         | [I] Trial Course Section of Student Assignment numbered 1 to 32                                                                                                                    |
| SecPair         | [I] Trial Group for Time of Day/Day of Week for Initial Student Registration numbered 1 to 16                                                                                             |
| REBlack         | [I] 1 if student identified to Institution as Black or African American, 0 if not                                                               |
| REHispanic      | [I] 1 if student identified to Institution as Hispanic or Latino/Latina, 0 if not                                                               |
| REAAPI          | [I] 1 if student identified to Institution as Asian American or Pacific Islander, 0 if not                                                      |
| REWhite         | [I] 1 if student identified to Institution as White, 0 if not                                                                                   |
| Cohort          | [I] Either FTiC (First Time in College), Transfer or No Cohort                                                                                  |
| MajorGrp        | [I] Grouped Major Categories ECS=Engingeering and Computer Science, OMS=Other Math and Science, BIO=Biology Related, Other=Any other major code |

Grade includes the letter grade outcome for the student if they persisted in the assigned section of the course on the usual A,B,C,D, or F scale with + or - possible for A, B, and C. DR indicates that the student dropped the course after the initial drop/add period and so recieved an outcome. Other modes of failure are represented by OF and include incompletes and other academic outcomes that might be unrelated to course performance (e.g. no credit assigned for administrative reasons). NA indicates no grade outcome exists and that the student was lost from trial allocation.

Section is a numeric representation from 1 to 32 of the section assigned to the student by the trial. It is not the section number used for enrollment records but corresponds to one.

SecPair is the original section group (time of day/days of week) selected by the student during registration prior to random allocation numbered 1 to 16. It is not a section number used for registration, but it corresponds to one prior to the random allocation.

RaEth and RE represent a single column, single membership record of
race and ethnicity maintained in institutional records for single
column analysis. REBlack, REHispanic, REAAPI and REWhite are columns
that encode the possibly multi-membership race or ethnicity
information maintained in institutional records.

MajorGrp fields contain the following majors from student declared
institutional data in each coded group.

| Code  | Majors                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|--------------------|--------------------------------------------------|
| ECS   | Environmental Engineering - BS, Computer Science - BS, Computer Science - BA, Computer Engineering - BS, Mechanical Engineering - BS, Engineering - BS, Civil Engineering - BS, Biomedical Engineering - BS                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| OMS   | Chemistry - BA, Chemistry - BS, Geosciences - BS, Mathematical Sciences - BS, Physics - BS                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| BIO   | Marine Biology - BS, Biological Sciences - BA, Biological Sciences - BS                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| Other | Accounting - BAcc, Art - BFA, Biochemistry - BS, Construction Mgt - BS, Dietetics and Nutrition - BS, Dual Enrollment - Full Time, Economics - BA, English - BA, Environmental Studies - BS, Exp-Admin & Management, Exp-Biological/Enviro Science, Exp-Global & Social Sciences, Exp-Health Sciences, Exp-Humanities & Arts, Exp-Physical Sci/Engineer, Finance - BBA, Global First Year Three, Hospitality Management - BS, Interdisciplinary Studies - BA, International Business - BBA, International Relations - BA, Internet of Things - BS, Liberal Studies - BA, Management - BBA, National Student Exchange A, Non-Degree Seeking Student, Philosophy - BA, Political Science - BA, Psychology - BA, Pub Relatns Adv & App Com- BS, Recreation Sport Mgt - BS, Sociology/Anthropology - BA, Transient Student |

## Sharing/Access information

Data was derived from the following sources: \* FIU institutional data
[I] \* data collected during the project [P]. Data may be used for
research purposes only.

## Code/Software

The data are ready for importation and analysis in R and the results
from the associated paper can be obtained using the packages available
for R as described in the paper and supplemental materials.
