import matplotlib.pyplot as plt
import seaborn as sns
import os

def dataset_overview(df, column=None):
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": df.columns.tolist(),
        "dtypes": df.dtypes.astype(str).to_dict()
    }

def statistical_summary(df, column=None):
    return df.describe(include='number').to_dict()

def missing_values(df, column=None):
    missing = df.isnull().sum()
    # Keep only columns with >0 missing
    missing = {col: count for col, count in missing.items() if count > 0}
    return missing

def duplicate_count(df, column=None):
    return int(df.duplicated().sum())

def column_mean(df, column=None):
    if column is None or column not in df.columns:
        return "Column not found."
    return df[column].mean()

def column_min(df, column=None):
    if column is None or column not in df.columns:
        return "Column not found."
    return df[column].min()

def column_max(df, column=None):
    if column is None or column not in df.columns:
        return "Column not found."
    return df[column].max()

def value_counts(df, column=None):
    if column is None or column not in df.columns:
        return "Column not found."
    return df[column].value_counts().to_dict()

def correlation_matrix(df, column=None):
    return df.corr(numeric_only=True)

def number_of_rows(df, column=None):
    return df.shape[0]

def number_of_columns(df, column=None):
    return df.shape[1]

def plot_numeric_columns(df, column=None, save_dir="plots"):
    os.makedirs(save_dir, exist_ok=True)
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    saved_paths = []
    for col in numeric_cols:
        plt.figure()
        sns.histplot(df[col], kde=True)
        plt.title(f"Distribution of {col}")
        path = os.path.join(save_dir, f"{col}.png")
        plt.savefig(path)
        plt.close()
        saved_paths.append(path)
    return saved_paths

KNOWN_ACTIONS = {
    "dataset_overview": dataset_overview,
    "statistical_summary": statistical_summary,
    "missing_values": missing_values,
    "duplicate_count": duplicate_count,
    "column_mean": column_mean,
    "column_min": column_min,
    "column_max": column_max,
    "value_counts": value_counts,
    "correlation_matrix": correlation_matrix,
    "number_of_rows": number_of_rows,
    "number_of_columns": number_of_columns,
    "plot_numeric_columns": plot_numeric_columns,
}