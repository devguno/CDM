import os
import pandas as pd

# Define the directory where the CSV files are located
directory = r'C:\Users\SNUH\Desktop\tmt\combine'

# Check if the directory exists
if not os.path.exists(directory):
    result = "Directory not found."
else:
    # List all CSV files in the directory
    csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]

    # Combine all CSV files into a single DataFrame
    combined_csv = pd.concat([pd.read_csv(os.path.join(directory, file)) for file in csv_files])

    # Save the combined DataFrame to a new CSV file
    combined_csv_file = os.path.join(directory, 'combined_csv.csv')
    combined_csv.to_csv(combined_csv_file, index=False)

    result = f"Combined CSV file created at: {combined_csv_file}"

result
