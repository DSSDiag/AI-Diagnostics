import sys
import pandas as pd
from src.data_loader import load_csv
from src.diagnostics import check_missing_values, check_data_types, calculate_basic_metrics
from src.report import generate_report

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <data_file_path>")
        sys.exit(1)

    data_path = sys.argv[1]
    df = load_csv(data_path)

    if df is None:
        print("Failed to load data.")
        sys.exit(1)

    results = {}

    print("Running diagnostics...")

    # Check for missing values
    results['missing_values'] = check_missing_values(df)

    # Check data types
    results['data_types'] = check_data_types(df)

    # Example: If 'target' column exists, calculate metrics assuming binary classification
    # For demonstration, we'll split the data into X and y if 'target' exists
    if 'target' in df.columns:
        y_true = df['target']
        # Simple dummy prediction for demonstration purposes (predicting majority class)
        # In a real scenario, you would load a model and predict
        majority_class = y_true.mode()[0]
        y_pred = [majority_class] * len(y_true)

        print("Calculating basic metrics (using majority class baseline)...")
        results['metrics'] = calculate_basic_metrics(y_true, y_pred)

    generate_report(results, "diagnostic_report.txt")

if __name__ == "__main__":
    main()
