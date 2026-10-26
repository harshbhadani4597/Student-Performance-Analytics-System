"""
main.py
Student Performance Analytics System
Runs the full analysis and prints the results.
"""

import pandas as pd
import functions as fn

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 20)


def heading(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def main():
    # ---- Step 2: Read the data ----
    df = fn.load_data("students.csv")

    heading("1. DATASET OVERVIEW")
    print(f"Number of records : {df.shape[0]}")
    print(f"Number of columns : {df.shape[1]}")
    print(f"Columns           : {list(df.columns)}")
    print("\nFirst 5 records:")
    print(df.head())
    print("\nMissing values per column:")
    print(df.isnull().sum().to_string())

    # ---- Step 3: Process the data ----
    df = fn.calculate_total_and_average(df)
    df = fn.assign_grades(df)
    df = fn.assign_pass_fail(df)

    heading("2. STUDENT RESULTS (Total, Average, Grade, Result)")
    print(df[["Student_ID", "Name", "Department", "Total", "Average", "Grade", "Result"]]
          .to_string(index=False))

    # ---- Step 4: Analysis ----
    stats = fn.class_statistics(df)
    heading("3. CLASS PERFORMANCE")
    print(f"Highest average : {stats['highest_avg']}  ({stats['highest_student']})")
    print(f"Lowest average  : {stats['lowest_avg']}  ({stats['lowest_student']})")
    print(f"Class average   : {stats['class_avg']}")
    print(f"Median average  : {stats['median_avg']}")
    print(f"Std deviation   : {stats['std_dev']}")

    pf = fn.pass_fail_statistics(df)
    heading("4. PASS / FAIL STATISTICS")
    print(f"Total students  : {pf['total']}")
    print(f"Passed          : {pf['passed']}")
    print(f"Failed          : {pf['failed']}")
    print(f"Pass percentage : {pf['pass_percentage']}%")
    print(f"\n(Pass rule: at least {fn.PASS_MARK} marks in every subject)")
    print("\nFailed students:")
    print(df[df["Result"] == "Fail"][["Student_ID", "Name", "Average"]].to_string(index=False))

    heading("5. GRADE DISTRIBUTION")
    print(fn.grade_distribution(df).to_string())

    subj = fn.subject_analysis(df)
    heading("6. SUBJECT-WISE ANALYSIS (sorted by average)")
    print(subj.to_string(index=False))
    print(f"\nBest subject  : {subj.iloc[0]['Subject']} (avg {subj.iloc[0]['Average']})")
    print(f"Weakest subject: {subj.iloc[-1]['Subject']} (avg {subj.iloc[-1]['Average']})")

    heading("7. TOP 5 PERFORMING STUDENTS")
    print(fn.top_performers(df, 5).to_string(index=False))

    heading("8. DEPARTMENT-WISE ANALYSIS")
    print(fn.department_analysis(df).to_string())

    heading("9. LOW ATTENDANCE ALERT (below %d%%)" % fn.MIN_ATTENDANCE)
    print(fn.low_attendance_students(df).to_string(index=False))

    # ---- Step 5: Save final output ----
    df.to_csv("results.csv", index=False)
    heading("DONE")
    print("Full results saved to results.csv")


if __name__ == "__main__":
    main()
