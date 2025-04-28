import pandas as pd
import json

# Parse the JSON response
with open('response.txt', 'r', encoding='utf-8') as f:
    # Filter out lines starting with ```
    json_content = ''.join(line for line in f if not line.strip().startswith('```'))
    data = json.loads(json_content)  # Parse the cleaned JSON

# Extract metadata
metadata = {
    "Name": data["Name"],
    "Date of Death": data["Date of Death"],
    "Baten (Net Assets)": data["Baten (Net Assets)"],
    "Schulden en Lasten (Net Liabilities)": data["Schulden en Lasten (Net Liabilities)"],
    "Saldo (Net Wealth)": data["Saldo (Net Wealth)"]
}

# Extract Assets and Liabilities
assets = pd.DataFrame(data['Overview']['Assets'])
assets['Type'] = 'Asset'  # Add a column to indicate type

liabilities = pd.DataFrame(data['Overview']['Liabilities'])
liabilities['Type'] = 'Liability'  # Add a column to indicate type

# Combine Assets and Liabilities
combined = pd.concat([assets, liabilities], ignore_index=True)

# Add metadata to each row
for key, value in metadata.items():
    combined[key] = value

# Export to a single CSV file
combined.to_csv('response.csv', index=False)

print("Combined data exported to 'response.csv'.")
