# 🏗️AI-Powered Construction Project Schedule Recommender

## Overview

Construction project scheduling requires domain expertise and experience with similar past projects. Creating schedules manually is time-consuming and error-prone.

This project builds an **AI-powered schedule recommendation system** that analyzes historical construction project data to automatically generate a recommended project schedule for a new project.

The system combines:

- Machine Learning similarity models

- Historical schedule retrieval

- Azure OpenAI Large Language Models

- Interactive visualization with Streamlit

The result is a **data-driven construction schedule recommendation system**.

## 🎯 Problem Statement

Organizations often have large repositories of completed project schedules. However, planners still need to design schedules manually.

The goal of this project is to:

Accept **new project details**

Identify **similar historical projects**

Retrieve their schedules

Use an **LLM to generate a recommended schedule**

## 🧠 Solution Approach

The system follows a **Retrieval Augmented Generation (RAG)** pipeline.
```
New Project Metadata
        ↓
Feature Engineering
        ↓
Similarity Detection (Machine Learning)
        ↓
Top-K Similar Projects
        ↓
Schedule Retrieval
        ↓
Schedule Aggregation
        ↓
LLM Schedule Generation
        ↓
Gantt Chart Visualization

```

## ⚙️ System Components
### 1️⃣ Similarity Model (Machine Learning)

A similarity model identifies projects most similar to the new project.

Features used include:

- Region

- Business Unit

- Office

- City

- State

- Core Market

- Market Sector

- Project Type

- Total Control Estimate

- Building Size

Techniques used:

- One-Hot Encoding for categorical features

- Standard Scaling for numerical features

- Cosine Similarity for project comparison

The model retrieves **Top-K most similar historical projects**.

### 2️⃣ Schedule Retrieval

Schedules of similar projects are retrieved using project identifiers.

Metadata file key:
```
CONTROL_JOB_NO
```
Schedule file key:
```
MAIN_PROJECTID
```
Schedule attributes include:

Phase (**PARWBSNAME**)

Task (**WBSNAME**)

Planned Start Date

Planned Finish Date

Task duration is computed as:
```
duration_days = planned_finish_date − planned_start_date
```

### 3️⃣ LLM Schedule Generation

Historical schedules are summarized and provided as context to **Azure OpenAI**.

The LLM generates a recommended schedule using:

- historical task patterns

- phase structure

- average durations

Example output format:
```
[
  {
    "phase": "Preconstruction",
    "task": "Design",
    "duration_days": 30,
    "predecessor": null,
    "reasoning": "Typical first stage in similar projects"
  }
]
```

### 4️⃣ Gantt Chart Visualization

The generated schedule is visualized using a Gantt Chart.

This allows planners to view:

- task sequencing

- project timeline

- phase distribution

Visualization tools:

- Plotly

- Streamlit

### 🖥️ Technology Stack

| Component | Technology |
|------|------|
| Frontend | Streamlit |
| Machine Learning | Scikit-learn |
| LLM |Azure OpenAI |
| Visualization | Plotly |
| Data Processing | Pandas |
| Programming Language | Python |


## 📂 Project Structure

```
project/
│
├── data/
│   ├── Project_JOB_meta_data.csv
│   └── Project_Schedule_Data.csv
│
├── notebooks/
│   └── construction_schedule_recommender.ipynb
│
├── app/
│   └── streamlit_app.py
│
├── src/
│   ├── preprocess.py
│   ├── similarity.py
│   ├── retrieval.py
│   ├── prompt_builder.py
│   └── llm_generator.py
│
├── outputs/
│   └── sample_schedule.json
│
├── requirements.txt
├── .env
└── README.md
```

## 🚀 Installation

Clone the repository:
```
git clone <repository_url>
cd project
```
Install dependencies:
```
pip install -r requirements.txt
```
## 🔐 Environment Setup

Create a .env file in the project root.

Example:
```
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_DEPLOYMENT=your_deployment_name
```

## ▶️ Running the Application

Start the Streamlit application:
```
streamlit run app/streamlit_app.py
```
Open the browser at:
```
Local URL: http://localhost:8501
Network URL: http://10.240.5.214:8501
```


## 🧪 Example Workflow

1.Enter project metadata

2.The system identifies similar historical projects

3.Historical schedules are retrieved

4.The LLM generates a recommended schedule

5.The schedule is visualized as a Gantt chart

## 📊 Example Output

Recommended Schedule:

| Phase	   |          Task	   |         Duration |
|------|------|----------|
| Preconstruction	|     Trade Agreements	 |   23 days |
| Preconstruction	   |  Design	  |          30 days |
| Construction	|     Site Preparation	 |   15 days |

The schedule is displayed as a **Gantt chart timeline**.

## ⚠️ Limitations

- Historical data may contain schedule outliers

- Task dependencies are inferred heuristically

- LLM output quality depends on prompt design

- Results depend on historical dataset quality

## 🔮 Future Improvements

- Possible improvements include:

- Embedding-based similarity models

- Vector search using FAISS

- Automatic task dependency learning

- Outlier detection for durations

- Multi-project evaluation

- Integration with project management tools

## 🏆 Hackathon Deliverables

This project includes:

- End-to-end ML + LLM pipeline

- Interactive Streamlit application

- Project similarity model

- LLM-based schedule generation

- Gantt chart visualization

## 👨‍💻 Author

Jay Pachupate pachupatejay2102@gmail.com

Hackathon Submission – AI Construction Schedule Recommendation System

# vConstruct-Hackathon-pachupatejay2102
Hackathon repo for pachupatejay2102@gmail.com
