import pandas as pd

def load_data(meta_path, schedule_path):
    meta_df = pd.read_csv(meta_path)
    schedule_df = pd.read_csv(schedule_path)
    return meta_df, schedule_df

def clean_metadata(df):
    df = df.copy()
    df.columns = [c.lower().strip().replace(" ", "_") for c in df.columns]
    return df

def clean_schedule(df):
    df = df.copy()
    df.columns = [c.lower().strip().replace(" ", "_") for c in df.columns]
    return df