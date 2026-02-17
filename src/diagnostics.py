import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def check_missing_values(df):
    """
    Check for missing values in the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.Series: A series with the count of missing values for each column.
    """
    if df is None:
        return None
    return df.isnull().sum()

def check_data_types(df):
    """
    Check the data types of the DataFrame columns.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.Series: A series with the data type for each column.
    """
    if df is None:
        return None
    return df.dtypes

def calculate_basic_metrics(y_true, y_pred):
    """
    Calculate basic classification metrics.

    Args:
        y_true (array-like): True labels.
        y_pred (array-like): Predicted labels.

    Returns:
        dict: A dictionary containing accuracy, precision, recall, and f1 score.
    """
    try:
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_true, y_pred, average='weighted', zero_division=0),
            'f1_score': f1_score(y_true, y_pred, average='weighted', zero_division=0)
        }
        return metrics
    except Exception as e:
        print(f"Error calculating metrics: {e}")
        return None
