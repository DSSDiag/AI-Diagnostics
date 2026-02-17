def generate_report(results, output_path):
    """
    Generate a simple text report from the diagnostic results.

    Args:
        results (dict): A dictionary containing diagnostic results.
        output_path (str): The path to save the report.
    """
    try:
        with open(output_path, 'w') as f:
            f.write("AI Diagnostics Report\n")
            f.write("=====================\n\n")

            if 'missing_values' in results:
                f.write("Missing Values per Column:\n")
                f.write(results['missing_values'].to_string())
                f.write("\n\n")

            if 'data_types' in results:
                f.write("Data Types per Column:\n")
                f.write(results['data_types'].to_string())
                f.write("\n\n")

            if 'metrics' in results:
                f.write("Model Performance Metrics:\n")
                for metric, value in results['metrics'].items():
                    f.write(f"{metric}: {value:.4f}\n")
                f.write("\n")

        print(f"Report generated successfully at {output_path}")
    except Exception as e:
        print(f"Error generating report: {e}")
