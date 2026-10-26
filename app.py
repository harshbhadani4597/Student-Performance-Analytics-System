"""
app.py
Streamlit web app for the Student Performance Analytics System.
Reuses the functions from functions.py, so the logic stays the same
as the console version (main.py).

Run locally:  streamlit run app.py
"""

import pandas as pd
import streamlit as st

import functions as fn

st.set_page_config(page_title="Student Performance Analytics", page_icon="📊", layout="wide")

st.title("📊 Student Performance Analytics System")
st.caption("Python · NumPy · Pandas | EWB Courses – Python with AI")


@st.cache_data
def load_and_process(source):
    """Load the CSV (path or uploaded file) and calculate all metrics."""
    df = pd.read_csv(source)
    df = fn.calculate_total_and_average(df)
    df = fn.assign_grades(df)
    df = fn.assign_pass_fail(df)
    return df


# ---------------- Sidebar ----------------
st.sidebar.header("Data")
uploaded = st.sidebar.file_uploader("Upload your own students CSV (optional)", type="csv")
st.sidebar.caption(
    "Required columns: Student_ID, Name, Department, "
    + ", ".join(fn.SUBJECTS) + ", Attendance"
)

try:
    df = load_and_process(uploaded if uploaded is not None else "students.csv")
except Exception as error:  # e.g. wrong columns in an uploaded file
    st.error(f"Could not process the file: {error}")
    st.stop()

st.sidebar.header("Grading & Pass Rules")
st.sidebar.markdown(
    f"""
- **Pass:** at least **{fn.PASS_MARK}** in every subject
- **Attendance shortage:** below **{fn.MIN_ATTENDANCE}%**
- **Grades (by average):** A+ ≥ 90, A ≥ 80, B ≥ 70, C ≥ 60, D ≥ 50, E ≥ 40, else F
"""
)

st.sidebar.header("Filter")
departments = sorted(df["Department"].unique())
selected = st.sidebar.multiselect("Department", departments, default=departments)
view = df[df["Department"].isin(selected)]

if view.empty:
    st.warning("Select at least one department in the sidebar.")
    st.stop()

# ---------------- Key numbers ----------------
stats = fn.class_statistics(view)
pf = fn.pass_fail_statistics(view)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Students", pf["total"])
c2.metric("Class Average", stats["class_avg"])
c3.metric("Passed", f"{pf['passed']} / {pf['total']}")
c4.metric("Pass %", f"{pf['pass_percentage']}%")
c5.metric("Highest Average", stats["highest_avg"], stats["highest_student"], delta_color="off")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📋 Student Results", "🏆 Top Performers", "📚 Subject Analysis", "🏫 Department & Grades", "⚠️ Alerts"]
)

# ---------------- Tab 1: all results ----------------
with tab1:
    st.subheader("Student results")
    search = st.text_input("Search by name or ID")
    table = view
    if search:
        mask = view["Name"].str.contains(search, case=False) | view["Student_ID"].str.contains(search, case=False)
        table = view[mask]
    st.dataframe(
        table[["Student_ID", "Name", "Department", *fn.SUBJECTS, "Total", "Average", "Grade", "Result", "Attendance"]],
        width="stretch",
        hide_index=True,
    )
    st.download_button(
        "Download results as CSV",
        view.to_csv(index=False).encode("utf-8"),
        file_name="results.csv",
        mime="text/csv",
    )

# ---------------- Tab 2: top performers ----------------
with tab2:
    st.subheader("Top performing students")
    n = st.slider("How many students?", 3, min(10, len(view)) if len(view) > 3 else 3, min(5, len(view)))
    top = fn.top_performers(view, n)
    st.dataframe(top, width="stretch", hide_index=True)
    st.bar_chart(top.set_index("Name")["Average"])

    st.markdown(
        f"**Highest:** {stats['highest_student']} ({stats['highest_avg']})  \n"
        f"**Lowest:** {stats['lowest_student']} ({stats['lowest_avg']})  \n"
        f"**Median:** {stats['median_avg']} · **Std deviation:** {stats['std_dev']}"
    )

# ---------------- Tab 3: subject analysis ----------------
with tab3:
    st.subheader("Subject-wise performance")
    subj = fn.subject_analysis(view)
    st.dataframe(subj, width="stretch", hide_index=True)
    st.bar_chart(subj.set_index("Subject")["Average"])
    st.success(f"Best subject: **{subj.iloc[0]['Subject']}** (average {subj.iloc[0]['Average']})")
    st.info(f"Weakest subject: **{subj.iloc[-1]['Subject']}** (average {subj.iloc[-1]['Average']})")

# ---------------- Tab 4: departments and grades ----------------
with tab4:
    left, right = st.columns(2)
    with left:
        st.subheader("Department-wise analysis")
        st.dataframe(fn.department_analysis(view), width="stretch")
    with right:
        st.subheader("Grade distribution")
        st.bar_chart(fn.grade_distribution(view))

# ---------------- Tab 5: alerts ----------------
with tab5:
    st.subheader("Failed students")
    failed = view[view["Result"] == "Fail"][["Student_ID", "Name", "Department", "Average"]]
    if failed.empty:
        st.success("No failed students 🎉")
    else:
        st.dataframe(failed, width="stretch", hide_index=True)

    st.subheader(f"Low attendance (below {fn.MIN_ATTENDANCE}%)")
    low = fn.low_attendance_students(view)
    if low.empty:
        st.success("No attendance shortage 🎉")
    else:
        st.dataframe(low, width="stretch", hide_index=True)

st.divider()
st.caption("Built with Python, NumPy, Pandas and Streamlit.")
