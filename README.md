# AI-Diagnostics

A comprehensive tool for diagnosing data quality and model performance.

## Installation

1. Clone the repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the diagnostics tool on your dataset (CSV format):

```bash
python main.py <path_to_your_data.csv>
```

## Features

- **Data Loading**: Supports CSV files.
- **Missing Value Check**: Identifies missing values in each column.
- **Data Type Check**: Lists data types for all columns.
- **Basic Metrics**: Calculates accuracy, precision, recall, and F1 score (assumes binary classification target 'target' exists).
- **Report Generation**: Generates a summary report in `diagnostic_report.txt`.

## Project Structure

- `src/`: Contains source code for data loading, diagnostics, and reporting.
- `main.py`: Entry point for the application.
- `requirements.txt`: List of dependencies.
- `sample_data.csv`: Sample dataset for testing.
