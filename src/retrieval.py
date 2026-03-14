def retrieve_schedules(schedule_df, project_ids, project_id_col="main_projectid"):
    schedule_df = schedule_df.copy()
    schedule_df[project_id_col] = schedule_df[project_id_col].astype(str)
    project_ids = [str(x) for x in project_ids]
    return schedule_df[schedule_df[project_id_col].isin(project_ids)].copy()

def summarize_schedule(schedules):
    work = schedules.copy()

    if "duration_days" not in work.columns:
        raise ValueError("duration_days column is missing before summarization.")

    summary = (
        work.groupby(["parwbsname", "wbsname"], dropna=False)
        .agg(
            avg_duration=("duration_days", "mean"),
            median_duration=("duration_days", "median"),
            task_frequency=("wbsname", "count"),
        )
        .reset_index()
        .sort_values(["task_frequency", "avg_duration"], ascending=[False, True])
    )

    summary["avg_duration"] = summary["avg_duration"].fillna(0).round(1)
    summary["median_duration"] = summary["median_duration"].fillna(0).round(1)

    return summary