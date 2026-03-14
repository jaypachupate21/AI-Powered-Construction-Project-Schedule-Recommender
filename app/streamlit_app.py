import os
import sys
import pandas as pd
import streamlit as st

import plotly.express as px
from datetime import datetime, timedelta


def build_gantt_df(schedule_json, project_start=None):
    if project_start is None:
        project_start = datetime.today().date()

    if not schedule_json:
        return pd.DataFrame()

    task_map = {}
    rows = []

    # first pass: sequential fallback
    current_start = project_start

    for item in schedule_json:
        task = str(item.get("task", "Unknown Task"))
        phase = str(item.get("phase", "Unknown Phase"))
        duration = item.get("duration_days", 1)
        predecessor = item.get("predecessor")

        try:
            duration = int(float(duration))
        except Exception:
            duration = 1

        if duration <= 0:
            duration = 1

        start_date = current_start

        # if predecessor exists and is already scheduled, start after it ends
        if predecessor and predecessor in task_map:
            start_date = task_map[predecessor]["finish_date"] + timedelta(days=1)

        finish_date = start_date + timedelta(days=duration - 1)

        row = {
            "Phase": phase,
            "Task": task,
            "Start": pd.to_datetime(start_date),
            "Finish": pd.to_datetime(finish_date),
            "DurationDays": duration,
            "Predecessor": predecessor,
        }

        rows.append(row)
        task_map[task] = {
            "start_date": start_date,
            "finish_date": finish_date,
        }

        current_start = finish_date + timedelta(days=1)

    return pd.DataFrame(rows)


def plot_gantt_chart(gantt_df):
    if gantt_df.empty:
        return None

    fig = px.timeline(
        gantt_df,
        x_start="Start",
        x_end="Finish",
        y="Task",
        color="Phase",
        hover_data=["Phase", "DurationDays", "Predecessor"],
        title="Recommended Project Schedule Gantt Chart"
    )

    fig.update_yaxes(autorange="reversed")
    fig.update_layout(height=600)
    return fig

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.preprocess import load_data, clean_metadata, clean_schedule
from src.similarity import build_similarity_model, find_similar_projects
from src.retrieval import retrieve_schedules, summarize_schedule
from src.prompt_builder import build_prompt
from src.llm_generator import generate_schedule

st.set_page_config(page_title="Construction Schedule Recommender", layout="wide")
st.title("Construction Schedule Recommender")

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
META_PATH = os.path.join(PROJECT_ROOT, "data", "Project_JOB_meta_data.csv")
SCHEDULE_PATH = os.path.join(PROJECT_ROOT, "data", "Project_Schedule_Data.csv")

@st.cache_data
def get_data():
    meta_df, schedule_df = load_data(META_PATH, SCHEDULE_PATH)
    meta_df = clean_metadata(meta_df)
    schedule_df = clean_schedule(schedule_df)
    return meta_df, schedule_df

meta_df, schedule_df = get_data()

st.subheader("Data Preview")
with st.expander("Metadata columns"):
    st.write(meta_df.columns.tolist())
with st.expander("Schedule columns"):
    st.write(schedule_df.columns.tolist())

required_meta_cols = [
    "control_job_no",
    "region_name",
    "business_unit",
    "office_name",
    "city",
    "state",
    "core_market",
    "market_sector",
    "project_type",
    "total_control_estimate",
    "building_size",
]

required_schedule_cols = [
    "main_projectid",
    "parwbsname",
    "wbsname",
    "plannedstartdate",
    "plannedfinishdate",
]

missing_meta = [c for c in required_meta_cols if c not in meta_df.columns]
missing_schedule = [c for c in required_schedule_cols if c not in schedule_df.columns]

if missing_meta:
    st.error(f"Missing metadata columns: {missing_meta}")
    st.stop()

if missing_schedule:
    st.error(f"Missing schedule columns: {missing_schedule}")
    st.stop()

pipeline, matrix = build_similarity_model(meta_df)

st.sidebar.header("New Project Input")

new_project = {
    "region_name": st.sidebar.text_input("Region Name", "Southwest"),
    "business_unit": st.sidebar.text_input("Business Unit", "Construction"),
    "office_name": st.sidebar.text_input("Office Name", "Phoenix"),
    "city": st.sidebar.text_input("City", "Phoenix"),
    "state": st.sidebar.text_input("State", "AZ"),
    "core_market": st.sidebar.text_input("Core Market", "Commercial"),
    "market_sector": st.sidebar.text_input("Market Sector", "Office"),
    "project_type": st.sidebar.text_input("Project Type", "New Build"),
    "total_control_estimate": st.sidebar.number_input("Total Control Estimate", min_value=0.0, value=20000000.0, step=100000.0),
    "building_size": st.sidebar.number_input("Building Size", min_value=0.0, value=80000.0, step=1000.0),
}

top_k = st.sidebar.slider("Top similar projects", min_value=1, max_value=10, value=5)

if st.button("Generate Recommended Schedule"):
    try:
        similar_df = find_similar_projects(new_project, meta_df.copy(), pipeline, matrix, top_k=top_k)

        st.subheader("Top Similar Projects")
        st.dataframe(similar_df, use_container_width=True)

        project_ids = similar_df["control_job_no"].tolist()

        schedules = retrieve_schedules(
            schedule_df=schedule_df,
            project_ids=project_ids,
            project_id_col="main_projectid"
        )

        if schedules.empty:
            st.warning("No matching schedules found for similar projects.")
            st.stop()

        schedules["plannedstartdate"] = pd.to_datetime(schedules["plannedstartdate"], errors="coerce")
        schedules["plannedfinishdate"] = pd.to_datetime(schedules["plannedfinishdate"], errors="coerce")
        schedules["duration_days"] = (
            schedules["plannedfinishdate"] - schedules["plannedstartdate"]
        ).dt.days

        schedules = schedules.dropna(subset=["wbsname"])
        schedules = schedules[schedules["wbsname"].astype(str).str.strip() != ""]

        st.subheader("Retrieved Historical Schedule Rows")
        st.dataframe(
            schedules[["main_projectid", "parwbsname", "wbsname", "plannedstartdate", "plannedfinishdate", "duration_days"]],
            use_container_width=True
        )

        summary = summarize_schedule(schedules)

        st.subheader("Schedule Summary")
        st.dataframe(summary, use_container_width=True)

        prompt = build_prompt(new_project, similar_df, summary)

        with st.expander("Prompt sent to model"):
            st.code(prompt)

        result = generate_schedule(prompt)

        st.subheader("Recommended Schedule")
        st.json(result)

        gantt_df = build_gantt_df(result)

        st.subheader("Gantt Chart")
        fig = plot_gantt_chart(gantt_df)
        if fig:
            st.plotly_chart(fig, width="stretch")

        with st.expander("Gantt Data"):
            st.dataframe(gantt_df, width="stretch")

        output_df = pd.DataFrame(result)
        st.download_button(
            "Download recommended schedule CSV",
            output_df.to_csv(index=False).encode("utf-8"),
            file_name="recommended_schedule.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(str(e))