# Student Performance Analytics System

A Python data-analysis project built with NumPy and Pandas for the **EWB Courses – Python with AI** program.

---

## 1. Project Title

**Student Performance Analytics System**

| Field | Details |
|---|---|
| Student Name | Harsh Kumar Bhadani |
| Student ID / Batch | _[Your ID / Batch]_ |
| Course | Python with AI – EWB Courses |
| Email | jeebitsat4597@gmail.com |

---

## 2. Objective

Schools and colleges hold large amounts of student marks, but reading raw numbers one by one makes it hard to see who is performing well, which subjects are weak, and who needs help.

This project reads student records from a CSV file and automatically:

- calculates total and average marks for every student,
- assigns grades using a clear grading rule,
- decides pass/fail using a clear condition,
- finds the highest, lowest and average performance,
- analyses each subject and each department,
- identifies top performers and students with low attendance.

The output is a readable report that can be understood without opening the code.

---

## 3. Technologies Used

| Tool | Purpose |
|---|---|
| Python 3 | Core language (variables, data types, loops, functions, conditions) |
| NumPy | Numerical calculations (sum, mean, max, min, median, std-dev, comparisons) |
| Pandas | Loading the CSV, DataFrame handling, filtering, sorting, groupby |
| Streamlit | Interactive web app version of the project |
| Git & GitHub | Version control and submission |

No machine learning is used, as per the assignment instructions.

---

## 4. Dataset Description

File: `students.csv` — **20 student records**, 9 columns.

| Column | Description |
|---|---|
| Student_ID | Unique ID (S101 – S120) |
| Name | Student name |
| Department | Computer Science, Electronics, Civil or Mechanical |
| Maths, Physics, Chemistry, English, Computer | Marks out of 100 for each subject |
| Attendance | Attendance percentage |

The dataset is realistic and mixed: it contains high scorers, average students, students who fail a subject, and students with low attendance. There are no missing values.

---

## 5. Implementation

### Rules used

**Grading rule (based on average marks)**

| Average | Grade |
|---|---|
| 90 and above | A+ |
| 80 – 89.99 | A |
| 70 – 79.99 | B |
| 60 – 69.99 | C |
| 50 – 59.99 | D |
| 40 – 49.99 | E |
| Below 40 | F |

**Pass / Fail condition:** a student passes only if they score **at least 40 in every subject**. Scoring below 40 in even one subject means Fail.

**Attendance shortage:** attendance below 75% is flagged.

### Step by step

1. **Load data** – `load_data()` uses `pd.read_csv()` to create a DataFrame. `main.py` shows the record count, columns, first rows and missing values.
2. **Totals and averages** – `calculate_total_and_average()` converts the subject columns to a NumPy array and uses `np.sum(axis=1)` and `np.mean(axis=1)`.
3. **Grades** – `assign_grades()` loops over every average and calls `get_grade()`, which checks the grading rule.
4. **Pass / Fail** – `assign_pass_fail()` loops over each row and `get_result()` uses `np.all(marks >= 40)`.
5. **Class statistics** – `class_statistics()` uses `np.max`, `np.min`, `np.mean`, `np.median`, `np.std`.
6. **Subject-wise analysis** – `subject_analysis()` loops through the subjects and computes average, highest, lowest, standard deviation and number passed.
7. **Top performers** – `top_performers()` sorts by average and returns the top *n* students with a rank.
8. **Extra analysis** – grade distribution, department-wise summary (`groupby`), and low-attendance alert.
9. **Save output** – the full processed table is saved to `results.csv`.

### Project structure

```
student-performance-analytics/
├── main.py                    # Runs the project and prints the analysis
├── app.py                     # Streamlit web app (live version)
├── functions.py               # Reusable calculation/processing functions
├── students.csv               # Dataset (20 records)
├── results.csv                # Generated output with Total, Average, Grade, Result
├── output.txt                 # Saved console output of the program
├── requirements.txt           # numpy, pandas, streamlit
├── README.md                  # Project documentation
└── Project_Documentation.md   # Same documentation (as suggested in the assignment)
```

### How to run

```bash
pip install -r requirements.txt
python main.py
```

---

## 6. Key Features

| Function (in `functions.py`) | What it does |
|---|---|
| `load_data()` | Reads the CSV into a DataFrame |
| `calculate_total_and_average()` | Total and average marks per student (NumPy) |
| `get_grade()` / `assign_grades()` | Grade from average marks (loop) |
| `get_result()` / `assign_pass_fail()` | Pass/Fail by the 40-mark rule (loop) |
| `class_statistics()` | Highest, lowest, class average, median, std-dev |
| `pass_fail_statistics()` | Passed, failed, pass percentage |
| `subject_analysis()` | Subject-wise performance table |
| `top_performers()` | Top-ranked students |
| `grade_distribution()` | Number of students per grade |
| `department_analysis()` | Department-wise averages and pass count |
| `low_attendance_students()` | Students below 75% attendance |

---

## 7. Output / Screenshots

Full program output is saved in `output.txt`. Key results:

**Class performance**

```
Highest average : 94.4  (Neha Gupta)
Lowest average  : 45.8  (Vikram Yadav)
Class average   : 69.73
Median average  : 71.7
```

**Pass / Fail**

```
Total students  : 20
Passed          : 18
Failed          : 2   (Vikram Yadav, Arjun Prasad)
Pass percentage : 90.0%
```

**Subject-wise analysis**

```
  Subject  Average  Highest  Lowest  Std_Dev  Passed
  English    73.45       92      52    12.42      20
 Computer    71.60       97      41    17.02      20
  Physics    68.75       95      42    16.30      20
    Maths    67.60       98      34    17.85      18
Chemistry    67.25       92      40    15.07      20
```

**Top 5 students**

```
 Rank Student_ID         Name       Department  Total  Average Grade
    1       S106   Neha Gupta Computer Science    472     94.4    A+
    2       S114   Ishita Das Computer Science    444     88.8     A
    3       S101 Aarav Sharma Computer Science    438     87.6     A
    4       S104  Sneha Singh      Electronics    436     87.2     A
    5       S120  Tanvi Joshi            Civil    434     86.8     A
```

> _Optional: add screenshots of your terminal output in a `screenshots/` folder and link them here, e.g. `![Output](screenshots/output.png)`._

---

## 8. Final Outcome

The project successfully reads the student dataset and produces a complete performance report. It answers the practical questions from the assignment:

- **Highest average:** Neha Gupta (94.4)
- **Best subject:** English (average 73.45); weakest subject: Chemistry (67.25)
- **Students passed:** 18 out of 20 (90%)
- **Overall class average:** 69.73

Extra findings: Computer Science is the best-performing department (average 85.07), while Mechanical is the lowest (53.30). All four students with attendance below 75% are also among the weaker performers, which suggests attendance and marks are linked in this dataset.

The program uses functions, loops, conditions, NumPy and Pandas as required, runs without errors, and writes the final table to `results.csv`.

---

## Live Web App (Streamlit)

The project also includes an interactive web version, `app.py`, which reuses the same functions from `functions.py`.

**Features:** key metrics, searchable student table with CSV download, top performers with chart, subject-wise analysis, department and grade distribution, failed-student and low-attendance alerts, department filter, and optional upload of your own CSV.

**Run locally:**

```bash
pip install -r requirements.txt
streamlit run app.py
```

**Live link:** _[Paste your Streamlit app link here]_

---

## 9. Challenges & Learning

| Challenge | How it was solved |
|---|---|
| Deciding a fair pass rule — average alone could let a student pass despite failing a subject | Used "at least 40 in every subject" with `np.all()`. This is why Vikram Yadav fails even though his average (45.8) is above 40. |
| Keeping the code readable | Split reusable logic into `functions.py` and kept `main.py` only for printing. |
| Using NumPy and Pandas together | Converted DataFrame columns to arrays with `.to_numpy()` for calculations and stored results back as new columns. |
| Making the output understandable without the code | Added numbered section headings and clear labels in `main.py`. |

**What I learned:** DataFrame handling, row-wise NumPy operations with `axis=1`, writing reusable functions, using `groupby` for summaries, and organising and documenting a project for GitHub.

---

## 10. GitHub Repository

🔗 https://github.com/harshbhadani4597/Student-Performance-Analytics-System
