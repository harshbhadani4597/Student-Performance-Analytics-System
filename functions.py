"""
functions.py
Reusable calculation/processing functions for the
Student Performance Analytics System.
"""

import numpy as np
import pandas as pd

# ---------------- Configuration ----------------
SUBJECTS = ["Maths", "Physics", "Chemistry", "English", "Computer"]
PASS_MARK = 40            # minimum marks needed in EVERY subject
MIN_ATTENDANCE = 75       # attendance % below this is flagged as shortage

# Grading rule (based on average marks):
#   90+ -> A+ | 80-89 -> A | 70-79 -> B | 60-69 -> C | 50-59 -> D | 40-49 -> E | <40 -> F
GRADE_RULES = [(90, "A+"), (80, "A"), (70, "B"), (60, "C"), (50, "D"), (40, "E")]


def load_data(file_path):
    """Read the student CSV file into a Pandas DataFrame."""
    return pd.read_csv(file_path)


def calculate_total_and_average(df, subjects=SUBJECTS):
    """Add Total and Average columns using NumPy (row-wise)."""
    marks = df[subjects].to_numpy()               # DataFrame -> NumPy array
    df["Total"] = np.sum(marks, axis=1)           # total per student
    df["Average"] = np.round(np.mean(marks, axis=1), 2)
    return df


def get_grade(average):
    """Return the grade for a given average using GRADE_RULES."""
    for cutoff, grade in GRADE_RULES:
        if average >= cutoff:
            return grade
    return "F"


def assign_grades(df):
    """Loop through every student and assign a grade."""
    grades = []
    for avg in df["Average"]:
        grades.append(get_grade(avg))
    df["Grade"] = grades
    return df


def get_result(marks):
    """Pass only if the student scored >= PASS_MARK in every subject."""
    return "Pass" if np.all(np.array(marks) >= PASS_MARK) else "Fail"


def assign_pass_fail(df, subjects=SUBJECTS):
    """Loop through rows and set the Result column."""
    results = []
    for _, row in df.iterrows():
        results.append(get_result(row[subjects].to_numpy(dtype=float)))
    df["Result"] = results
    return df


def class_statistics(df):
    """Highest, lowest and average performance of the whole class."""
    avg = df["Average"].to_numpy()
    return {
        "highest_avg": float(np.max(avg)),
        "highest_student": df.loc[df["Average"].idxmax(), "Name"],
        "lowest_avg": float(np.min(avg)),
        "lowest_student": df.loc[df["Average"].idxmin(), "Name"],
        "class_avg": round(float(np.mean(avg)), 2),
        "median_avg": round(float(np.median(avg)), 2),
        "std_dev": round(float(np.std(avg)), 2),
    }


def pass_fail_statistics(df):
    """Count of passed/failed students and pass percentage."""
    total = len(df)
    passed = int((df["Result"] == "Pass").sum())
    failed = total - passed
    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "pass_percentage": round(passed / total * 100, 2),
    }


def subject_analysis(df, subjects=SUBJECTS):
    """Subject-wise average, highest, lowest, std-dev and pass count."""
    rows = []
    for subject in subjects:
        scores = df[subject].to_numpy()
        rows.append({
            "Subject": subject,
            "Average": round(float(np.mean(scores)), 2),
            "Highest": int(np.max(scores)),
            "Lowest": int(np.min(scores)),
            "Std_Dev": round(float(np.std(scores)), 2),
            "Passed": int(np.sum(scores >= PASS_MARK)),
        })
    return pd.DataFrame(rows).sort_values("Average", ascending=False).reset_index(drop=True)


def top_performers(df, n=5):
    """Return the top-n students ranked by average marks."""
    top = df.sort_values("Average", ascending=False).head(n).copy()
    top.insert(0, "Rank", range(1, len(top) + 1))
    return top[["Rank", "Student_ID", "Name", "Department", "Total", "Average", "Grade"]]


def grade_distribution(df):
    """Number of students in each grade."""
    order = ["A+", "A", "B", "C", "D", "E", "F"]
    counts = df["Grade"].value_counts()
    return counts.reindex(order, fill_value=0)


def department_analysis(df):
    """Department-wise average, student count and pass count."""
    summary = df.groupby("Department").agg(
        Students=("Student_ID", "count"),
        Avg_Marks=("Average", "mean"),
        Avg_Attendance=("Attendance", "mean"),
        Passed=("Result", lambda r: (r == "Pass").sum()),
    ).round(2)
    return summary.sort_values("Avg_Marks", ascending=False)


def low_attendance_students(df):
    """Students whose attendance is below MIN_ATTENDANCE."""
    return df[df["Attendance"] < MIN_ATTENDANCE][["Student_ID", "Name", "Attendance"]]
