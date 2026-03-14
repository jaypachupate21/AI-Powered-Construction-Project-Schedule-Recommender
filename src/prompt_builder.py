import json

def build_prompt(new_project, similar_projects, schedule_summary):
    similar_projects_records = similar_projects.to_dict(orient="records")
    schedule_summary_records = schedule_summary.head(50).to_dict(orient="records")

    prompt = f"""
You are a construction scheduling expert.

Use the new project details and the retrieved historical schedule patterns to generate a recommended schedule.

NEW PROJECT:
{json.dumps(new_project, indent=2)}

TOP SIMILAR PROJECTS:
{json.dumps(similar_projects_records, indent=2, default=str)}

HISTORICAL SCHEDULE SUMMARY:
{json.dumps(schedule_summary_records, indent=2, default=str)}

Instructions:
- Create a realistic high-level recommended schedule.
- Use historical task names where possible.
- Preserve logical sequencing.
- Use parwbsname as the phase when helpful.
- Estimate duration_days from historical averages.
- Return only valid JSON.
- Use this exact format:

[
  {{
    "phase": "string",
    "task": "string",
    "duration_days": 0,
    "predecessor": null,
    "reasoning": "short explanation"
  }}
]
"""
    return prompt.strip()