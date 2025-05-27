import pandas as pd
import json
import argparse
import os

def process_financial_data(input_json_path, output_csv_path):
    """
    Parses financial data from a JSON file, processes it,
    and exports it to a CSV file.

    Args:
        input_json_path (str): Path to the input JSON file.
        output_csv_path (str): Path to the output CSV file.
    """
    try:
        # Parse the JSON response
        with open(input_json_path, 'r', encoding='utf-8') as f:
            json_content = ''.join(line for line in f if not line.strip().startswith('```'))
            data = json.loads(json_content)

    except FileNotFoundError:
        print(f"Error: Input file '{input_json_path}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{input_json_path}'. Please ensure it's valid JSON.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading or parsing the JSON file: {e}")
        return

    try:
        # Extract metadata
        metadata = {
            "Name": data.get("Name", "N/A"),
            "Date of Death": data.get("Date of Death", "N/A"),
            "Baten (Net Assets)": data.get("Baten (Net Assets)", 0),
            "Schulden en Lasten (Net Liabilities)": data.get("Schulden en Lasten (Net Liabilities)", 0),
            "Saldo (Net Wealth)": data.get("Saldo (Net Wealth)", 0)
        }

        # Extract Assets and Liabilities
        overview_data = data.get('Overview', {})
        assets_data = overview_data.get('Assets', [])
        liabilities_data = overview_data.get('Liabilities', [])

        if not assets_data and not liabilities_data:
            print("Warning: No 'Assets' or 'Liabilities' found in the 'Overview' section of the JSON.")

        assets = pd.DataFrame(assets_data)
        if not assets.empty:
            # --- CHANGE IS HERE ---
            if 'name' in assets.columns: # Check if 'name' column exists before renaming
                assets.rename(columns={'name': 'description'}, inplace=True)
            else:
                print("Warning: 'name' column not found in Assets. Cannot rename to 'description'.")
            assets['Type'] = 'Asset'
        else:
            # Ensure consistent columns even if empty, reflecting the desired final column name
            # Assuming the other main column from JSON is 'value' based on your sample output
            assets = pd.DataFrame(columns=['description', 'value', 'Type'])


        liabilities = pd.DataFrame(liabilities_data)
        if not liabilities.empty:
            # --- CHANGE IS HERE ---
            if 'name' in liabilities.columns: # Check if 'name' column exists before renaming
                liabilities.rename(columns={'name': 'description'}, inplace=True)
            else:
                print("Warning: 'name' column not found in Liabilities. Cannot rename to 'description'.")
            liabilities['Type'] = 'Liability'
        else:
            # Ensure consistent columns even if empty
            liabilities = pd.DataFrame(columns=['description', 'value', 'Type'])


        # Combine Assets and Liabilities
        if assets.empty and liabilities.empty:
            combined = pd.DataFrame()
            print("Warning: Both Assets and Liabilities lists are empty. CSV will contain metadata only (if any).")
        elif assets.empty:
            combined = liabilities.copy()
        elif liabilities.empty:
            combined = assets.copy()
        else:
            combined = pd.concat([assets, liabilities], ignore_index=True)


        if not combined.empty:
            for key, value in metadata.items():
                combined[key] = value
        else:
            print("No asset/liability data; creating CSV with metadata summary.")
            combined = pd.DataFrame([metadata])


        combined.to_csv(output_csv_path, index=False, encoding='utf-8')
        print(f"Combined data exported to '{output_csv_path}'.")

    except KeyError as e:
        print(f"Error: Missing expected key in JSON data: {e}. Please check the JSON structure.")
    except Exception as e:
        print(f"An unexpected error occurred during data processing or CSV export: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process financial data from a JSON file and export to CSV.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter # Shows default values in help
    )

    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the input JSON file (e.g., 'response_ex2.txt')."
    )

    parser.add_argument(
        "-o", "--output_file",
        type=str,
        default=None, # Default will be derived from input file name
        help="Path to the output CSV file (e.g., 'response_ex2.csv'). "
             "If not provided, it defaults to the input file name with a .csv extension."
    )

    args = parser.parse_args()

    # Determine default output file name if not provided
    output_file_path = args.output_file
    if output_file_path is None:
        base_name, _ = os.path.splitext(args.input_file)
        output_file_path = base_name + ".csv"

    process_financial_data(args.input_file, output_file_path)
