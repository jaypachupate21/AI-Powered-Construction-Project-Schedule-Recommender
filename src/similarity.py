import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

def build_similarity_model(meta_df):
    numeric_cols = ["total_control_estimate", "building_size"]
    categorical_cols = [
        "region_name",
        "business_unit",
        "office_name",
        "city",
        "state",
        "core_market",
        "market_sector",
        "project_type",
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline([
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler()),
                ]),
                numeric_cols,
            ),
            (
                "cat",
                Pipeline([
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("onehot", OneHotEncoder(handle_unknown="ignore")),
                ]),
                categorical_cols,
            ),
        ]
    )

    pipeline = Pipeline([("preprocess", preprocessor)])
    matrix = pipeline.fit_transform(meta_df)
    return pipeline, matrix

def find_similar_projects(new_project, meta_df, pipeline, matrix, top_k=5):
    new_df = pd.DataFrame([new_project])
    new_vec = pipeline.transform(new_df)
    similarities = cosine_similarity(new_vec, matrix)[0]

    result = meta_df.copy()
    result["similarity_score"] = similarities

    cols_to_show = [
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
        "similarity_score",
    ]
    cols_to_show = [c for c in cols_to_show if c in result.columns]

    return result.sort_values("similarity_score", ascending=False).head(top_k)[cols_to_show]